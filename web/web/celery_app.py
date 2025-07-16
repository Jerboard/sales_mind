from celery import Celery
from .settings import REDIS_HOST, REDIS_PORT

# Имя «web_client» может быть любым — важно только одно: брокер указывает
# куда шлём задачи. Worker уже запущен и слушает этот же брокер.
celery_app = Celery(
    'web_client',
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)

