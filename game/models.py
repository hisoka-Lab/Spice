from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    """User profile for the game"""
    RANK_CHOICES = [
        ('newcomer', 'Newcomer 🌱'),
        ('regular', 'Regular 🍺'),
        ('connoisseur', 'Connoisseur 🥃'),
        ('master', 'Master 🍷'),
        ('legend', 'Legend 👑'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=400)  # Game currency
    character_x = models.IntegerField(default=400)  # Character X position
    character_y = models.IntegerField(default=300)  # Character Y position
    character_sprite = models.CharField(max_length=50, default='player.png')
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    bar_points = models.IntegerField(default=0)  # Bar points for ranking up
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='newcomer')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_rank_display_with_icon(self):
        rank_icons = {
            'newcomer': '🌱 Newcomer',
            'regular': '🍺 Regular',
            'connoisseur': '🥃 Connoisseur',
            'master': '🍷 Master',
            'legend': '👑 Legend',
        }
        return rank_icons.get(self.rank, '🌱 Newcomer')
    
    def update_rank(self):
        """Update rank based on points"""
        if self.bar_points >= 1000:
            self.rank = 'legend'
        elif self.bar_points >= 500:
            self.rank = 'master'
        elif self.bar_points >= 200:
            self.rank = 'connoisseur'
        elif self.bar_points >= 50:
            self.rank = 'regular'
        else:
            self.rank = 'newcomer'
        self.save()

    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.get_rank_display_with_icon()})"

class BarMessage(models.Model):
    """Messages in the bar"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bartender', 'Bartender'),
        ('system', 'System'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='user')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}"

class Dream(models.Model):
    """Dreams sold in the shop"""
    DREAM_TYPES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('adventure', 'Adventure'),
        ('love', 'Love'),
        ('mystery', 'Mystery'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    dream_type = models.CharField(max_length=20, choices=DREAM_TYPES)
    price = models.IntegerField()  # Price in coins
    is_sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bought_dreams')
    created_at = models.DateTimeField(auto_now_add=True)
    sold_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - ${self.price}"

class Quest(models.Model):
    """เควสในเกม"""
    QUEST_TYPES = [
        ('talk', 'คุยกับ NPC'),
        ('collect', 'เก็บของ'),
        ('explore', 'สำรวจ'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    quest_type = models.CharField(max_length=20, choices=QUEST_TYPES)
    reward_coins = models.IntegerField()
    reward_exp = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class UserQuest(models.Model):
    """เควสของผู้เล่น"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'quest']

    def __str__(self):
        return f"{self.user.username} - {self.quest.title}"

class DrinkOrder(models.Model):
    """การสั่งเหล้าในบาร์"""
    DRINK_TYPES = [
        # เบียร์ (ราคาจริง x 4)
        ('heineken', 'Heineken 🍺'),
        ('chang', 'ช้าง 🍺'),
        ('singha', 'สิงห์ 🍺'),
        ('leo', 'ลีโอ 🍺'),
        ('corona', 'Corona 🍺'),
        
        # วิสกี้
        ('johnnie_walker_red', 'Johnnie Walker Red 🥃'),
        ('johnnie_walker_black', 'Johnnie Walker Black 🥃'),
        ('jack_daniels', 'Jack Daniel\'s 🥃'),
        ('jameson', 'Jameson 🥃'),
        ('macallan_12', 'Macallan 12 🥃'),
        ('macallan_18', 'Macallan 18 🥃'),
        
        # ไวน์
        ('red_wine', 'Red Wine 🍷'),
        ('white_wine', 'White Wine 🍷'),
        ('champagne', 'Champagne 🥂'),
        ('prosecco', 'Prosecco 🥂'),
        
        # ค็อกเทล
        ('mojito', 'Mojito 🍹'),
        ('margarita', 'Margarita 🍹'),
        ('cosmopolitan', 'Cosmopolitan 🍹'),
        ('old_fashioned', 'Old Fashioned 🍹'),
        ('manhattan', 'Manhattan 🍹'),
        
        # เหล้าแรง
        ('vodka', 'Vodka 🍸'),
        ('gin', 'Gin 🍸'),
        ('rum', 'Rum 🍸'),
        ('tequila', 'Tequila 🍸'),
        
        # พรีเมี่ยม
        ('hennessy_xo', 'Hennessy XO 🥃'),
        ('remy_martin_xo', 'Remy Martin XO 🥃'),
        ('dom_perignon', 'Dom Pérignon 🥂'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    drink_type = models.CharField(max_length=30, choices=DRINK_TYPES)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_drinks', null=True, blank=True)
    message = models.TextField(blank=True)  # ข้อความที่ส่งมาพร้อมเหล้า
    created_at = models.DateTimeField(auto_now_add=True)

    def get_price(self):
        """ราคาเหล้าตามราคาจริง x 4 (1:4 ratio)"""
        prices = {
            # เบียร์ (60-120 บาท -> 15-30 เหรียญ)
            'heineken': 30,
            'chang': 20,
            'singha': 20,
            'leo': 16,
            'corona': 32,
            
            # วิสกี้ (800-8000 บาท -> 200-2000 เหรียญ)
            'johnnie_walker_red': 200,
            'johnnie_walker_black': 400,
            'jack_daniels': 300,
            'jameson': 350,
            'macallan_12': 800,
            'macallan_18': 2000,
            
            # ไวน์ (400-1200 บาท -> 100-300 เหรียญ)
            'red_wine': 120,
            'white_wine': 100,
            'champagne': 200,
            'prosecco': 160,
            
            # ค็อกเทล (200-400 บาท -> 50-100 เหรียญ)
            'mojito': 60,
            'margarita': 70,
            'cosmopolitan': 80,
            'old_fashioned': 90,
            'manhattan': 85,
            
            # เหล้าแรง (600-1000 บาท -> 150-250 เหรียญ)
            'vodka': 180,
            'gin': 200,
            'rum': 160,
            'tequila': 220,
            
            # พรีเมี่ยม (4000-12000 บาท -> 1000-3000 เหรียญ)
            'hennessy_xo': 2400,
            'remy_martin_xo': 2800,
            'dom_perignon': 3000,
        }
        return prices.get(self.drink_type, 20)
    
    def get_drink_info(self):
        """ข้อมูลเหล้า"""
        drink_info = {
            'heineken': {
                'name': 'Heineken',
                'alcohol': '5%',
                'origin': 'Netherlands',
                'description': 'Premium lager beer with a refreshing taste, popular worldwide'
            },
            'chang': {
                'name': 'Chang',
                'alcohol': '5%',
                'origin': 'Thailand',
                'description': 'Classic Thai beer with a smooth taste, perfect for hot weather'
            },
            'johnnie_walker_black': {
                'name': 'Johnnie Walker Black Label',
                'alcohol': '40%',
                'origin': 'Scotland',
                'description': 'Premium blended whisky aged 12 years with rich, complex flavors'
            },
            'macallan_18': {
                'name': 'The Macallan 18 Years',
                'alcohol': '43%',
                'origin': 'Scotland',
                'description': 'Legendary single malt whisky aged 18 years with luxurious character'
            },
            'mojito': {
                'name': 'Mojito',
                'alcohol': '10%',
                'origin': 'Cuba',
                'description': 'Refreshing cocktail with rum, mint, and lime, perfect for hot days'
            },
            'dom_perignon': {
                'name': 'Dom Pérignon',
                'alcohol': '12.5%',
                'origin': 'France',
                'description': 'Legendary champagne, symbol of luxury and success'
            }
        }
        return drink_info.get(self.drink_type, {
            'name': self.get_drink_type_display(),
            'alcohol': 'N/A',
            'origin': 'N/A',
            'description': 'Quality alcoholic beverage'
        })

    def __str__(self):
        return f"{self.buyer.username} สั่ง {self.get_drink_type_display()}"
