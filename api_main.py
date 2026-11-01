import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from celery.result import AsyncResult
import uvicorn
from tasks import celery_app
from fastapi.middleware.cors import CORSMiddleware

# Import Celery app and tasks
from tasks import run_scraping

app = FastAPI(
    title="Natural Scraping API",
    description="Agentic AI & Web Scraping API powered by FastAPI, Celery, Redis, Playwright and SeleniumBase",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    urls: List[str]
    scrape_type: str

@app.post("/scrape", summary="Start Background Scraping Task")
async def scrape_endpoint(request: ScrapeRequest):
    if not request.urls:
        raise HTTPException(status_code=400, detail="Kindly Provide At Least One URL")

    try:
        
        # Sending task to Celery + Redis Queue (Non-Blocking)
        task = run_scraping.delay(request.urls , request.scrape_type) #type: ignore
        
        return {
            "status": "Queued",
            "message": "Scraping task has started in the background.",
            "task_id": task.id,
            "status_check_url": f"/scrape/status/{task.id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while queueing the task: {str(e)}")


@app.get("/scrape/status/{task_id}", summary="Check Scraping Task Status & Get Results")
async def get_task_status(task_id: str):
    """
    Through this endpoint, the frontend/client can check real-time status.
    """
    if not task_id:
        raise HTTPException(status_code=400, detail="Kindly Provide Valid Task ID")

    task_result = AsyncResult(task_id, app=celery_app) # Continuously fetches updates from Celery on project processing progress
    
    response = {
        "task_id": task_id,
        "status": task_result.status
    }

    if task_result.status == "PENDING":
        response["message"] = "Task is waiting in the queue..."
    elif task_result.status == "STARTED":
        response["message"] = "Scraper is active and scraping links..."
    elif task_result.status == "SUCCESS":
        response["message"] = "Scraping completed successfully!"
        response["data"] = task_result.result
    elif task_result.status == "FAILURE":
        response["message"] = "An error occurred during task execution."
        response["error"] = str(task_result.result)
    
    return response


@app.get("/scrape/downloads/{session_id}/{file_format}", summary="Download Pro Excel/CSV Data")
async def download_endpoint(session_id: str, file_format: str):
    if not session_id:
        raise HTTPException(status_code=400, detail="Kindly Provide Session ID")

    base_dir = f"user_downloads/{session_id}"
    
    if not os.path.exists(base_dir):
        raise HTTPException(status_code=404, detail="Session folder not found or has expired.")
        
    ext = ".csv" if file_format.lower() == "csv" else ".xlsx"
    
    for file_name in os.listdir(base_dir):
        if file_name.endswith(ext):
            file_path = os.path.join(base_dir, file_name)
            return FileResponse(
                path=file_path,
                filename=file_name,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if ext == '.xlsx' else 'text/csv'
            )

    raise HTTPException(status_code=404, detail=f"{file_format.upper()} file does not exist in this session.")

if __name__ == "__main__":
    uvicorn.run("api_main:app", host="127.0.0.1", port=8800, reload=False)

