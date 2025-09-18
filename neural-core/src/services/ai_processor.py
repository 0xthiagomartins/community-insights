import logging
import os
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from models import Project, Message, Summary
from services.database import DatabaseManager
from services.relevance_analyzer import RelevanceAnalyzer
from utils.config import Config

logger = logging.getLogger(__name__)

@dataclass
class CostEstimate:
    """Estrutura para estimativa de custo"""
    total_cost: float
    message_count: int
    cost_per_message: float
    estimated_tokens: int

class AIProcessor:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.relevance_analyzer = RelevanceAnalyzer()
        self._setup_langchain()
    
    def _setup_langchain(self):
        """Configura o LangChain com OpenAI"""
        try:
            # Set OpenAI API key
            os.environ["OPENAI_API_KEY"] = self.config.OPENAI_API_KEY
            
            # Initialize ChatOpenAI
            self.llm = ChatOpenAI(
                model=self.config.DEFAULT_MODEL,
                temperature=0.1,
                verbose=self.config.LANGCHAIN_VERBOSE
            )
            
            # Create prompt template
            self.prompt_template = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are an expert community analyst who specializes in analyzing community discussions and extracting key insights. 
                
Your task is to analyze community messages and create a comprehensive summary that highlights:
1. Key announcements and updates
2. Important discussions and decisions  
3. Community sentiment and concerns
4. Technical developments
5. Governance activities

Format your response as a clear, structured markdown summary with the following sections:
## Key Announcements
## Development Updates
## Community Highlights  
## Summary

Be concise but informative, focusing on actionable insights that would be valuable for community members."""),
                HumanMessage(content="""Please analyze the following community messages from {project_name} and create a comprehensive summary:

{messages_text}

Focus on extracting the most important information and presenting it in a clear, structured format.""")
            ])
            
            logger.info("✅ LangChain configured successfully")
            
        except Exception as e:
            logger.error(f"❌ Error setting up LangChain: {e}")
            raise
    
    def estimate_cost(self, project: Project, start_date: datetime, end_date: datetime) -> CostEstimate:
        """Estima o custo de processamento para um projeto e período"""
        try:
            # Busca mensagens no período
            messages = self.db.get_messages_by_project(
                project.id, start_date, end_date
            )
            
            if not messages:
                return CostEstimate(
                    total_cost=0.0,
                    message_count=0,
                    cost_per_message=0.0,
                    estimated_tokens=0
                )
            
            # Estima tokens (aproximação simples)
            total_chars = sum(len(msg.content) for msg in messages)
            estimated_tokens = total_chars // 4  # Aproximação: 4 chars = 1 token
            
            # Adiciona tokens de saída estimados
            output_tokens = 500  # Resumo estimado
            total_tokens = estimated_tokens + output_tokens
            
            # Calcula custo (GPT-3.5 Turbo pricing)
            input_cost = (estimated_tokens / 1000) * 0.0015  # $0.0015 per 1K tokens
            output_cost = (output_tokens / 1000) * 0.002     # $0.002 per 1K tokens
            total_cost = input_cost + output_cost
            
            cost_per_message = total_cost / len(messages) if messages else 0.0
            
            return CostEstimate(
                total_cost=total_cost,
                message_count=len(messages),
                cost_per_message=cost_per_message,
                estimated_tokens=total_tokens
            )
            
        except Exception as e:
            logger.error(f"❌ Error estimating cost: {e}")
            raise
    
    def generate_summary(self, project: Project, start_date: datetime, end_date: datetime) -> Summary:
        """Gera um resumo para um projeto e período"""
        try:
            # Busca mensagens no período
            messages = self.db.get_messages_by_project(
                project.id, start_date, end_date
            )
            
            if not messages:
                raise ValueError(f"No messages found for project {project.name} in the specified period")
            
            # Estima custo antes do processamento
            cost_estimate = self.estimate_cost(project, start_date, end_date)
            
            # Verifica limite de custo
            if cost_estimate.total_cost > self.config.MAX_COST_PER_SUMMARY:
                raise ValueError(f"Estimated cost ${cost_estimate.total_cost:.2f} exceeds limit ${self.config.MAX_COST_PER_SUMMARY}")
            
            # Prepara dados para processamento
            messages_text = self._prepare_messages_for_ai(messages)
            
            # Cria o prompt
            prompt = self.prompt_template.format_messages(
                project_name=project.name,
                messages_text=messages_text
            )
            
            # Executa o processamento
            result = self.llm.invoke(prompt)
            summary_content = result.content
            
            # Calcula custo real (aproximação)
            actual_cost = cost_estimate.total_cost * 1.1  # 10% de margem
            
            # Gera metadata e citações (sempre)
            logger.info("Generating metadata and citations...")
            metadata_json, citations_json, high_relevance_count = self._generate_metadata_and_citations(
                messages, summary_content, project.name
            )
            
            # Cria o resumo no banco
            summary = self.db.create_summary(
                project_id=project.id,
                content=summary_content,
                date_range_start=start_date,
                date_range_end=end_date,
                cost_estimate=cost_estimate.total_cost,
                actual_cost=actual_cost,
                message_count=len(messages),
                summary_metadata=metadata_json,
                citations=citations_json,
                high_relevance_count=high_relevance_count
            )
            
            logger.info(f"✅ Summary generated for {project.name} with {len(messages)} messages")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating summary: {e}")
            raise
    
    def _generate_metadata_and_citations(self, messages: List[Message], summary_content: str, project_name: str) -> tuple:
        """Gera metadata e citações para o resumo"""
        try:
            # Analisa relevância das mensagens
            relevance_scores = self.relevance_analyzer.analyze_messages_batch(messages)
            
            # Gera metadata de relevância
            metadata = self.relevance_analyzer.generate_relevance_metadata(messages, relevance_scores)
            
            # Gera citações baseadas no resumo
            citations = self._extract_citations_from_summary(summary_content, messages, relevance_scores)
            
            # Conta mensagens de alta relevância
            high_relevance_count = len([s for s in relevance_scores if s.score >= 80])
            
            # Converte para JSON
            metadata_json = json.dumps(metadata, indent=2)
            citations_json = json.dumps(citations, indent=2)
            
            logger.info(f"Generated metadata for {len(messages)} messages with {high_relevance_count} high-relevance")
            
            return metadata_json, citations_json, high_relevance_count
            
        except Exception as e:
            logger.error(f"Error generating metadata and citations: {e}")
            return None, None, 0

    def _extract_citations_from_summary(self, summary_content: str, messages: List[Message], relevance_scores: List) -> List[Dict[str, Any]]:
        """Extrai citações do resumo baseado nas mensagens de alta relevância"""
        citations = []
        
        # Mapeia scores por message_id
        score_map = {score.message_id: score for score in relevance_scores}
        
        # Pega mensagens de alta relevância
        high_relevance_messages = []
        for message in messages:
            if message.id in score_map and score_map[message.id].score >= 80:
                high_relevance_messages.append((message, score_map[message.id]))
        
        # Ordena por relevância
        high_relevance_messages.sort(key=lambda x: x[1].score, reverse=True)
        
        # Cria citações para as top mensagens
        for message, score in high_relevance_messages[:20]:  # Top 20 mensagens
            citation = {
                "message_id": message.id,
                "telegram_message_id": message.telegram_message_id,
                "author": message.author,
                "timestamp": message.timestamp.isoformat(),
                "content_preview": message.content[:200] + "..." if len(message.content) > 200 else message.content,
                "relevance_score": score.score,
                "category": score.category,
                "confidence": score.confidence,
                "keywords": score.keywords,
                "reasoning": score.reasoning
            }
            citations.append(citation)
        
        return citations

    def _prepare_messages_for_ai(self, messages: List[Message]) -> str:
        """Prepara mensagens para processamento de IA"""
        formatted_messages = []
        
        for msg in messages:
            author = msg.author or "Unknown"
            timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M")
            content = msg.content[:500]  # Limita tamanho para evitar tokens excessivos
            
            formatted_messages.append(
                f"[{timestamp}] {author}: {content}"
            )
        
        return "\n\n".join(formatted_messages)