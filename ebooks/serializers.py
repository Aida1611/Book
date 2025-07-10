from rest_framework import serializers
from .models import Subject, EBook, EBookAudio


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']  # замени на реальные поля Subject


class EBookSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = EBook
        fields = [
            'id',
            'title',
            'author',
            'subject',
            'grade',
            'part',
            'year',
            'image',
            'type',  # добавляем тип
        ]

    def get_type(self, obj):
        return "ebook"


class EBookAudioSerializer(serializers.ModelSerializer):
    ebook = EBookSerializer(read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = EBookAudio
        fields = [
            'id',
            'audio_type',
            'page',
            'audio_file',
            'ebook',
            'type',  # добавляем тип
        ]

    def get_type(self, obj):
        return "audio"
