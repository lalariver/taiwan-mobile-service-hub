from . import models  # noqa: F401
from .database import DATABASE_PATH, Base, engine


def initialize_database() -> None:
    """建立尚不存在的資料表。"""

    Base.metadata.create_all(bind=engine)

    print("Database initialization completed.")
    print(f"Database path: {DATABASE_PATH}")
    print(
        "Registered tables: "
        f"{', '.join(Base.metadata.tables.keys())}"
    )


if __name__ == "__main__":
    initialize_database()