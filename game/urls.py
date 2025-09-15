from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('bar/', views.bar_view, name='bar'),
    path('bar/send/', views.send_message, name='send_message'),
    path('bar/buy-drink/', views.buy_drink, name='buy_drink'),
    path('dreams/', views.dream_shop, name='dream_shop'),
    path('dreams/sell/', views.sell_dream, name='sell_dream'),
    path('dreams/buy/<int:dream_id>/', views.buy_dream, name='buy_dream'),
    path('map/', views.game_map, name='map'),
    path('map/move/', views.move_character, name='move_character'),
    path('quests/', views.quest_board, name='quest_board'),
    path('quest/<int:quest_id>/complete/', views.complete_quest, name='complete_quest'),
]