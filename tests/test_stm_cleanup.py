import pytest
from greeummcp.adapters.greeum_adapter import GreeumAdapter

@pytest.mark.asyncio
async def test_stm_cleanup(tmp_path):
    adapter = GreeumAdapter(data_dir=str(tmp_path), greeum_config={"ttl_short": 1})
    stm = adapter.stm_manager

    # add memory with short ttl
    mem_id = stm.add_memory("단기 기억", ttl_type="short")
    assert mem_id is not None

    # force expire by calling cleanup after >1s
    import time
    time.sleep(1.1)

    cleaned = stm.cleanup_expired()
    assert cleaned >= 1 