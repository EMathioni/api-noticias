from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

client = MongoClient("localhost", 27017)
mdb = client.flask_noticias
app = Flask(__name__)

@app.route("/")
def index():
    search = request.args.get('pesquisa')
    doc = mdb.noticia
    counter = doc.find({"$text": {"$search": f"{search}"}}).count()
    all_results_list = []
    if counter == 0:
        return render_template('index.html', success='No', counter=counter, search=search)
    else:
        for x in doc.find({"$text": {"$search": f"{search}"}}):
            all_results = {
                '_id': x['_id'],
                'title': x['title'],
                'text': x['text'],
                'author': x['author']
            }
            all_results_list.append(all_results)

        return render_template('index.html', all_results=all_results_list, success=True, counter=counter)


@app.route("/create")
def create_notice():
    return render_template('create.html')


@app.route("/creating")
def creating():
    title = request.args.get("title")
    text = request.args.get("text")
    author = request.args.get("author")
    if title == "" or text == "" or author == "":
        return render_template('create.html', success=False)
    else:
        o = ObjectId()
        mdb.noticia.insert_one({
            '_id': str(o),
            'title': title,
            'text': text,
            'author': author,
            'timestamp': datetime.datetime.now()
        })
        return render_template('create.html', success=True)


@app.route("/<id>")
def news(id):
    try:
        page_data = []
        for x in mdb.noticia.find({"_id": f"{id}"}):
            result = {
                'title': x['title'],
                'text': x['text'],
                'author': x['author']
            }
            page_data.append(result)

        return render_template('id.html', results=page_data)
    except:
        return redirect('/')


@app.route("/api", methods=['GET'])
def api_news():
    api_data = []
    for x in mdb.noticia.find():
        api_data.append(x)
    return jsonify(api_data)


@app.route("/api/<id>")
def api_news_id(id):
    api_data = []
    for x in mdb.noticia.find({"_id": f'{id}'}):
        api_data.append(x)
    return jsonify(api_data)


@app.route("/delete")
def page_delete():
    search = request.args.get('pesquisa')
    doc = mdb.noticia
    counter = doc.find({"$text": {"$search": f"{search}"}}).count()
    all_results_list = []
    if counter == 0:
        return render_template('delete.html', confirm=False, search=search, counter=counter)
    else:
        for x in doc.find({"$text": {"$search": f"{search}"}}):
            all_results = {
                '_id': x['_id'],
                'title': x['title'],
                'text': x['text'],
                'author': x['author']
            }
            all_results_list.append(all_results)

        return render_template('delete.html', all_results=all_results_list, confirm=True, counter=counter)


@app.route("/delete/<id>")
def delete(id):
    msg_counter = mdb.noticia.find({"_id": f"{id}"}).count()
    mdb.noticia.remove({"_id": f"{id}"})
    msg_deleted = mdb.noticia.find({"_id": f"{id}"}).count()
    return render_template('delete.html', msg_deleted=msg_deleted, msg_counter=msg_counter, counter=0)


@app.route("/update")
def update_news():
    return render_template("update.html")


@app.route('/updating')
def updating():
    search = request.args.get('search')
    find = mdb.noticia.find({"$text": {"$search": f"{search}"}})
    result_list = []
    for x in find:
        result = {
            '_id': x['_id'],
            'title': x['title'],
            'text': x['text'],
            'author': x['author'],
            'timestamp': datetime.datetime.now()
        }
        result_list.append(result)
    return render_template('update.html', result_list=result_list)


@app.route('/updating/<id>')
def updating_news(id):
    return render_template('updating.html', id=id)


@app.route('/updated/<id>')
def updated(id):
    new_title = request.args.get('title')
    new_text = request.args.get('text')
    new_author = request.args.get('author')
    if new_title != "" and new_text != "" and new_author != "":
        for x in mdb.noticia.find({"_id": f"{id}"}):
            mdb.noticia.update_one({"title": f"{x['title']}"}, {"$set": {"title": f'{new_title}'}})
            mdb.noticia.update_one({"text": f"{x['text']}"}, {"$set": {"text": f'{new_text}'}})
            mdb.noticia.update_one({"author": f"{x['author']}"}, {"$set": {"author": f'{new_author}'}})
            msg = "Notícia atualizada!"

    elif new_title == "" and new_text != "" and new_author != "":
        for x in mdb.noticia.find({"_id": f"{id}"}):
            mdb.noticia.update_one({"text": f"{x['text']}"}, {"$set": {"text": f'{new_text}'}})
            mdb.noticia.update_one({"author": f"{x['author']}"}, {"$set": {"author": f'{new_author}'}})
            msg = "Texto e autor atualizados"

    elif new_title != "" and new_text == "" and new_author != "":
        for x in mdb.noticia.find({"_id": f"{id}"}):
            mdb.noticia.update_one({"title": f"{x['title']}"}, {"$set": {"title": f'{new_title}'}})
            mdb.noticia.update_one({"author": f"{x['author']}"}, {"$set": {"author": f'{new_author}'}})
            msg = "Título e autor atualizados"

    elif new_title != "" and new_text != "" and new_author == "":
        for x in mdb.noticia.find({"_id": f"{id}"}):
            mdb.noticia.update_one({"title": f"{x['title']}"}, {"$set": {"title": f'{new_title}'}})
            mdb.noticia.update_one({"text": f"{x['text']}"}, {"$set": {"text": f'{new_text}'}})
            msg = "Título e texto atualizados"

    elif new_title != "" and new_text == "" and new_author == "":
        for x in mdb.noticia.find({"_id": f"{id}"}):
            mdb.noticia.update_one({"title": f"{x['title']}"}, {"$set": {"title": f'{new_title}'}})
            msg = "Título atualizado"

    elif new_title == "" and new_text != "" and new_author == "":
        for x in mdb.noticia.find({"_id": f"{id}"}):
            mdb.noticia.update_one({"text": f"{x['text']}"}, {"$set": {"text": f'{new_text}'}})
            msg = "Texto atualizado"

    else:
        msg = "Nenhuma alteração feita"

    return render_template("updating.html", msg=msg)
