import json
from asgiref.sync import async_to_sync

from .models import Room, Deck, Table, Player


def sitAtTable(self, data):
    # stackSize = data['stackSize']
    stackSize = 5000
    seatNumber = data['seatNumber']
    
    #TODO: change the username to what the frontend returns
    self.playerDBEntry = Player.objects.create(username='ahahahahaha', stackSize=stackSize, table=self.tableDBEntry)
    
    if getattr(self.tableDBEntry, 'player'+str(seatNumber)) == None:
        setattr(self.tableDBEntry, 'player'+str(seatNumber), self.playerDBEntry)
        self.tableDBEntry.save()
        self.seatNumber = seatNumber
        
    else:
        self.send(text_data=json.dumps(
            {'command': 'systemMessage', 
             'message': 'Seat taken'}))

    
def globalMessages(self, data):
    async_to_sync(self.channel_layer.group_send) (
        self.roomGroupID, {'type': 'chatMessage', 'message': data['message']}
    )
    
    

def shuffleAndDeal(self, data):
    self.tableDBEntry = Table.objects.filter(room=self.roomDBEntry)[0]
    self.tableDBEntry.buttonPosition += 1
    
    # update button position
    for i in range(8):
        position = str((int(self.tableDBEntry.buttonPosition)+i-1)%8+1)
        if getattr(self.tableDBEntry, 'player'+position) != None:
            self.tableDBEntry.buttonPosition = position
            self.tableDBEntry.save()
            break
    else:
        self.send(text_data=json.dumps(
            {'command': 'systemMessage', 
             'message': 'There are no players'}))
        return
    
    
    playersInGame = {}
    
    
    counter = 1
    for i in range(8):
        position = str((int(self.tableDBEntry.buttonPosition)+i)%8+1)
        player = getattr(self.tableDBEntry, 'player'+position)
        if player != None:
            playersInGame['player'+position] = counter
            counter += 1
            print(counter)
    
            
    
    if (len(playersInGame) == 1) or (len(playersInGame) == 2):
        self.send(text_data=json.dumps(
            {'command': 'systemMessage', 
             'message': "Needs at least 3 players"}))
        return
    
    
    playersInGame['type'] = 'newGame'
    
    
    if self.deckDBEntry != None:
        self.deckDBEntry.delete()
    self.deckDBEntry = Deck.objects.create(table=self.tableDBEntry)
    self.tableDBEntry.stage = 'preflop'
    self.tableDBEntry.pot = 0
    self.tableDBEntry.save()
    async_to_sync(self.channel_layer.group_send) (
        self.roomGroupID, playersInGame
    )
    
    
    
def dealFlop(self, data):
     async_to_sync(self.channel_layer.group_send) (
        self.roomGroupID, {'type': 'dealFlop'}
    )

def dealTurn(self, data):
     async_to_sync(self.channel_layer.group_send) (
        self.roomGroupID, {'type': 'dealTurn'}
    )

def dealRiver(self, data):
     async_to_sync(self.channel_layer.group_send) (
        self.roomGroupID, {'type': 'dealRiver'}
    )

