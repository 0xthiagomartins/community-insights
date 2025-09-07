from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .project import Project

class Message(SQLModel, table=True):
    """Modelo para mensagens coletadas do Telegram"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    telegram_message_id: int = Field(index=True)
    content: str
    author: Optional[str] = Field(default=None)
    timestamp: datetime = Field(index=True)
    message_type: str = Field(default="text")  # text, link, etc.
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamento com Project
    project: Optional["Project"] = Relationship(back_populates="messages")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
