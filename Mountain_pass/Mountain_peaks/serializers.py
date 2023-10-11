from .models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
       model = Author
       fields = ['id', 'surname', 'name', 'patronymic', 'email', 'telephone']

    # При сохранении пользователя, проверяем его наличие в БД по email
    #def save(self, **kwargs):
    #    self.is_valid()
    #    current_user = Author.objects.filter(email=self.validated_data.get['email'])
    #    if current_user.exists():
    #        return current_user.first()
    #    else:
    #        new_user = Author.objects.create(
    #            surname=self.validated_data.get('surname'),
    #            name=self.validated_data.get('name'),
    #            patronymic=self.validated_data.get('patronymic'),
    #            telephone=self.validated_data.get('telephone'),
    #            email=self.validated_data.get('email'),
    #        )
    #        return new_user


class CoordinateSerializer(serializers.ModelSerializer):
   class Meta:
       model = Coordinate
       fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
       model = Level
       fields = ['winter', 'spring', 'summer', 'autumn']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
       model = Image
       fields = ['title', 'photo']

class PeakSerializer(WritableNestedModelSerializer):
#class PeakSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    coords = CoordinateSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Peak
        fields = ['id', 'country', 'category', 'title', 'other_titles', 'connect', 'add_time', 'status', 'method_of_passage', 'user', 'coords', 'level',
                  'images']

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        images = validated_data.pop('images')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')

        user, created = Author.objects.get_or_create(**user)

        #current_user = Author.objects.filter(email=user['email'])
        #if current_user.exists():
        #    user_serializer = AuthorSerializer(data=user)
        #    user_serializer.is_valid(raise_exception=True)
        #    user = user_serializer.save()
        #else:
        #    user = Author.objects.create(**user)

        coords = Coordinate.objects.create(**coords)
        level = Level.objects.create(**level)

        peak = Peak.objects.create(**validated_data, user=user, coords=coords, level=level)

        if images:
            for image in images:
                image_name = image.pop('title')
                image = image.pop('photo')
                Image.objects.create(peak=peak, title=image_name, photo=image)

        peak.save()
        return peak

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')
        level_data = validated_data.pop('level')

        user = instance.user
        coords = instance.coords
        level = instance.level

        instance.country = validated_data.get('country', instance.country)
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.method_of_passage = validated_data.get('method_of_passage', instance.method_of_passage)
        instance.save()

        coords.latitude = coords_data.get('latitude', coords.latitude)
        coords.longitude = coords_data.get('longitude', coords.longitude)
        coords.height = coords_data.get('height', coords.height)
        coords.save()

        level.winter = level_data.get('winter', level.winter)
        level.summer = level_data.get('summer', level.summer)
        level.autumn = level_data.get('autumn', level.autumn)
        level.spring = level_data.get('spring', level.spring)
        level.save()

        images = Image.objects.filter(peak=instance)
        images.delete()  # удаляем старые объекты и записываем новые изображения
        if images_data:
            for image in images_data:
                image_name = image.pop('title')
                image = image.pop('photo')
                Image.objects.create(peak=instance, title=image_name, photo=image)

        return instance

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            user_fields_for_validation = [
                instance_user.surname != data_user['surname'],
                instance_user.name != data_user['name'],
                instance_user.patronymic != data_user['patronymic'],
                instance_user.telephone != data_user['telephone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Отказ': 'Данные пользователя не могут быть изменены!',
                    }
                )
        return data

