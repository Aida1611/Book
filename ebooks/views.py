from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import Subject, EBook, EBookAudio
from .serializers import SubjectSerializer, EBookSerializer, EBookAudioSerializer
from .filters import EBookFilter, EBookAudioFilter
from .pagination import EBookPagination, EBookAudioPagination

from .filters import EBookFilter, EBookAudioFilter

# --- Обычные Django views для шаблонов ---
def home(request):
    latest_books = EBook.objects.order_by('-id')[:5]
    return render(request, 'home.html', {'latest_books': latest_books})


def book_detail(request, book_id):
    book = get_object_or_404(EBook, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})


def book_list(request):
    books = EBook.objects.all()

    subject_filter = request.GET.get('subject')
    if subject_filter:
        books = books.filter(subject__id=subject_filter)

    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    books = books.order_by('id')

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ebooks/book_list.html', {
        'page_obj': page_obj,
        'subjects': Subject.objects.all(),
        'selected_subject': subject_filter,
        'search_query': search_query,
    })


# --- Фильтры для DRF API ---
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


# --- DRF ViewSets с правильной пагинацией ---
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # Можно не указывать пагинацию, если не нужна или использовать дефолт
    # pagination_class = EBookPagination  # если надо


class EBookViewSet(viewsets.ModelViewSet):
    queryset = EBook.objects.select_related("subject").all()
    serializer_class = EBookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EBookFilter
    pagination_class = EBookPagination  # 15 записей на страницу


class EBookAudioViewSet(viewsets.ModelViewSet):
    queryset = EBookAudio.objects.select_related("ebook").all()
    serializer_class = EBookAudioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EBookAudioFilter
    pagination_class = EBookAudioPagination  # 10 записей на страницу
