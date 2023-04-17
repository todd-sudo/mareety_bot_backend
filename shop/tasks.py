from config import celery_app
from parser.parser import ParserMareety


@celery_app.task(
    bind=True,
    name=f"shop.parser_mareety_task",
    default_retry_delay=60 * 60 * 30,
    max_retries=5,
    soft_time_limit=60 * 60 * 35,
    time_limit=60 * 60 * 35,
)
def parser_mareety_task(self):
    ParserMareety().runner()
