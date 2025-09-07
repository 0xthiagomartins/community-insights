from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .project import Project

class Summary(SQLModel, table=True):
    """Modelo para resumos gerados"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    content: str
    date_range_start: datetime = Field(index=True)
    date_range_end: datetime = Field(index=True)
    cost_estimate: float = Field(default=0.0)
    actual_cost: float = Field(default=0.0)
    message_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamento com Project
    project: Optional["Project"] = Relationship(back_populates="summaries")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
