from django.db import models
from random import shuffle


cards = ['Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh',
         'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd',
         'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks',
         'Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc']



class Room(models.Model):
    roomID = models.CharField(max_length=10)
    
    def __str__(self):
        return self.roomID
    
        

class Table(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, default=None)
    sb = models.PositiveIntegerField()
    bb = models.PositiveIntegerField()
    buttonPosition = models.PositiveSmallIntegerField()
    stage = models.CharField(max_length=8, default='preflop')  #should be one of 'preflop', 'flop', 'turn', 'river' or 'showdown'
    pot = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.buttonPosition:
            self.buttonPosition = 1
        super(Table, self).save(*args, **kwargs)
        
        

class Player(models.Model):
    username = models.CharField(max_length=15)
    stackSize = models.PositiveIntegerField()
    folded = models.BooleanField(default=False)
    shoved = models.BooleanField(default=False)
    betThisRound = models.IntegerField(default=0)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=None, null=True)
    
    def __str__(self):
        return self.username
    
    

class Deck(models.Model):
    table = models.OneToOneField(Table, on_delete=models.CASCADE, default=None)
    
    def save(self, *args, **kwargs):
        shuffledDeck = cards.copy()
        shuffle(shuffledDeck)
        for i in range(52):
            setattr(self, 'card'+str(i+1), shuffledDeck[i])
        super(Deck, self).save(*args, **kwargs)



for i in range(52):
    Deck.add_to_class('card'+str(i+1), models.CharField(max_length=2))
    
for i in range(8):
    Table.add_to_class('player'+str(i+1), models.OneToOneField(Player, on_delete=models.CASCADE, default=None, related_name='player'+str(i+1), null=True))