

from lib.TaxiEnv import TaxiEnv
import numpy as np

env = TaxiEnv(True)

ActionRow = []
StatesRow = []

done_states = []

distTable = np.ones((5,5))


(next_state, reward, done, info1, info2) = env.move(env.getRandomMove())

# while(len(ActionRow) > 0):
#     print("s")

#actionsOrder =  1,2,3,4,5,6 (down, up, right,left,pick up, drop off)

print(env.lastState)
#env.printCurState()


print(info2["action_mask"])

done = False




#(next_state, reward, done, info1, info2) = env.move(env.getRandomMove())
#action = env.env.action_space.sample(info2["action_mask"])

# print(next_state)
# print(reward)
# print(done)
# print(info1)
# print(info2)

# print(env.getSize())






#while not done:


#env.move(env.getRandomMove())