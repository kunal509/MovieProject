import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- 1. PRODUCTION CONFIGURATION ---
# This ensures the server finds your files and doesn't cache the old CSS
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# --- 2. DATABASE PATHING ---
def get_db_connection():
    # This finds the exact folder where this app.py is running
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'movies.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    return conn

# --- 3. MAIN WEBSITE ROUTE ---
@app.route('/')
def home():
    conn = get_db_connection()
    movies_from_db = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies_from_db)

# --- 4. SECRET ADMIN PAGE ROUTE ---
@app.route('/admin')
def admin():
    conn = get_db_connection()
    movies_from_db = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('admin.html', movies=movies_from_db)

# --- 5. ADD A MOVIE ---
@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.form['title']
    year = request.form['year']
    description = request.form['description']
    poster = request.form['poster']
    video = request.form['video']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO movies (title, year, description, poster, video) VALUES (?, ?, ?, ?, ?)',
                 (title, year, description, poster, video))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# --- 6. DELETE A MOVIE ---
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# --- 7. OPEN THE EDIT PAGE ---
@app.route('/edit_movie/<int:movie_id>')
def edit_movie(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    return render_template('edit.html', movie=movie)

# --- 8. SAVE UPDATES ---
@app.route('/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    title = request.form['title']
    year = request.form['year']
    description = request.form['description']
    poster = request.form['poster']
    video = request.form['video']
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE movies
        SET title = ?, year = ?, description = ?, poster = ?, video = ?
        WHERE id = ?
    ''', (title, year, description, poster, video, movie_id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Production mode: debug is off for global safety
    app.run()