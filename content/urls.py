from django.urls import path
from .views import UploadFeed, LikeFeed, BookmarkFeed, CommentFeed

urlpatterns = [
	path('upload', UploadFeed.as_view()),
	path('like', LikeFeed.as_view()),
	path('bookmark', BookmarkFeed.as_view()),
	path('comment', CommentFeed.as_view())
]
