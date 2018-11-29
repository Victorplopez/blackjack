import BlackJackEnviornment
import random

totalPlays = 10000
wins = 0 # keep track of number of wins
losses = 0 # keep track of number of losses
ties = 0 # keep track of number of ties
naturals = 0 # keep track of number of natural blackjacks
naturals = 0 # keep track of number of natural blackjacks
env = BlackJackEnviornment.BlackjackEnv()
for i in range (totalPlays):
    done = False   #re-initialize to false each iteration for each play

    iteration = 1  # used to determine natural blackJack
    randomCard = random.randint(1,10)

    env.set_dealers_hand(1, randomCard)
    env.set_players_hand(10,1)
    while(done is False):
        sum,dealers,usableAce = env._get_obs()

        move = env.step(0) #stay each time
        action = 0

        if (move[2] == True):  # move[2] is done value
            done = True
            if(move[1] == 1):  # move[1] hold the reward value
                wins += 1.00  # if > 0 then agent has won
            elif(move[1] == 0):
                ties += 1.00
            else:
                losses += 1.00

        if (iteration == 1 and action == 0 and move[0][0] == 21):
            naturals += 1.00

        env.reset()
        iteration = 1  # reset iteration for each hand

winRate = (wins/totalPlays) * 100
tieRate = (ties/totalPlays) * 100
lossRate = (losses/totalPlays) * 100
winPlusTieRate = winRate + tieRate

print "Total Plays: ", totalPlays
print "-------------"
print "Wins: ", wins, "| Win Rate: ", winRate
print "Natural BlackJacks: ", naturals
print " "
print "Ties: ", ties, "| Tie Rate: ", tieRate
print " "
print "Losses: ", losses, "| Loss Rate: ", lossRate
print " "
print "Win + Tie Rate: ", winPlusTieRate/100