from app.db.database import async_session_maker
from app.models.users import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, delete, select


async def find_one_or_none(**filter_by):
    async with async_session_maker() as session:
        query = select(User).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def create_user(**user_data):
    async with async_session_maker() as session:
        async with session.begin():
            new_user = User(**user_data)
            session.add(new_user)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_user


async def update_user(user_id, **values):
    async with async_session_maker() as session:
        async with session.begin():
            query = (
                update(User)
                .where(User.user_id == user_id)
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount


async def delete_user(user_id):
    async with async_session_maker() as session:
        async with session.begin():
            query = delete(User).filter_by(User.user_id == user_id)
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
