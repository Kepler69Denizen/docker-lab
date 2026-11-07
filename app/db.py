from os import getenv
from sqlalchemy import (
    BigInteger,
    Numeric,
    Column,
    Identity,
    MetaData,
    SmallInteger,
    Table,
)
from sqlalchemy.ext.asyncio import create_async_engine

metadata = MetaData()

iris_predicts = Table(
    "iris_predicts",
    metadata,
    Column("id", BigInteger, Identity(), primary_key=True),
    Column("sepal_length", Numeric, nullable=False),
    Column("sepal_width", Numeric, nullable=False),
    Column("petal_length", Numeric, nullable=False),
    Column("petal_width", Numeric, nullable=False),
    Column("predict", SmallInteger, nullable=False),
)

db_url = getenv("DATABASE_URL")

engine = create_async_engine(
    db_url,
    echo=True,
    pool_size=2,
    max_overflow=3,
)


async def add_predict(*, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float, predict: int) -> None:
    async with engine.connect() as connect:
        await connect.execute(
            iris_predicts.insert().values(
                sepal_length=sepal_length,
                sepal_width=sepal_width,
                petal_length=petal_length,
                petal_width=petal_width,
                predict=predict
            )
        )
        await connect.commit()


async def create_tables() -> None:
    async with engine.begin() as connect:
        await connect.run_sync(metadata.create_all)


async def close_database() -> None:
    await engine.dispose()
