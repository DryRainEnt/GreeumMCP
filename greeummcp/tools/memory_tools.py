"""
Memory-related tools for GreeumMCP.

This module contains standalone tool functions that can be registered with the MCP server
and interact with Greeum memory components.
"""
from typing import Dict, List, Any, Optional
import asyncio

class MemoryTools:
    """Memory tools for GreeumMCP."""
    
    def __init__(self, block_manager, stm_manager, cache_manager, temporal_reasoner):
        """
        Initialize MemoryTools with required Greeum components.
        
        Args:
            block_manager: BlockManager instance
            stm_manager: STMManager instance
            cache_manager: CacheManager instance
            temporal_reasoner: TemporalReasoner instance
        """
        self.block_manager = block_manager
        self.stm_manager = stm_manager
        self.cache_manager = cache_manager
        self.temporal_reasoner = temporal_reasoner
    
    async def add_memory(self, content: str, importance: float = 0.5) -> str:
        """
        Add a new memory to the long-term storage.
        
        Args:
            content: The content of the memory to store
            importance: The importance of the memory (0.0-1.0)
        
        Returns:
            Memory ID of the created memory
        """
        from memory_engine.text_utils import process_user_input
        
        processed = process_user_input(content)
        
        # Add to long-term memory
        memory_id = self.block_manager.add_block(
            context=processed.get("context", content),
            keywords=processed.get("keywords", []),
            tags=processed.get("tags", []),
            importance=importance,
            embedding=processed.get("embedding", None)
        )
        
        # Also add to short-term memory with medium TTL
        self.stm_manager.add_memory(content, ttl_type="medium")
        
        return str(memory_id)
    
    async def query_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search memories by query text.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
        
        Returns:
            List of matching memory blocks
        """
        from memory_engine.text_utils import process_user_input, compute_embedding
        
        processed = process_user_input(query)
        query_embedding = processed.get("embedding", compute_embedding(query))
        query_keywords = processed.get("keywords", [])
        
        # Update cache with query
        self.cache_manager.update_cache(
            query_embedding=query_embedding,
            query_keywords=query_keywords
        )
        
        # Get relevant blocks through cache
        results = self.cache_manager.get_relevant_blocks(
            query_embedding=query_embedding,
            query_keywords=query_keywords,
            limit=limit
        )
        
        # Format results
        formatted_results = []
        for block in results:
            formatted_results.append({
                "id": block.get("id", ""),
                "content": block.get("context", ""),
                "timestamp": block.get("timestamp", ""),
                "keywords": block.get("keywords", []),
                "importance": block.get("importance", 0.5)
            })
        
        return formatted_results
    
    async def retrieve_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific memory by ID.
        
        Args:
            memory_id: The ID of the memory to retrieve
        
        Returns:
            Memory block data
        """
        memory = self.block_manager.get_memory(memory_id)
        if not memory:
            return {"error": "Memory not found"}
        
        return {
            "id": memory_id,
            "content": memory.get("context", ""),
            "timestamp": memory.get("timestamp", ""),
            "keywords": memory.get("keywords", []),
            "importance": memory.get("importance", 0.5)
        }
    
    async def update_memory(self, memory_id: str, content: str) -> Dict[str, Any]:
        """
        Update an existing memory.
        
        Args:
            memory_id: The ID of the memory to update
            content: The new content for the memory
        
        Returns:
            Status of the update operation
        """
        try:
            self.block_manager.update_memory(memory_id, content)
            return {"success": True, "message": "Memory updated successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        Delete a memory by ID.
        
        Args:
            memory_id: The ID of the memory to delete
        
        Returns:
            Status of the delete operation
        """
        try:
            self.block_manager.delete_memory(memory_id)
            return {"success": True, "message": "Memory deleted successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def search_time(self, time_query: str, language: str = "auto") -> List[Dict[str, Any]]:
        """
        Search memories based on time references.
        
        Args:
            time_query: Query containing time references (e.g., "yesterday", "3 days ago")
            language: Language of the query ("ko", "en", or "auto")
        
        Returns:
            List of memories matching the time reference
        """
        results = self.temporal_reasoner.search_by_time_reference(
            time_query,
            margin_hours=12
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.get("id", ""),
                "content": result.get("context", ""),
                "timestamp": result.get("timestamp", ""),
                "time_relevance": result.get("time_relevance", 0.0),
                "keywords": result.get("keywords", [])
            })
        
        return formatted_results
    
    async def get_stm_memories(self, limit: int = 10, include_expired: bool = False) -> List[Dict[str, Any]]:
        """
        Get short-term memories.
        
        Args:
            limit: Maximum number of memories to return
            include_expired: Whether to include expired memories
        
        Returns:
            List of short-term memories
        """
        memories = self.stm_manager.get_memories(
            limit=limit,
            include_expired=include_expired
        )
        
        # Format results
        formatted_results = []
        for memory in memories:
            formatted_results.append({
                "id": memory.get("id", ""),
                "content": memory.get("content", ""),
                "timestamp": memory.get("timestamp", ""),
                "ttl": memory.get("ttl", 0),
                "expired": memory.get("expired", False)
            })
        
        return formatted_results
    
    async def forget_stm(self, memory_id: str) -> Dict[str, Any]:
        """
        Forget a short-term memory.
        
        Args:
            memory_id: The ID of the short-term memory to forget
        
        Returns:
            Status of the forget operation
        """
        try:
            self.stm_manager.forget(memory_id)
            return {"success": True, "message": "Short-term memory forgotten"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def cleanup_expired_memories(self) -> Dict[str, Any]:
        """
        Clean up expired short-term memories.
        
        Returns:
            Number of memories cleaned up
        """
        try:
            count = self.stm_manager.cleanup_expired()
            return {"success": True, "count": count, "message": f"Cleaned up {count} expired memories"}
        except Exception as e:
            return {"success": False, "message": str(e)} 