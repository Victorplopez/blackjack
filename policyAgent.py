import gym
import random

env = gym.make('Blackjack-v0')

totalPlays = 100000
wins = 0 # keep track of number of wins
losses = 0 # keep track of number of losses
ties = 0 # keep track of number of ties

for i in range (totalPlays):
    done = False   #re-initialize to false each iteration for each play
    
    while(done is False):
        sum,dealers,usableAce = env._get_obs()
			
        if not usableAce:
            if sum<=11 or (dealers>7 and sum<=16):
                move = env.step(1)
            else:
                move = env.step(0)
        else:       #Doesnt have usable ace
            if sum<=18:
                move=env.step(1)
            else:
                move=env.step(0)
			
        if (move[2] == True):  # move[2] is done value
            done = True
            if(move[1] == 1):  # move[1] hold the reward value
            	wins += 1.00  # if > 0 then agent has won
            elif(move[1] == 0):
				ties += 1.00
            else:
				losses += 1.00

        env.reset()

winRate = (wins/totalPlays) * 100
tieRate = (ties/totalPlays) * 100
lossRate = (losses/totalPlays) * 100

print "Total Plays: ", totalPlays
print "-------------"
print "Wins: ", wins, "| Win Rate: ", winRate
print " "
print "Ties: ", ties, "| Tie Rate: ", tieRate
print " "
print "Losses: ", losses, "| Loss Rate: ", lossRate