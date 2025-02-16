from pydantic.main import BaseModel


class ResponseErrorItem(BaseModel):
    code: str
    message: str


class Response500Error(BaseModel):
    class_name: str
    message: str
