import blackJackEnvironment

def print_hand(hand):
    output = ""
    for card in hand:
        output += "[ " + str(card) + " ]  "
    return output

def playRound():
    reward = 0

    roundFinished = False
    while (not roundFinished):
        action = -2
        playersSum, dealersCards, usableAce = env._get_obs()
        cash = env.get_current_cash()
        playersHand = env.get_players_hand()
        print ("---------------------")
        print("Dealers card [" + str(dealersCards) + "]")
        print("Your cards " + print_hand(playersHand)
              + "\nSum Of Hand = " + str(playersSum) + "\nCash Remaining = $" + str(cash))

        while (action != 1 and action != 0):
            action = input("Enter an action: \n' 0' to stay\n' 1' to hit\n")


        observation, reward, roundFinished,test = env.step(action)

    dealersCards = env.get_dealers_hand()
    dealersSum = env.get_dealers_hand_sum()
    playersHand = env.get_players_hand()
    playersSum = env.get_players_sum()

    print("---------------------")

    #End of Round
    if(reward == 1):  # move[1] hold the reward value
        print("You won")  # if > 0 then agent has won
        if dealersSum>21:
            print("The Dealer Busted")
        else:
            print("Your Hand Beat The Dealers!")

    elif(reward == 0):
        print ("It's a tie\nAt least you didn't lose any money!")
    else:
        print ("You Lost")
        if playersSum>21:
            print("You Busted!")
        else:
            print("The Dealer Beat Your Hand!")

    print("Dealers Hand: "+print_hand(dealersCards))
    print("Dealers  Sum: " + str(dealersSum))
    print("Players Hand: "+ print_hand(playersHand))
    print("Players  Sum: " + str(playersSum))
    print("---------------------")

    return env.get_current_cash()



env = blackJackEnvironment.BlackjackEnv()

donePlaying = False

env.reset()

while (not donePlaying):
    env.reset()
    observation = env._get_obs()
    currentCash = env.get_current_cash()
    print("---------------------")

    print("Welcome to BlackJack")
    print("You currently have: $" + str(currentCash))
    print("Good Luck Have Fun")
    currentCash = playRound()
    print("You currently have: $" + str(currentCash))
    answer = ""
    while (answer != 1 and answer != 0):
        answer = input("Do you want to continue playing? \n'1' For Yes\n'0' For No\n")
    if answer == 0 or currentCash < 0:
        print("You are done, Thanks for playing! :)")
        donePlaying = True