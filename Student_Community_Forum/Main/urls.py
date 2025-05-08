from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin_view, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('discussion/', views.discussion, name='discussion'),
    path('groupchat/', views.groupchat, name='groupchat'),
    path('settings/', views.settings,name='settings'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/create/', views.creatediscussion, name='creatediscussion'),
    path('groupchat/join/<int:groupchat_id>/', views.join_groupchat, name='join_groupchat'),
    path('groupchat/<int:groupchat_id>/', views.groupchat_room, name='groupchat_room'),
    path('groupchat/create/', views.create_groupchat, name='create_groupchat'),
    path('groupchat/<int:groupchat_id>/leave/', views.leave_groupchat, name='leave_groupchat'),
    path('groupchat/<int:groupchat_id>/delete/', views.delete_groupchat, name='delete_groupchat'),
    path('groupchat/join/<int:groupchat_id>/', views.join_groupchat, name='join_groupchat'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)