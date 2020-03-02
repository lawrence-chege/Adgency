"""
This module runs the app and tests
"""
import os
from app import create_app
from migrations import DbModel
from werkzeug.exceptions import NotFound
config = os.getenv('FLASK_CONFIG')


APP = create_app("default")
with APP.app_context():
        db = DbModel(APP)
        # db.init_db(APP)
        db.create_tables()

if __name__ == "__main__":
    APP.run(debug = True)