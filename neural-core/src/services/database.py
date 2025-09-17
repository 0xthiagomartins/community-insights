import logging
from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, select
from models import Project, Message, Summary
from utils.config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url: Optional[str] = None):
        self.config = Config()
        self.db_url = db_url or self.config.DATABASE_URL
        self.engine = create_engine(self.db_url, echo=False)
        self._create_tables()
    
    def _create_tables(self):
        """Cria as tabelas no banco de dados"""
        try:
            SQLModel.metadata.create_all(self.engine)
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Retorna uma sessão do banco de dados"""
        return Session(self.engine)
    
    # Métodos para Project
    def create_project(self, name: str, telegram_group: str, is_active: bool = True) -> Project:
        """Cria um novo projeto"""
        with self.get_session() as session:
            project = Project(
                name=name,
                telegram_group=telegram_group,
                is_active=is_active
            )
            session.add(project)
            session.commit()
            session.refresh(project)
            logger.info(f"Project '{name}' created successfully")
            return project
    
    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Busca um projeto pelo nome"""
        with self.get_session() as session:
            statement = select(Project).where(Project.name == name)
            return session.exec(statement).first()
    
    def get_all_projects(self) -> List[Project]:
        """Retorna todos os projetos"""
        with self.get_session() as session:
            statement = select(Project)
            return list(session.exec(statement))
    
    def update_project(self, project_id: int, **kwargs) -> Optional[Project]:
        """Atualiza um projeto"""
        with self.get_session() as session:
            project = session.get(Project, project_id)
            if not project:
                return None
            
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            project.updated_at = datetime.utcnow()
            session.add(project)
            session.commit()
            session.refresh(project)
            return project
    
    # Métodos para Message
    def get_messages_by_project(self, project_id: int, 
                               start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> List[Message]:
        """Busca mensagens de um projeto em um período"""
        with self.get_session() as session:
            statement = select(Message).where(Message.project_id == project_id)
            
            if start_date:
                statement = statement.where(Message.timestamp >= start_date)
            if end_date:
                statement = statement.where(Message.timestamp <= end_date)
            
            statement = statement.order_by(Message.timestamp.desc())
            return list(session.exec(statement))
    
    def count_messages_by_project(self, project_id: int,
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> int:
        """Conta mensagens de um projeto em um período"""
        with self.get_session() as session:
            statement = select(Message).where(Message.project_id == project_id)
            
            if start_date:
                statement = statement.where(Message.timestamp >= start_date)
            if end_date:
                statement = statement.where(Message.timestamp <= end_date)
            
            return len(list(session.exec(statement)))
    
    # Métodos para Summary
    def create_summary(self, project_id: int, content: str,
                      date_range_start: datetime, date_range_end: datetime,
                      cost_estimate: float = 0.0, actual_cost: float = 0.0,
                      message_count: int = 0) -> Summary:
        """Cria um novo resumo"""
        with self.get_session() as session:
            summary = Summary(
                project_id=project_id,
                content=content,
                date_range_start=date_range_start,
                date_range_end=date_range_end,
                cost_estimate=cost_estimate,
                actual_cost=actual_cost,
                message_count=message_count
            )
            session.add(summary)
            session.commit()
            session.refresh(summary)
            logger.info(f"✅ Summary created for project {project_id}")
            return summary
    
    def get_summaries_by_project(self, project_id: int) -> List[Summary]:
        """Busca resumos de um projeto"""
        with self.get_session() as session:
            statement = select(Summary).where(
                Summary.project_id == project_id
            ).order_by(Summary.created_at.desc())
            return list(session.exec(statement))
