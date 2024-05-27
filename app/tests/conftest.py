import sys

import pytest as pytest
from sqlalchemy import select
sys.path.append('../..')
from app.db.database import get_session
from app.db.models import tasks
from app.main import create_app


@pytest.fixture(scope="session")
def app():
    """
    Фикстура для создания экземпляра приложения.

    Создает экземпляр приложения с помощью функции `create_app`.

    Returns:
      Flask: экземпляр приложения.
    """
    app = create_app()
    return app


@pytest.fixture(scope="function")
def db_session(app):
    """
    Фикстура для создания сессии базы данных.

    Создает сессию базы данных с помощью функции `get_session`.
    Откатывает все изменения и закрывает сессию после выполнения теста.

    Args:
      app (Flask): экземпляр приложения.

    Yields:
      sqlalchemy.orm.session.Session: сессия базы данных.
    """
    with app.app_context():
        session = get_session()
        yield session
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(app):
    """Фикстура для создания тестового клиента.

    Создает тестового клиента для взаимодействия с приложением.

    Args:
      app (Flask): экземпляр приложения.

    Returns:
      flask.testing.FlaskClient: тестовый клиент.
    """
    return app.test_client()


@pytest.fixture(scope="function")
def task_id(db_session):
    """Фикстура для получения идентификатора задачи.

    Выполняет запрос к базе данных и возвращает идентификатор первой задачи.

    Args:
      db_session (sqlalchemy.orm.session.Session): сессия базы данных.

    Returns:
      int: идентификатор задачи.
    """
    stmt = select(tasks)
    data = db_session.execute(stmt).first()
    return data.id




