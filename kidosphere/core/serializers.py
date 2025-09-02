# core/serializers.py

from rest_framework import serializers
from .models import User, Post, Follow, Message, Comment, Notification
from django.contrib.auth.password_validation import validate_password

# User registration serializer with password confirmation
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Confirm password

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'password', 'password2', 'profile_picture', 'bio')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = user.object.create_user(
username = validated_data["username"],
email = validated_data.get("email"),
password = validated_data["password"],
        )
        return user


# Serializer for User info (for profile display)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'age', 'profile_picture', 'bio')


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user info

    class Meta:
        model = Post
        fields = ('id', 'user', 'content_type', 'content_url', 'text', 'tags', 'is_public', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(user=user, **validated_data)


# Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
        read_only_fields = ('id', 'created_at')


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message_text', 'sent_at', 'is_read')
        read_only_fields = ('id', 'sender', 'sent_at')

    def create(self, validated_data):
        sender = self.context['request'].user
        message = Message.objects.create(sender=sender, **validated_data)
        return message


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'comment_text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)


# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'content', 'is_read', 'created_at')
        read_only_fields = ("'id', 'user', 'created_at'")

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=False)  # optional

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),  #empty if not provided
            password=validated_data["password"]
        )
        return user