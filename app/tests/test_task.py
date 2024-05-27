from http import HTTPStatus

from app.tests.data_for_test import data_for_create_task, field_task, data_for_update_task


def test_get_empty_list_tasks(client, db_session):
	"""
    Тест для получения пустого списка задач.

    Выполняет GET-запрос к API-маршруту `/api/tasks` и проверяет, что список задач пуст.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
    """
	response = client.get("/api/tasks")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json == [], "Список задач не пустой"


def test_create_task(client, db_session):
	"""
    Тест для создания задачи.

    Выполняет POST-запрос к API-маршруту `/api/tasks` с данными задачи и проверяет, что ответ содержит созданную задачу.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
    """
	response = client.post("/api/tasks", json=data_for_create_task)
	answer = response.json
	assert answer['title'] == data_for_create_task['title']
	assert answer['description'] == data_for_create_task['description']
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."


def test_get_list_menu(client, db_session):
	"""
    Тест для получения списка задач после создания задачи.

    Выполняет GET-запрос к API-маршруту `/api/tasks` и проверяет, что список задач не пуст и содержит все необходимые поля.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
    """
	response = client.get("/api/tasks")
	answer_response = response.json
	assert response.json != [], "Список задач пустой"
	for task in answer_response:
		for field in field_task:
			assert field in task, f"В задаче нет поля {field}."
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."


def test_get_task_by_id(client, db_session, task_id):
	"""
    Тест для получения задачи по идентификатору.

    Выполняет GET-запрос к API-маршруту `/api/tasks/{task_id}` и проверяет, что ответ содержит задачу с заданным идентификатором.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
      task_id (int): идентификатор задачи.
    """
	response = client.get(f"/api/tasks/{task_id}")
	answer_response = response.json
	assert answer_response['id'] == task_id
	assert answer_response['title'] == data_for_create_task['title']
	assert answer_response['description'] == data_for_create_task['description']
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."


def test_update_task(client, db_session, task_id):
	"""
    Тест для обновления задачи.

    Выполняет PUT-запрос к API-маршруту `/api/tasks/{task_id}` с обновленными данными задачи и проверяет, что ответ содержит обновленную задачу.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
      task_id (int): идентификатор задачи.
    """
	response = client.put(f"/api/tasks/{task_id}", json=data_for_update_task)
	answer = response.json
	if "title" in data_for_update_task:
		assert answer['title'] == data_for_update_task['title']
	if "description" in data_for_update_task:
		assert answer['description'] == data_for_update_task['description']
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."


def test_get_task_by_id_after_update(client, db_session, task_id):
	"""
    Тест для получения задачи по идентификатору после обновления.

    Выполняет GET-запрос к API-маршруту `/api/tasks/{task_id}` и проверяет, что ответ содержит обновленную задачу.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
      task_id (int): идентификатор задачи.
    """
	response = client.get(f"/api/tasks/{task_id}")
	answer_response = response.json
	print(answer_response)
	assert answer_response['id'] == task_id
	assert answer_response['title'] == data_for_update_task['title']
	assert answer_response['description'] == data_for_update_task['description']
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."


def test_delete_task(client, db_session, task_id: int):
	"""
    Тест для удаления задачи и получения задачи по id после ее удаления.

    Выполняет DELETE-запрос к API-маршруту `/api/tasks/{task_id}` и проверяет, что ответ содержит подтверждение удаления и что задача удалена из базы данных.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
      task_id (int): идентификатор задачи.
    """
	response = client.delete(f"/api/tasks/{task_id}")
	answer_response = response.json
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response['access'] == True, "Ошибка удаления задачи."
	response = client.get(f"/api/tasks/{task_id}")
	answer_response = response.json
	assert answer_response["error"] == f"Задачи с id {task_id} не существует", "Статус ответа не 200."


def test_get_empty_list_tasks_after_delete(client, db_session):
	"""Тест для получения пустого списка задач после удаления.

    Выполняет GET-запрос к API-маршруту `/api/tasks` и проверяет, что список задач пуст.

    Args:
      client (flask.testing.FlaskClient): тестовый клиент.
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.
    """
	response = client.get("/api/tasks")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json == [], "Список задач не пустой"
