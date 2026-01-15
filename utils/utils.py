# from pydantic import BaseModel, EmailStr

# class Submission(BaseModel):
#     id: int
#     lw_num: int
#     lot_num: str
#     num_lens: int 
#     location: str 
#     comments: str | None
#     submitter_id: int
#     submitter_fname: str
#     submitter_lname:str
#     submitter_email: EmailStr

# def create_submission_from_json(data):
#     return Submission(**data)
