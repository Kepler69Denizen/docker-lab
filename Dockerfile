ARG PYTHON_IMAGE=python:3.11.18-slim


# ===== Стадия 1: сборка зависимостей =====
FROM ${PYTHON_IMAGE} AS builder

WORKDIR /build

# Копирование бинарных файлов uv для более быстрого и удобного взаимодействия
# со средой Python.
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

# Системные пакеты, нужные только на этапе компиляции (в финальный образ не попадут)
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
gcc \
&& rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .

# UV_PROJECT_ENVIRONMENT - указать uv в какой директории создать виртуальное окружение.
# UV_COMPILE_BYTECODE - включить предварительную компиляцию Python кода в байткод .pyc
# при установке зависимостей.
# Сейчас включено (1). __pycache__ создается сразу для всех зависимостей во время сборки,
# чтобы не компилировать его во время первого запуска приложения.
# UV_PYTHON_DOWNLOADS - включить установку интерпретатора Python из интернета.
# Выключено (0), потому что интерпретатор уже загружен вместе с образом и его не нужно
# дополнительно устанавливать.
ENV UV_PROJECT_ENVIRONMENT=/opt/.venv \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0

# Установка зависимостей.
# --locked - проверяет соответствие pyproject.toml и uv.lock,
# не позволяя uv автоматически изменить lock-файл.
# --no-install-project - не устанавливает сам проект как Python-пакет.
# --no-group (имя группы) - не устанавливать определенную группу зависимостей.
# (dependency-groups в pyproject.toml)
# --no-cache - отключает использование постоянного кэша uv.
RUN uv sync --locked --no-install-project --no-group dev --no-group test --no-cache


# ===== Стадия 2: исполняемый образ =====
FROM ${PYTHON_IMAGE} AS runtime

WORKDIR /app

# Копируем только venv из стадии builder (без компиляторов)
COPY --from=builder /opt/.venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"

# Копирование исходного кода приложения
COPY app/ .

# Непривилегированный пользователь (рекомендация по безопасности)
RUN useradd -m -u 1000 appuser && \
mkdir -p /data && \
chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8000

# Запуск ASGI-сервера uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

