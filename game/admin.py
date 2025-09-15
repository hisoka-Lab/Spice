from django.contrib import admin
from .models import UserProfile, BarMessage, Dream, Quest, UserQuest, DrinkOrder

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'coins', 'level', 'experience', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username']

@admin.register(BarMessage)
class BarMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message_type', 'content', 'timestamp', 'is_active']
    list_filter = ['message_type', 'timestamp', 'is_active']
    search_fields = ['content', 'sender__username']

@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'dream_type', 'price', 'is_sold', 'created_at']
    list_filter = ['dream_type', 'is_sold', 'created_at']
    search_fields = ['title', 'description', 'seller__username']

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ['title', 'quest_type', 'reward_coins', 'reward_exp', 'is_active']
    list_filter = ['quest_type', 'is_active']
    search_fields = ['title', 'description']

@admin.register(UserQuest)
class UserQuestAdmin(admin.ModelAdmin):
    list_display = ['user', 'quest', 'is_completed', 'started_at', 'completed_at']
    list_filter = ['is_completed', 'started_at']
    search_fields = ['user__username', 'quest__title']

@admin.register(DrinkOrder)
class DrinkOrderAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'drink_type', 'recipient', 'created_at']
    list_filter = ['drink_type', 'created_at']
    search_fields = ['buyer__username', 'recipient__username']
