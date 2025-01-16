import pytest
from sqlalchemy import text

from db import get_session

@pytest.mark.asyncio
async def test_database_connection():
    session = await get_session()
    try:
        result = await session.execute(text("SELECT 1"))
        one = result.scalar_one()
        assert one == 1
        print(f"Database connection successful. Received value: {one}")
    except Exception as e:
        pytest.fail(f"Ошибочка: {e}")
    finally:
        await session.close()