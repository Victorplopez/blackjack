# odds to receive 1 -> 9 in deck = 1/13 or 7.692307692% in our simple variation
# odds to receive 10 in deck = 4/13 or 30.769230769%

import BlackJackEnviornment

env = BlackJackEnviornment.BlackjackEnv()

totalPlays = 1
wins = 0  # keep track of number of wins
losses = 0  # keep track of number of losses
ties = 0  # keep track of number of ties
naturals = 0  # keep track of number of natural blackjacks

# Rewards are calculated based on winning+tieing probability if player stays at given state. After running simulation 100000 times.
rewardMatrix = [[.1494, .3163, .3262, .3528, .3716, .3607, .3422, .3199, .2915, .2757],  # Sum = 4
                [.1512, .319, .3287, .3467, .3683, .3663, .3432, .3144, .3029, .2745],  # Sum = 5
                [.1529, .3195, .3293, .3512, .369, .3688, .3456, .3205, .3038, .2705],  # Sum = 6
                [.1548, .3183, .3299, .344, .3735, .3678, .3377, .3183, .2921, .2746],  # Sum = 7
                [.1489, .3192, .3329, .3482, .3594, .3664, .3385, .3129, .2976, .2777],  # Sum = 8
                [.151, .3115, .3314, .3416, .3588, .3677, .3486, .3114, .2973, .2797],  # Sum = 9
                [.154, .3149, .3414, .3452, .3661, .3631, .3399, .3216, .2937, .2778],  # Sum = 10
                [.1533, .3083, .3332, .3493, .3607, .3656, .3473, .3184, .3027, .2722],  # Sum = 11
                [.1476, .3118, .3331, .3458, .3659, .3591, .3373, .3177, .3001, .2824],  # Sum = 12
                [.1604, .3232, .3288, .353, .3716, .3723, .3447, .3195, .3018, .2765],  # Sum = 13
                [.149, .3145, .328, .3439, .3644, .362, .3358, .3184, .3007, .2726],  # Sum = 14
                [.1512, .3152, .3294, .3434, .3678, .3588, .3403, .3131, .3002, .2774],  # Sum = 15
                [.1512, .3152, .326, .3368, .3717, .3642, .3387, .3178, .3045, .2769],  # Sum = 16
                [.3255, .4613, .4793, .4835, .492, .563, .5253, .488, .4646, .4179],  # Sum = 17
                [.484, .6127, .6229, .6215, .6346, .6747, .7029, .6459, .6035, .5626],  # Sum = 18
                [.661, .7431, .748, .7518, .7577, .7881, .7985, .8207, .7636, .7135],  # Sum = 19
                [.8257, .88, .8768, .8819, .8807, .8914, .9036, .9076, .9209, .8527],  # Sum = 20
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]  # Sum = 21

# Probability to transition to card value 1->10 on hit
probabilityArray = \
    [0.076923077, 0.076923077, 0.076923077, 0.076923077, 0.076923077, 0.076923077, 0.076923077, 0.076923077,
     0.076923077, 0.307692308]


# Vk+1(s)<-max a Sum(P(s'|s,a)[R(s,a,s')+gammaVk(s')
def valueIteration(state, action):

    sum, dealers = state

    value = 0 #initialize

    if (action == 0):
        reward = rewardMatrix[sum - 4][dealers - 1]
        probability = 1.0
        value = probability * reward
    else:
        for i in range(10):
            if sum+(i+1) > 21:
                value = 0
            else:
                value = (value + valueIteration((sum+(i+1),dealers), 0)) * probabilityArray[i] # +1 to offset index
                value = (value + valueIteration((sum+(i+1),dealers), 1)) * probabilityArray[i]
    print value
    return value


for i in range(totalPlays):
    done = False  # re-initialize to false each iteration for each play

    iteration = 1  # used to determine natural blackJack
    env.reset()

    while (done is False):
        sum, dealers, usableAce = env._get_obs()
        state = (sum, dealers)

        if (valueIteration(state, 0) >= valueIteration(state, 1)):
            action = 0

        else:
            action = 1

        print "state: ", state
        print "action: ", action

        realMove = env.step(action)

        if (realMove[2] == True):  # move[2] is done value
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


winRate = (wins / totalPlays) * 100
tieRate = (ties / totalPlays) * 100
lossRate = (losses / totalPlays) * 100

print "Total Plays: ", totalPlays
print "-------------"
print "Wins: ", wins, "| Win Rate: ", winRate
print "Natural BlackJacks: ", naturals
print " "
print "Ties: ", ties, "| Tie Rate: ", tieRate
print " "
print "Losses: ", losses, "| Loss Rate: ", lossRate