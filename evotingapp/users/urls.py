from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'
urlpatterns = [
    path('available/', views.view_polls, name='view_polls'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/result/', views.results, name='results'),
    path('results/', views.all_result, name='all_result'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
