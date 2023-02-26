from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from html_sanitizer import Sanitizer
from sqlalchemy import text
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(app.instance_path, 'songs.db')
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * \
    1024 * 1024  # set max file size to 16 MB


# make a strong secret key
app.secret_key = 'secret key'
app.app_context().push()
# set up application context
with app.app_context():
    db = SQLAlchemy(app)


# create a database model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    url = db.Column(db.Text)


# create the database
db.create_all()

# create a route for the home page
@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('song_list.html', songs=songs)

# create a route for the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        file = request.files['file']
        # sanitize the input to prevent XSS attacks and other malicious code from being injected into the database and the file system 
        sanitizer = Sanitizer()
        title = sanitizer.sanitize(title)
        artist = sanitizer.sanitize(artist)
        album = sanitizer.sanitize(album)
        # save the file
        filename = secure_filename(file.filename)
        url = os.path.abspath(app.config['UPLOAD_FOLDER']) + '/' + filename
        file.save(url)
        print(url)
        song = Song(title=title, artist=artist, album=album, url=filename)
        # insert the song into the database using raw SQL so we can use the sanitized input without worrying about SQL injection
        sql = text(
            'INSERT INTO song (title, artist, album, url) VALUES (:title, :artist, :album, :url)')
        db.session.execute(sql, {
                           'title': song.title, 'artist': song.artist, 'album': song.album, 'url': song.url})
        # commit the changes to the database
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('upload.html')

# create a route for the search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        songs = Song.query.filter(
            (Song.title.like('%' + query + '%')) |
            (Song.artist.like('%' + query + '%')) |
            (Song.album.like('%' + query + '%'))
        ).all()
        # find the similar songs with the given keyword
        return render_template('song_list.html', songs=songs)
    return render_template('search.html')

# create a route for the delete page
@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    song = Song.query.get_or_404(id)
    filelocation = os.path.abspath(
        app.config['UPLOAD_FOLDER']) + '/' + song.url
    # delete the song from the file system
    os.remove(filelocation)
    # delete the song from the database
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('index'))

# create a route for the stream page
@app.route('/play/<int:id>')
def play(id):
    song = Song.query.get_or_404(id)
    return render_template('stream.html', song=song)

# create a route for the download page
@app.route('/download/<int:id>')
def download(id):
    song = Song.query.get_or_404(id)
    filelocation = os.path.abspath(
        app.config['UPLOAD_FOLDER']) + '/' + song.url

    return send_file(filelocation, as_attachment=True)

# run the application in debug mode so we can see any errors that occur in the browser instead of the terminal window 
if __name__ == '__main__':
    app.run(debug=True)
