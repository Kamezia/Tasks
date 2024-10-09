from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    


class TaskWriteOnlySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ('name', 'task_type', 'task_highlites', 'created_at', 'user')

class TaskReadOnlySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Task
        fields = ('id', 'name', 'task_type', 'task_highlites', 'created_at', 'user')
