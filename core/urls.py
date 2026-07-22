from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('newsroom/', views.newsroom, name='newsroom'),
    path('blog/', views.blog, name='blog'),
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    path('community/', views.community, name='community'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
