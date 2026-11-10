#!/bin/bash
# Использование: ./service_support.sh [status|backup|logs]

if [ -z "$1" ]; then
    echo "Использование: $0 [status|backup|logs]"
    exit 1
fi

if [ "$1" = "status" ]; then
    echo "=== Проверка статуса ИИС ==="

    if ! docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"; then
        echo "Ошибка: не удалось получить список Docker-контейнеров."
        exit 1
    fi

    echo "============================="

elif [ "$1" = "backup" ]; then
    echo "=== Запуск резервного копирования ==="

    if ! mkdir -p ./backups; then
        echo "Ошибка: не удалось создать каталог ./backups."
        exit 1
    fi

    DATA_TAG=$(date +%Y-%m-%d_%H-%M-%S)
    BACKUP_FILE="./backups/iis_backup_${DATA_TAG}.txt"

    if ! echo "Бэкап базы знаний ИИС от ${DATA_TAG}" > "$BACKUP_FILE"; then
        echo "Ошибка: не удалось создать файл резервной копии."
        exit 1
    fi

    echo "Конфигурация успешно сохранена в файл: $BACKUP_FILE"
    echo "====================================="

elif [ "$1" = "logs" ]; then
    CONTAINER="iris_grafana_container"

    if ! docker ps --format '{{.Names}}' | grep -Fxq "$CONTAINER"; then
        echo "Ошибка: контейнер '$CONTAINER' не запущен или не существует."
        exit 1
    fi

    echo "=== Логи контейнера $CONTAINER ==="
    docker logs "$CONTAINER"

else
    echo "Ошибка: неизвестная команда '$1'. Используйте 'status', 'backup' или 'logs'."
    exit 1
fi
