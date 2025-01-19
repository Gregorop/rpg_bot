from sqlalchemy import Column, BigInteger, Integer, Boolean
from sqlalchemy import select
from sqlalchemy.orm import relationship, joinedload

from models import Base

class User(Base):
    __tablename__ = "user_table"
    pk = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    banned = Column(Boolean, default=False, nullable=False)
    
    heroes = relationship('Hero', back_populates="owner")

    def __repr__(self):
        return f"User(в базе:{self.pk}, tg_id:{self.tg_id} {self.banned * 'ЗАБАНЕН'}"

    async def get_user_by_tg_id(session,id):
        result = await session.execute(
                    select(User)
                    .options(joinedload(User.heroes))
                    .where(User.tg_id==id)
                    )
        user = result.unique().one()[0]
        return user

    async def add_user(session, tg_id):
        user = User(tg_id=tg_id)
        session.add(user)
        return user

    async def delete_user_by_tg(session, tg_id):
        user = await User.get_user_by_tg_id(session, tg_id)
        
        if user:  
            session.delete(user) 
            await session.flush()
            return True  
            
        return False 