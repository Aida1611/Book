from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator  # <-- добавьте эту строку
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Предмет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

class EBook(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название электронной книги')
    author = models.CharField(max_length=255, verbose_name='Автор')
    slug = models.SlugField(unique=True, verbose_name='Уникальный идентификатор (slug)')
    description = models.TextField(blank=True, verbose_name='Описание')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, verbose_name='Предмет')
    grade = models.IntegerField(default=1, null=False, blank=False, verbose_name='Класс')
    part = models.CharField(max_length=50, blank=True, verbose_name='Часть')
    year = models.PositiveSmallIntegerField(verbose_name='Год издания')
    image = models.ImageField(upload_to='ebooks/images/', blank=True, null=True, verbose_name='Обложка')
    related_studies = models.ManyToManyField('self', blank=True, verbose_name='Связанные материалы')

    def __str__(self):
        return f'{self.title} ({self.author})'

    class Meta:
        verbose_name = 'Электронная книга'
        verbose_name_plural = 'Электронные книги'
        ordering = ['title']


class EBookAudio(models.Model):
    AUDIO_TYPES = [
        ('basic', _('Основное')),
        ('repetition', _('Повторение')),
    ]

    ebook = models.ForeignKey(
        EBook,
        on_delete=models.CASCADE,
        related_name='audios',
        verbose_name=_('Учебник')
    )
    audio_type = models.CharField(
        _('Тип аудио'),
        max_length=10,
        choices=AUDIO_TYPES
    )
    audio_file = models.FileField(
        _('Аудиофайл'),
        upload_to='ebooks/audios/'
    )
    page = models.PositiveIntegerField(
        _('Страница'),
        validators=[MinValueValidator(1)],
        blank=True,
        null=True
    )
    audio_label = models.CharField(
        _('Метка аудио'),
        max_length=255,
        blank=True,
        help_text=_('например, "Unit 1 – Track 3"')
    )

    class Meta:
        verbose_name = _('Аудиофайл')
        verbose_name_plural = _('Аудиофайлы')
        ordering = ['ebook', 'page', 'audio_type']

    def __str__(self):
        return f"{self.ebook.title} – {self.audio_label or self.get_audio_type_display()}"
