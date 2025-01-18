import pytest

from models import User


@pytest.mark.asyncio
class TestUser:

    async def test_add_user(self,session):
        tg_id = 123456
        result = await User.add_user(tg_id)
        assert result.pk == 1

    async def test_get_user(self,session):
        tg_id = 123456
        result = await User.get_user_by_tg_id(tg_id)
        assert result.pk == 1