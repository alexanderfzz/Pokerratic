from django.shortcuts import render

def index(request):
    return render(request, 'game/index.html')

def room(request, roomID):
    context = {
        'roomID': roomID,
    }
    return render(request, 'game/room.html', context=context)