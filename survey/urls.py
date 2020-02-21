from django.urls import path, re_path
from . import views

app_name = 'survey'

urlpatterns = [
	
	path('', views.main_base_view, name='main_base'),
	path('survey/<link1>/<date_link>/', views.survey, name='survey'),
	path('list/',views.wilayah_list, name='wilayah_list'),
	path('new/',views.wilayah_create, name='wilayah_new'),
	path('edit/<int:pk>/',views.wilayah_update, name='wilayah_edit'),
	path('delete/<int:pk>/',views.wilayah_delete, name='wilayah_delete'),
	path('wilayah/', views.wilayah, name='wilayah'),
	path('login/', views.login, name='login'),
	path('signup/', views.signup, name='signup'),
	path('main/',views.main, name='main'),
	path('logout/', views.logout_view, name='logout')


] 