from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('demo',views.demo,name="demo"),
    path('show',views.show,name="show"),
    path('',views.index,name="index"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)