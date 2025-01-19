import pytest

from models import User, Hero

@pytest.mark.asyncio
class TestHero:

    async def test_add_hero(self, session):
        tg_id = 56
        avatar_id = 'fakebase64string'
        user = await User.add_user(session, tg_id)
        await session.commit()
        await session.refresh(user)
        
        hero = await Hero.add_hero(session, user.pk, avatar_id, 'aboba')
        await session.refresh(user)
        heroes = await user.awaitable_attrs.heroes
        assert len(heroes) == 1
        assert heroes[0].nickname == 'aboba'
        assert hero.energy == 100