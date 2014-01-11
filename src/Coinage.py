import Skype4Py
import time
import json
import coolpoints

with open('data/users.json') as f:
    db = json.load(f)
    
class Coin:
	def __init__(self):
		self.skype = Skype4Py.Skype()
		if self.skype.Client.IsRunning == False:
			self.skype.Client.Start()
		self.skype.Attach()
		self.skype.OnMessageStatus = self.RunFunction

		self.listen = False
		self.start = time.clock()
		self.mode = ''
		self.context = ''
		self.accounts = db['Accounts']
		self.listen = False

	def RunFunction(self, Message, Status):
		if Status == 'SENT' or Status == 'RECEIVED':
			cmd = Message.Body.split(' ')[0]
			if cmd in self.functions.keys():
				self.context = Message
				self.functions[cmd](self)
			elif self.listen:
				print self.ParseAnswer(Message, Message.Body)

	def PrintCommands(self):
		temp = 'Commands: '
		for item in self.functions.keys():
			temp += (item + ', ')
		self.context.Chat.SendMessage(temp[:-2])


	#def ParseAnswer(self, Message, query):
		#if query.lower() == self.currentAnswer.lower():
			#try:
				#self.scoreboard[Message.FromHandle] = int(self.scoreboard[Message.FromHandle]) + 1
			#except KeyError:
				#self.scoreboard[Message.FromHandle] = 1
			#Message.Chat.SendMessage("/me {0}[{1}] is Correct! A: {2}".format(Message.FromHandle, str(self.scoreboard[Message.FromHandle]), self.currentAnswer))
			#self.SaveScores()
			#if self.mode == 'shuffle':
				#self.SetShuffle()
			#else:
				#self.SetQuestion()
		#else:
			#pass

	def GetUser(self):
		self.context.Chat.SendMessage('/me ' + self.context.FromHandle)

	
	def Reg(self):
	    coin = coolpoints.Coolpoints(self.context.FromHandle, 100)
	    if not coin.check(self.context.FromHandle):
		coin.register()
		coin.dump()
		self.context.Chat.SendMessage("/me [Bank of CoolPoints]: " + self.context.FromHandle + " has successfully opened an account , here take this welcome package of [100CP]")
	    else:
		self.context.Chat.SendMessage("/me [Bank of CoolPoints]: " + self.context.FromHandle + " has already opened an account!")
	
	def checkbal(self):
		coin = coolpoints.Coolpoints(self.context.FromHandle, '')
		self.context.Chat.SendMessage("/me [Bank of CoolPoints]: " + self.context.FromHandle + " [Balance]: " + str(self.accounts[self.context.FromHandle])) 
		
	    
	functions = {
	"!register":		Reg, 
	"!balance":             checkbal,
	"!commands":            PrintCommands,
	}

if __name__ == "__main__":
	Fuck = Coin()
	while True:
		time.sleep(1)