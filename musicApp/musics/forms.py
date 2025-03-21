from django import forms

from musicApp.settings import session
from musicApp.utils import handle_session
from musics.models import Album


class DisabledFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True



class AlbumBaseForm(forms.Form):
    album_name = forms.CharField(
        label="Album name:",
        max_length=30,
        required=True,
    )

    image_url = forms.URLField(
        label="Image URL:",
        required=True,
    )

    price = forms.DecimalField(
        label="Price:",
        min_value=0.0,
        required=True,
    )


class AlbumCreateForm(AlbumBaseForm):
    ...


class AlbumEditForm(AlbumBaseForm):
    ...


class AlbumDeleteForm(DisabledFieldsMixin, AlbumBaseForm):
    ...

class SongBaseForm(forms.Form):
    song_name = forms.CharField(
        max_length=200,
        required=True,
    )

    album = forms.ChoiceField(
        label="Album:",
        choices=[],
    )

    # album = forms.ModelChoiceField(
    #     label="Album:",
    #     queryset=Album.objects.all()
    # )

    @handle_session(session)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        albums = session.query(Album).all()
        self.fields['album'].choices = [(album.id, album.album_name) for album in albums]


class SongCreateForm(SongBaseForm):
    music_file_data = forms.FileField(
        label="Music File: ",
        required=True,
    )
