
#competitive highscores
#dynamic skill guides
#bank system
import math
class player:
	def __init__(self,name, skills):
		self.name   = name.strip("\n")
		self.skills = skills
		self.rawxp = 0
		for i in self.skills:
			self.rawxp += self.makeXPRaw(i[0],i[1])
	def makeXPRaw(self, prestige, xp):
		return ((2**prestige)*xp)+((2**prestige-1)*200000000)
	def returnSkill(self,skill):
		skillls = {"prayer" : 5,"cooking" : 7,"woodcutting" : 8, "fletching" : 9, "fishing" : 10, "firemaking" : 11, "crafting" : 12, "smithing" : 13, "mining" : 14, "herblore" : 15, "agility" : 16, "thieving" : 17, "farming" : 19, "runecrafting" : 20, "hunter" : 21, "construction" : 22, "summoning" : 23}
		return self.skills[skillls[skill]][0],self.skills[skillls[skill]][1]
	def remainingxp(self, skill, xp=200000000):
		
		skillls = {"prayer" : 5,"cooking" : 7,"woodcutting" : 8, "fletching" : 9, "fishing" : 10, "firemaking" : 11, "crafting" : 12, "smithing" : 13, "mining" : 14, "herblore" : 15, "agility" : 16, "thieving" : 17, "farming" : 19, "runecrafting" : 20, "hunter" : 21, "construction" : 22, "summoning" : 23}		
		if skill in skillls:
			rawxp = self.makeXPRaw(self.skills[skillls[skill]][0],self.skills[skillls[skill]][1])
			xpgoal = self.makeXPRaw(self.skills[skillls[skill]][0],xp)
			remainingfor200m = xpgoal-rawxp
			msg = "For **"+self.name+"** to get "+skill+" to "+format(xp,',d')+"\nCurrent xp and prestige: P"+ str(self.skills[skillls[skill]][0])+" "+format(self.skills[skillls[skill]][1],',d')+"XP\n"
			with open("skills/"+skill+".csv","r") as f:
				for l in f:
					li = l.split(";")
					item = li[0]
					xpx = int(li[1])
					msg += str(math.ceil(remainingfor200m/xpx))+" "+item+" are needed for "+format(xp,',d')+"\n"
			return msg