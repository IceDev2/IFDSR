from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    path('pengumuman/', views.announcement_list, name='announcements'),
    path('pengumuman/<slug:slug>/', views.announcement_detail, name='announcement_detail'),

    path('anggota/', views.member_list, name='members'),

    path('album/', views.album_list, name='albums'),
    path('album/<int:pk>/', views.album_detail, name='album_detail'),

    path('dashboard/', views.dashboard, name='dashboard'),

    # Auth register
    path('accounts/register/', views.register, name='register'),

    # Forum
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/tulis/', views.forum_create, name='forum_create'),
    path('forum/<slug:slug>/', views.forum_detail, name='forum_detail'),
    path('forum/<slug:slug>/edit/', views.forum_edit, name='forum_edit'),
    path('forum/<slug:slug>/hapus/', views.forum_delete, name='forum_delete'),
]
