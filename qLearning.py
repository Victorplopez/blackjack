import BlackJackEnviornment
import random

env = BlackJackEnviornment.BlackjackEnv()

totalPlays = initialPlayCount = 100000
epsilon = 1.0  # Starting with a high epsilon and gradually decrementing
alpha = 0.5
gamma = 0.05  # aka Discount. No need for gamma in our environment but we are using it to match formulas

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
        Q[observ] = dict((i, 0.0) for i in range(2))

def maxQ(observ):
    addNewQ(observ)
    return max(Q[observ].values())

def decrementEpsilon():
    global epsilon, alpha  # because Python is dumb

    if(totalPlays > 0):
        small_decrement = (0.1 * epsilon) / (0.3 * totalPlays)  # reduces epsilon slowly
        big_decrement = (0.8 * epsilon) / (0.4 * totalPlays)  # reduces epilon faster

        if totalPlays > 0.7 * totalPlays:
            epsilon -= small_decrement
        elif totalPlays > 0.3 * totalPlays:
            epsilon -= big_decrement
        elif totalPlays > 0:
            epsilon -= small_decrement
        else:
            epsilon = 0.0
            alpha = 0.0

def chooseAction(observ):
    global epsilon

    addNewQ(observ)

    if random.random() > epsilon:
        if (Q[observ][0] < Q[observ][1]):
            action = 1

        elif (Q[observ][0] > Q[observ][1]):
            action = 0

        else:
            action = random.randint(0, 1)

    else:
        action = random.randint(0, 1)

    decrementEpsilon()

    return action

# def chooseAction(observ):
#     addNewQ(observ)
#
#     if (Q[observ][1] > Q[observ][0]):
#         action = 1
#
#     else:
#         action = 0
#
#     return action


while totalPlays > 0:
    observ = env.reset()
    done = False

    while done is False:
        action = chooseAction(observ)
        move = env.step(action)
        observPrime = move[0]
        reward = move[1]
        done = move[2]
        Q[observ][action] += alpha * (reward + (gamma * maxQ(observPrime)) - Q[observ][action])
        observ = observPrime
        """
        self.Q[observation][action] += self.alpha * (reward
                                                     + (self.gamma * self.get_maxQ(next_observation))
                                                     - self.Q[observation][action])
        """

        #Q[observ][action] *= (1 - alpha) + alpha * (reward + (gamma * maxQ(observPrime))- Q[observ][action])
        # (1-alpha) * Q(s,a) + alpha(Reward + discount * next observation)

    totalPlays -= 1

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




