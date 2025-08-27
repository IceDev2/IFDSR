from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class SiteSetting(models.Model):
    nama_kelas = models.CharField(max_length=100)
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    deskripsi_singkat = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Pengaturan Situs'
        verbose_name_plural = 'Pengaturan Situs'

    def __str__(self):
        return self.nama_kelas


class Announcement(models.Model):
    judul = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    isi = models.TextField()
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    gambar_header = models.ImageField(upload_to='pengumuman/', blank=True, null=True)

    class Meta:
        ordering = ['-tanggal_upload']
        verbose_name = 'Pengumuman'
        verbose_name_plural = 'Pengumuman'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.judul)[:50] or 'pengumuman'
            candidate = base
            i = 1
            while Announcement.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[self.slug])

    def __str__(self):
        return self.judul


class Member(models.Model):
    nama = models.CharField(max_length=120)
    foto = models.ImageField(upload_to='anggota/', blank=True, null=True)
    bio_singkat = models.CharField(max_length=200, blank=True)
    jabatan = models.CharField(max_length=120, blank=True)
    instagram = models.URLField(blank=True)
    quote = models.CharField(max_length=200, blank=True)
    urutan = models.PositiveIntegerField(default=0, help_text='Untuk sorting tampilan')

    class Meta:
        ordering = ['urutan', 'nama']
        verbose_name = 'Anggota'
        verbose_name_plural = 'Anggota'

    def __str__(self):
        return self.nama


class Album(models.Model):
    nama = models.CharField(max_length=140)
    deskripsi = models.TextField(blank=True)
    tanggal_acara = models.DateField()
    cover = models.ImageField(upload_to='album_cover/', blank=True, null=True)

    class Meta:
        ordering = ['-tanggal_acara']
        verbose_name = 'Album Foto'
        verbose_name_plural = 'Album Foto'

    def get_absolute_url(self):
        return reverse('album_detail', args=[self.pk])

    def __str__(self):
        return f"{self.nama} ({self.tanggal_acara})"


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='foto')
    gambar = models.ImageField(upload_to='album_foto/')
    caption = models.CharField(max_length=200, blank=True)
    diupload = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-diupload']
        verbose_name = 'Foto'
        verbose_name_plural = 'Foto'

    def __str__(self):
        return self.caption or f"Foto di {self.album.nama}"


# ===== Forum =====
class Post(models.Model):
    STATUS = (('published', 'Published'), ('draft', 'Draft'))

    judul = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    isi = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    gambar = models.ImageField(upload_to='forum/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='published')
    is_pinned = models.BooleanField(default=False)
    dibuat = models.DateTimeField(auto_now_add=True)
    diubah = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-dibuat']
        verbose_name = 'Post Forum'
        verbose_name_plural = 'Post Forum'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.judul)[:50] or 'post'
            candidate = base
            i = 1
            while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('forum_detail', args=[self.slug])

    def __str__(self):
        return self.judul


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='komentar')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isi = models.TextField()
    dibuat = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['dibuat']
        verbose_name = 'Komentar'
        verbose_name_plural = 'Komentar'

    def __str__(self):
        return f"Komentar oleh {self.author} di {self.post}"
