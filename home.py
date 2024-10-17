from fastapi import FastAPI, UploadFile, File, HTTPException
from redis import Redis
from pymongo import MongoClient
from models import SamplePaper, Question, Section, SamplePaperUpdate
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from celery.result import AsyncResult
from gemini_tasks import extract_pdf_task ,celery_app, extract_text_task
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
redis_client = Redis(host='localhost', port=6379)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['sample_papers_db']

# @app.get("/")
# async def home():
#     # redis_client.set('text', "abc")
#     return {'name':'Helloworlds'}

@app.post("/papers")
async def create_paper(paper: SamplePaper):
    paper_data = paper.dict()
    db.papers.insert_one(paper_data)
    return {"paper_id": paper.paper_id}

@app.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    cached_paper = redis_client.get(paper_id)
    if cached_paper:
        return json.loads(cached_paper)
    paper = db.papers.find_one({"paper_id": paper_id})

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # Convert ObjectId to string before returning the document
    paper['_id'] = str(paper['_id'])
    redis_client.set(paper_id, json.dumps(paper))
    return paper

@app.put("/papers/{paper_id}")
async def update_sample_paper(paper_id: str, update_data: SamplePaperUpdate):
    # Check if the sample paper exists
    existing_paper = db.papers.find_one({"paper_id": paper_id})
    if not existing_paper:
        raise HTTPException(status_code=404, detail="Sample paper not found")

    # Prepare the updated fields
    updated_fields = {}

    if update_data.title is not None:
        updated_fields['title'] = update_data.title
    if update_data.sections is not None:
        # Convert the Pydantic models to dictionaries
        updated_fields['sections'] = [section.dict() for section in update_data.sections]

    # Only perform the update if there are fields to update
    if updated_fields:
        db.papers.update_one({"paper_id": paper_id}, {"$set": updated_fields})

    # Invalidate cache if exists
    redis_client.delete(paper_id)

    # Convert ObjectId to string before returning the updated document
    existing_paper['_id'] = str(existing_paper['_id'])
    
    # Return the updated paper data from the database
    updated_paper = db.papers.find_one({"paper_id": paper_id})
    updated_paper['_id'] = str(updated_paper['_id'])
    
    return updated_paper


    


@app.post("/extract/pdf/")
async def extract_pdf(pdf: UploadFile = File(...)):
    # Save PDF temporarily
    pdf_file_path = f"tmp/{pdf.filename}"
    with open(pdf_file_path, "wb") as f:
        f.write(pdf.file.read())
    
    # Enqueue the Celery task
    # import pdb;pdb.set_trace()
    task = extract_pdf_task.apply_async(args=[pdf_file_path], queue='pdf_extraction_queue')
    # task = extract_pdf_task.delay(pdf_file_path)
    
    # Return the task ID to check later
    return {"task_id": task.id}

@app.post("/extract/text")
async def extract_from_text(text: str):
    # Use Gemini to extract text
    task = extract_text_task.apply_async(args=[text], queue='text_extraction_queue')
    
    # Return extracted data as SamplePaper format
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """
    Get the status of an ongoing task.
    """
    task_result = AsyncResult(task_id,app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "Pending"}
    elif task_result.state == 'SUCCESS':
        return {"status": "Success", "result": task_result.result}
    else:
        return {"status": task_result.state}
