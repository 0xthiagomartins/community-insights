import logging
from pathlib import Path
from cli.commands import app

def setup_logging():
    log_dir = Path("../shared/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "neural_core.log"),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("crewai").setLevel(logging.INFO)

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("🤖 Starting Neural Core Service...")
    logger.info("💻 Launching CLI interface...")
    
    try:
        app()
    except Exception as e:
        logger.error(f"💥 Fatal error in Neural Core: {e}")
        raise

if __name__ == "__main__":
    main()
