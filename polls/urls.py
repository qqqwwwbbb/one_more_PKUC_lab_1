from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.Register.as_view(), name='register'),
    path('<int:pk>/profile', views.Profile.as_view(), name='profile'),
    path('<int:pk>/delete_user', views.DeleteUser.as_view(), name='delete_user'),
    path('<int:pk>/update_user', views.UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
