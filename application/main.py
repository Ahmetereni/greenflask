import os
from flask import Blueprint, render_template, session, send_file, request, redirect, url_for, flash
from flask_login import login_required
from path import mypath
from werkzeug.utils import secure_filename
from application.dochandler import preprocessor

main = Blueprint('main', __name__)

# setting up directory
ABSOLUTE_PATH = mypath()
ALLOWED_EXTENSIONS = {'pdf', 'docx', "txt"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/view/<path:filename>')
@login_required
def send_attachment(filename):
    strusername = str(session["username"])
    userfile = os.path.join(ABSOLUTE_PATH, 'static', 'users', strusername, filename)
    return send_file(userfile)


@main.route('/view', methods=['GET', 'POST'])
def view():
    strusername = str(session["username"])
    users_dir = os.path.join(ABSOLUTE_PATH, 'static', 'users', strusername)

    # Ensure the user's directory exists
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)

    upload_files = request.files.getlist('file')

    if request.method == 'POST':
        for file in upload_files:
            filename = file.filename
            if allowed_file(filename):
                file_path = os.path.join(users_dir, secure_filename(file.filename))
                file.save(file_path)
                
                # Process the uploaded file
                extension = filename.rsplit('.', 1)[1].lower()
                processed_filepath = os.path.join(users_dir, filename)
                # preprocessor(filepath=processed_filepath,
                #              filename=filename, username=strusername, extension=extension)

        return render_template('view.html', users_dir=os.listdir(users_dir), dirname=strusername)

    return render_template('view.html', users_dir=os.listdir(users_dir), dirname=strusername)


@main.route('/delete/<path:filename>', methods=['GET'])
@login_required
def delete(filename):
    # from haystack.document_stores import ElasticsearchDocumentStore
    strusername = str(session["username"])
    # document_store = ElasticsearchDocumentStore(
    #     host="localhost", username="elastic", password="WbLoke8xGtKNRu*RPdjd", index=f"{strusername}")

    userfile = os.path.join(ABSOLUTE_PATH, 'static', 'users', strusername, filename)

    filters = {"name": filename}
    try:
        # Remove file from filesystem
        if os.path.exists(userfile):
            os.remove(userfile)
        else:
            flash("File not found", "error")
            return redirect(url_for('main.view'))

        # Remove document from Elasticsearch
        # document_store.delete_documents(index=strusername, filters=filters)
        
        flash("File deleted successfully", "success")
        return redirect(url_for('main.view'))

    except FileNotFoundError:
        flash("Error: File not found", "error")
    except PermissionError:
        flash("Error: Permission denied", "error")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
    
    return redirect(url_for('main.view'))
