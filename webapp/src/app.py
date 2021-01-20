import os
import sys
import json
import logging

logging.basicConfig(
    format="%(asctime)s : %(filename)s : %(threadName)s_%(thread)d(%(funcName)s)[LINE:%(lineno)d] : %(levelname)s : %(message)s",
    level=logging.DEBUG,
    filename='/var/log/webapp/flask.log',
    filemode='w')

from flask import Flask, flash, render_template, request, redirect, jsonify, Response
from forms import SearchForm

from configurator import Config
from database import Database

TABLE = os.getenv('TABLE')
DATABASE = os.getenv('DATABASE')
DB_PASSWORD = os.getenv('ROOT_PASSWORD')
DATABASE = Database("config.ini", "mysql", TABLE)

app = Flask(__name__)
app.secret_key = "flask rocks!"

@app.route('/', methods = ['POST', 'GET'])
def index():
    search = SearchForm()
    if request.method == 'POST':
        return search_result()
    return render_template('index.html', form=search)

def search_result():
    form = SearchForm()
    results = DATABASE.search_text(form.search.data)
    logging.info("WEB Search: data - %s", form.search.data)

    if not results:
        not_found = [('null', 'Not found', 'null', 'null')]
        logging.info("WEB Search: No data was found in DB")
        return render_template('index.html', form=form, results=not_found)
    else:
        logging.info("WEB Search: Found - %s datas in DB", len(results))
        return render_template('index.html', form=form, results=results)

@app.route('/api_search', methods = ['POST', 'GET'])
def api_search():
    """ Принимает данные через адресную строку
        Посылает json ответ
    """
    data = request.args.get('data')
    if data:
        logging.info("API Search: Data - %s", data)
        results = DATABASE.search_text(data)

        if results:
            logging.info("API Search: Found - %s datas in DB", len(results))
            main_json = []

            for res in results:
                datetime = res[2].strftime("%Y-%m-%d %H:%M:%S")
                temp = {
                    "id" : res[0],
                    "text" : res[1],
                    "created_date" : datetime,
                    "rubrics" : res[3]
                }
                main_json.append(temp)
            return Response(
                json.dumps(main_json, ensure_ascii=False).encode('utf8'),
                mimetype='application/json'
            )

        else:
            logging.info("API Search: Not Found any data in DB")
            err_json = {"error" : "not_found"}
            return Response(
                json.dumps(err_json, ensure_ascii=False).encode('utf8'),
                mimetype='application/json'
            )

    else:
        logging.info("API Search: Data wasn't sent")
        err_json = {"error" : "give_me_data"}
        return Response(
            json.dumps(err_json, ensure_ascii=False).encode('utf8'),
            mimetype='application/json'
        )


@app.route('/del', methods = ['POST', 'GET'])
def delete_item():
    """ Get row id for deletion
        http://localhost:8888/del?id=38
    """
    data = request.args.get('id')

    if data:
        logging.info("API Deletion: id - %s", data)
        result = DATABASE.delete_row(data)
    else:
        logging.info("API Deletion: No ID was sent")
        result = 2

    if result == 0:
        logging.info("API Deletion: id - %s. Successfull deleted", data)
        answer = 'deleted'
    elif result == 2:
        answer = 'give_me_id'
    else:
        logging.info("API Deletion: ID - %s wasn't found in DB", data)
        answer = 'id_not_found'

    return Response(
        json.dumps({"result": answer}, ensure_ascii=False).encode('utf8'),
        mimetype='application/json'
        )


if __name__ == '__main__':
    config = Config()
    app.run(
        host=config.host,
        port=config.port
    )
