import os
from flask import Flask, request, abort
from werkzeug.utils import secure_filename

"""Приложение для загрузки картинок с расширением jpg и jpeg
   с размером не более 100 кбайт.
   Например:
   curl -i -X POST -F file="@/home/user/image.jpg" http://127.0.0.1:5000/upload

"""

UPLOAD_FOLDER="./uploads"
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024


def allowed_file(filename):
    """Возвращаем файл с нужным расширением"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """ Сохраняем файл в UPLOAD_FOLDER"""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'Success\n'
        else:
            return abort(404)
    else:
        abort(404)

if __name__ == '__main__':
    app.run()