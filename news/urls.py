from django.urls import path  # Use 'path' for URL routing
from . import views  # Import views from the current app
from django.urls import re_path


urlpatterns = [
    path("news", views.NewsApi),  # create news
    path("news/<int:id>/", views.NewsApi),  # For GET (single news), PUT, and DELETE
    path("news/paginated/", views.PaginatedNewsApi),
    path("news/reactions", views.ReactionApi),
    path("news/statistics", views.StatisticsView),
    
    # For GET (single news), PUT, and DELETE
    # path('news/paginated/', views.NewsApi),  #  paginated for all and each tag
    # path('news/statistics/', views.NewsApi),  # New statistics
    # path('news/reactions/<int:id>/', views.NewsApi),  # Reactions => Like, dislike and view
]
