from django.urls import path, include
from musics.views import index, create_album, edit_album, delete_album, album_details, create_song, serve_song, \
    play_song

urlpatterns = [
    path('', index, name='index'),
    path('album/', include([
        path('create/', create_album, name='create-album'),
        path('edit/<int:pk>/', edit_album, name='edit-album'),
        path('delete/<int:pk>/', delete_album, name='delete-album'),
        path('details/<int:pk>/', album_details, name='details-album'),
    ])),
    path('song/', include([
        path('create/', create_song, name='create-song'),
        path('serve-song/<int:album_id>/<int:song_id>/', serve_song, name='serve-song'),
        path('play-song/<int:pk>/', play_song, name='play-song'),
    ]))
]
