from django.urls import path
from .views import DeleteComment, UploadFeed, LikeFeed, BookmarkFeed, CommentFeed, DeleteFeed

urlpatterns = [
	path('upload', UploadFeed.as_view()),
	path('like', LikeFeed.as_view()),
	path('bookmark', BookmarkFeed.as_view()),
	path('comment', CommentFeed.as_view()),
	path('delete_comment', DeleteComment.as_view()),
	path('delete_feed', DeleteFeed.as_view())
]
