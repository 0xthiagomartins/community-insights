import asyncio
import logging
from typing import List, Optional
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Message as TelegramMessage
from telethon.errors import FloodWaitError, ChannelPrivateError
from models import Project, Message
from services.database import DatabaseManager
from utils.config import Config

logger = logging.getLogger(__name__)

class TelegramCollector:
    def __init__(self, api_id: int, api_hash: str, phone: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = None
        self.db = DatabaseManager()
        self.config = Config()
    
    async def start(self):
        """Inicia o cliente Telegram"""
        try:
            self.client = TelegramClient(
                self.config.SESSIONS_DIR / "crypto_insights",
                self.api_id,
                self.api_hash
            )
            
            await self.client.start(phone=self.phone)
            logger.info("Telegram client started successfully")
            
        except Exception as e:
            logger.error(f"Error starting Telegram client: {e}")
            raise
    
    async def disconnect(self):
        """Desconecta o cliente Telegram"""
        if self.client:
            await self.client.disconnect()
            logger.info("Telegram client disconnected")
    
    async def collect_messages(self, project: Project):
        """Coleta mensagens de um projeto"""
        try:
            logger.info(f"Starting collection for project: {project.name}")
            
            # Busca o grupo/canal
            entity = await self.client.get_entity(project.telegram_group)
            
            # Busca a última mensagem coletada
            last_message_id = project.last_collected_message_id or 0
            
            # Coleta mensagens novas
            messages_collected = 0
            async for message in self.client.iter_messages(
                entity,
                min_id=last_message_id,
                limit=self.config.MAX_MESSAGES_PER_COLLECTION
            ):
                if await self._process_message(message, project):
                    messages_collected += 1
                
                # Atualiza o ID da última mensagem coletada
                if message.id > last_message_id:
                    last_message_id = message.id
            
            # Atualiza o projeto com o último ID coletado
            if last_message_id > (project.last_collected_message_id or 0):
                self.db.update_project(
                    project.id,
                    last_collected_message_id=last_message_id
                )
            
            logger.info(f"Collected {messages_collected} new messages for {project.name}")
            
        except FloodWaitError as e:
            logger.warning(f"Rate limit hit for {project.name}, waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except ChannelPrivateError:
            logger.error(f"Channel {project.telegram_group} is private or inaccessible")
        except Exception as e:
            logger.error(f"Error collecting messages from {project.name}: {e}")
            raise
    
    async def _process_message(self, message: TelegramMessage, project: Project) -> bool:
        """Processa uma mensagem individual"""
        try:
            # Filtra apenas mensagens de texto
            if not message.text:
                return False
            
            # Verifica se a mensagem já existe
            existing_message = self._get_existing_message(project.id, message.id)
            if existing_message:
                return False
            
            # Extrai informações da mensagem
            content = message.text
            author = None
            if message.sender:
                if hasattr(message.sender, 'username') and message.sender.username:
                    author = f"@{message.sender.username}"
                elif hasattr(message.sender, 'first_name'):
                    author = message.sender.first_name
                    if hasattr(message.sender, 'last_name') and message.sender.last_name:
                        author += f" {message.sender.last_name}"
            
            # Determina o tipo da mensagem
            message_type = "text"
            if "http" in content:
                message_type = "link"
            
            # Cria a mensagem no banco
            self.db.create_message(
                project_id=project.id,
                telegram_message_id=message.id,
                content=content,
                author=author,
                timestamp=message.date,
                message_type=message_type
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing message {message.id}: {e}")
            return False
    
    def _get_existing_message(self, project_id: int, telegram_message_id: int) -> Optional[Message]:
        """Verifica se uma mensagem já existe no banco"""
        with self.db.get_session() as session:
            from sqlmodel import select
            statement = select(Message).where(
                Message.project_id == project_id,
                Message.telegram_message_id == telegram_message_id
            )
            return session.exec(statement).first()
    
    async def test_connection(self, telegram_group: str) -> bool:
        """Testa a conexão com um grupo/canal"""
        try:
            entity = await self.client.get_entity(telegram_group)
            logger.info(f"Successfully connected to {telegram_group}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to {telegram_group}: {e}")
            return False
