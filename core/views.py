from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse

from .models import (
    SiteSetting,
    Announcement,
    Member,
    Album,
    Post,
    Comment,
)
from .forms import PostForm, CommentForm


def landing(request):
    setting = SiteSetting.objects.first()
    pengumuman_terbaru = Announcement.objects.all()[:3]
    album_terbaru = Album.objects.all()[:6]

    # Kumpulkan item slider dari Album (cover) dan Pengumuman (gambar_header)
    albums = (
        Album.objects.exclude(cover__isnull=True)
        .exclude(cover="")
        .order_by("-tanggal_acara")[:6]
    )
    anns = (
        Announcement.objects.exclude(gambar_header__isnull=True)
        .exclude(gambar_header="")
        .order_by("-tanggal_upload")[:6]
    )

    slider_items = []
    for a in albums:
        slider_items.append(
            {
                "img_url": a.cover.url,
                "title": a.nama,
                "subtitle": a.tanggal_acara.strftime("%d %b %Y"),
                "url": getattr(a, "get_absolute_url", lambda: reverse("album_detail", args=[a.pk]))(),
            }
        )
    for p in anns:
        slider_items.append(
            {
                "img_url": p.gambar_header.url,
                "title": p.judul,
                "subtitle": p.tanggal_upload.strftime("%d %b %Y"),
                "url": getattr(p, "get_absolute_url", lambda: reverse("announcement_detail", args=[p.slug]))(),
            }
        )

    # Unik per URL dan batasi maksimal 6
    unique, seen = [], set()
    for it in slider_items:
        if it["img_url"] and it["url"] not in seen:
            unique.append(it)
            seen.add(it["url"])
        if len(unique) >= 6:
            break

    return render(
        request,
        "core/landing.html",
        {
            "setting": setting,
            "pengumuman_terbaru": pengumuman_terbaru,
            "album_terbaru": album_terbaru,
            "slider_items": unique,
        },
    )


def announcement_list(request):
    items = Announcement.objects.all()
    return render(request, "core/announcements_list.html", {"items": items})


def announcement_detail(request, slug):
    item = get_object_or_404(Announcement, slug=slug)
    return render(request, "core/announcement_detail.html", {"item": item})


def member_list(request):
    items = Member.objects.all()
    return render(request, "core/members_list.html", {"items": items})


def album_list(request):
    items = Album.objects.all()
    return render(request, "core/albums_list.html", {"items": items})


def album_detail(request, pk):
    item = get_object_or_404(Album, pk=pk)
    return render(request, "core/album_detail.html", {"item": item})


@staff_member_required
def dashboard(request):
    return render(
        request,
        "core/dashboard.html",
        {
            "total_pengumuman": Announcement.objects.count(),
            "total_anggota": Member.objects.count(),
            "total_album": Album.objects.count(),
        },
    )


# ===== Auth =====
def register(request):
    if request.user.is_authenticated:
        messages.info(request, "Kamu sudah login.")
        return redirect("forum_list")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Registrasi berhasil. Silakan login.")
        return redirect("login")
    return render(request, "registration/register.html", {"form": form})


# ===== Forum =====
def forum_list(request):
    qs = Post.objects.filter(status="published")
    p = Paginator(qs, 10)
    page = request.GET.get("page")
    items = p.get_page(page)
    return render(request, "core/forum_list.html", {"items": items})


def forum_detail(request, slug):
    item = get_object_or_404(Post, slug=slug, status="published")
    komentar = item.komentar.filter(is_approved=True)
    form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = item
            c.author = request.user
            c.save()
            messages.success(request, "Komentar ditambahkan.")
            return redirect("forum_detail", slug=item.slug)

    return render(
        request,
        "core/forum_detail.html",
        {"item": item, "komentar": komentar, "form": form},
    )


@login_required
def forum_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        messages.success(request, "Post dibuat.")
        return redirect("forum_detail", slug=obj.slug)
    return render(request, "core/forum_form.html", {"form": form, "mode": "create"})


@login_required
def forum_edit(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if not (request.user.is_staff or obj.author_id == request.user.id):
        return HttpResponseForbidden("Tidak boleh mengedit post ini.")
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post diperbarui.")
        return redirect("forum_detail", slug=obj.slug)
    return render(
        request, "core/forum_form.html", {"form": form, "mode": "edit", "obj": obj}
    )


@login_required
def forum_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if not (request.user.is_staff or obj.author_id == request.user.id):
        return HttpResponseForbidden("Tidak boleh menghapus post ini.")
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Post dihapus.")
        return redirect("forum_list")
    return render(request, "core/forum_delete_confirm.html", {"obj": obj})
