# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 08:27:02 2023

@author: user1
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


# Spotify API credentials from Spotify
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'


def get_playlists():
    playlists = sp.user_playlists(username)
    playlist_names = [playlist['name'] for playlist in playlists['items']]
    return playlist_names


def get_songs(playlist_name):
    songs = []
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            while tracks:
                for item in tracks['items']:
                    track = item['track']
                    artist = track['artists'][0]['name']
                    song_name = track['name']
                    album_name = track['album']['name']
                    year = track['album']['release_date'][:4]
                    songs.append([artist, song_name, album_name, year])
                tracks = sp.next(tracks)
    return songs


def export_to_text_file():
    playlist_name = playlist_listbox.get(tk.ACTIVE)
    if not playlist_name:
        messagebox.showwarning('No Playlist Selected', 'Please select a playlist.')
        return

    songs = get_songs(playlist_name)

    file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    if not file_path:
        return

    with open(file_path, 'w') as file:
        file.write('Artist|Song Name|Album Name|Year\n')
        for song in songs:
            file.write('|'.join(song) + '\n')

    messagebox.showinfo('Export Complete', 'Playlist exported successfully.')


# Spotify API authentication
auth_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# GUI setup
window = tk.Tk()
window.title('Spotify Playlist Viewer')
window.geometry('400x300')

# Playlist listbox
playlist_listbox = tk.Listbox(window)
playlist_listbox.pack(padx=10, pady=10)

# Get playlists button
get_playlists_button = tk.Button(window, text='Get Playlists', command=lambda: playlist_listbox.insert(tk.END, *get_playlists()))
get_playlists_button.pack(pady=5)

# Songs listbox
songs_listbox = tk.Listbox(window)
songs_listbox.pack(padx=10, pady=10)

# Export button
export_button = tk.Button(window, text='Export to Text File', command=export_to_text_file)
export_button.pack(pady=5)

# Run the GUI
window.mainloop()
