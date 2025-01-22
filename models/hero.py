from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer
from sqlalchemy.orm import relationship

from models import Base, User, Map

class Hero(Base):
    __tablename__ = "hero_table"
    pk = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey(User.pk), nullable=False)
    owner = relationship('User', back_populates="heroes", lazy='joined')

    avatar_file_in_tg_id = Column(String(256), nullable=False) #id фотки из телеги
    nickname = Column(String(25), nullable=False)

    energy = Column(Integer, default=100)

    
    def __repr__(self) -> str:
        return f"{self.nickname}, энергии {self.energy}"

    async def first_spawn_hero(session, owner_id, avatar_id, nick):
        hero = Hero(owner_id=owner_id, avatar_file_in_tg_id=avatar_id, nickname=nick)
        session.add(hero)
        await session.commit()
        await session.refresh(hero)

        map_tile = await Map.get_free_mapTile(session,'grass')
        map_tile.hero_id = hero.pk
        session.add(map_tile)
        await session.commit()

        return hero