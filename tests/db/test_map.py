import pytest
from sqlalchemy import select

from models import Map


@pytest.mark.asyncio
async def test_tiles(session):
    session.add(Map(x=5, y=10, tile_name="water"))
    await session.commit()

    result = await session.execute(select(Map))
    res = result.scalars().all()
    assert len(res) == 1

    result = await Map.mapTile_by_cors(session=session,x=5,y=10)
    assert result.tile.name == "water"
    