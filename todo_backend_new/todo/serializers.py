from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
# Import the validate_password function
from django.contrib.auth.password_validation import validate_password
from .models import Todo, CustomUser
# Import the TokenObtainPairSerializer class
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')


# class UserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     username = serializers.CharField(
#         max_length=32,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(min_length=8, write_only=True)

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'],
#                                         validated_data['password'])
#         return user

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password',
                  'password2', 'bio', 'cover_photo')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            cover_photo=validated_data['cover_photo']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    notes = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
