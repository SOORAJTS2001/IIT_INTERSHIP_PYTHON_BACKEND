from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from flask import flash
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

# Define the Song model
class Song:
    def __init__(self, title, artist, album, filename, url):
        self.title = title
        self.artist = artist
        self.album = album
        self.filename = filename
        self.url = url

# Define a list to hold all the uploaded songs
songs_list = []

# Define a function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Define the index route
@app.route('/')
def index():
    return render_template('index.html', songs=songs_list)

# Define the upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty part without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Check if the file extension is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = request.host_url + 'uploads/' + filename
            song = Song(request.form['title'], request.form['artist'], request.form['album'], filename, url)
            songs_list.append(song)
            return redirect(url_for('index'))
    return render_template('upload.html')

# Define the delete route
@app.route('/delete/<filename>')
def delete(filename):
    # Remove the song from the songs list and delete the file from the server
    for song in songs_list:
        if song.filename == filename:
            songs_list.remove(song)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

# Define the search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        print(keyword)
        search_results = []
        for song in songs_list:
            if keyword.lower() in song.title.lower() or keyword.lower() in song.artist.lower() or keyword.lower() in song.album.lower():
                search_results.append(song)
        return render_template('search.html', keyword=keyword, search_results=search_results)
    return render_template('search.html')

# Define the stream route
@app.route('/stream/<filename>')
def stream(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True)
