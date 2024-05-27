import datetime

from sqlalchemy import Table, Column, String, TIMESTAMP
from sqlalchemy import Integer

from app.db.database import metadata


# Определение таблицы `tasks` в базе данных
tasks = Table(
  'tasks',  # Имя таблицы
  metadata,  # Коллекция метаданных, к которой принадлежит таблица

  Column('id', Integer, primary_key=True),
  Column('title', String(30), nullable=True, unique=True),
  Column('description', String(500), nullable=True),
  Column('created_at', TIMESTAMP, nullable=False, default=datetime.datetime.now()),
  Column('updated_at', TIMESTAMP, nullable=False, default=datetime.datetime.now())
)
