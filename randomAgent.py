import gym
import random

env = gym.make('Blackjack-v0')

totalPlays = 10000
wins = 0 # keep track of number of wins
losses = 0 # keep track of number of losses
ties = 0 # keep track of number of ties
naturals = 0 # keep track of number of natural blackjacks

for i in range (totalPlays):
	done = False   #re-initialize to false each iteration for each play

	iteration = 1  # used to determine natural blackJack

	while(done is False):
		action = random.randint(0, 1)

		move = env.step(action) # 0 = stay, 1 = hit

		if(move[2] == True):   #move[2] is done value
			done = True

			if (move[2] == True):  # move[2] is done value
				done = True
				if (move[1] == 1):  # move[1] hold the reward value
					wins += 1.00  # if > 0 then agent has won
				elif (move[1] == 0):
					ties += 1.00
				else:
					losses += 1.00

			if (iteration == 1 and action == 0 and move[0][0] == 21):
				naturals += 1.00

		iteration += 1

		env.reset()
		iteration = 1  # reset iteration for each hand

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