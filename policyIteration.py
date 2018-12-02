import BlackJackEnviornment

lookupTable = {}


env=BlackJackEnviornment.BlackjackEnv()

for playerCard1 in range (10):
    playerCard1
    for playerCard2 in range (10):
        if playerCard1>=playerCard2:
            for dealerCard in range (10):
                env.set_dealers_hand(dealerCard,BlackJackEnviornment.draw_card())
                env.set_players_hand(playerCard1,playerCard2)
                observation = env._get_obs()
                lookupTable[(observation)] = 0
                for i in range (999):#loop for staying
                    env.reset()
                    env.set_players_hand(playerCard1,playerCard2)
                    env.set_dealers_hand(dealerCard,BlackJackEnviornment.draw_card())
                    observation = env._get_obs()
                    move = env.step(0)

                    #The game is over
                    if move[2] is True:
                        # Win or tie
                        if move [1] == 1 or move[1] == 0:
                            lookupTable[(observation)] = lookupTable[(observation)]-1
                        # Lost
                        # else:
                    # The game is not over

                #loop for hitting
                for i in range (999):
                    env.reset()
                    env.set_players_hand(playerCard1, playerCard2)
                    env.set_dealers_hand(dealerCard, BlackJackEnviornment.draw_card())
                    observation = env._get_obs()
                    move = env.step(1)

                    # The game is over
                    if move[2] is True:
                        # Win or tie
                        if move[1] == 1 or move[1] == 0 and observation is not None:
                            lookupTable[(observation)] = lookupTable[(observation)] + 1

                    # The game is not over
                    else:
                        observation=env._get_obs()
                        if lookupTable.get(observation):
                            if lookupTable[observation] > 0:
                                env.step(1)
                            else:
                                env.step(0)
                        else:
                            lookupTable[observation]=0

print lookupTable.items()