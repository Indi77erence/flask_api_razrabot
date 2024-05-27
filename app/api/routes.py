from typing import Union
from flask_pydantic import validate
from flask_restful import Resource
from sqlalchemy import select, insert, update, delete

from app.api.schemas import CreateTask, UpdateTask, DeleteTask, ResponseModel, ErrorResponse
from app.api.services import convert_json_to_dict, create_response_model
from app.db.database import session_maker
from app.db.models import tasks


class Task(Resource):
    def get(self, task_id: int = None) -> Union[ResponseModel, list[ResponseModel]]:
        """

        Метод, который выполняет поиск всех задач если или конкретной.

        Принимает 1 аргумент:
        - task_id - id задачи, которую необходимо получить.
        Возвращает или список объектов класса task или один конкретный.

        """
        with session_maker() as session:
            if task_id:
                stmt = select(tasks).where(tasks.c.id == task_id)
                data = session.execute(stmt).first()
                if data is None:
                    return ErrorResponse(error=f"Задачи с id {task_id} не существует").dict()
                task = create_response_model(data)
                return convert_json_to_dict(task)
            stmt = select(tasks)
            data = session.execute(stmt)
            all_tasks = [create_response_model(task) for task in data]
            return convert_json_to_dict(all_tasks)

    @validate(CreateTask)
    def post(self, body: CreateTask) -> ResponseModel:
        """

        Метод, который создаёт новую задачу.

        Принимает 1 аргумент:
        - body - модель Pydantic по которой будет создана задача.
        Возвращает объект класса task.

        """
        with session_maker() as session:
            stmt = insert(tasks).values(dict(body.model_dump(exclude_none=True)))
            session.execute(stmt)
            session.commit()
            # Не знаю почему, но функция returning постоянно ругалась на синтаксис, хотя делал по документации.
            # Поэтому вот:
            insert_task = session.execute(select(tasks).where(tasks.c.title == body.title)).first()
            task = create_response_model(insert_task)
            return convert_json_to_dict(task), 201

    @validate(UpdateTask)
    def put(self, task_id: int, body: UpdateTask) -> ResponseModel:
        """

        Метод, который обновляет задачу.

        Принимает 2 аргумента:
        - task_id - id задачи, которую необходимо обновить.
        - body - модель Pydantic по которой будет обновлена задача.
        Возвращает объект класса task.

        """
        with session_maker() as session:
            stmt = update(tasks).where(tasks.c.id == task_id).values(dict(body.model_dump(exclude_none=True)))
            session.execute(stmt)
            session.commit()
            # Не знаю почему, но функция returning постоянно ругалась на синтаксис, хотя делал по документации.
            # Поэтому вот:
            update_task = session.execute(select(tasks).where(tasks.c.id == task_id)).first()
            task = create_response_model(update_task)
            return convert_json_to_dict(task)

    def delete(self, task_id: int) -> DeleteTask:
        """

        Метод, который удаляет задачу.

        Принимает 1 аргумента:
        - task_id - id задачи, которую необходимо удалить.

        Возвращает статус удаления задачи.

        """
        with session_maker() as session:
            data = session.execute(select(tasks).where(tasks.c.id == task_id)).first()
            if data is None:
                return ErrorResponse(error=f"Задачи с id {task_id} не существует").dict()
            stmt = delete(tasks).where(tasks.c.id == task_id)
            session.execute(stmt)
            session.commit()
            return {"access": True}
