from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from app.mcq_generation import MCQGenerator
from typing import List, Optional
import json
import random

app = FastAPI()

class ErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    message: str
    details: Optional[List[ErrorDetail]] = None

class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None

class UserCreate(BaseModel):
    challenge: str
    input: str

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "details": None}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = [{"log":e["loc"], "msg":e["msg"], "type":e["type"]} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": error_details}
    )

@app.post("/nlp3/", response_model=SuccessResponse)
async def create_user(user_data: UserCreate):
    challenge = user_data.challenge
    input = user_data.input

    if challenge != "nlp3":
        return JSONResponse(
            status_code=422,
            content={"message": "I'm not doing that challenge, sorry!", "details": None}
        )
    
    if len(input.split())< 500 or len(input.split()) > 1500:
        return JSONResponse(
            status_code=422,
            content={"message": "Input length is not suitable", "details": None}
        )
    
    MCQ_Generator = MCQGenerator(True)
    questions = MCQ_Generator.generate_mcq_questions(input, 12)[0:12] # Set number of questions to 12, can change this

    for question in questions:
            question.distractors.append(question.answerText)
            random.shuffle(question.distractors)

    return JSONResponse(
        status_code=200,
        content = {
            "msg": "we got data succesfully",
            "details": '\n\n'.join(str(q) for q in questions)
        }
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




