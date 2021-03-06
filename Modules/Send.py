import spotipy


def create_playlist(name, ls_track, token):
    sp = spotipy.Spotify(auth=token)
    user = ''.join(filter(lambda i: i.isdigit(), sp.current_user()['uri']))
    sp.user_playlist_create(user, name)
    playlist = sp.user_playlists(user)
    playlist_id = (playlist['items'][0]['id'])
    for song in ls_track:
        sp.playlist_add_items(playlist_id, [song])

