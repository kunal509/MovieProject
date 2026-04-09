import sqlite3

connection = sqlite3.connect('movies.db')
cursor = connection.cursor()

# 1. NEW: Completely wipe the old table so we don't get duplicates
cursor.execute('DROP TABLE IF EXISTS movies')

# 2. Create the fresh table
cursor.execute('''
    CREATE TABLE movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year TEXT NOT NULL,
        description TEXT,
        poster TEXT,
        video TEXT
    )
''')

# 3. UPDATE YOUR VIDEOS HERE
movies_data = [
    ("Night of the Living Dead", "1968", "A classic public domain horror film.", "poster1.jpg", "Dhurandhar.mp4"),
    ("Big Buck Bunny", "2008", "A giant rabbit gets revenge.", "poster2.jpg", "bunny_movie.mp4"),
    ("Sita Sings the Blues", "2008", "An animated film.", "poster3.jpg", "sita_movie.mp4")
]

# 4. Inject the new data
cursor.executemany('''
    INSERT INTO movies (title, year, description, poster, video)
    VALUES (?, ?, ?, ?, ?)
''', movies_data)

connection.commit()
connection.close()

print("Database completely reset and updated with new videos, sir!")