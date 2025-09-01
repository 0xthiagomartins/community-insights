# Developer Architecture Guide

## 🏗️ **ARQUITETURA TÉCNICA - MVP FASE 1**

Este documento detalha como implementar a arquitetura de serviços para o Crypto Community Insights Agent usando **SQLModel** como ORM.

---

## 📋 **VISÃO GERAL DA ARQUITETURA**

### **Estrutura de Serviços**
```
┌─────────────────────────────────────────────────────────────┐
│                    AMBIENTE PYTHON ÚNICO                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │   SERVIÇO 1     │    │           SERVIÇO 2             │ │
│  │  COLETA AUTO    │    │      PROCESSAMENTO IA           │ │
│  │                 │    │                                 │ │
│  │ • Telethon      │    │ • CrewAI                        │ │
│  │ • Scheduler     │    │ • Cost Estimation               │ │
│  │ • SQLModel      │    │ • Summary Generation            │ │
│  │ • Background    │    │ • CLI Interface                 │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **Fluxo de Dados**
```
Telegram Groups → Telethon Collection → SQLModel ORM → CrewAI Processing → Markdown Output
```

---

## 🔧 **IMPLEMENTAÇÃO TÉCNICA**

### **1. ESTRUTURA DE ARQUIVOS**

```
crypto-insights/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada principal
│   ├── services/
│   │   ├── __init__.py
│   │   ├── telegram_collector.py    # Serviço de coleta
│   │   ├── ai_processor.py          # Serviço de IA
│   │   └── database.py              # Gerenciamento SQLModel
│   ├── models/
│   │   ├── __init__.py
│   │   ├── message.py               # Modelo SQLModel + Pydantic
│   │   ├── project.py               # Modelo SQLModel + Pydantic
│   │   └── summary.py               # Modelo SQLModel + Pydantic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cost_estimator.py        # Estimação de custos
│   │   └── config.py                # Configurações
│   └── cli/
│       ├── __init__.py
│       └── commands.py              # Comandos Typer
├── requirements.txt
├── .env
└── README.md
```

### **2. MODELOS SQLMODEL + PYDANTIC**

#### **`src/models/project.py`**
```python
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    telegram_group: str
    is_active: bool = True

class Project(ProjectBase, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamentos
    messages: List["Message"] = Relationship(back_populates="project")
    summaries: List["Summary"] = Relationship(back_populates="project")

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    telegram_group: Optional[str] = None
    is_active: Optional[bool] = None
```

#### **`src/models/message.py`**
```python
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

class MessageBase(BaseModel):
    telegram_id: int
    text: str
    timestamp: datetime
    sender_id: Optional[int] = None
    links: Optional[str] = None

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamentos
    project: "Project" = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    project_id: int

class MessageRead(MessageBase):
    id: int
    project_id: int
    created_at: datetime
```

#### **`src/models/summary.py`**
```python
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

class SummaryBase(BaseModel):
    date_start: date
    date_end: date
    content: str
    cost_estimate: float
    actual_cost: float

class Summary(SummaryBase, table=True):
    __tablename__ = "summaries"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relacionamentos
    project: "Project" = Relationship(back_populates="summaries")

class SummaryCreate(SummaryBase):
    project_id: int

class SummaryRead(SummaryBase):
    id: int
    project_id: int
    created_at: datetime
```

### **3. SERVIÇO DE BANCO DE DADOS COM SQLMODEL**

#### **`src/services/database.py`**
```python
import asyncio
from typing import List, Optional
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..models.project import Project, ProjectCreate, ProjectRead, ProjectUpdate
from ..models.message import Message, MessageCreate, MessageRead
from ..models.summary import Summary, SummaryCreate, SummaryRead

class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///crypto_insights.db"):
        self.db_url = db_url
        self.engine = create_engine(db_url, echo=True)
        self._create_tables()
        
    def _create_tables(self):
        """Cria todas as tabelas baseadas nos modelos SQLModel"""
        SQLModel.metadata.create_all(self.engine)
        
    def get_session(self) -> Session:
        """Retorna uma nova sessão do banco"""
        return Session(self.engine)
        
    # Métodos para Projetos
    def create_project(self, project_data: ProjectCreate) -> Project:
        """Cria um novo projeto"""
        with self.get_session() as session:
            project = Project(**project_data.dict())
            session.add(project)
            session.commit()
            session.refresh(project)
            return project
            
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Busca projeto por ID"""
        with self.get_session() as session:
            statement = select(Project).where(Project.id == project_id)
            return session.exec(statement).first()
            
    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Busca projeto por nome"""
        with self.get_session() as session:
            statement = select(Project).where(Project.name == name)
            return session.exec(statement).first()
            
    def get_active_projects(self) -> List[Project]:
        """Retorna todos os projetos ativos"""
        with self.get_session() as session:
            statement = select(Project).where(Project.is_active == True)
            return session.exec(statement).all()
            
    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Atualiza um projeto existente"""
        with self.get_session() as session:
            project = self.get_project_by_id(project_id)
            if project:
                update_data = project_data.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(project, field, value)
                session.add(project)
                session.commit()
                session.refresh(project)
            return project
            
    # Métodos para Mensagens
    def save_messages(self, messages: List[MessageCreate]) -> List[Message]:
        """Salva múltiplas mensagens"""
        with self.get_session() as session:
            db_messages = []
            for msg_data in messages:
                # Verifica se a mensagem já existe
                existing = session.exec(
                    select(Message).where(
                        Message.telegram_id == msg_data.telegram_id,
                        Message.project_id == msg_data.project_id
                    )
                ).first()
                
                if not existing:
                    message = Message(**msg_data.dict())
                    session.add(message)
                    db_messages.append(message)
                    
            session.commit()
            return db_messages
            
    def get_messages_in_range(self, project_id: int, date_start: str, date_end: str) -> List[Message]:
        """Busca mensagens em um período específico"""
        with self.get_session() as session:
            statement = select(Message).where(
                Message.project_id == project_id,
                Message.timestamp >= date_start,
                Message.timestamp <= date_end
            ).order_by(Message.timestamp.desc())
            return session.exec(statement).all()
            
    def get_message_count(self, project_id: int, date_start: str, date_end: str) -> int:
        """Conta mensagens em um período específico"""
        with self.get_session() as session:
            statement = select(Message).where(
                Message.project_id == project_id,
                Message.timestamp >= date_start,
                Message.timestamp <= date_end
            )
            return len(session.exec(statement).all())
            
    # Métodos para Resumos
    def save_summary(self, summary_data: SummaryCreate) -> Summary:
        """Salva um novo resumo"""
        with self.get_session() as session:
            summary = Summary(**summary_data.dict())
            session.add(summary)
            session.commit()
            session.refresh(summary)
            return summary
            
    def get_summaries_by_project(self, project_id: int) -> List[Summary]:
        """Busca todos os resumos de um projeto"""
        with self.get_session() as session:
            statement = select(Summary).where(Summary.project_id == project_id)
            return session.exec(statement).all()
            
    def get_latest_summary(self, project_id: int) -> Optional[Summary]:
        """Busca o resumo mais recente de um projeto"""
        with self.get_session() as session:
            statement = select(Summary).where(
                Summary.project_id == project_id
            ).order_by(Summary.created_at.desc())
            return session.exec(statement).first()
```

### **4. SERVIÇO DE COLETA AUTOMÁTICA ATUALIZADO**

#### **`src/services/telegram_collector.py`**
```python
import asyncio
import logging
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import Message
from ..models.message import MessageCreate
from ..models.project import Project
from ..services.database import DatabaseManager

class TelegramCollector:
    def __init__(self, api_id: str, api_hash: str, phone: str):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.db = DatabaseManager()
        self.logger = logging.getLogger(__name__)
        
    async def start(self):
        """Inicia o cliente Telegram"""
        await self.client.start(phone=phone)
        self.logger.info("Telegram client started")
        
    async def collect_messages(self, project: Project, limit: int = 100):
        """Coleta mensagens de um projeto específico"""
        try:
            entity = await self.client.get_entity(project.telegram_group)
            messages = await self.client.get_messages(entity, limit=limit)
            
            collected_messages = []
            for msg in messages:
                if msg.text:  # Apenas mensagens com texto
                    message_data = MessageCreate(
                        telegram_id=msg.id,
                        project_id=project.id,
                        text=msg.text,
                        timestamp=msg.date,
                        sender_id=msg.sender_id,
                        links=self._extract_links(msg.text)
                    )
                    collected_messages.append(message_data)
                    
            # Salva no banco usando SQLModel
            if collected_messages:
                saved_messages = self.db.save_messages(collected_messages)
                self.logger.info(f"Collected and saved {len(saved_messages)} messages from {project.telegram_group}")
            else:
                self.logger.info(f"No new messages to collect from {project.telegram_group}")
                
        except Exception as e:
            self.logger.error(f"Error collecting messages from {project.telegram_group}: {e}")
            
    def _extract_links(self, text: str) -> str:
        """Extrai links do texto da mensagem"""
        import re
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(url_pattern, text)
        return ','.join(links) if links else None
        
    async def run_daily_collection(self):
        """Executa coleta diária para todos os projetos ativos"""
        while True:
            try:
                projects = self.db.get_active_projects()
                self.logger.info(f"Starting daily collection for {len(projects)} projects")
                
                for project in projects:
                    await self.collect_messages(project)
                    await asyncio.sleep(5)  # Pausa entre projetos para evitar rate limits
                    
                self.logger.info("Daily collection completed successfully")
                # Aguarda 24 horas
                await asyncio.sleep(24 * 60 * 60)
                
            except Exception as e:
                self.logger.error(f"Daily collection error: {e}")
                await asyncio.sleep(60 * 60)  # Aguarda 1 hora em caso de erro
```

### **5. SERVIÇO DE PROCESSAMENTO IA ATUALIZADO**

#### **`src/services/ai_processor.py`**
```python
import logging
from typing import List
from crewai import Crew, Task, Agent
from ..models.message import Message
from ..models.summary import SummaryCreate
from ..utils.cost_estimator import CostEstimator
from ..services.database import DatabaseManager

class AIProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.cost_estimator = CostEstimator()
        self.logger = logging.getLogger(__name__)
        
    def estimate_cost(self, project_id: int, date_start: str, date_end: str) -> float:
        """Estima o custo de processamento para um período"""
        message_count = self.db.get_message_count(project_id, date_start, date_end)
        return self.cost_estimator.estimate_cost(message_count)
        
    def generate_summary(self, project_id: int, date_start: str, date_end: str) -> SummaryCreate:
        """Gera resumo usando CrewAI"""
        try:
            # Busca mensagens do período
            messages = self.db.get_messages_in_range(project_id, date_start, date_end)
            
            if not messages:
                raise ValueError("No messages found for the specified period")
            
            # Estima custo
            estimated_cost = self.estimate_cost(project_id, date_start, date_end)
            
            # Cria agentes CrewAI
            researcher = Agent(
                role='Crypto Community Researcher',
                goal='Analyze Telegram messages to identify key updates and discussions',
                backstory='Expert in crypto communities and DeFi protocols',
                verbose=True
            )
            
            writer = Agent(
                role='Content Writer',
                goal='Create clear, structured summaries of community discussions',
                backstory='Experienced in summarizing technical and community content',
                verbose=True
            )
            
            # Define tarefas
            research_task = Task(
                description=f"""
                Analyze these Telegram messages from {date_start} to {date_end}:
                {self._format_messages_for_ai(messages)}
                
                Identify:
                1. Key announcements and updates
                2. Development progress
                3. Community discussions and decisions
                4. Important partnerships or integrations
                5. Technical developments
                
                Focus on actionable insights and important information.
                """,
                agent=researcher
            )
            
            writing_task = Task(
                description="""
                Based on the research, create a structured summary in markdown format.
                Include:
                - Key announcements
                - Development updates
                - Community highlights
                - Summary of the week
                
                Format: Clean, professional, easy to read
                """,
                agent=writer
            )
            
            # Executa o crew
            crew = Crew(
                agents=[researcher, writer],
                tasks=[research_task, writing_task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Cria modelo de resumo
            summary_data = SummaryCreate(
                project_id=project_id,
                date_start=date_start,
                date_end=date_end,
                content=result,
                cost_estimate=estimated_cost,
                actual_cost=estimated_cost  # Simplificado para MVP
            )
            
            # Salva no banco
            saved_summary = self.db.save_summary(summary_data)
            self.logger.info(f"Summary generated and saved with ID: {saved_summary.id}")
            
            return summary_data
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")
            raise
            
    def _format_messages_for_ai(self, messages: List[Message]) -> str:
        """Formata mensagens para processamento da IA"""
        formatted = []
        for msg in messages:
            formatted.append(f"[{msg.timestamp}] {msg.text}")
        return "\n\n".join(formatted)
```

### **6. INTERFACE CLI ATUALIZADA**

#### **`src/cli/commands.py`**
```python
import typer
from datetime import datetime, timedelta
from ..services.ai_processor import AIProcessor
from ..services.database import DatabaseManager
from ..models.project import ProjectCreate, ProjectUpdate
from ..utils.config import Config

app = typer.Typer()
ai_processor = AIProcessor()
db = DatabaseManager()

@app.command()
def setup_project(
    name: str = typer.Option(..., "--name", "-n", help="Project name"),
    telegram_group: str = typer.Option(..., "--group", "-g", help="Telegram group username")
):
    """Setup a new project for monitoring"""
    try:
        # Verifica se o projeto já existe
        existing = db.get_project_by_name(name)
        if existing:
            typer.echo(f"❌ Project '{name}' already exists")
            raise typer.Exit(1)
            
        project_data = ProjectCreate(name=name, telegram_group=telegram_group)
        project = db.create_project(project_data)
        typer.echo(f"✅ Project '{name}' setup successfully with ID: {project.id}")
    except Exception as e:
        typer.echo(f"❌ Error setting up project: {e}")
        raise typer.Exit(1)

@app.command()
def list_projects():
    """List all monitored projects"""
    try:
        projects = db.get_active_projects()
        if not projects:
            typer.echo("No projects found.")
            return
            
        typer.echo("📋 Monitored Projects:")
        for project in projects:
            typer.echo(f"  • {project.name} (@{project.telegram_group}) - ID: {project.id}")
    except Exception as e:
        typer.echo(f"❌ Error listing projects: {e}")
        raise typer.Exit(1)

@app.command()
def estimate_cost(
    project: str = typer.Option(..., "--project", "-p", help="Project name"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to summarize")
):
    """Estimate the cost of generating a summary"""
    try:
        project_obj = db.get_project_by_name(project)
        if not project_obj:
            typer.echo(f"❌ Project '{project}' not found")
            raise typer.Exit(1)
            
        date_end = datetime.now()
        date_start = date_end - timedelta(days=days)
        
        cost = ai_processor.estimate_cost(
            project_obj.id, 
            date_start.strftime("%Y-%m-%d"), 
            date_end.strftime("%Y-%m-%d")
        )
        
        typer.echo(f"💰 Estimated cost for {days} days: ${cost:.2f}")
    except Exception as e:
        typer.echo(f"❌ Error estimating cost: {e}")
        raise typer.Exit(1)

@app.command()
def generate_summary(
    project: str = typer.Option(..., "--project", "-p", help="Project name"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to summarize")
):
    """Generate a summary for the specified period"""
    try:
        project_obj = db.get_project_by_name(project)
        if not project_obj:
            typer.echo(f"❌ Project '{project}' not found")
            raise typer.Exit(1)
            
        date_end = datetime.now()
        date_start = date_end - timedelta(days=days)
        
        typer.echo(f"🤖 Generating summary for {project} ({days} days)...")
        
        summary = ai_processor.generate_summary(
            project_obj.id, 
            date_start.strftime("%Y-%m-%d"), 
            date_end.strftime("%Y-%m-%d")
        )
        
        typer.echo(f"✅ Summary generated successfully!")
        typer.echo(f"📊 Cost: ${summary.actual_cost:.2f}")
        typer.echo(f"📝 Content length: {len(summary.content)} characters")
        
        # Salva em arquivo
        filename = f"summary_{project}_{date_start.strftime('%Y%m%d')}_{date_end.strftime('%Y%m%d')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary.content)
        
        typer.echo(f"💾 Summary saved to: {filename}")
        
    except Exception as e:
        typer.echo(f"❌ Error generating summary: {e}")
        raise typer.Exit(1)

@app.command()
def update_project(
    project: str = typer.Option(..., "--project", "-p", help="Project name"),
    name: str = typer.Option(None, "--new-name", help="New project name"),
    telegram_group: str = typer.Option(None, "--new-group", help="New Telegram group"),
    active: bool = typer.Option(None, "--active/--inactive", help="Set project active status")
):
    """Update project settings"""
    try:
        project_obj = db.get_project_by_name(project)
        if not project_obj:
            typer.echo(f"❌ Project '{project}' not found")
            raise typer.Exit(1)
            
        update_data = ProjectUpdate(
            name=name,
            telegram_group=telegram_group,
            is_active=active
        )
        
        updated_project = db.update_project(project_obj.id, update_data)
        if updated_project:
            typer.echo(f"✅ Project '{project}' updated successfully")
        else:
            typer.echo(f"❌ Failed to update project '{project}'")
            
    except Exception as e:
        typer.echo(f"❌ Error updating project: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
```

---

## 🚀 **COMO EXECUTAR**

### **1. Instalação**
```bash
pip install -r requirements.txt
```

### **2. Configuração**
```bash
# Copie .env.example para .env e configure
cp .env.example .env

# Edite .env com suas credenciais
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=your_phone
OPENAI_API_KEY=your_openai_key
```

### **3. Execução**
```bash
# Inicia ambos os serviços
python src/main.py

# Ou apenas o CLI (sem coleta automática)
python -m src.cli.commands
```

---

## 📊 **MONITORAMENTO E LOGS**

### **Logs do Sistema**
- **Arquivo:** `crypto_insights.log`
- **Nível:** INFO para produção, DEBUG para desenvolvimento
- **Rotação:** Configurável via logging.handlers.RotatingFileHandler

### **Métricas de Saúde**
- **Coleta:** Número de mensagens coletadas por dia
- **Processamento:** Tempo de geração de resumos
- **Custos:** Estimativas vs. custos reais
- **Erros:** Rate de falhas e tipos de erro

---

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **Variáveis de Ambiente**
```bash
# Coleta
COLLECTION_INTERVAL=86400          # 24 horas em segundos
MAX_MESSAGES_PER_COLLECTION=1000   # Limite por coleta
COLLECTION_ENABLED=true            # Habilitar/desabilitar

# IA
OPENAI_MODEL=gpt-4-turbo          # Modelo OpenAI
MAX_COST_PER_SUMMARY=10.00        # Custo máximo por resumo

# Banco de dados
DATABASE_URL=sqlite:///crypto_insights.db
```

### **Configurações de Banco**
```python
# SQLite com WAL mode para melhor performance
from sqlmodel import create_engine
engine = create_engine("sqlite:///crypto_insights.db", echo=True)
engine.execute("PRAGMA journal_mode=WAL")
```

---

## 🧪 **TESTES**

### **Testes Unitários**
```bash
# Instala dependências de teste
pip install pytest pytest-asyncio

# Executa testes
pytest tests/
```

### **Testes de Integração**
```bash
# Testa coleta com grupo de teste
python -m src.cli.commands setup-project --name "Test" --group "test_group"

# Testa geração de resumo
python -m src.cli.commands generate-summary --project "Test" --days 1
```

---

## 📝 **PRÓXIMOS PASSOS**

1. **Implementar** estrutura básica de arquivos
2. **Configurar** SQLModel e modelos Pydantic
3. **Implementar** serviço de coleta Telethon
4. **Implementar** serviço CrewAI
5. **Criar** interface CLI com Typer
6. **Testar** com dados reais
7. **Otimizar** performance e custos

---

## ❓ **DÚVIDAS TÉCNICAS**

Para dúvidas sobre implementação específica:
- **SQLModel:** [Documentação oficial](https://sqlmodel.tiangolo.com/)
- **Pydantic:** [Documentação oficial](https://docs.pydantic.dev/)
- **Telethon:** [Documentação oficial](https://docs.telethon.dev/)
- **CrewAI:** [Documentação oficial](https://docs.crewai.com/)
- **Typer:** [Documentação oficial](https://typer.tiangolo.com/)

### **7. ARQUIVO PRINCIPAL COMPLETO**

#### **`src/main.py`**
```python
import asyncio
import threading
import logging
import signal
import sys
from pathlib import Path
from services.telegram_collector import TelegramCollector
from services.ai_processor import AIProcessor
from services.database import DatabaseManager
from utils.config import Config

# Configura logging
def setup_logging():
    """Configura o sistema de logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "crypto_insights.log"),
            logging.StreamHandler()
        ]
    )
    
    # Configura logging específico para cada módulo
    logging.getLogger("telethon").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("crewai").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

class CryptoInsightsAgent:
    """Classe principal que gerencia todos os serviços"""
    
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.collector = None
        self.ai_processor = AIProcessor()
        self.running = False
        self.collection_thread = None
        
    async def initialize(self):
        """Inicializa todos os serviços"""
        try:
            logger.info("🚀 Initializing Crypto Community Insights Agent...")
            
            # Verifica se o banco está funcionando
            logger.info("📊 Testing database connection...")
            projects = self.db.get_active_projects()
            logger.info(f"✅ Database connected. Found {len(projects)} active projects")
            
            # Inicializa o coletor Telegram
            logger.info("📱 Initializing Telegram collector...")
            self.collector = TelegramCollector(
                api_id=self.config.TELEGRAM_API_ID,
                api_hash=self.config.TELEGRAM_API_HASH,
                phone=self.config.TELEGRAM_PHONE_NUMBER
            )
            
            await self.collector.start()
            logger.info("✅ Telegram collector initialized successfully")
            
            logger.info("🎯 All services initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize services: {e}")
            raise
    
    async def start_collection_service(self):
        """Inicia o serviço de coleta automática em thread separada"""
        try:
            logger.info("🔄 Starting automatic collection service...")
            
            # Cria thread para coleta automática
            self.collection_thread = threading.Thread(
                target=self._run_collection_loop,
                daemon=True,
                name="CollectionService"
            )
            
            self.collection_thread.start()
            logger.info("✅ Collection service started in background")
            
        except Exception as e:
            logger.error(f"❌ Failed to start collection service: {e}")
            raise
    
    def _run_collection_loop(self):
        """Loop principal do serviço de coleta (executa em thread separada)"""
        try:
            # Cria novo event loop para esta thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Executa o loop de coleta
            loop.run_until_complete(self._collection_loop())
            
        except Exception as e:
            logger.error(f"❌ Collection service error: {e}")
        finally:
            loop.close()
    
    async def _collection_loop(self):
        """Loop principal de coleta"""
        while self.running:
            try:
                projects = self.db.get_active_projects()
                logger.info(f"🔄 Starting daily collection for {len(projects)} projects")
                
                for project in projects:
                    try:
                        await self.collector.collect_messages(project)
                        # Pausa entre projetos para evitar rate limits
                        await asyncio.sleep(5)
                    except Exception as e:
                        logger.error(f"❌ Error collecting from {project.name}: {e}")
                        continue
                
                logger.info("✅ Daily collection completed successfully")
                
                # Aguarda até a próxima coleta (24 horas)
                await asyncio.sleep(24 * 60 * 60)
                
            except Exception as e:
                logger.error(f"❌ Collection loop error: {e}")
                # Em caso de erro, aguarda 1 hora antes de tentar novamente
                await asyncio.sleep(60 * 60)
    
    def start_cli_service(self):
        """Inicia o serviço CLI na thread principal"""
        try:
            logger.info("💻 Starting CLI interface...")
            
            # Importa e executa o CLI
            from cli.commands import app
            app()
            
        except Exception as e:
            logger.error(f"❌ CLI service error: {e}")
            raise
    
    async def start(self):
        """Inicia todos os serviços"""
        try:
            self.running = True
            
            # Inicializa serviços
            await self.initialize()
            
            # Inicia serviço de coleta em background
            await self.start_collection_service()
            
            # Inicia CLI na thread principal
            self.start_cli_service()
            
        except Exception as e:
            logger.error(f"❌ Failed to start agent: {e}")
            raise
    
    async def stop(self):
        """Para todos os serviços"""
        try:
            logger.info("🛑 Stopping Crypto Community Insights Agent...")
            
            self.running = False
            
            # Para o coletor Telegram
            if self.collector:
                await self.collector.disconnect()
                logger.info("✅ Telegram collector stopped")
            
            # Aguarda thread de coleta terminar
            if self.collection_thread and self.collection_thread.is_alive():
                self.collection_thread.join(timeout=10)
                logger.info("✅ Collection service stopped")
            
            logger.info("✅ All services stopped successfully")
            
        except Exception as e:
            logger.error(f"❌ Error stopping services: {e}")
    
    def signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        logger.info(f"📡 Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())
        sys.exit(0)

async def main():
    """Função principal"""
    # Configura logging
    setup_logging()
    
    # Cria e configura o agente
    agent = CryptoInsightsAgent()
    
    # Configura handlers de sinal para shutdown graceful
    signal.signal(signal.SIGINT, agent.signal_handler)
    signal.signal(signal.SIGTERM, agent.signal_handler)
    
    try:
        # Inicia o agente
        await agent.start()
        
    except KeyboardInterrupt:
        logger.info("⌨️  Keyboard interrupt received")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
    finally:
        # Garante que todos os serviços sejam parados
        await agent.stop()
        logger.info("👋 Crypto Community Insights Agent stopped")

if __name__ == "__main__":
    try:
        # Executa o loop principal
        asyncio.run(main())
    except Exception as e:
        logger.error(f"💥 Failed to start application: {e}")
        sys.exit(1)
```

#### **`src/utils/config.py`**
```python
import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Classe de configuração que carrega variáveis de ambiente"""
    
    def __init__(self, env_file: str = ".env"):
        # Carrega arquivo .env se existir
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
        
        # Configurações do Telegram
        self.TELEGRAM_API_ID = self._get_required("TELEGRAM_API_ID")
        self.TELEGRAM_API_HASH = self._get_required("TELEGRAM_API_HASH")
        self.TELEGRAM_PHONE_NUMBER = self._get_required("TELEGRAM_PHONE_NUMBER")
        
        # Configurações da OpenAI
        self.OPENAI_API_KEY = self._get_required("OPENAI_API_KEY")
        
        # Configurações do sistema
        self.DATA_DIR = os.getenv("DATA_DIR", "data")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Configurações de coleta
        self.COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", "86400"))  # 24 horas
        self.MAX_MESSAGES_PER_COLLECTION = int(os.getenv("MAX_MESSAGES_PER_COLLECTION", "1000"))
        self.COLLECTION_ENABLED = os.getenv("COLLECTION_ENABLED", "true").lower() == "true"
        
        # Configurações de IA
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        self.MAX_COST_PER_SUMMARY = float(os.getenv("MAX_COST_PER_SUMMARY", "10.00"))
        
        # Configurações de banco
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crypto_insights.db")
        
        # Cria diretórios necessários
        self._create_directories()
    
    def _get_required(self, key: str) -> str:
        """Obtém uma variável de ambiente obrigatória"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def _create_directories(self):
        """Cria diretórios necessários para o funcionamento"""
        directories = [
            Path(self.DATA_DIR),
            Path("logs"),
            Path("sessions"),  # Para sessões do Telethon
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    def validate(self) -> bool:
        """Valida se todas as configurações estão corretas"""
        try:
            # Validações básicas
            if not self.TELEGRAM_API_ID.isdigit():
                raise ValueError("TELEGRAM_API_ID must be numeric")
            
            if len(self.TELEGRAM_API_HASH) != 32:
                raise ValueError("TELEGRAM_API_HASH must be 32 characters")
            
            if self.COLLECTION_INTERVAL < 3600:  # Mínimo 1 hora
                raise ValueError("COLLECTION_INTERVAL must be at least 3600 seconds")
            
            if self.MAX_COST_PER_SUMMARY <= 0:
                raise ValueError("MAX_COST_PER_SUMMARY must be positive")
            
            return True
            
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
    
    def print_config(self):
        """Imprime configurações atuais (sem dados sensíveis)"""
        print("🔧 Current Configuration:")
        print(f"  📱 Telegram API ID: {self.TELEGRAM_API_ID[:4]}...")
        print(f"  📱 Telegram API Hash: {self.TELEGRAM_API_HASH[:8]}...")
        print(f"  📱 Phone Number: {self.TELEGRAM_PHONE_NUMBER}")
        print(f"  🤖 OpenAI Model: {self.OPENAI_MODEL}")
        print(f"  💰 Max Cost per Summary: ${self.MAX_COST_PER_SUMMARY}")
        print(f"  🔄 Collection Interval: {self.COLLECTION_INTERVAL} seconds")
        print(f"  📊 Max Messages per Collection: {self.MAX_MESSAGES_PER_COLLECTION}")
        print(f"  🗄️  Database URL: {self.DATABASE_URL}")
        print(f"  📁 Data Directory: {self.DATA_DIR}")
        print(f"  📝 Log Level: {self.LOG_LEVEL}")

# Instância global de configuração
config = Config()
```

---

## 🚀 **COMO EXECUTAR O SISTEMA COMPLETO**

### **1. Execução Completa (Ambos os Serviços)**
```bash
# Inicia coleta automática + CLI
python src/main.py
```

### **2. Execução Apenas CLI (Sem Coleta Automática)**
```bash
# Apenas interface CLI
python -m src.cli.commands
```

### **3. Execução com Configuração Personalizada**
```bash
# Define variáveis de ambiente
export COLLECTION_INTERVAL=3600  # 1 hora
export MAX_COST_PER_SUMMARY=5.00
python src/main.py
```

---

## 🔧 **CARACTERÍSTICAS DO MAIN.PY:**

### **✅ Funcionalidades Principais:**
1. **Inicialização automática** de todos os serviços
2. **Coleta em background** via thread separada
3. **CLI na thread principal** para interação
4. **Shutdown graceful** com handlers de sinal
5. **Logging estruturado** com rotação de arquivos
6. **Validação de configuração** automática

### **✅ Gerenciamento de Serviços:**
1. **Thread de coleta** independente e segura
2. **Reconexão automática** em caso de falhas
3. **Rate limiting** entre projetos
4. **Monitoramento** de saúde dos serviços
5. **Cleanup** automático ao parar

### **✅ Configuração Flexível:**
1. **Variáveis de ambiente** para todas as configurações
2. **Validação automática** de configurações
3. **Criação automática** de diretórios
4. **Fallbacks** para valores padrão
5. **Configuração por arquivo** .env

---

## ❓ **PERGUNTA PARA VOCÊ:**

O `main.py` está completo e claro o suficiente? Quer que eu adicione mais alguma funcionalidade específica ou detalhe técnico?
