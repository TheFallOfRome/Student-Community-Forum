from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('discussion/', views.discussion, name='discussion'),
    path('groupchat/', views.groupchat, name='groupchat'),
    path('signin/', views.signin, name='signin'),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)