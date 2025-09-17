import asyncio
import logging
import signal
import sys
from pathlib import Path
from services.telegram_collector import TelegramCollector
from services.database import DatabaseManager
from services.command_monitor import CommandMonitor
from utils.config import Config

def setup_logging():
    log_dir = Path("../shared/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "oracle_eye.log"),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("telethon").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

class OracleEyeService:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.collector = None
        self.command_monitor = CommandMonitor()
        self.running = False

    async def initialize(self):
        logger.info("Initializing Oracle Eye Service...")
        logger.info("Testing database connection...")
        projects = self.db.get_active_projects()
        logger.info(f"Database connected. Found {len(projects)} active projects")
        logger.info("Initializing Telegram collector...")
        self.collector = TelegramCollector(
            api_id=self.config.TELEGRAM_API_ID,
            api_hash=self.config.TELEGRAM_API_HASH,
            phone=self.config.TELEGRAM_PHONE_NUMBER
        )
        await self.collector.start()
        logger.info("Telegram collector initialized successfully")
        logger.info("Oracle Eye Service initialized successfully!")

    async def start_collection_loop(self):
        logger.info("Starting continuous collection loop...")
        while self.running:
            try:
                # Check for immediate collection commands first
                commands = self.command_monitor.check_for_commands()
                if commands:
                    logger.info(f"Processing {len(commands)} immediate collection commands")
                    for command in commands:
                        await self.process_immediate_command(command)
                
                # Check for projects ready for scheduled collection
                projects_ready = self.db.get_projects_ready_for_collection()
                if projects_ready:
                    logger.info(f"Starting scheduled collection for {len(projects_ready)} projects")
                    for project in projects_ready:
                        try:
                            await self.collector.collect_messages(project)
                            # Schedule next collection after successful collection
                            self.db.schedule_next_collection(project.id, self.config.COLLECTION_INTERVAL)
                            await asyncio.sleep(5)  # Small delay between projects
                        except Exception as e:
                            logger.error(f"Error collecting from {project.name}: {e}")
                            continue
                    
                    logger.info("Scheduled collection cycle completed successfully")
                else:
                    logger.info("No projects ready for collection at this time")
                
                # Wait 1 minute before checking again (instead of 24 hours)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Collection loop error: {e}")
                await asyncio.sleep(60 * 60)  # Wait 1 hour on error
    
    async def process_immediate_command(self, command):
        """Process an immediate collection command"""
        project_name = command["project_name"]
        try:
            logger.info(f"Processing immediate collection for {project_name}")
            
            # Mark as processing
            self.command_monitor.mark_command_processing(project_name)
            
            # Get project from database
            project = self.db.get_project_by_name(project_name)
            if not project:
                self.command_monitor.mark_command_failed(project_name, "Project not found")
                return
            
            # Collect messages
            messages_before = self.db.get_message_count(project.id)
            await self.collector.collect_messages(project)
            messages_after = self.db.get_message_count(project.id)
            messages_collected = messages_after - messages_before
            
            # Schedule next collection after immediate collection
            self.db.schedule_next_collection(project.id, self.config.COLLECTION_INTERVAL)
            
            # Mark as completed
            self.command_monitor.mark_command_completed(project_name, messages_collected)
            logger.info(f"Immediate collection completed for {project_name}: {messages_collected} new messages")
            
        except Exception as e:
            error_msg = f"Error in immediate collection: {e}"
            logger.error(error_msg)
            self.command_monitor.mark_command_failed(project_name, error_msg)

    async def start(self):
        self.running = True
        await self.initialize()
        await self.start_collection_loop()

    async def stop(self):
        logger.info("Stopping Oracle Eye Service...")
        self.running = False
        if self.collector:
            await self.collector.disconnect()
            logger.info("Telegram collector stopped")
        logger.info("Oracle Eye Service stopped successfully")

    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())
        sys.exit(0)

async def main():
    setup_logging()
    service = OracleEyeService()
    signal.signal(signal.SIGINT, service.signal_handler)
    signal.signal(signal.SIGTERM, service.signal_handler)
    try:
        await service.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await service.stop()
        logger.info("Oracle Eye Service stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Failed to start Oracle Eye Service: {e}")
        sys.exit(1)
