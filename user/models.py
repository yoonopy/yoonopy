from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
	"""
	프로필사진
	유저이름
	닉네임
	이메일주소
	비밀번호
	"""
	email = models.EmailField(unique=True)
	name = models.CharField(max_length=30)
	user_id = models.CharField(unique=True, max_length=30)
	profile_image = models.CharField(max_length=256, default='default_profile.png',)

	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.user_id

	class Meta:
		db_table = "User" # 테이블이름 정하기
