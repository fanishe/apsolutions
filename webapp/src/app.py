import os
import sys
from flask import Flask
from configurator import Config

TABLE = os.getenv('TABLE')
DATABASE = os.getenv('DATABASE')
DB_PASSWORD = os.getenv('ROOT_PASSWORD')

if not TABLE or not DATABASE or not DB_PASSWORD:
    print("ERROR: Check Environments TABLE, DATABASE and DB_PASSWORD")
    sys.exit(1)
else:
    print(f"Database environment loaded {TABLE=}, {DATABASE=}, {DB_PASSWORD=}")


app = Flask(__name__)
config = Config()

@app.route('/', methods = ['POST', 'GET'])
def search():
    database = Database(
        "config.ini",
        "mysql",
        config.get_param("tables", "main_table")
    )
    return '<h1> HELLO MAZAFAKA </h1>'


if __name__ == '__main__':
    app.run(
        host=config.host,
        port=config.port
    )
