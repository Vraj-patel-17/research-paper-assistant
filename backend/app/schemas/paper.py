from pydantic import BaseModel
class PaperResponse(BaseModel):
    id:int
    title:str
    authors:str
    abstract:str
    pdf_url:str
