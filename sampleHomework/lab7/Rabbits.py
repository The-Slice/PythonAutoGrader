import sys
import random
import math

#rabbit class 
class Rabbit:

	#constructor
	def __init__(self, gender):
		self.gender = gender
		self.daysOld = 0
		self.litterSize = 0
		self.gestationRecoveryPeriod = 0
		
	#increases rabbits age by one day
	def increaseAge(self):
		self.daysOld = self.daysOld + 1
		
	#decreases recovery by one day
	def decreaseGestationRecoveryPeriod(self):
		self.gestationRecoveryPeriod = self.gestationRecoveryPeriod - 1
		
	#randomly picks a littersize for rabbit
	def findLitterSize(self):
		self.litterSize = random.randint(3,8)
		
	#randomly picks a gestation period 
	def findGestationPeriod(self):
		self.gestationRecoveryPeriod = random.randint(35,39)
		
#helper method that picks either male or female randomly 
def findGender():
	number = random.randint(0,1)
	
	if number == 0:
		gender = "m"
	else:
		gender = "f"
		
	return gender
	

#while loop runs 10 trials each 365 interations long representing one year

#number of trials
trials = 10

print("Starting with 3 female rabbits and 1 male rabbit all at 0 days of age, after 1 year:")

#total variables for avarage
totalMales = 0
totalFemales = 0
totalPopulation = 0

#list to hold each population of each trial
malesList = []
femalesList = []
populationList = []

trial = 0
while trial < trials:

	# -- Start of Simulation --	
	
	#start population with one male and two female rabbits
	rabbitFather = Rabbit("m")
	rabbitMotherOne = Rabbit("f")
	rabbitMotherTwo = Rabbit("f")
	rabbitMotherThree = Rabbit("f")

	#rabbits list to hold all rabbits birthed in one year
	#babies list to hold new born rabbits each day and empty into rabbits list at the end of each day
	rabbits = [rabbitFather , rabbitMotherOne, rabbitMotherTwo, rabbitMotherThree]
	babies = []

	#population counter variables
	males = 1
	females = 3
	rabbitCount = 4

	day = 0
	while day < 365:
		
		#Iterate over each rabbit in list. If male then iterate over rabbit list again and look for available female
		#Otherwise, if original rabbit is female and available to breed, iterate over list and look for male. 
		#Lastly, if female is not available to breed, decrease her gestation period by one day and continue iteration 
		#over rabbit list
		
		for rabbit in rabbits:
			rabbit.increaseAge()
			
			if rabbit.gender == "f" and rabbit.daysOld >= 100 and rabbit.gestationRecoveryPeriod == 0:
				
				for nextRabbit in rabbits:
					
					if nextRabbit.gender == "m":
						
						#rabbits can mate so calculate littersize and gestation period
						rabbit.findLitterSize()
						rabbit.findGestationPeriod()
						
						#print("here littersize" + str(rabbit.litterSize))
						
						#for each baby in litter create baby, find its gender and add to babies list
						litter = 0
						while litter < rabbit.litterSize:
							baby = Rabbit(findGender())
							if baby.gender == "m":
								#iterate male population
								males = males + 1
							else:
								#iterate female population
								females = females + 1
							
							babies.append(baby)
							
							#iterate population
							rabbitCount = rabbitCount + 1
							
							litter = litter + 1
						
						break
				
				
			elif rabbit.gender == "f" and rabbit.gestationRecoveryPeriod > 0:
			
				#rabbit is pregnate female so decrease gestation period by one day
				rabbit.decreaseGestationRecoveryPeriod()
				
		#add babies to rabbit master list
		rabbits.extend(babies)

		#after babies have been added to master list, clear them from babies list
		babies.clear()
		
		#iterate day 
		day = day + 1
	
	#capture data for average and standard deviation
	malesList.append(males)
	totalMales = totalMales + males
	
	femalesList.append(females)
	totalFemales = totalFemales + females
	
	populationList.append(rabbitCount)
	totalPopulation = totalPopulation + rabbitCount
	
	print("Trial " + str(trial) + ": " + str(rabbitCount) + " rabbits, " + str(females) + " females and " + str(males) + " males.")
	
	trial = trial + 1
	
#mean of males population
averageTotalMales = totalMales / trials	

#mean of females population
averageTotalFemales = totalFemales / trials	

#mean of rabbit population
averageTotalPopulation = totalPopulation / trials	

#find standard deviation of male rabbit population
totalOfSquaresMale = 0
for items in malesList:
	totalOfSquaresMale = totalOfSquaresMale + ((items - averageTotalMales) ** 2)
	
meanOfSquaresMale = totalOfSquaresMale / trials
standardDeviationMales = math.sqrt(meanOfSquaresMale)

#find standard deviation of female rabbit population
totalOfSquaresFemale = 0
for items in femalesList:
	totalOfSquaresFemale = totalOfSquaresFemale + ((items - averageTotalFemales) ** 2)
	
meanOfSquaresFemale = totalOfSquaresFemale / trials
standardDeviationFemales = math.sqrt(meanOfSquaresFemale)

#find standard deviation of rabbit population
totalOfSquaresPopulation = 0
for items in populationList:
	totalOfSquaresPopulation = totalOfSquaresPopulation + ((items - averageTotalPopulation) ** 2)
	
meanOfSquaresPopulation = totalOfSquaresPopulation / trials
standardDeviationPopulation = math.sqrt(meanOfSquaresPopulation)
	
print("Average number of rabbits: " + str(totalPopulation / 10) + " with std of %.2f" % standardDeviationPopulation)
print("Average number of female rabbits: " + str(totalFemales / 10) + " with std of %.2f" % standardDeviationFemales)
print("Average number of male rabbits: " + str(totalMales / 10) + " with std of %.2f" % standardDeviationMales)
