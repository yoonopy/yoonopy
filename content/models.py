from django.db import models
from django.db.models import EmailField


class Feed(models.Model):
	content    = models.TextField()
	image      = models.TextField()
	profile_image = models.TextField()
	email = models.EmailField(verbose_name='email', null=True)
	user_id    = models.CharField(max_length=30)
	like_count = models.IntegerField()

class Like(models.Model):
	# 좋아요
	feed_id = models.IntegerField()
	email   = models.EmailField()

	class Meta:
		indexes = [
			models.Index(fields=['feed_id']),
			models.Index(fields=['email'])
        ]

class Bookmark(models.Model):
	# 북마크
	feed_id = models.IntegerField()
	email   = models.EmailField()
	
	class Meta:
		indexes = [
            models.Index(fields=['feed_id']),
            models.Index(fields=['email'])
		]

class Comment(models.Model):
    # 댓글
	feed_id  = models.IntegerField()
	email    = models.EmailField()
	user_id  = models.CharField(max_length=30)
	comment = models.CharField(max_length=300)

	class Meta:
		indexes = [
            models.Index(fields=['feed_id']),
            models.Index(fields=['email'])
		]

