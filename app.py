from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from html_sanitizer import Sanitizer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'songs.db')
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # set max file size to 16 MB


#make a strong secret key
app.secret_key = 'secret key'
app.app_context().push()
# set up application context
with app.app_context():
    db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    url = db.Column(db.Text)
db.create_all()
@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('song_list.html', songs=songs)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        file = request.files['file']
        sanitizer = Sanitizer()
        title= sanitizer.sanitize(title)
        artist = sanitizer.sanitize(artist)
        album = sanitizer.sanitize(album)
        filename = secure_filename(file.filename)
        url = os.path.abspath(app.config['UPLOAD_FOLDER']) + '/' + filename
        file.save(url)
        print(url)
        song = Song(title=title, artist=artist, album=album, url=filename)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        songs = Song.query.filter(
            (Song.title.like('%' + query + '%')) |
            (Song.artist.like('%' + query + '%')) |
            (Song.album.like('%' + query + '%'))
        ).all()
        return render_template('song_list.html', songs=songs)
    return render_template('search.html')

@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete(id):
    song = Song.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/play/<int:id>')
def play(id):
    song = Song.query.get_or_404(id)
    return render_template('stream.html', song=song)

@app.route('/download/<int:id>')
def download(id):
    song = Song.query.get_or_404(id)
    filelocation = os.path.abspath(app.config['UPLOAD_FOLDER']) + '/' + song.url
    
    return send_file(filelocation, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
