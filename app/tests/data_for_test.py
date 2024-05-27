data_for_create_task = {
    "title": "test",
    "description": "test description",
}
data_for_update_task = {
    "title": "test_update",
    "description": "test description v2",
}

field_task = ("id",
              "title",
              "description",
              "created_at",
              "updated_at",)

db_url = 'mysql+pymysql://user:user@localhost/mydb'

test_db_url = 'mysql+pymysql://user:user@localhost/mydb_test'
