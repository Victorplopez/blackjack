#odds to receive 1 -> 9 in deck = 1/13 or 7.692307692% in our simple variation
#odds to receive 10 in deck = 4/13 or 30.769230769%

import gym
import random

env = gym.make('Blackjack-v0')

totalPlays = 10000
wins = 0 # keep track of number of wins
losses = 0 # keep track of number of losses
ties = 0 # keep track of number of ties
naturals = 0 # keep track of number of natural blackjacks

def runSimulation(seed, action):

	obs = env._get_obs()
	finished = False
	env.seed(seed)
	env.reset()
	value = 0 #initialize

	sum = obs[0]
	prob = 1 #initialized to 1

	while (finished is False):

		move = env.step(action)

		if(action == 1): #only needed for hit action
			diff = move[0][0] - sum
			if(diff == 10):
				prob = .30769230769
			else:
				prob = .07692307692

		if (move[2] == True):  # move[2] is done value
			finished = True
			if (move[1] == 1):  # move[1] hold the reward value
				value = 1.00 * prob # if > 0 then agent has won
			elif (move[1] == 0):
				value = 0
			else:
				value = -1.00 * prob

		else:
			action = 0

	return value

for i in range (totalPlays):
	done = False   #re-initialize to false each iteration for each play

	iteration = 1 # used to determine natural blackJack
	reward = 0 #initialize reward to 0

	while(done is False):

		mySeed = random.randint(0, 100000)

		env.seed(mySeed)
		env.reset()

		if (runSimulation(mySeed, 0) >= runSimulation(mySeed, 1)):
			action = 0

		else:
			action = 1

		env.seed(mySeed)
		env.reset()

		realMove = env.step(action)

		if(realMove[2] == True):   #move[2] is done value
			done = True
			if (realMove[1] == 1):  # move[1] hold the reward value
				wins += 1.00  # if > 0 then agent has won
			elif (realMove[1] == 0):
				ties += 1.00
			else:
				losses += 1.00

			if (iteration == 1 and action == 0 and realMove[0][0] == 21):
				naturals += 1.00

		iteration += 1
	
		env.reset()
		iteration = 1 #reset iteration for each hand
		
winRate = (wins/totalPlays) * 100
tieRate = (ties/totalPlays) * 100
lossRate = (losses/totalPlays) * 100

print "Total Plays: ", totalPlays
print "-------------"
print "Wins: ", wins, "| Win Rate: ", winRate
print "Natural BlackJacks: ", naturals
print " "
print "Ties: ", ties, "| Tie Rate: ", tieRate
print " "
print "Losses: ", losses, "| Loss Rate: ", lossRate