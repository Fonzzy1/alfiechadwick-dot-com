import spotipy


def create_playlist(name, track_list, token):
    sp = spotipy.Spotify(auth=token)
    user = ''.join(filter(lambda i: i.isdigit(), sp.current_user()['uri']))
    sp.user_playlist_create(user, name)
    playlist = sp.user_playlists(user)
    playlist_id = (playlist['items'][0]['id'])
    for song in track_list:
        sp.playlist_add_items(playlist_id, [song])
