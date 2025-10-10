from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'newsapi'

urlpatterns = [
    # Main endpoint to trigger news refresh (web view)
    path('', views.trigger_news_refresh, name='trigger_refresh'),
    
    # API endpoints
    path('api/', views.NewsListAPIView.as_view(), name='news_list'),
    path('api/refresh/', views.refresh_news, name='refresh_news'),
    
    # Legacy support (deprecated)
    path('api/legacy/', views.all_news.as_view(), name='legacy_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)