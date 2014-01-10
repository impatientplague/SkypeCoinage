from modules import *
import Skype4Py
import time
import pickledb

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
		self.db = pickledb.load('coinage.db', False)

	def RunFunction(self, Message, Status):
		if Status == 'SENT' or Status == 'RECEIVED':
			cmd = Message.Body.split(' ')[0]
			if cmd in self.functions.keys():
				self.context = Message
				self.functions[cmd](self)
			elif self.listen:
				self.ParseAnswer(Message, Message.Body)

	def PrintCommands(self):
		temp = 'Commands: '
		for item in self.functions.keys():
			temp += (item + ', ')
		self.context.Chat.SendMessage(temp[:-2])


	def ParseAnswer(self, Message, query):
		if query.lower() == self.currentAnswer.lower():
			try:
				self.scoreboard[Message.FromHandle] = int(self.scoreboard[Message.FromHandle]) + 1
			except KeyError:
				self.scoreboard[Message.FromHandle] = 1
			Message.Chat.SendMessage("/me {0}[{1}] is Correct! A: {2}".format(Message.FromHandle, str(self.scoreboard[Message.FromHandle]), self.currentAnswer))
			self.SaveScores()
			if self.mode == 'shuffle':
				self.SetShuffle()
			else:
				self.SetQuestion()
		else:
			pass

	def GetUser(self):
		self.context.Chat.SendMessage('/me ' + self.context.FromHandle)

	
	def Reg(self):	
		coin = coolpoints.Coolpoints(self.context.FromHandle, 100)
		coin.register()
		self.context.Chat.SendMessage("/me [Bank of CoolPoints]: " + self.context.FromHandle + " has successfully opened an account , here take this welcome package of [100CP]")
		
	def checkbal(self):
		coin = coolpoints.Coolpoints(self.context.FromHandle, '')
		bal = str(coin.balance)
		self.context.Chat.SendMessage("/me [Bank of CoolPoints]: " + self.context.FromHandle + " [Balance]: " + bal) 
		
	functions = {
	"!register":		Reg, 
	"!balance":             checkbal,
	"!commands":            PrintCommands,
	}

if __name__ == "__main__":
	Fuck = Coin()
	while True:
		time.sleep(1)