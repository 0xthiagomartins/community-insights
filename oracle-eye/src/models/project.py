from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .message import Message
    from .summary import Summary

class Project(SQLModel, table=True):
    """Modelo para projetos monitorados"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    telegram_group: str = Field(index=True)
    is_active: bool = Field(default=True)
    last_collected_message_id: Optional[int] = Field(default=None)
    next_collection_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamentos
    messages: List["Message"] = Relationship(back_populates="project")
    summaries: List["Summary"] = Relationship(back_populates="project")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
