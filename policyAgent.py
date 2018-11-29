import BlackJackEnviornment

totalPlays = 99999

wins = 0 # keep track of number of wins
losses = 0 # keep track of number of losses
ties = 0 # keep track of number of ties
naturals = 0 # keep track of number of natural blackjacks
naturals = 0 # keep track of number of natural blackjacks

env = BlackJackEnviornment.BlackjackEnv()
for i in range (totalPlays):
    iteration=1
    done = False   #re-initialize to false each iteration for each play

    # if env.get_current_cash() <= 0:
    #     done = True

    env.reset()
    # env.set_players_hand(6,5)
    while(done is False):
        plays = i  # used to determine natural blackJack
        sum,dealers,usableAce,cash = env._get_obs()

        if not usableAce:
            if sum<=11 or (dealers>7 and sum<=16):
                move = env.step(1)
                action = 1

            else:
                move = env.step(0)
                action = 0

        else:       #Doesnt have usable ace
            if sum<=18:
                move=env.step(1)
                action = 1

            else:
                move=env.step(0)
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
        iteration += 1

        env.reset()
        iteration = 1  # reset iteration for each hand

winRate = (wins/plays) * 100
tieRate = (ties/plays) * 100
lossRate = (losses/plays) * 100
print(env.get_current_cash())
print("Total Plays: ", plays)
print("-------------")
print("Wins: ", wins, "| Win Rate: ", winRate)
print("Natural BlackJacks: ", naturals)
print(" ")
print("Ties: ", ties, "| Tie Rate: ", tieRate)
print(" ")
print("Losses: ", losses, "| Loss Rate: ", lossRate)