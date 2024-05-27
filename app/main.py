from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from app.api.routes import Task


def create_app():
	"""
	Функция для создания экземпляра приложения Flask.

	Конфигурирует расширение Flask-SQLAlchemy и расширение Flask-RESTful,
	создает экземпляр приложения и регистрирует ресурс для API.

	Returns:
	  Flask: экземпляр приложения.
	"""
	app = Flask(__name__)
	api = Api(app)
	api.add_resource(Task, '/api/tasks', '/api/tasks/<int:task_id>')
	SWAGGER_URL = '/api/docs'
	API_URL = '/static/swagger.yaml'
	swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Test application"},)
	app.register_blueprint(swaggerui_blueprint)
	return app


# Проверка, запускается ли скрипт как главный
if __name__ == '__main__':
	my_app = create_app()
	my_app.run(debug=True, port=3000, host='localhost')

