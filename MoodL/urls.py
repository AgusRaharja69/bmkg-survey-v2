
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from survey.views import *

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', include('survey.urls')),
    path('survey/<link1>/<date_link>/', survey, name='survey'),
    path('list/', wilayah_list, name='wilayah_list'),
	path('new/', wilayah_create, name='wilayah_new'),
	path('edit/<int:pk>/', wilayah_update, name='wilayah_edit'),
	path('delete/<int:pk>/', wilayah_delete, name='wilayah_delete'),
    path('login/', login, name='login'),
    path('wilayah/', wilayah, name='wilayah'),
    path('signup/',signup, name='signup'),
    path('main/', main, name='main'),
    #path('logout/', logout_view, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)