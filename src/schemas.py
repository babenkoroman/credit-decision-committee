from pydantic import BaseModel

class ApplicationDTO(BaseModel): 
    first_name: str | None 
    second_name: str | None 
    applicant_id: int | None 
    credit_sum: float | None 