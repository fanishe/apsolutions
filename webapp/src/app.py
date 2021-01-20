import os
import sys
import json
import logging
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
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_result(search)
    return render_template('index.html', form=search)

@app.route('/results', methods = ['POST', 'GET'])
def search_result(search):
    form = SearchForm()
    search_string = form.search.data

    results = []
    results = DATABASE.search_text(search_string)

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('index.html', form=search, results=results)

@app.route('/api_search', methods = ['POST', 'GET'])
def api_search():
    """ Принимает данные через адресную строку
        Посылает json ответ
    """
    data = request.args.get('data')
    results = DATABASE.search_text(data)

    if results:
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
        return Response(json.dumps(main_json, ensure_ascii=False).encode('utf8'), mimetype='application/json')

    else:
        err_json = {"error" : "not_found"}
        return Response(json.dumps(err_json, ensure_ascii=False).encode('utf8'), mimetype='application/json')


@app.route('/del', methods = ['POST', 'GET'])
def delete_item():
    """ Get row id for deletion
        http://localhost:8888/del?id=38
    """
    data = request.args.get('id')
    result = DATABASE.delete_row(data)

    if reusult == 0:
        answer = 'deleted'
    else:
        anwer = 'deletion_error'

    return Response(json.dumps({"result": answer}, ensure_ascii=False).encode('utf8'), mimetype='application/json')


if __name__ == '__main__':
    config = Config()
    app.run(
        host=config.host,
        port=config.port
    )
