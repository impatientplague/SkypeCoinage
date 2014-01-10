import pickledb

class Coolpoints(object):
    def __init__(self, name, coins):
        self.name = name
        self.coins = coins
        self.db = pickledb.load('coinage.db', False)
        self.balance = self.db.get(self.name)

    def register(self):
        self.db.set(self.name, self.coins)
        self.db.dump()
    
    def addcoin(self, num):
        num2 = self.db.get(self.name)
        addit = num + num2
        self.db.set(self.name, addit)
        print self.db.get(self.name)
        self.db.dump()
    
    def givecoin(self, rev, amount):
        g = self.db.get(self.name)
        r = self.db.get(rev)
        if g > 1:
            a = self.db.get(self.name)
            sub = a - amount
            self.db.set(self.name, sub)
            self.db.set(rev, amount)
            self.db.dump()
        else:
            print 'you do not have enough cool points'


