from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register_view, name='register'),
    path('search', views.search, name='search'),
    path('today', views.today, name='today'),
    path('save', views.save, name='save'),
    path('records', views.records, name='records'),
    path('set', views.set, name='set'),
    path('recomendations', views.recomendations, name='recomendations'),
    path('bmi', views.bmi, name='bmi'),
    path('bmi_get', views.bmi_get, name='bmi_get'),
]