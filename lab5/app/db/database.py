from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker, AsyncAttrs)
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.core.config import get_db_url


DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)  # ассинхроное подключение к бд
# фабрика ассинхроных сессий
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    # абстрактный класс от к-го будут наследоваться все модели
    __abstract__ = True

    # ипределет имя табл на основе имени класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
