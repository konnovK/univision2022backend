from pydantic import BaseModel


class CreateFacultyRequest(BaseModel):
    password: str
    faculty: list[str]


class OneFinalAudienceResult(BaseModel):
        faculty: int
        points: int
        added: int


class CreateFinalAudienceResult(BaseModel):
    password: str
    data: list[OneFinalAudienceResult]


class CheckPasswordError(BaseModel):
    message: str