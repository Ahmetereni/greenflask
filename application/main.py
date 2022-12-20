# main.py
import os
from flask import Blueprint, render_template, session, send_file, request, redirect, url_for
from flask_login import login_required
from path import mypath
from werkzeug.utils import secure_filename
from application.dochandler import preprocessor

main = Blueprint('main', __name__)
# setting up directory
ABSOLUTE_PATH = mypath()
ALLOWED_EXTENSIONS = {'pdf', 'docx', "txt"}
# ,txt,docx


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/view/<path:filename>')
@login_required
def send_attachment(filename):
    # setting up directory
    strusername = str(session["username"])
    userfile = f"{ABSOLUTE_PATH}\\static\\users\\{strusername}\\{filename}"
    return send_file(userfile)


@main.route('/view', methods=['GET', 'POST'])
def view():

    strusername = str(session["username"])
    users_dir = f"{ABSOLUTE_PATH}\\static\\users\\{strusername}"

    upload_files = request.files.getlist('file')

    if request.method == 'POST':
        
        for file in upload_files:
            filename = file.filename
            if allowed_file(filename):
                file.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), users_dir, secure_filename(file.filename)))
                extension = filename.rsplit('.', 1)[1].lower()
                processed_filepath = f"{users_dir}\{filename}"
                preprocessor(filepath=processed_filepath,
                             filename=filename, username=strusername, extension=extension)
    # tuple(i for i in os.listdir(users_dir)
        return render_template('view.html', users_dir=os.listdir(users_dir), dirname=strusername)
    return render_template('view.html', users_dir=os.listdir(users_dir), dirname=strusername)


@main.route('/delete/<path:filename>', methods=['GET'])
@login_required
def delete(filename):
    from haystack.document_stores import ElasticsearchDocumentStore
    strusername = str(session["username"])
    document_store = ElasticsearchDocumentStore(
        host="localhost", username="elastic", password="WbLoke8xGtKNRu*RPdjd", index=f"{strusername}")
    # setting up directory

    userfile = f"{ABSOLUTE_PATH}\\static\\users\\{strusername}\\{filename}"

    filters = {
        "name": f"{filename}"
    }
    try:
        os.remove(userfile)
        # print(document_store.get_all_documents(index="document"))

        document_store.delete_documents(
            index=f"{strusername}", filters=filters)
        # print(document_store.get_all_documents(index="document"))

        return redirect(url_for('main.view'))
    except:

        return "Error deleting file"
