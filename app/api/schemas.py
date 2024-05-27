from datetime import datetime
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    Модель Pydantic для ответа api на запрос получения задачи.
    """
    id: int
    title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime


class ResponseListModel(ResponseModel):
    """
    Модель Pydantic для ответа api на запрос получения списка задач.
    """
    data: list[ResponseModel]


class CreateTask(BaseModel):
    """
    Модель Pydantic для создания задачи.
    """
    title: str | None = None
    description: str | None = None


class UpdateTask(BaseModel):
    """
    Модель Pydantic для обновления задачи.
    """
    title: str | None = None
    description: str | None = None
    updated_at: datetime = datetime.utcnow()


class DeleteTask(BaseModel):
    """
    Модель Pydantic для удаления задачи.
    """
    status: bool


class ErrorResponse(BaseModel):
    """
    Модель Pydantic для ответа api на запрос ошибки.
    """
    error: str
