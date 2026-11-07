import joblib
import os

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


# Путь внутри контейнера; каталог /data монтируется volume
MODEL_PATH = "/data/model.joblib"


def train_and_save():
    """Обучает модель и сохраняет её на диск."""
    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X, y)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    """Загружает модель с диска или обучает заново."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_and_save()
