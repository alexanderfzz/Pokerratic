from asgiref.sync import async_to_sync

def putInChips(self, amount):
    self.playerDBEntry.stackSize -= amount
    self.playerDBEntry.betThisRound += amount
    data = {'type': 'gameActionComplete', 
            'position': str(self.relativePosToButton), 
            'amount': str(amount),
            'folded': 'False', 
            'shoved': 'False'}
    if self.playerDBEntry.stackSize == 0:
        self.playerDBEntry.shoved = True
        data['shoved'] = 'True'
    self.playerDBEntry.save()
    
    async_to_sync(self.channel_layer.group_send) (
        self.roomGroupID, data)


def raiseChips(self, amount, latestBet, latestBetDelta):
    pass

def callChips(self, amount):
    pass

def fold(self):
    pass

def isLegalRaise(self, amount, latestBet, latestBetDelta):
    pass

def createSidePot(self):
    pass

def paySmallBlind(self):
    payable = max(self.tableDBEntry.sb, self.playerDBEntry.stackSize)
    self.playerDBEntry.stackSize -= payable
    self.tableDBEntry.pot += payable
    data = {'type': 'gameActionComplete', 
            'currentAction': 'paySmall',
            'amount': str(payable),
            'folded': 'False',
            'shoved': 'False'}
    self.playerDBEntry.betThisRound = payable
    if self.playerDBEntry.stackSize==0:
        data['shoved'] = 'True'
        self.playerDBEntry.shoved = False
    self.playerDBEntry.save()
    self.tableDBEntry.save()
    async_to_sync(self.channel_layer.group_send) (self.roomGroupID, data)
    

def payBigBlind(self):
    self.playerDBEntry.stackSize -= self.tableDBEntry.bb
    self.tableDBEntry.pot += self.tableDBEntry.bb
    self.playerDBEntry.save()
    self.tableDBEntry.save()