from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing_extensions import AsyncGenerator

from model import load_model
from db import close_database, create_tables, add_predict


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_tables()
    yield
    await close_database()


app = FastAPI(
    title="IIS Iris Classifier",
    version="1.0.0",
    lifespan=lifespan
)

model = load_model()


class IrisFeatures(BaseModel):
    """Входные признаки цветка ириса"""
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class IrisFeaturesReturn(IrisFeatures):
    """Возвращаемые данные о цветке ириса"""
    predict: int


@app.get("/", status_code=200)
async def root():
    """Проверка доступности сервиса."""
    return {
        "status": "ok",
        "service": "IIS Iris Classifier"
    }


@app.post("/predict", response_model=IrisFeaturesReturn, status_code=201)
async def predict(features: IrisFeatures):
    """Возвращает предсказанный класс ириса (0, 1 или 2)"""

    data = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]]
    predict_ = int(model.predict(data)[0])

    await add_predict(
        sepal_width=features.sepal_width,
        sepal_length=features.sepal_length,
        petal_width=features.petal_width,
        petal_length=features.petal_length,
        predict=predict_
    )

    return {
        "sepal_length": features.sepal_length,
        "sepal_width": features.sepal_width,
        "petal_length": features.petal_length,
        "petal_width": features.petal_width,
        "predict": predict_
    }

