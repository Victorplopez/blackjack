import BlackJackEnviornment
import random

env = BlackJackEnviornment.BlackjackEnv()

totalPlays = initialPlayCount = 100
epsilon = 1.0  # Starting with a high epsilon and gradually decrementing
alpha = 0.5
gamma = 1.0  # aka Discount. No need for gamma in our environment but we are using it to match formulas

Q = dict()  # Creates a dictionary of tuples


wins = 0  # keep track of number of wins
losses = 0  # keep track of number of losses
ties = 0  # keep track of number of ties
naturals = 0  # keep track of number of natural blackjacks

obs = env.reset()

def readable_action(observ):
    """
    Pass observation to agent and get human readable action
    H is hit, S is stick and '-' means the state is unseen and a random action is taken
    """
    if observ not in Q:
        displayAction = "-"
    else:
        displayAction = "H" if chooseAction(observ) else "S"
    return displayAction


def addNewQ(observ):
    if observ not in Q:
        Q[observ] = dict((choose, 0.0) for choose in env.actions)

def maxQ(observ):
    addNewQ(observ)
    return max(Q[observ].values())

def chooseAction(observ):
    global epsilon
    if random.random() > epsilon:
        for i in range(2):
            if Q[observ][i] == maxQ(observ):
                acction = 0
    else:
        acction = random.randint(0, 1)

    #decrementEpsilon()

    return acction

def decrementEpsilon():

    global epsilon, alpha  # because Python is dumb
    epsilon = totalPlays * 0.01


    """
    if totalPlays > 90:
        epsilon = 1.0
    elif (totalPlays <= 90) and (totalPlays > 80):
        epsilon = 0.9
    elif (totalPlays <= 80) and (totalPlays > 70):
        epsilon = 0.8
    elif (totalPlays <= 70) and (totalPlays > 60):
        epsilon = 0.7
    elif (totalPlays <= 60) and (totalPlays > 50):
        epsilon = 0.6
    elif (totalPlays <= 50) and (totalPlays > 40):
        epsilon = 0.5
    else:
        epsilon = 0.0

    if totalPlays > 0.9 * initialPlayCount:
         epsilon = 1.0
    elif (totalPlays < 0.9 * initialPlayCount) and (totalPlays > 0.7 * initialPlayCount):
        epsilon -= 0.05
    elif (totalPlays < 0.7 * initialPlayCount) and (totalPlays > 0.4 * initialPlayCount):
        epsilon -= 0.1
    else:
        epsilon = 0.0
        alpha = 0.0
"""



while totalPlays > 0:
    observ = env.reset()
    action = chooseAction(observ)
    #decrementEpsilon()
    move = env.step(action)
    observPrime = move[0]
    reward = move[1]
    addNewQ(observ)
    """
    self.Q[observation][action] += self.alpha * (reward
                                                 + (self.gamma * self.get_maxQ(next_observation))
                                                 - self.Q[observation][action])
    """

    Q[observ][action] += alpha * (reward + (gamma * maxQ(observPrime)) - Q[observ][action])

    #Q[observ][action] *= (1 - alpha) + alpha * (reward + (gamma * maxQ(observPrime))- Q[observ][action])

    # (1-alpha) * Q(s,a) + alpha(Reward + discount * next observation)
    totalPlays -= 1
    print(epsilon)
    print(totalPlays)


#print(Q)


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
        actions_not_usable.append(readable_action(observation))
        observation = (players_hand, dealers_upcard, True)
        actions_usable.append(readable_action(observation))

    print("{:>10} | {} | {}".format(players_hand, actions_not_usable, actions_usable))




