from django.contrib import admin
from .models import SiteSetting, Announcement, Member, Album, Photo, Post, Comment

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('judul', 'admin', 'tanggal_upload')
    list_filter = ('tanggal_upload', 'admin')
    search_fields = ('judul', 'isi')
    prepopulated_fields = {"slug": ("judul",)}

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'urutan')
    list_editable = ('urutan',)
    search_fields = ('nama', 'jabatan')

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tanggal_acara')
    date_hierarchy = 'tanggal_acara'
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'caption', 'diupload')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('judul', 'author', 'status', 'is_pinned', 'dibuat')
    list_filter = ('status', 'is_pinned', 'dibuat')
    search_fields = ('judul', 'isi', 'author__username')
    prepopulated_fields = {"slug": ("judul",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'dibuat', 'is_approved')
    list_filter = ('is_approved', 'dibuat')
    search_fields = ('isi', 'author__username', 'post__judul')
