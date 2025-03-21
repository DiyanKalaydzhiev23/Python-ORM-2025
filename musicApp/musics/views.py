from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render, redirect
from musicApp.settings import session
from musicApp.utils import handle_session
from musics.forms import AlbumCreateForm, SongBaseForm, AlbumEditForm, AlbumDeleteForm, SongCreateForm
from musics.models import Album, Song


@handle_session(session)
def index(request):
    context = {
        'albums': session.query(Album).all()
    }

    return render(request, 'common/index.html', context)


@handle_session(session)
def create_album(request):
    context = {
        'form': AlbumCreateForm()
    }

    if request.method == "POST":
        form = AlbumCreateForm(request.POST)

        if form.is_valid():
            new_album = Album(
                album_name=form.cleaned_data['album_name'],
                image_url=form.cleaned_data['image_url'],
                price=form.cleaned_data['price'],
            )

            session.add(new_album)

            return redirect('index')

    return render(request, 'albums/create-album.html', context)


@handle_session(session)
def edit_album(request, pk: int):
    album = session.query(Album).filter_by(id=pk).one()
    form = None

    if request.method == "GET":
        initial_data = {
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }

        form = AlbumEditForm(initial=initial_data)

    if request.method == "POST":
        form = AlbumEditForm(request.POST)

        if form.is_valid():
            album.album_name = form.cleaned_data['album_name']
            album.image_url = form.cleaned_data['image_url']
            album.price = form.cleaned_data['price']

            return redirect('index')

    context = {
        'album': album,
        'form': form,
    }

    return render(request, 'albums/edit-album.html', context)


@handle_session(session)
def delete_album(request, pk: int):
    album = session.query(Album).filter_by(id=pk).one()
    form = None

    if request.method == "GET":
        initial_data = {
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }

        form = AlbumDeleteForm(initial=initial_data)

    if request.method == "POST":
        session.delete(album)
        return redirect('index')

    context = {
        'album': album,
        'form': form,
    }

    return render(request, 'albums/delete-album.html', context)



@handle_session(session)
def album_details(request, pk: int):
    context = {
        "album": session.query(Album).filter_by(id=pk).first()
    }

    return render(request, 'albums/album-details.html', context)


@handle_session(session)
def create_song(request):
    context = {
        'form': SongCreateForm(),
    }

    if request.method == 'POST':
        form = SongCreateForm(request.POST, request.FILES)

        if form.is_valid():
            new_song = Song(
                song_name=form.cleaned_data['song_name'],
                album_id=form.cleaned_data['album'],
                music_file_data=request.FILES['music_file_data'].read(),
            )

            session.add(new_song)

            return redirect('index')

    return render(request, 'songs/create-song.html', context)


@handle_session(session)
def play_song(request, pk: int):
    context = {
        'song': session.query(Song).filter_by(id=pk).one(),
    }

    return render(request, 'songs/music-player.html', context)


@handle_session(session)
def serve_song(request, album_id: int, song_id: int):
    song = session.query(Song).filter_by(album_id=album_id, id=song_id).one()

    response = HttpResponse(
        song.music_file_data,
        content_type='audio/mpeg',
    )
    response['Content-Disposition'] = 'inline; filename={}'.format(song.song_name)
    return response
