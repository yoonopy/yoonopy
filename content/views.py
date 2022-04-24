from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from uuid import uuid4
from .models import Feed
from stagram.settings import MEDIA_ROOT


class UploadFeed(APIView):
	def post(self, request):

		file = request.FILES['file']
		ext  = os.path.splitext(str(file.name))[1]  # 확장자

		uuid_name = uuid4().hex + ext # 고유id
		save_path = os.path.join(MEDIA_ROOT, uuid_name)

		# 파일쓰기
		with open(save_path, 'wb+') as f:
			for chunk in file.chunks():
				f.write(chunk)

		# data.get 로 파일 받기
		content = request.data.get('content', )
		image   = uuid_name
		profile_image = request.data.get('profile_image', )
		user_id = request.data.get('user_id', )

		Feed.objects.create(content=content, image=image,
		                    profile_image=profile_image, user_id=user_id, like_count=0)

		return Response(status=200)