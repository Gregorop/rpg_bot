from sqlalchemy import Column, BigInteger, Integer, Boolean
from sqlalchemy import select

from models.base import Base

from db import connection

class User(Base):
    __tablename__ = "user_table"
    pk = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    banned = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"User(в базе:{self.pk}, tg_id:{self.tg_id} {self.banned * 'ЗАБАНЕН'}"

    @connection
    async def get_user_by_tg_id(session,id):
        result = await session.execute(select(User).where(User.tg_id==id))
        user = result.scalars().one_or_none()
        return user

    @connection
    async def add_user(session, tg_id):
        user = User(tg_id=tg_id)
        session.add(user)
        await session.commit()
        return user

    @connection
    async def delete_user_by_tg(session, tg_id):
        user = await User.get_user_by_tg_id(session, tg_id)
        
        if user:  
            await session.delete(user) 
            await session.commit() 
            return True  
            
        return False 