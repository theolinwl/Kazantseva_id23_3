from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


# mapped для сопоставления с питоновскими типами и структурой таблицы в бд
class User(Base):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(user_id={self.user_id}, "
                f"email={self.email}")
