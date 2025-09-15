# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bar_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rank',
            field=models.CharField(
                choices=[
                    ('newcomer', 'มือใหม่ 🌱'),
                    ('regular', 'ลูกค้าประจำ 🍺'),
                    ('connoisseur', 'ผู้เชี่ยวชาญ 🥃'),
                    ('master', 'ปรมาจารย์ 🍷'),
                    ('legend', 'ตำนาน 👑'),
                ],
                default='newcomer',
                max_length=20
            ),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='coins',
            field=models.IntegerField(default=400),
        ),
        migrations.AlterField(
            model_name='drinkorder',
            name='drink_type',
            field=models.CharField(
                choices=[
                    ('heineken', 'Heineken 🍺'),
                    ('chang', 'ช้าง 🍺'),
                    ('singha', 'สิงห์ 🍺'),
                    ('leo', 'ลีโอ 🍺'),
                    ('corona', 'Corona 🍺'),
                    ('johnnie_walker_red', 'Johnnie Walker Red 🥃'),
                    ('johnnie_walker_black', 'Johnnie Walker Black 🥃'),
                    ('jack_daniels', 'Jack Daniel\'s 🥃'),
                    ('jameson', 'Jameson 🥃'),
                    ('macallan_12', 'Macallan 12 🥃'),
                    ('macallan_18', 'Macallan 18 🥃'),
                    ('red_wine', 'Red Wine 🍷'),
                    ('white_wine', 'White Wine 🍷'),
                    ('champagne', 'Champagne 🥂'),
                    ('prosecco', 'Prosecco 🥂'),
                    ('mojito', 'Mojito 🍹'),
                    ('margarita', 'Margarita 🍹'),
                    ('cosmopolitan', 'Cosmopolitan 🍹'),
                    ('old_fashioned', 'Old Fashioned 🍹'),
                    ('manhattan', 'Manhattan 🍹'),
                    ('vodka', 'Vodka 🍸'),
                    ('gin', 'Gin 🍸'),
                    ('rum', 'Rum 🍸'),
                    ('tequila', 'Tequila 🍸'),
                    ('hennessy_xo', 'Hennessy XO 🥃'),
                    ('remy_martin_xo', 'Remy Martin XO 🥃'),
                    ('dom_perignon', 'Dom Pérignon 🥂'),
                ],
                max_length=30
            ),
        ),
    ]