from django.shortcuts import render


def home(request):
    """Render the project homepage (templates/main.html)."""
    return render(request, 'main.html')
