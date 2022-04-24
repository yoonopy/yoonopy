from rest_framework.views import APIView
from django.shortcuts import render




class Login(APIView):
    
	def get(self, request):
		print("\n 로그인 페이지")
		return render(request, "user/login.html")

	def post(self, request):
    		return render(request, "user/login.html")


class Join(APIView):

	def get(self, request):
		print("\n 회원가입 페이지")
		return render(request, "user/join.html")

	def post(self, request):
		return render(request, "user/join.html")
