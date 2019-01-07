from django.conf import settings
from django.core import serializers
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import DeleteView

from accounts.models import Artist, Profile, Category, User
from .models import Work
from .forms import WorkForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.forms import modelformset_factory

def about_us(request):
    return render(request, 'artist/about_us.html')


def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, user_id=artist_id)
    works = Work.objects.filter(artist=artist_id).select_related('artist')
    return render(request, 'artist/artist_detail.html', {'artist': artist, 'works': works, })


def work_list(request):
    works = Work.objects.prefetch_related('category').all().select_related('artist')
    recent_works = works.order_by('-created_at')[:3]

    title = request.GET.get('title', '')
    if title:
        works = works.filter(title__icontains=title)

    artist_name = request.GET.get('artist_name', '')
    if artist_name:
        profiles = Profile.objects.filter(name__icontains=artist_name).select_related('user')
        works = []
        for profile in profiles:
            artist = Artist.objects.get(user=profile.user)
            works.extend(list(artist.work_set.all()))

    category_name = request.GET.get('category_name', '')
    categories = Category.objects.all()
    category = None
    if category_name:
        category = Category.objects.get(name__icontains=category_name)
        works = category.work_set.all().select_related('artist')

    tag = request.GET.get('tag', '')
    if tag:
        works = works.filter(tags__icontains=tag)

    count = len(works)

    # pagination
    page = request.GET.get('page')
    paginator = Paginator(works, 5)
    try:
        works = paginator.page(page)
    except PageNotAnInteger:
        works = paginator.page(1)
    except EmptyPage:
        works = paginator.page(paginator.num_pages)

    context = {
    'works': works, 'recent_works': recent_works,'count': count, 'title': title, 'tag': tag, 'artist_name': artist_name, 'category_name': category_name, 'categories':categories, 'category': category, }

    return render(request, 'artist/work_list.html', context)

def work_detail(request, id):
    work = get_object_or_404(Work, id=id)
    total_likes = work.total_likes()
    return render(request, 'artist/work_detail.html', {'work': work, 'total_likes': total_likes,})

@login_required
def like_work(request):
    work = get_object_or_404(Work, id=request.POST.get('work_id'))
    if request.user != work.artist.user:
        work.likes.add(request.user)
    return redirect(work.get_absolute_url())


def works_by_category(request, category):
    category = get_object_or_404(Category, name=category)
    works = category.work_set.all().select_related('artist')
    count = works.count()
    return render(request, 'artist/works_by_category.html', {'category': category, 'works': works, 'count': count,})


@login_required
def work_create(request, work=None):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        artist = get_object_or_404(Artist, user_id=request.user)
        category = get_object_or_404(Category, id=request.POST.get('category'))
        if form.is_valid():
            work = form.save(commit=False)
            work.artist = artist
            work.save()
            work.category.set = category
            form.save_m2m()
            messages.success(request, '새 작품을 저장했습니다.')
            return redirect(work)
    else:
        form = WorkForm()
    return render(request, 'artist/work_form.html', {'form': form, })

@login_required
def work_edit(request, id):
    work = get_object_or_404(Work, id=id)
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        artist = get_object_or_404(Artist, user_id=request.user)
        category = get_object_or_404(Category, id=request.POST.get('category'))

        if form.is_valid():
            work = form.save(commit=False)
            work.artist = artist
            work.save()
            work.category.set = category
            form.save_m2m()
            messages.success(request, '내용을 수정했습니다.')
            return redirect(work)
    else:
        form = WorkForm(instance=work)
    return render(request, 'artist/work_form.html', {'form': form,})



work_delete = DeleteView.as_view(model=Work, success_url=reverse_lazy('profile'))
