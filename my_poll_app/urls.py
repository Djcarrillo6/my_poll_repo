from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.reg, name='register'),
    path('login', views.log, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('create', views.create, name='create'),
    path('vote/<poll_id>', views.vote, name='vote'),
    path('results/<poll_id>', views.results, name='results'),
    path('delete/<poll_id>', views.delete_poll, name='delete'),
]
