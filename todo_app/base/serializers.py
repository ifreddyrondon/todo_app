from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils import timezone
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password',
                  'confirm_password', 'tasks', )

    def create(self, validated_data):
        username = validated_data.get('username', None)
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)
        if password != confirm_password:
            raise serializers.ValidationError('The password and the confirm password must be equals.')

        return get_user_model().objects.create_user(username=username, password=password)

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
        else:
            raise serializers.ValidationError('The password and the confirm password must be equals.')

        instance.updated_at = timezone.now()
        instance.save()
        update_session_auth_hash(self.context.get('request'), instance)

        return instance
