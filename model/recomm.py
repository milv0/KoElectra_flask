import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from model.emotion import Emotion

client_credentials_manager = SpotifyClientCredentials(
    client_id='ID',
    client_secret='SECRET'
    )

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
Emo = Emotion()

## mode - major: 1, minor: 0
## min, max 대신 target으로 변경

def recommandMusics(emotion):
    seed_artist=["3HqSLMAZ3g3d5poNaI7GOU", "3Nrfpe0tUJi4K4DXYWgMUX"]
    seed_genre=["k-pop"]
    seed_track=["1r9xUipOqoNwggBpENDsvJ"]

    rec1 = {}
    rec2 = {}

    # JOY 기쁨
    if emotion == Emo.JOY:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.9,
            target_energy=0.9,
            target_valence=0.9,
            target_tempo=120
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.3,
            target_energy=0.3,
            target_valence=0.3,
            target_tempo=60
            )

    # HOPE 희망
    elif emotion == Emo.HOPE:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.6,
            target_energy=0.9,
            target_valence=0.9,
            target_tempo=120
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.3,
            target_energy=0.3,
            target_valence=0.3,
            target_tempo=70
            )

    # NEUTRALITY 중립
    elif emotion == Emo.NEUTRALITY:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.5,
            target_energy=0.5,
            target_valence=0.5,
            target_tempo=100
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.6,
            target_energy=0.6,
            target_valence=0.6,
            target_tempo=100
            )

    # SADNESS 슬픔
    elif emotion == Emo.SADNESS:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.1,
            target_energy=0.1,
            target_valence=0.1,
            target_tempo=60
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.6,
            target_energy=0.7,
            target_valence=0.9,
            target_tempo=120
            )

    # ANGER 분노
    elif emotion == Emo.ANGER:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.5,
            target_energy=0.9,
            target_valence=0.3,
            target_tempo=120
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.9,
            target_energy=0.8,
            target_valence=0.8,
            target_tempo=100
            )

    # ANXIETY 불안
    elif emotion == Emo.ANXIETY:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.3,
            target_energy=0.3,
            target_valence=0.2,
            target_tempo=80
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.5,
            target_energy=0.5,
            target_valence=0.9,
            target_tempo=110
            )

    # TIREDNESS 피곤
    elif emotion == Emo.TIREDNESS:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.1,
            target_energy=0.3,
            target_valence=0.4,
            target_tempo=70
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.6,
            target_energy=0.6,
            target_valence=0.6,
            target_tempo=120
            )

    # REGERT 후회
    elif emotion == Emo.REGRET:
        rec1 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.1,
            target_energy=0.2,
            target_valence=0.2,
            target_tempo=80
            )
        rec2 = sp.recommendations(
            seed_artists=seed_artist,
            seed_genres=seed_genre,
            seed_tracks=seed_track,
            limit=5,
            target_danceability=0.3,
            target_energy=0.6,
            target_valence=0.6,
            target_tempo=100
            )


    return rec1['tracks'], rec2['tracks']
