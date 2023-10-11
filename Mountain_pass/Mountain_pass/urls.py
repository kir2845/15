from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Mountain_peaks import views


router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewset)
router.register(r'coordinates', views.CoordinateViewset)
router.register(r'levels', views.LevelViewset)
router.register(r'images', views.ImageViewset)
router.register(r'submitData', views.SubmitDataViewset)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]