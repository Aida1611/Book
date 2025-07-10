from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Subject, EBook, EBookAudio

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class EBookAudioInline(admin.TabularInline):
    model = EBookAudio
    extra = 1
    fields = ('audio_label', 'audio_type', 'page', 'audio_file', 'audio_player')
    readonly_fields = ('audio_player',)
    ordering = ('page',)
    verbose_name = _('Аудиофайл')
    verbose_name_plural = _('Аудиофайлы')

    def audio_player(self, obj):
        if obj.audio_file:
            return format_html(
                '<audio controls style="width:300px;">'
                '<source src="{}" type="audio/mpeg">'
                'Ваш браузер не поддерживает аудио.'
                '</audio>',
                obj.audio_file.url
            )
        return "Аудиофайл не загружен"
    audio_player.short_description = "Прослушать аудио"

@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'grade', 'subject', 'slug')
    list_filter = ('title', 'grade', 'year')
    search_fields = ('title', 'author')
    filter_horizontal = ('related_studies',)

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'slug', 'description')
        }),
        (_('Детали'), {
            'fields': ('subject', 'grade', 'part', 'year', 'image')
        }),
        (_('Связанные материалы'), {
            'fields': ('related_studies',)
        }),
    )

    inlines = [EBookAudioInline]

@admin.register(EBookAudio)
class EBookAudioAdmin(admin.ModelAdmin):
    list_display = ('ebook', 'audio_type', 'audio_label', 'page', 'audio_link')
    list_filter = ('audio_type', 'ebook', 'page')
    search_fields = ('ebook__title', 'audio_label')
    ordering = ('ebook', 'page', 'audio_type')
    readonly_fields = ('audio_link',)

    def audio_link(self, obj):
        if obj.audio_file and hasattr(obj.audio_file, 'url'):
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">Слушать аудио</a>',
                obj.audio_file.url
            )
        return "Аудиофайл не загружен"
    audio_link.short_description = "Аудио файл"
