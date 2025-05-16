"""
Greeum adapter module for connecting Greeum components to MCP server.

This module provides adapter classes to bridge between Greeum memory components
and MCP server components.
"""
from typing import Dict, List, Any, Optional, Union
import os
import time

class GreeumAdapter:
    """
    Greeum adapter for interfacing with MCP.
    
    This adapter serves as a bridge between Greeum memory engine components
    and the MCP server, handling data conversion and proxy method calls.
    """
    
    def __init__(self, data_dir: str = "./data", greeum_config: Optional[Dict[str, Any]] = None):
        """
        Initialize Greeum adapter.
        
        Args:
            data_dir: Directory to store memory data
            greeum_config: Additional configuration for Greeum components
        """
        self.data_dir = data_dir
        self.config = greeum_config or {}
        self._initialized = False
        
        # Initialize components on first use to avoid import issues
        self._block_manager = None
        self._stm_manager = None
        self._cache_manager = None
        self._prompt_wrapper = None
        self._temporal_reasoner = None
    
    def initialize(self):
        """Initialize Greeum components if not already initialized."""
        if self._initialized:
            return
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        from memory_engine.block_manager import BlockManager
        from memory_engine.stm_manager import STMManager
        from memory_engine.cache_manager import CacheManager
        from memory_engine.prompt_wrapper import PromptWrapper
        from memory_engine.temporal_reasoner import TemporalReasoner
        
        # Initialize with custom embedding model if provided
        embedding_model = self.config.get("embedding_model", None)
        
        # Initialize core components
        self._block_manager = BlockManager(
            data_dir=self.data_dir,
            embedding_model=embedding_model
        )
        
        self._stm_manager = STMManager(
            data_dir=self.data_dir,
            ttl_short=self.config.get("ttl_short", 3600),
            ttl_medium=self.config.get("ttl_medium", 86400),
            ttl_long=self.config.get("ttl_long", 604800)
        )
        
        self._cache_manager = CacheManager(
            block_manager=self._block_manager,
            capacity=self.config.get("cache_capacity", 10)
        )
        
        self._prompt_wrapper = PromptWrapper(
            cache_manager=self._cache_manager,
            stm_manager=self._stm_manager
        )
        
        # Set custom template if provided
        if "prompt_template" in self.config:
            self._prompt_wrapper.set_template(self.config["prompt_template"])
        
        self._temporal_reasoner = TemporalReasoner(
            db_manager=self._block_manager,
            default_language=self.config.get("default_language", "auto")
        )
        
        self._initialized = True
    
    @property
    def block_manager(self):
        """Get the BlockManager instance, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._block_manager
    
    @property
    def stm_manager(self):
        """Get the STMManager instance, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._stm_manager
    
    @property
    def cache_manager(self):
        """Get the CacheManager instance, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._cache_manager
    
    @property
    def prompt_wrapper(self):
        """Get the PromptWrapper instance, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._prompt_wrapper
    
    @property
    def temporal_reasoner(self):
        """Get the TemporalReasoner instance, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._temporal_reasoner
    
    def convert_memory_to_dict(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a Greeum memory block to a standardized dictionary format."""
        if not memory:
            return {}
        
        return {
            "id": memory.get("id", ""),
            "content": memory.get("context", memory.get("content", "")),
            "timestamp": memory.get("timestamp", ""),
            "keywords": memory.get("keywords", []),
            "tags": memory.get("tags", []),
            "importance": memory.get("importance", 0.5),
            "embedding": memory.get("embedding", [])
        }
    
    def convert_memory_list(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert a list of Greeum memory blocks to standardized format."""
        return [self.convert_memory_to_dict(memory) for memory in memories] 