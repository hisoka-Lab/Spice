from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import UserProfile, BarMessage, Dream, Quest, UserQuest, DrinkOrder
import json
import random

def index(request):
    """Main game page"""
    return render(request, 'game/index.html')

@login_required
def bar_view(request):
    """Bar page for chatting"""
    # Create UserProfile if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get latest 50 messages
    messages_list = BarMessage.objects.filter(is_active=True)[:50]
    
    context = {
        'profile': profile,
        'messages': messages_list,
    }
    return render(request, 'game/bar.html', context)

@login_required
def send_message(request):
    """Send message in the bar"""
    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if content:
            # Create user message
            BarMessage.objects.create(
                sender=request.user,
                message_type='user',
                content=content
            )
            
            # Random bartender response (if no one else is talking)
            recent_messages = BarMessage.objects.filter(
                timestamp__gte=timezone.now() - timezone.timedelta(minutes=1)
            ).count()
            
            if recent_messages <= 1:  # If only our message exists
                bartender_responses = [
                    "Hmm... that's interesting.",
                    "Sounds like you have quite a story.",
                    "Need another drink?",
                    "How's your day going?",
                    "You come here often?",
                    "Your story reminds me of another customer...",
                    "That's what I call a good tale.",
                    "Life's full of surprises, isn't it?",
                ]
                
                # Wait a moment then respond
                import time
                time.sleep(2)
                
                BarMessage.objects.create(
                    message_type='bartender',
                    content=random.choice(bartender_responses)
                )
    
    return redirect('game:bar')

@login_required
def dream_shop(request):
    """Dream shop interior for walking around and buying dreams"""
    profile = get_object_or_404(UserProfile, user=request.user)
    dreams = Dream.objects.filter(is_sold=False)
    
    context = {
        'profile': profile,
        'dreams': dreams,
    }
    return render(request, 'game/dream_shop_interior.html', context)

@login_required
def sell_dream(request):
    """Sell dream"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        dream_type = request.POST.get('dream_type')
        price = int(request.POST.get('price', 0))
        
        if title and description and price > 0:
            Dream.objects.create(
                seller=request.user,
                title=title,
                description=description,
                dream_type=dream_type,
                price=price
            )
            messages.success(request, 'Dream listed successfully!')
        else:
            messages.error(request, 'Please fill in all required fields')
    
    return redirect('game:dream_shop')

@login_required
def buy_dream(request, dream_id):
    """Buy dream"""
    dream = get_object_or_404(Dream, id=dream_id, is_sold=False)
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if profile.coins >= dream.price:
        # หักเหรียญ
        profile.coins -= dream.price
        profile.save()
        
        # เพิ่มเหรียญให้ผู้ขาย
        seller_profile, created = UserProfile.objects.get_or_create(user=dream.seller)
        seller_profile.coins += dream.price
        seller_profile.save()
        
        # อัพเดทสถานะฝัน
        dream.buyer = request.user
        dream.is_sold = True
        dream.sold_at = timezone.now()
        dream.save()
        
        messages.success(request, f'Purchased dream "{dream.title}" successfully!')
    else:
        messages.error(request, 'Not enough coins!')
    
    return redirect('game:dream_shop')

@login_required
def buy_drink(request):
    """ซื้อเหล้า"""
    if request.method == 'POST':
        drink_type = request.POST.get('drink_type')
        recipient_username = request.POST.get('recipient', '').strip()
        message = request.POST.get('message', '')
        
        profile = get_object_or_404(UserProfile, user=request.user)
        
        # สร้าง DrinkOrder object ชั่วคราวเพื่อคำนวณราคา
        temp_order = DrinkOrder(drink_type=drink_type)
        price = temp_order.get_price()
        
        if profile.coins >= price:
            recipient = None
            if recipient_username:
                try:
                    from django.contrib.auth.models import User
                    recipient = User.objects.get(username=recipient_username)
                except User.DoesNotExist:
                    messages.error(request, 'User not found')
                    return redirect('game:bar')
            
            # หักเหรียญ
            profile.coins -= price
            
            # Add bar points (more expensive drinks give more points)
            points_earned = max(1, price // 50)  # Every 50 coins = 1 point
            profile.bar_points += points_earned
            
            # Update rank
            old_rank = profile.rank
            profile.update_rank()
            
            profile.save()
            
            # Create drink order
            order = DrinkOrder.objects.create(
                buyer=request.user,
                drink_type=drink_type,
                recipient=recipient,
                message=message
            )
            
            # Create bar message
            drink_info = order.get_drink_info()
            if recipient:
                bar_message = f"{request.user.username} bought {drink_info['name']} for {recipient.username}"
                if message:
                    bar_message += f' with message: "{message}"'
            else:
                bar_message = f"{request.user.username} ordered {drink_info['name']}"
                if message:
                    bar_message += f' with message: "{message}"'
            
            BarMessage.objects.create(
                message_type='system',
                content=bar_message
            )
            
            # Notify if rank up
            if old_rank != profile.rank:
                messages.success(request, f'Congratulations! You ranked up to {profile.get_rank_display_with_icon()}!')
            
            messages.success(request, f'Ordered {drink_info["name"]} successfully! (+{points_earned} points)')
        else:
            messages.error(request, f'Not enough coins! Need ${price}')
    
    return redirect('game:bar')

@login_required
def game_map(request):
    """Bangkok night game map"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    available_quests = Quest.objects.filter(is_active=True)
    user_quests = UserQuest.objects.filter(user=request.user, is_completed=False)
    
    # Ensure character starts in valid position
    if profile.character_x < 10:
        profile.character_x = 600
    if profile.character_y < 220:
        profile.character_y = 400
    profile.save()
    
    context = {
        'profile': profile,
        'available_quests': available_quests,
        'user_quests': user_quests,
    }
    return render(request, 'game/map.html', context)

@login_required
def move_character(request):
    """Move character with bounds checking"""
    if request.method == 'POST':
        data = json.loads(request.body)
        x = data.get('x', 0)
        y = data.get('y', 0)
        
        # Constrain movement to map bounds
        x = max(10, min(1150, x))
        y = max(220, min(750, y))
        
        profile = get_object_or_404(UserProfile, user=request.user)
        profile.character_x = x
        profile.character_y = y
        profile.save()
        
        return JsonResponse({'status': 'success', 'x': x, 'y': y})
    
    return JsonResponse({'status': 'error'})

@login_required
def quest_board(request):
    """Quest board view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    available_quests = Quest.objects.filter(is_active=True)
    user_quests = UserQuest.objects.filter(user=request.user, is_completed=False)
    
    context = {
        'profile': profile,
        'available_quests': available_quests,
        'user_quests': user_quests,
    }
    return render(request, 'game/quest_board.html', context)

@login_required
def complete_quest(request, quest_id):
    """Complete quest"""
    quest = get_object_or_404(Quest, id=quest_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    
    user_quest, created = UserQuest.objects.get_or_create(
        user=request.user,
        quest=quest,
        defaults={'is_completed': True, 'completed_at': timezone.now()}
    )
    
    if not user_quest.is_completed:
        user_quest.is_completed = True
        user_quest.completed_at = timezone.now()
        user_quest.save()
        
        # ให้รางวัล
        profile.coins += quest.reward_coins
        profile.experience += quest.reward_exp
        
        # Level up
        if profile.experience >= profile.level * 100:
            profile.level += 1
            profile.experience = 0
            messages.success(request, f'Level up! You are now level {profile.level}')
        
        profile.save()
        
        messages.success(request, f'Quest "{quest.title}" completed! Received ${quest.reward_coins} and {quest.reward_exp} EXP')
    
    return redirect('game:map')
