from django.contrib import admin
from django.urls import path, include
from . import views, settings
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # 앱이름,
    # path('admin/', admin.site.urls),
    # path('content/upload', views.UploadFeed.as_view())
    path('', views.MainFeed.as_view(), name='main'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)