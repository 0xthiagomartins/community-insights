import logging
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
from crewai import Agent, Task, Crew, Process
from models import Project, Message, Summary
from services.database import DatabaseManager
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
        self._setup_crewai()
    
    def _setup_crewai(self):
        """Configura os agentes CrewAI"""
        try:
            # Agente analisador de mensagens
            self.message_analyzer = Agent(
                role="Crypto Community Analyst",
                goal="Analyze crypto community messages and identify important information",
                backstory="You are an expert crypto analyst who understands community dynamics, project updates, and market sentiment.",
                verbose=True,
                allow_delegation=False
            )
            
            # Agente gerador de resumos
            self.summary_generator = Agent(
                role="Content Summarizer",
                goal="Create clear, structured summaries of crypto community discussions",
                backstory="You are a skilled content creator who can distill complex information into actionable insights.",
                verbose=True,
                allow_delegation=False
            )
            
            logger.info("✅ CrewAI agents configured successfully")
            
        except Exception as e:
            logger.error(f"❌ Error setting up CrewAI: {e}")
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
            
            # Calcula custo (GPT-4 Turbo pricing)
            input_cost = (estimated_tokens / 1000) * 0.01  # $0.01 per 1K tokens
            output_cost = (output_tokens / 1000) * 0.03    # $0.03 per 1K tokens
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
            
            # Cria tarefas CrewAI
            analysis_task = Task(
                description=f"""
                Analyze the following crypto community messages from {project.name} 
                and identify the most important information:
                
                {messages_text}
                
                Focus on:
                - Key announcements and updates
                - Important discussions and decisions
                - Community sentiment and concerns
                - Technical developments
                - Governance activities
                """,
                agent=self.message_analyzer,
                expected_output="Structured analysis of key information from the messages"
            )
            
            summary_task = Task(
                description="""
                Create a clear, structured summary based on the analysis.
                Format the summary in markdown with the following sections:
                
                ## Key Announcements
                ## Development Updates  
                ## Community Highlights
                ## Summary
                
                Make it concise but informative, focusing on actionable insights.
                """,
                agent=self.summary_generator,
                expected_output="Well-structured markdown summary"
            )
            
            # Executa o processamento
            crew = Crew(
                agents=[self.message_analyzer, self.summary_generator],
                tasks=[analysis_task, summary_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            summary_content = str(result)
            
            # Calcula custo real (aproximação)
            actual_cost = cost_estimate.total_cost * 1.1  # 10% de margem
            
            # Cria o resumo no banco
            summary = self.db.create_summary(
                project_id=project.id,
                content=summary_content,
                date_range_start=start_date,
                date_range_end=end_date,
                cost_estimate=cost_estimate.total_cost,
                actual_cost=actual_cost,
                message_count=len(messages)
            )
            
            logger.info(f"✅ Summary generated for {project.name} with {len(messages)} messages")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating summary: {e}")
            raise
    
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
