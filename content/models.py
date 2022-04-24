from django.db import models

class Feed(models.Model):
	content    = models.TextField()
	image      = models.TextField()
	profile_image = models.TextField()
	email = models.EmailField(verbose_name='email', null=True)
	user_id    = models.CharField(max_length=30)
	like_count = models.IntegerField()



