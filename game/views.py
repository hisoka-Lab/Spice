from django.shortcuts import render

def game_view(request):
    """Render the main game page."""
    return render(request, 'game/index.html')
