import gym

env = gym.make('Blackjack-v0')

env.seed(0)
env.reset()
obs1 = env._get_obs()

print "obs1: ", obs1
print "step1", env.step(1)
print "step2", env.step(1)

print "----------------------"

env.seed(0)
env.reset()
obs2 = env._get_obs()

print "obs2: ", obs2
print "step1", env.step(1)
print "step2", env.step(1)