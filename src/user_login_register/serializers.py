from django.contrib.auth.models import User
from rest_framework import serializers

# User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'

        ]

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }
    

    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        user.save()
        return user