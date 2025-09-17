import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class CommandMonitor:
    def __init__(self):
        self.commands_dir = Path("../shared/commands")
        self.commands_dir.mkdir(parents=True, exist_ok=True)
    
    def check_for_commands(self) -> list[Dict[str, Any]]:
        """Check for pending collection commands"""
        commands = []
        
        try:
            for command_file in self.commands_dir.glob("collect_*.json"):
                try:
                    with open(command_file, 'r') as f:
                        command_data = json.load(f)
                    
                    if command_data.get("status") == "pending":
                        commands.append(command_data)
                        logger.info(f"Found pending command: {command_data['project_name']}")
                
                except Exception as e:
                    logger.error(f"Error reading command file {command_file}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error checking for commands: {e}")
        
        return commands
    
    def mark_command_processing(self, project_name: str):
        """Mark a command as being processed"""
        command_file = self.commands_dir / f"collect_{project_name.lower()}.json"
        
        try:
            if command_file.exists():
                with open(command_file, 'r') as f:
                    command_data = json.load(f)
                
                command_data["status"] = "processing"
                command_data["processing_started"] = datetime.utcnow().isoformat() + "Z"
                
                with open(command_file, 'w') as f:
                    json.dump(command_data, f, indent=2)
                
                logger.info(f"Marked command as processing: {project_name}")
        
        except Exception as e:
            logger.error(f"Error marking command as processing: {e}")
    
    def mark_command_completed(self, project_name: str, messages_collected: int = 0):
        """Mark a command as completed and create status file"""
        command_file = self.commands_dir / f"collect_{project_name.lower()}.json"
        status_file = self.commands_dir / f"status_{project_name.lower()}.json"
        
        try:
            # Update command file
            if command_file.exists():
                with open(command_file, 'r') as f:
                    command_data = json.load(f)
                
                command_data["status"] = "completed"
                command_data["completed_at"] = datetime.utcnow().isoformat() + "Z"
                command_data["messages_collected"] = messages_collected
                
                with open(command_file, 'w') as f:
                    json.dump(command_data, f, indent=2)
            
            # Create status file
            status_data = {
                "command": "status",
                "project_name": project_name,
                "status": "completed",
                "messages_collected": messages_collected,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
            
            logger.info(f"Marked command as completed: {project_name} ({messages_collected} messages)")
        
        except Exception as e:
            logger.error(f"Error marking command as completed: {e}")
    
    def mark_command_failed(self, project_name: str, error_message: str):
        """Mark a command as failed"""
        command_file = self.commands_dir / f"collect_{project_name.lower()}.json"
        status_file = self.commands_dir / f"status_{project_name.lower()}.json"
        
        try:
            # Update command file
            if command_file.exists():
                with open(command_file, 'r') as f:
                    command_data = json.load(f)
                
                command_data["status"] = "failed"
                command_data["failed_at"] = datetime.utcnow().isoformat() + "Z"
                command_data["error"] = error_message
                
                with open(command_file, 'w') as f:
                    json.dump(command_data, f, indent=2)
            
            # Create status file
            status_data = {
                "command": "status",
                "project_name": project_name,
                "status": "failed",
                "error": error_message,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
            
            logger.error(f"Marked command as failed: {project_name} - {error_message}")
        
        except Exception as e:
            logger.error(f"Error marking command as failed: {e}")
