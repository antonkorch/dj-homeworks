from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, Likes


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['status'] == 'DRAFT' and data['creator']['id'] != self.context['request'].user.id:
            return None
        return data

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        open_adv_count = Advertisement.objects.filter(
            creator=self.context["request"].user,
            status=AdvertisementStatusChoices.OPEN
        ).count()
        status = data.get('status', None)
        if open_adv_count >= 10 and status != AdvertisementStatusChoices.CLOSED:
            raise serializers.ValidationError("Превышено максимальное количество объявлений")

        return data

class LikesSerializer(serializers.ModelSerializer):
    """Serializer для лайков."""

    class Meta:
        model = Likes
        fields = ('id', 'creator', 'advertisement')
        read_only_fields = ['creator']
    

    def validate(self, data):
        creator = self.context['request'].user
        advertisement = data['advertisement']
        if Likes.objects.filter(creator=creator, advertisement=advertisement).exists():
            raise serializers.ValidationError('Лайк уже поставлен')
        if advertisement.creator == creator:
            raise serializers.ValidationError('Нельзя лайкнуть свое объявление')
        return data


