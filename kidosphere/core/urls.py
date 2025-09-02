from django.urls import path
from .views import (
    RegisterView, UserDetailView,
    PostListCreateView, PostDetailView,
    FollowListView, FollowingListView, FollowCreateView, 
    FollowDeleteView,
    MessageListCreateView,
    CommentListCreateView, CommentDetailView,
    NotificationListView,
    ProtectedView,   
    home,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", home, name='home'),

    # Authentication
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #  Protected route for testing auth
    path('protected/', ProtectedView.as_view(), name='protected'),

    # User profiles
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Follows
    path('follow/<int:user_id>/', FollowCreateView.as_view(), name='follow-create'),
    path('unfollow/<int:user_id>/', FollowDeleteView.as_view(), name='follow-delete'),
    path('followers/<int:user_id>/', FollowListView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='following-list'),

    # Messages
    path('messages/<int:user_id>/', MessageListCreateView.as_view(), name='message-list-create'),

    # Comments
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]