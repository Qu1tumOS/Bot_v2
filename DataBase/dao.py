from DataBase.connect import async_session_maker, Stats, User, User_access, Lesson
from sqlalchemy import insert, select, update
from sqlalchemy.engine.result import MappingResult

class BaseDAO:
    model = None
    
    @classmethod
    async def __get_query_result(cls, **filter_by) -> MappingResult:
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings()
            
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        result: MappingResult = await cls.__get_query_result(**filter_by)
        return result.one_or_none()
    
    
    @classmethod
    async def find_all(cls, **filter_by):
        result: MappingResult = await cls.__get_query_result(**filter_by)
        return result.all()
    
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def update_user(cls, id, **data):
        async with async_session_maker() as session:
            query = update(cls.model).values(**data).filter_by(id=id)
            await session.execute(query)
            await session.commit()
    
    @classmethod
    async def user_info(cls, id):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(id=id)
                user = await session.execute(query)
                return user.scalar_one()
            
            except Exception:
                return None
                
            
class Stats(BaseDAO):
    model = Stats
class User(BaseDAO):
    model = User
class User_access(BaseDAO):
    model = User_access
class Lesson(BaseDAO):
    model = Lesson

# async def log():
#     async with async_session_maker() as session:
#         query = await session.execute(select(User).filter_by(id=2))
#         user = query.scalar_one()
#         print(user.id)

#         await session.execute(update(User).values(collage='aga').filter_by(id=2))
#         await session.commit()