from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Question(BaseModel):
    question_id: str
    text: str
    answer: Optional[str]

class Section(BaseModel):
    section_id: str
    title: str
    questions: List[Question]

class SamplePaper(BaseModel):
    paper_id: str
    title: str
    sections: List[Section]
    
    @validator('sections', pre=True, each_item=True)
    def validate_sections(cls, section):
        if not section.get('questions'):
            raise ValueError("Each section must have at least one question.")
        return section
    
class SamplePaperUpdate(BaseModel):
    title: Optional[str] = None
    sections: Optional[List[Section]] = None
