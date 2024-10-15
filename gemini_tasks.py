from celery import Celery
import time
from open_ai import extract_data_from_pdf, extract_data_from_text
# import gemini  # Ensure this is the correct import

# Initialize Celery app
celery_app = Celery('gemini_tasks', 
                     broker='redis://localhost:6379/0', 
                     backend='redis://localhost:6379/0')

celery_app.conf.task_routes = {
    'gemini_tasks.extract_text_task': {'queue': 'text_extraction_queue'},
    'gemini_tasks.extract_pdf_task': {'queue': 'pdf_extraction_queue'}
}

# You can also add additional configuration settings
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task
def extract_pdf_task(pdf_file_path: str):
    """
    Task to extract data from PDF using Gemini
    """
    # Call the function to extract PDF data
    extracted_data = gemini_extract_from_pdf(pdf_file_path)
    
    if extracted_data is None:
        raise Exception("PDF extraction failed")
    
    # Return the extracted data as needed
    return extracted_data

def gemini_extract_from_pdf(pdf_file_path: str):
    """
    Integrates with OpenAi API to extract data from the given PDF.
    """
    try:
        
        extracted_data = extract_data_from_pdf(pdf_file_path)
        print(extracted_data)  # Ensure this function exists
        
        return extracted_data
    except Exception as e:
        # Handle any exceptions or errors
        print(f"Error during PDF extraction: {str(e)}")
        return None
@celery_app.task
def extract_text_task(text : str):
    """
    Integrates with OpenAi API to extract data from the given PDF.
    """
    try:
        
        extracted_data = extract_data_from_text(text)
        # print(extracted_data)  # Ensure this function exists
        
        return extracted_data
    except Exception as e:
        # Handle any exceptions or errors
        print(f"Error during PDF extraction: {str(e)}")
        return None
