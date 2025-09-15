from django.core.management.base import BaseCommand
from game.models import Quest

class Command(BaseCommand):
    help = 'สร้างข้อมูลเริ่มต้นสำหรับเกม'

    def handle(self, *args, **options):
        # สร้างเควสเริ่มต้น
        quests = [
            {
                'title': 'Guild Initiation',
                'description': 'Complete your first mission for the Adventurer\'s Guild. Talk to 3 different NPCs in the city.',
                'quest_type': 'talk',
                'reward_coins': 100,
                'reward_exp': 50,
            },
            {
                'title': 'Merchant\'s Request',
                'description': 'Help the traveling merchant by delivering a package to the blacksmith.',
                'quest_type': 'collect',
                'reward_coins': 75,
                'reward_exp': 35,
            },
            {
                'title': 'Find the Lost Cat',
                'description': 'A cat has gone missing! Search around the city and bring it back to its owner.',
                'quest_type': 'collect',
                'reward_coins': 50,
                'reward_exp': 25,
            },
            {
                'title': 'City Patrol',
                'description': 'Help the town guard by patrolling the main roads and reporting any suspicious activity.',
                'quest_type': 'explore',
                'reward_coins': 80,
                'reward_exp': 40,
            },
            {
                'title': 'Ancient Mystery',
                'description': 'The old sage needs help deciphering ancient texts. Visit the temple and gather information.',
                'quest_type': 'explore',
                'reward_coins': 120,
                'reward_exp': 60,
            },
            {
                'title': 'Rare Materials',
                'description': 'The blacksmith needs special ores for crafting. Explore the city outskirts to find them.',
                'quest_type': 'collect',
                'reward_coins': 90,
                'reward_exp': 45,
            },
        ]

        for quest_data in quests:
            quest, created = Quest.objects.get_or_create(
                title=quest_data['title'],
                defaults=quest_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'สร้างเควส "{quest.title}" เรียบร้อย')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'เควส "{quest.title}" มีอยู่แล้ว')
                )

        self.stdout.write(
            self.style.SUCCESS('สร้างข้อมูลเริ่มต้นเสร็จสิ้น!')
        )