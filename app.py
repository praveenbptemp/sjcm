import streamlit as st
import sqlite3
from datetime import datetime

# Set Streamlit app-wide configurations
st.set_page_config(
    page_title='SJCM INDIA',
    layout="centered",
    initial_sidebar_state="expanded"
)

# Set custom CSS styles
st.markdown(
    """
    <style>
    :root {
        --primary-color: #98eecc;
        --background-color: #79e0ee;
        --secondary-background-color: #d0f5be;
        --text-color: #000000;
        --font-family: serif;
    }

    .song-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    

    .song-details {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;  /* Align to the center */
        margin-bottom: 20px;
    }

    .song-details p {
        flex: 1;
        margin: 5px;
    }
    .song-details p.center {
        text-align: center;  /* Align to the center */
    }

    .header-text {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a connection to the SQLite database
conn = sqlite3.connect('lyrics.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS songs
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              album TEXT,
              artists TEXT,
              year DATE,
              genre TEXT,
              language TEXT,
              lyrics TEXT,
              audio_link TEXT)''')


# Function to get artists for a given song ID
def get_song_artists(song_id):
    c.execute('SELECT artists FROM songs WHERE id = ?', (song_id,))
    artists = c.fetchone()[0]
    return artists.split(',')


# Main function for the view songs page
def view_songs_app():
    st.title('View Songs')
    st.markdown('<hr>', unsafe_allow_html=True)

    # Search input
    search_term = st.text_input('Search by Song ID, Title, Artist, Year, Genre, Language, or Lyrics')

    # Get songs based on search term
    c.execute(
        "SELECT * FROM songs WHERE title LIKE ? OR id = ? OR artists LIKE ? OR year LIKE ? OR genre LIKE ? OR language LIKE ? OR lyrics LIKE ?",
        (
            '%' + search_term + '%', search_term, '%' + search_term + '%', '%' + search_term + '%',
            '%' + search_term + '%',
            '%' + search_term + '%', '%' + search_term + '%'))
    songs = c.fetchall()

    # Display songs
    for song in songs:
        song_id, song_title, song_album, song_artists, song_year, song_genre, song_language, song_lyrics, song_audio_link = song

        # Apply custom formatting to the song details
        st.markdown(f'<div class="song-title">{song_title}</div>', unsafe_allow_html=True)
        st.markdown('<div class="song-details">', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Song ID: </strong> {song_id}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Album:</strong> {song_album}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Artists:</strong> {song_artists}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Year:</strong> {song_year}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Genre:</strong> {song_genre}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Language:</strong> {song_language}</p>', unsafe_allow_html=True)
        st.markdown(
            f'<p><strong>Audio Link:</strong> <a href="{song_audio_link}" target="_blank">{song_audio_link}</a></p>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Lyrics:</strong> {song_lyrics}</p>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)


# Main function for the entry songs page
def entry_songs_app():
    st.title('Entry Songs')
    st.markdown('<hr>', unsafe_allow_html=True)

    # Check if the user is authorized to access the entry page
    password = st.text_input('Enter the password to access the song entry page', type='password')
    if password != 'Dpaul@777':  # Replace 'your_password' with your desired password
        st.error('Invalid password. Please try again or contact the administrator for access.')
        return

    # Song details input
    song_title = st.text_input('Title')
    song_album = st.text_input('Album')
    song_artists = st.text_input('Artists')
    song_year = st.text_input('Year')
    song_genre = st.text_input('Genre')
    song_language = st.text_input('Language')
    song_lyrics = st.text_area('Lyrics')
    song_audio_link = st.text_input('Audio Link')

    # Save song button
    if st.button('Save Song'):
        # Insert song details into the database
        c.execute(
            'INSERT INTO songs (title, album, artists, year, genre, language, lyrics, audio_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (song_title, song_album, song_artists, song_year, song_genre, song_language, song_lyrics, song_audio_link))
        conn.commit()
        st.success('Song saved successfully!')

        # Clear input fields after saving
        song_title = ''
        song_album = ''
        song_artists = ''
        song_year = ''
        song_genre = ''
        song_language = ''
        song_lyrics = ''
        song_audio_link = ''

    # View songs button
    if st.button('View Songs'):
        view_songs_app()


# Main function to run the app
def main():
    st.markdown('<div class="header-text">Welcome to Soldiers of Jesus Christ Ministries SJCM India</div>',
                unsafe_allow_html=True)

    # Set the default menu selection to View Songs
    menu = 'View Songs'

    # Sidebar menu
    menu = st.sidebar.selectbox('Menu', ['Entry Songs', 'View Songs'], index=1)

    if menu == 'Entry Songs':
        entry_songs_app()
    elif menu == 'View Songs':
        view_songs_app()


# Run the app
if __name__ == '__main__':
    main()
