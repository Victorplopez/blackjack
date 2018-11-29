import BlackJackEnviornment
import random

env = BlackJackEnviornment.BlackjackEnv()

totalPlays = 1
alpha = .5

wins = 0  # keep track of number of wins
losses = 0  # keep track of number of losses
ties = 0  # keep track of number of ties
naturals = 0  # keep track of number of natural blackjacks

obs = env.reset()

while totalPlays > 0:
    env.step(random.randint(0, 1))






# Print headers to give more information about output
print("{:^10} | {:^50} | {:^50}".format("Player's", "Dealer's upcard when ace is not usable",
                                        "Dealer's upcard when ace is usable"))
print("{0:^10} | {1} | {1}".format("Hand", [str(upcard) if not upcard == 10 else 'A'
                                            for upcard in list_dealers_upcard]))
print(''.join(['-' for _ in range(116)]))
for players_hand in list_players_hand:
    actions_usable = []
    actions_not_usable = []
    for dealers_upcard in list_dealers_upcard:
        observation = (players_hand, dealers_upcard, False)
        actions_not_usable.append(readable_action(observation, agent))
        observation = (players_hand, dealers_upcard, True)
        actions_usable.append(readable_action(observation, agent))

    print("{:>10} | {} | {}".format(players_hand, actions_not_usable, actions_usable))

print("Average payout after {} rounds is {}".format(num_rounds, sum(payouts) / num_samples))