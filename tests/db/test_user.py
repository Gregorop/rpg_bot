import pytest

from models import User


@pytest.mark.asyncio
class TestUser:

    async def test_add_user(self, session):
        tg_id = 123456
        user = await User.add_user(session, tg_id)
        await session.commit()
        result = await User.get_user_by_tg_id(session, tg_id)
        assert user.pk == result.pk