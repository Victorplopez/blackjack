import blackJackEnvironment
import random

env = blackJackEnvironment.BlackjackEnv()

totalPlays = initialPlayCount = 100000
epsilon = 1.0  # Starting with a high epsilon and gradually decreasing
alpha = 0.2
gamma = 0.1  # aka Discount

Q = dict()  # Creates a dictionary of tuples

wins = 0  # keep track of number of wins
losses = 0  # keep track of number of losses
ties = 0  # keep track of number of ties
naturals = 0  # keep track of number of natural blackjacks

#usable ace feature
def feature1(observ):
    _, _, usableAce = observ

    if(usableAce):
        feature = 1.25
    else:
        feature = 1.00

    return feature

#ideal sum feature
def feature2(observ):
    sum, dealersCard, usableAce = observ

    if(sum < 12):
        feature = 0.75
    elif(sum > 11 and sum < 17):
        feature = 1.00
    else:
        feature = 1.25

    return feature

def displayActions(observ):
    if observ not in Q:
        displayAction = "-"
    else:
        displayAction = "H" if chooseAction(observ) else "S"
    return displayAction


def addNewQValue(observ):
    if observ not in Q:
        Q[observ] = dict((i, 0.0) for i in range(2))


def maxQValue(observ):
    addNewQValue(observ)
    return max(Q[observ].values())


def decreaseEpsilon():
    global epsilon, alpha

    if (totalPlays > 0):
        smallDecrease = (0.1 * epsilon) / (0.5 * totalPlays)  # reduce epsilon slowly
        bigDecrease = (0.8 * epsilon) / (0.3 * totalPlays)  # reduce epsilon faster

        if totalPlays > 0.75 * totalPlays:
            epsilon -= smallDecrease
        elif totalPlays > 0.35 * totalPlays:
            epsilon -= bigDecrease
        elif totalPlays > 0:
            epsilon -= smallDecrease
        else:
            epsilon = 0.0
            alpha = 0.0


def chooseAction(observ):
    global epsilon

    addNewQValue(observ)

    if random.random() > epsilon:
        if (Q[observ][0] < Q[observ][1]):
            action = 1

        elif (Q[observ][0] > Q[observ][1]):
            action = 0

        else:
            action = random.randint(0, 1)

    else:
        action = random.randint(0, 1)

    decreaseEpsilon()

    return action


# sampling iterations
while totalPlays > 0:
    observ = env.reset()
    done = False
    weight1 = 0.0  # weight initialized to 0.0
    weight2 = 0.0

    while done is False:
        action = chooseAction(observ)
        move = env.step(action)
        observPrime = move[0]
        reward = move[1]
        done = move[2]
        difference = (reward + (gamma * maxQValue(observPrime)) - Q[observ][action])
        weight1 += alpha * (difference) * feature1(observ)
        weight2 += alpha * (difference) * feature2(observ)
        Q[observ][action] += (weight1 * feature1(observ)) + (weight2 * feature2(observ))
        observ = observPrime

    totalPlays -= 1

print("Q's: "+ str(Q))

# Print headers to give more information about output
print("{:^10} | {:^50} | {:^50}".format("Player's", "Dealer's upcard when ace is not usable",
                                        "Dealer's upcard when ace is usable"))
print("{0:^10} | {1} | {1}".format("Hand", [str(upcard) if not upcard == 10 else 'A'
                                            for upcard in range(1, 11)]))
print(''.join(['-' for _ in range(116)]))
for players_hand in range(1, 22):
    actions_usable = []
    actions_not_usable = []
    for dealers_upcard in range(1, 11):
        observation = (players_hand, dealers_upcard, False)
        actions_not_usable.append(displayActions(observation))
        observation = (players_hand, dealers_upcard, True)
        actions_usable.append(displayActions(observation))

    print("{:>10} | {} | {}".format(players_hand, actions_not_usable, actions_usable))

# iterations after obtaining sample data
totalPlays = 1000  # reset totalPlays for optimal simulation
while totalPlays > 0:
    observ = env.reset()
    done = False
    epsilon = 0

    iteration = 1

    while done is False:
        action = chooseAction(observ)
        epsilon = 0
        move = env.step(action)
        observPrime = move[0]
        done = move[2]
        observ = observPrime

        if (iteration == 1 and action == 0 and move[0][0] == 21):
            naturals += 1.00

        iteration += 1

    if (move[2] == True):  # move[2] is done value
        if (move[1] == 1):  # move[1] hold the reward value
            wins += 1.00  # if > 0 then agent has won
        elif (move[1] == 0):
            ties += 1.00
        else:
            losses += 1.00

    totalPlays -= 1

winRate = (wins / initialPlayCount) * 100
tieRate = (ties / initialPlayCount) * 100
lossRate = (losses / initialPlayCount) * 100

print("Total Plays: " + str(totalPlays))
print("-------------")
print("Wins: " + str(wins) + "| Win Rate: " + str(winRate))
print("Natural BlackJacks: " + str(naturals))
print(" ")
print("Ties: " + str(ties) + "| Tie Rate: " + str(tieRate))
print(" ")
print("Losses: " + str(losses) + "| Loss Rate: " + str(lossRate))