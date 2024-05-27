from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import create_engine

from app.db.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

"""
Создаем интерфейс для взаимодействия с базой данных MySQL
"""
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
#engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_TEST_NAME}")
"""
Создаем фабрику сессий для создания новых сессий базы данных.
"""
session_maker = sessionmaker(engine, class_=Session, expire_on_commit=False)

"""
Создаем базовый класс для всех наших моделей данных.
"""
Base: DeclarativeMeta = declarative_base()

"""
Создаем объект метаданных, который будет хранить информацию о наших моделях данных.
Метаданные используются для создания таблиц в базе данных.
"""
metadata = MetaData()


def get_session():
	"""
	Вспомогательная функция для получения сессии базы данных.
	Это гарантирует, что мы используем одну и ту же сессию для всех запросов в одном блоке кода.
	"""
	with session_maker() as session:
		return session
