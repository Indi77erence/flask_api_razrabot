import datetime
import json
from typing import Union

from app.api.schemas import ResponseModel


def create_response_model(task):
    """Создает экземпляр класса ResponseModel из модели Task."""
    return ResponseModel(id=task.id, title=task.title, description=task.description,
                         created_at=task.created_at, updated_at=task.updated_at).json()


def convert_json_to_dict(json_data: Union[str, list[str]]) -> json:
    """
    Не обращать внимание, это из-за Pydantic пришлось, так как данные некрасиво выводились.
    Преобразует данные JSON в словарь с датами в формате GMT.
    """
    if isinstance(json_data, str):
        data = json.loads(json_data)
        for key, value in data.items():
            if key in ["created_at", "updated_at"]:
                data[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S GMT")
        return data
    else:
        data_list = []
        for json_str in json_data:
            data = json.loads(json_str)
            for key, value in data.items():
                if key in ["created_at", "updated_at"]:
                    data[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime(
                        "%a, %d %b %Y %H:%M:%S GMT")
            data_list.append(data)
        return data_list
