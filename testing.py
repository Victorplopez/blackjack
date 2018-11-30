import gym
from qAgentClass import Agent

env = gym.make('Blackjack-v0')

agent = Agent(env=env, epsilon=1.0, alpha=0.5, gamma=0.2, num_episodes_to_train=800)

num_rounds = 1  # Payout calculated over num_rounds
num_samples = 10000  # num_rounds simulated over num_samples

payouts = []

observation = env.reset()
round = 1
total_payout = 0  # to store total payout over 'num_rounds'
# Take action based on Q-table of the agent and learn based on that until 'num_episodes_to_train' = 0
while round <= num_rounds * num_samples:
    action = agent.choose_action(observation)
    next_observation, payout, is_done, _ = env.step(action)
    agent.learn(observation, action, payout, next_observation)
    payouts.append(payout)
    observation = next_observation
    if is_done:
        observation = env.reset()  # Environment deals new cards to player and dealer
        round += 1

num_observations = 0
list_players_hand = range(1, 22)
list_dealers_upcard = range(1, 11)

# print(agent.valid_actions)
# print(agent.Q)


def readable_action(observation, agent):
    """
    Pass observation to agent and get human readable action
    H is hit, S is stick and '-' means the state is unseen and a random action is taken
    """
    if observation not in agent.Q:
        action = "-"
    else:
        action = "H" if agent.choose_action(observation) else "S"
    return action


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