from django.contrib import admin

from .models import Room, Deck, Table, Player

listOfModels = [Room, Deck, Table, Player]

admin.site.register(listOfModels)