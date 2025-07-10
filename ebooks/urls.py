from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # импортируем твой файл views.py

# DRF‑роутер
router = DefaultRouter()
router.register(r"subjects", views.SubjectViewSet)
router.register(r"ebooks", views.EBookViewSet)
router.register(r"audio", views.EBookAudioViewSet)

urlpatterns = [
    # HTML‑страницы
    path("", views.home, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),

    # API
    path("api/", include(router.urls)),
]
