# Flask Music App

This is a Flask web application that allows users to upload, play, and download music files. It uses SQLite to store the music file information, and html_sanitizer to sanitize user input to prevent XSS attacks.

## Prerequisites

To run this application, you'll need the following installed on your system:

- Python 3.x
- Flask
- Flask_SQLAlchemy
- html_sanitizer

## Installation

1. Clone this repository to your local machine using `https://github.com/username/flask-music-app.git`.
2. `cd` into the project directory.
3. Create a virtual environment using `python -m venv venv`.
4. Activate the virtual environment using `source venv/bin/activate`.
5. Install the required packages using `pip install -r requirements.txt`.
6. Create the database by running the following commands:

```
$ export FLASK_APP=app.py
$ flask db init
$ flask db migrate -m "Initial migration."
$ flask db upgrade
```


7. Run the app using 
```
$ flask run
```
8. Open your browser and go to `http://localhost:5000/`.

## Usage

### Uploading Music

1. Click on the "Upload" button in the navigation bar.
2. Fill in the required information in the form.
3. Click the "Choose File" button to select the music file to upload.
4. Click the "Upload" button to upload the file.

### Searching for Music

1. Click on the "Search" button in the navigation bar.
2. Enter a search query into the search bar.
3. Press the "Enter" key or click the "Search" button to perform the search.
4. The search results will be displayed on the page.

### Playing Music

1. Click on the "View" button next to a song in the song list.
2. The music player will be displayed on the page.
3. Click the "Play" button to play the song.

### Downloading Music

1. Click on the "Download" button next to a song in the song list.
2. The music file will be downloaded to your device.

### Deleting Music

1. Click on the "Delete" button next to a song in the song list.




