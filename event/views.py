from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages

from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.shortcuts import render
from .models import Event
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from datetime import date
from .forms import ContactForm

def event_list(request):
    event = Event.objects.first()
    return redirect('event:event_detail', id=event.id)

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    event_list = Event.objects.prefetch_related('category').all()
    title = request.GET.get('title', '')
    if title:
        event_list = event_list.filter(title__icontains=title)

    # pagination
    paginator = Paginator(event_list, 2)
    page = request.GET.get('page', 1)
    try:
        event_list = paginator.page(page)
    except PageNotAnInteger:
        event_list = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'event/event_detail.html', {'event': event, 'event_list': event_list, 'title': title, })


def contact(request):
    form = ContactForm
    if request.method == 'POST':
        form = form(request.POST)
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        email_message = '{lastname}{firstname} 님 / {email}  아래의 메세지를 보내주셨습니다. 가능한 빨리 답장 드리겠습니다.: .'.format(
                lastname=lastname, firstname=firstname, email=email
            )
        email_message += "\n\n{0}".format(message)
            #send_mail(message, email_message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        try:
            send_mail(
                        firstname,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False
                        )
            confirm_message = '연락 감사합니다. 가능한 빨리 답장 드리겠습니다.'
            messages.success(request, confirm_message)

        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('event:contact')

    else:
        pass
    return render(request, 'event/contact.html', {'form': form})


def send_email(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        send_mail('subject goes here', 'Message goes here', settings.EMAIL_HOST_USER, [email], fail_silently=False )
        return HttpResponse('Handling Post ' + email)
    return render(request, 'event/send_email.html')
