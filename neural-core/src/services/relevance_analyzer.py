"""
Serviço para análise de relevância de mensagens
"""
import json
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

from models.message import Message

logger = logging.getLogger(__name__)

@dataclass
class RelevanceScore:
    """Estrutura para score de relevância"""
    message_id: int
    score: float  # 0-100
    category: str  # announcement, development, community, spam
    confidence: float  # 0-1
    keywords: List[str]
    reasoning: str

class RelevanceAnalyzer:
    """Analisador de relevância de mensagens"""
    
    def __init__(self):
        self.high_relevance_keywords = [
            # Anúncios oficiais
            "announce", "launch", "release", "partnership", "listing", "staking",
            "governance", "proposal", "vote", "upgrade", "mainnet", "testnet",
            
            # Desenvolvimento
            "update", "fix", "bug", "feature", "roadmap", "milestone",
            "development", "code", "commit", "merge", "deploy",
            
            # Técnico
            "consensus", "blockchain", "smart contract", "defi", "nft",
            "tokenomics", "whitepaper", "documentation", "api"
        ]
        
        self.spam_keywords = [
            "moon", "lambo", "pump", "dump", "hodl", "diamond hands",
            "wen", "wen moon", "to the moon", "buy the dip", "sell the news"
        ]
        
        self.admin_indicators = [
            "admin", "moderator", "official", "team", "founder", "ceo",
            "developer", "core team", "taraxa", "project"
        ]

    def analyze_message_relevance(self, message: Message) -> RelevanceScore:
        """Analisa a relevância de uma mensagem individual"""
        
        content = message.content.lower()
        author = message.author.lower() if message.author else ""
        
        # Score base
        score = 50.0
        category = "community"
        confidence = 0.5
        keywords = []
        reasoning_parts = []
        
        # Verificar se é admin/official
        is_admin = any(indicator in author for indicator in self.admin_indicators)
        if is_admin:
            score += 30
            category = "announcement"
            confidence += 0.3
            reasoning_parts.append("Official/admin message")
        
        # Verificar keywords de alta relevância
        high_rel_count = 0
        for keyword in self.high_relevance_keywords:
            if keyword in content:
                high_rel_count += 1
                keywords.append(keyword)
                score += 5
                confidence += 0.05
        
        if high_rel_count > 0:
            reasoning_parts.append(f"Contains {high_rel_count} high-relevance keywords")
            if category == "community":
                category = "development" if high_rel_count >= 3 else "community"
        
        # Verificar keywords de spam
        spam_count = 0
        for keyword in self.spam_keywords:
            if keyword in content:
                spam_count += 1
                score -= 10
                confidence += 0.1
        
        if spam_count > 0:
            reasoning_parts.append(f"Contains {spam_count} spam indicators")
            if spam_count >= 2:
                category = "spam"
                score = max(0, score - 20)
        
        # Verificar comprimento da mensagem
        if len(content) < 20:
            score -= 15
            reasoning_parts.append("Very short message")
        elif len(content) > 200:
            score += 5
            reasoning_parts.append("Detailed message")
        
        # Verificar se contém links
        if "http" in content or "www." in content:
            score += 10
            reasoning_parts.append("Contains links")
        
        # Verificar se contém números (pode ser preço, data, etc.)
        if any(char.isdigit() for char in content):
            score += 5
            reasoning_parts.append("Contains numerical data")
        
        # Normalizar score
        score = max(0, min(100, score))
        confidence = max(0, min(1, confidence))
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Standard community message"
        
        return RelevanceScore(
            message_id=message.id,
            score=score,
            category=category,
            confidence=confidence,
            keywords=keywords,
            reasoning=reasoning
        )

    def analyze_messages_batch(self, messages: List[Message]) -> List[RelevanceScore]:
        """Analisa relevância de um lote de mensagens"""
        logger.info(f"Analyzing relevance for {len(messages)} messages")
        
        scores = []
        for message in messages:
            try:
                score = self.analyze_message_relevance(message)
                scores.append(score)
            except Exception as e:
                logger.error(f"Error analyzing message {message.id}: {e}")
                # Score padrão em caso de erro
                scores.append(RelevanceScore(
                    message_id=message.id,
                    score=50.0,
                    category="community",
                    confidence=0.3,
                    keywords=[],
                    reasoning="Analysis error - default score"
                ))
        
        logger.info(f"Relevance analysis completed for {len(scores)} messages")
        return scores

    def get_high_relevance_messages(self, messages: List[Message], threshold: float = 80.0) -> List[Tuple[Message, RelevanceScore]]:
        """Retorna mensagens de alta relevância"""
        scores = self.analyze_messages_batch(messages)
        
        high_relevance = []
        for message, score in zip(messages, scores):
            if score.score >= threshold:
                high_relevance.append((message, score))
        
        logger.info(f"Found {len(high_relevance)} high-relevance messages (threshold: {threshold})")
        return high_relevance

    def generate_relevance_metadata(self, messages: List[Message], scores: List[RelevanceScore]) -> Dict[str, Any]:
        """Gera metadata sobre relevância das mensagens"""
        
        total_messages = len(messages)
        high_relevance_count = len([s for s in scores if s.score >= 80])
        medium_relevance_count = len([s for s in scores if 50 <= s.score < 80])
        low_relevance_count = len([s for s in scores if s.score < 50])
        
        # Categorias
        categories = {}
        for score in scores:
            cat = score.category
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        # Top keywords
        all_keywords = []
        for score in scores:
            all_keywords.extend(score.keywords)
        
        keyword_counts = {}
        for keyword in all_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Estatísticas
        avg_score = sum(s.score for s in scores) / len(scores) if scores else 0
        avg_confidence = sum(s.confidence for s in scores) / len(scores) if scores else 0
        
        metadata = {
            "total_messages": total_messages,
            "relevance_breakdown": {
                "high_relevance": high_relevance_count,
                "medium_relevance": medium_relevance_count,
                "low_relevance": low_relevance_count
            },
            "categories": categories,
            "top_keywords": top_keywords,
            "statistics": {
                "average_score": round(avg_score, 2),
                "average_confidence": round(avg_confidence, 3),
                "high_relevance_percentage": round((high_relevance_count / total_messages) * 100, 2) if total_messages > 0 else 0
            },
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
        
        return metadata
