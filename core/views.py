from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm, NewsletterForm
from .models import (
    FAQ, BlogCategory, BlogPost, Country, ForumCategory, Industry,
    JobPosition, KBArticle, News, Partner, ServiceCategory, Testimonial,
)


def home(request):
    context = {
        'categories': (ServiceCategory.objects.filter(is_active=True)
                       .prefetch_related('services')),
        'industries': Industry.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'payment_partners': Partner.objects.filter(is_active=True, kind='payments'),
        'cloud_partners': Partner.objects.filter(is_active=True, kind='cloud'),
        'client_logos': Partner.objects.filter(is_active=True, kind='client'),
        'countries': Country.objects.filter(is_active=True),
        'faqs': FAQ.objects.filter(is_active=True),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'index.html', context)


def services(request):
    context = {
        'categories': (ServiceCategory.objects.filter(is_active=True)
                       .prefetch_related('services')),
        'industries': Industry.objects.filter(is_active=True),
    }
    return render(request, 'services.html', context)


def about(request):
    context = {
        'countries': Country.objects.filter(is_active=True),
        'client_logos': Partner.objects.filter(is_active=True, kind='client'),
    }
    return render(request, 'about.html', context)


def careers(request):
    context = {'jobs': JobPosition.objects.filter(is_active=True)}
    return render(request, 'careers.html', context)


def newsroom(request):
    context = {'news_items': News.objects.filter(is_published=True)}
    return render(request, 'newsroom.html', context)


def blog(request):
    context = {
        'categories': BlogCategory.objects.all(),
        'posts': (BlogPost.objects.filter(is_published=True)
                  .select_related('category')),
    }
    return render(request, 'blog.html', context)


def knowledge_base(request):
    context = {
        'categories': ServiceCategory.objects.filter(is_active=True),
        'articles': (KBArticle.objects.filter(is_published=True)
                     .select_related('category')),
    }
    return render(request, 'knowledge_base.html', context)


def community(request):
    context = {'forum_categories': ForumCategory.objects.all()}
    return render(request, 'community.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Your message is in. Our team replies within "
                "one business day.")
            return redirect('contact')
    else:
        form = ContactForm()
    context = {
        'form': form,
        'countries': Country.objects.filter(is_active=True),
        'categories': ServiceCategory.objects.filter(is_active=True),
    }
    return render(request, 'contact.html', context)


@require_POST
def newsletter_subscribe(request):
    """Hero / footer email capture. Works as normal POST or fetch()."""
    form = NewsletterForm(request.POST)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if form.is_valid():
        try:
            form.save()
            msg = "You're in! We'll be in touch shortly."
            ok = True
        except IntegrityError:
            msg = "You're already on the list — talk soon."
            ok = True
    else:
        msg = "Please enter a valid email address."
        ok = False

    if is_ajax:
        return JsonResponse({'ok': ok, 'message': msg})
    messages.success(request, msg) if ok else messages.error(request, msg)
    return redirect(request.POST.get('next') or 'home')
