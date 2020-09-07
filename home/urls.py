from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('review/',views.review, name='review'),
    path('approve/', views.approve, name='approve'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

]