import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from collections import defaultdict

from .models import Room, Deck, Table, Player
from . import commands



class RoomConsumer(WebsocketConsumer):
    
    connectedUsersCount = defaultdict(lambda: 0)
    playerAtTable = defaultdict(lambda: 0)

    
    commands = {
        'sit': commands.sitAtTable,
        'globalChat': commands.globalMessages,
        'newGame': commands.shuffleAndDeal,
        #temporary
        'dealFlop': commands.dealFlop,
        'dealTurn': commands.dealTurn,
        'dealRiver': commands.dealRiver,
    }
    
    
    def connect(self):
        self.roomID = self.scope['url_route']['kwargs']['roomID']
        self.roomGroupID = 'room_{}'.format(self.roomID)
        
        async_to_sync(self.channel_layer.group_add) (
            self.roomGroupID, self.channel_name
        )
             
        self.accept()
        
        
        rooms = Room.objects.filter(roomID=self.roomID)
        if len(rooms) != 0:
            self.roomDBEntry = rooms[0]
            self.tableDBEntry = Table.objects.filter(room=self.roomDBEntry)[0]
            decks = Deck.objects.filter(table=self.tableDBEntry)
            self.deckDBEntry = None if len(decks)==0 else decks[0]
            print('room found')
        else:
            self.roomDBEntry = Room.objects.create(roomID=self.roomID)
            self.tableDBEntry = Table.objects.create(room=self.roomDBEntry, sb=5, bb=5)
            self.deckDBEntry = None
            print('room created')

        
        RoomConsumer.connectedUsersCount[self.roomID] += 1
        
    
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard) (
            self.roomGroupID, self.channel_name
        )
        RoomConsumer.connectedUsersCount[self.roomID] -= 1
        # todo: also need to somehow remove the playerDBEntry from the table
        
        if RoomConsumer.connectedUsersCount[self.roomID] == 0:
            self.roomDBEntry.delete()
        self.close()


    
    def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
        self.commands[command](self, data)
        
        
        
    
    
    
    
    
    
    
    def chatMessage(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps(
            {'command': 'receivedGlobalMessage', 
             'message': message}))
        
        
    def newGame(self, event):
        # change the data serializing method later
        self.playerDBEntry.folded = False
        self.playerDBEntry.shoved = False
        self.playerDBEntry.betThisRound = 0
        self.playerDBEntry.save()
        self.latestBet = 0
        self.latestBetDelta = self.tableDBEntry.bb
        self.deckDBEntry = Deck.objects.filter(table=self.tableDBEntry)[0]
        if self.seatNumber != -1:
            self.position = event['player'+str(self.seatNumber)]
            holeCard1 = getattr(self.deckDBEntry, 'card'+str(self.position))
            holeCard2 = getattr(self.deckDBEntry, 'card'+str(self.position+8))
            holecardsHand = holeCard1+" "+holeCard2
            self.send(text_data=json.dumps(
                {'command': 'receivedHoleCards',
                'message': holecardsHand}
            ))


            
    
    def dealFlop(self, event):
        self.playerDBEntry.betThisRound = 0
        self.playerDBEntry.save()
        self.latestBet = 0
        self.latestBetDelta = 0
        flop = 'flop: '+getattr(self.deckDBEntry, 'card18')+" "+getattr(self.deckDBEntry, 'card19')+" "+getattr(self.deckDBEntry, 'card20')
        self.send(text_data=json.dumps(
            {'command': 'receivedFlop', 
             'message': flop}))
        
    
    def dealTurn(self, event):
        self.playerDBEntry.betThisRound = 0
        self.playerDBEntry.save()
        self.latestBet = 0
        self.latestBetDelta = 0
        turn = 'turn: '+getattr(self.deckDBEntry, 'card22')
        self.send(text_data=json.dumps(
            {'command': 'receivedTurn',
             'message': turn}
        ))
    
    
    def dealRiver(self, event):
        self.playerDBEntry.betThisRound = 0
        self.playerDBEntry.save()
        self.latestBet = 0
        self.latestBetDelta = 0
        river = 'river: '+getattr(self.deckDBEntry, 'card24')
        self.send(text_data=json.dumps(
            {'command': 'receivedTurn',
             'message': river}
        ))
