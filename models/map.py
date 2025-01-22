from requests import get
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, String
from sqlalchemy import Index

from sqlalchemy.orm import relationship
from sqlalchemy import select

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
    hero = relationship('Hero', backref='map_tile', lazy='joined')

    @property
    def tile(self):
        return tiles[self.tile_name]

    def __repr__(self) -> str:
        return f"x:{self.x},y:{self.y}, тип {self.tile_name}"

    async def mapTile_by_cors(session, x,y):
        from_db = await session.execute(select(Map).where(Map.x == x).where(Map.y == y))
        return from_db.scalar_one_or_none()
    
    async def mapTile_by_id(session, id):
        from_db = await session.execute(select(Map).where(Map.pk == id))
        return from_db.scalar_one_or_none()