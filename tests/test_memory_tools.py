import tempfile
import pytest
from greeummcp.adapters.greeum_adapter import GreeumAdapter
from greeummcp.tools.memory_tools import MemoryTools

def get_memory_tools(tmp_path):
    adapter = GreeumAdapter(data_dir=str(tmp_path))
    mt = MemoryTools(
        adapter.block_manager,
        adapter.stm_manager,
        adapter.cache_manager,
        adapter.temporal_reasoner,
    )
    return mt

@pytest.mark.asyncio
async def test_add_and_query_memory(tmp_path):
    mt = get_memory_tools(tmp_path)

    memory_id = await mt.add_memory("파이썬은 재미있어", importance=0.9)

    results = await mt.query_memory("파이썬", limit=10)

    assert any(r["id"] == memory_id for r in results) 