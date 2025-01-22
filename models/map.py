from sqlalchemy import select, func, asc
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, Null, String
from sqlalchemy import Index

from sqlalchemy.orm import relationship

from random import randint

from models import Base, tiles

class Map(Base):
    __tablename__ = "map_table"
    __table_args__ = (
        Index('_x_y_idx', 'x', 'y', unique=True),
    )

    pk = Column(Integer, primary_key=True)
    
    x = Column(Integer)
    y = Column(Integer)
    
    tile_name = Column(String, nullable=False)

    #герой который занял клетку
    hero_id = Column(BigInteger, ForeignKey('hero_table.pk'), nullable=True)
    hero = relationship('Hero', backref='map_tile', lazy='select')

    @property
    def tile(self):
        return tiles[self.tile_name]

    def __repr__(self) -> str:
        return f"x:{self.x},y:{self.y}, тип {self.tile_name}"

    async def create_far(session,what):
        res = await session.execute(
                                select(Map)
                                .where(Map.hero_id.is_(None))
                                .order_by(asc(Map.x))
                                .limit(1)
                                )
        
        max_x_tile = res.scalar_one_or_none()
        if max_x_tile is None:
            new_x, new_y = 0,0
        else:
            new_x, new_y = max_x_tile.x, max_x_tile.y + randint(-50,50)

        new_map = Map(x=new_x,y=new_y,tile_name=what)
        session.add(new_map)
        await session.commit()
        await session.refresh(new_map)
        return new_map

    async def get_free_mapTile(session,what):

        need_new = await session.execute(select(func.count())
                                         .select_from(select(Map)
                                                      .where(Map.hero_id.is_(None))
                                                      .subquery()))
        if need_new.scalar() < 25:
            await Map.create_far(session,what)

        res = await session.execute(
                            select(Map)
                            .where(Map.hero_id.is_(None))
                            .where(Map.tile_name == what)
                            .order_by(func.random())
                            .limit(1)
                            )
        return res.scalar_one_or_none()

    async def mapTile_by_cors(session, x,y):
        from_db = await session.execute(select(Map).where(Map.x == x).where(Map.y == y))
        return from_db.scalar_one_or_none()
    
    async def mapTile_by_id(session, id):
        from_db = await session.execute(select(Map).where(Map.pk == id))
        return from_db.scalar_one_or_none()