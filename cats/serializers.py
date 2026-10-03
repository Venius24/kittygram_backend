import base64
import binascii

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
import webcolors


import datetime as dt

from .models import Achievement, AchievementCat, Cat


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            try:
                header, imgstr = data.split(';base64,', 1)
                ext = header.split('/')[-1]
                if ext not in ('jpeg', 'jpg', 'png', 'gif', 'webp'):
                    raise ValueError
                data = ContentFile(base64.b64decode(imgstr, validate=True), name='temp.' + ext)
            except (ValueError, binascii.Error):
                raise serializers.ValidationError('Некорректное изображение в base64.')

        return super().to_internal_value(data)


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(required=False, many=True)
    color = Hex2NameColor()
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Cat
        fields = (
            'id', 'name', 'color', 'birth_year', 'achievements', 'owner', 'age',
            'image'
            )
        read_only_fields = ('owner',)

    def get_age(self, obj):
        return dt.date.today().year - obj.birth_year

    def validate_birth_year(self, value):
        if value < 1900 or value > dt.date.today().year:
            raise serializers.ValidationError('Укажите год рождения с 1900 по текущий.')
        return value

    def _save_achievements(self, cat, achievements):
        names = [item['name'] for item in achievements]
        if len(names) != len(set(names)):
            raise serializers.ValidationError({'achievements': 'Достижения не должны повторяться.'})
        instances = [Achievement.objects.get_or_create(name=name)[0] for name in names]
        cat.achievements.set(instances)

    @transaction.atomic
    def create(self, validated_data):
        achievements = validated_data.pop('achievements', [])
        cat = Cat.objects.create(**validated_data)
        self._save_achievements(cat, achievements)
        return cat

    @transaction.atomic
    def update(self, instance, validated_data):
        achievements = validated_data.pop('achievements', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if achievements is not None:
            self._save_achievements(instance, achievements)
        return instance
