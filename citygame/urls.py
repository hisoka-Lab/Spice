from django.contrib import admin
from django.urls import path, include
from game.views import game_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('board.urls')),
    path('', game_view, name='game'),
]
