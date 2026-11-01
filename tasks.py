import logging
from scraping_main import main as scraper_main
from celery import Celery
from pydantic_v2_main import settings

# Celery App Initialization
celery_app = Celery(
    "scraping_service",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["tasks"]
)

# Production Configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,         # Results 1 ghante tak Redis me store rahenge
    task_track_started=True,     # Task Execution Status track karne ke liye
    worker_prefetch_multiplier=2 # Web Scraping memory efficiency ke liye
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@celery_app.task(name="tasks.run_scraping", bind=True)
def run_scraping(self, urls: list[str] , scrape_for):
    """
    Celery Task: Redis Queue se URLs receive karta hai aur
    Background me Playwright/SeleniumBase Scraping Engine ko execute karta hai.
    """
    task_id = self.request.id
    logging.info(f"🚀 [Celery Worker] Task {task_id} started for {len(urls)} URLs.")
    
    try:
        # Synchronous Scraper execution inside Celery Worker process
        results = scraper_main(urls , scrape_for)
        logging.info(f"✅ [Celery Worker] Task {task_id} completed successfully.")
        return results
    except Exception as e:
        logging.error(f"❌ [Celery Worker] Task {task_id} failed with error: {e}")
        return {
            "status": "Fail", 
            "message": f"Scraping task execution failed: {str(e)}"
        }

