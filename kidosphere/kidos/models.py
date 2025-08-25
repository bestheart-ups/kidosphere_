from django.contrib.auth.models import AbstractUser
from django.db import models

#creating kidosphere models

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def _str_(self):
        return self.username


class Post(models.Model):
    CONTENT_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    content_url = models.URLField(blank=True, null=True)  # URL for image/video
    text = models.TextField(blank=True, null=True)        # Text content if applicable
    tags = models.JSONField(blank=True, null=True)        # Optional list of tags
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Post {self.id} by {self.user.username}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows

    def _str_(self):
        return f"{self.follower.username} follows {self.following.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def _str_(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.sent_at}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Notification for {self.user.username}: {'Read' if self.is_read else 'Unread'}"
