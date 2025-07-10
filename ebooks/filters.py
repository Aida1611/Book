import django_filters
from .models import EBook, EBookAudio

class EBookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')
    subject = django_filters.NumberFilter(field_name='subject__id')

    class Meta:
        model = EBook
        fields = ['title', 'author', 'subject']


class EBookAudioFilter(django_filters.FilterSet):
    audio_type = django_filters.CharFilter(field_name='audio_type', lookup_expr='iexact')
    page = django_filters.NumberFilter(field_name='page')
    ebook = django_filters.CharFilter(field_name='ebook__title', lookup_expr='icontains')

    class Meta:
        model = EBookAudio
        fields = ['audio_type', 'page', 'ebook']
