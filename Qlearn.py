import numpy as np
import random
import time
from IPython.display import clear_output
#import lib.TaxiEnv

import gymnasium as gym
import time
from IPython.display import clear_output
import numpy as np
import random
import seaborn as sns
from lib.TaxiEnv import TaxiEnv

env = TaxiEnv()
obsSpace, actiSpace = env.getSize()



all_epochs = []
all_penalties = []
q_table = np.zeros([obsSpace,actiSpace])
alpha = 0.1
gamma = 0.6
epsilon = 0.1
verbose = True
episodes = 100000

for i in range(1, episodes+1):
    state = env.getLastState()
    epochs, penalties, reward = 0,0,0
    done = False

    while not done:        
        if random.uniform(0,1) < epsilon:
            #Explore
            action = env.getRandomMove()         
        else:
            #Exploit
            action = np.argmax(q_table[state])
            

        #print(env.step(action))
        (next_state, reward, done, info1, info2) = env.move(action)

        old_value = q_table[state,action]
        next_max = np.max(q_table[next_state])

        new_value = (1-alpha) * old_value+alpha*(reward+gamma*next_max)
        #Alpha - jak moc měníme váhy jednotlivých hodnot při každé iteraci - learning rate
        #               (u transformerů např se často jedná o základní hodnotu 5e-5 a pomalu se zmenšuje - optimalizace konvergence na gradientu)
        #Gamma - přidává snahu o optimalizaci a dosažení výsledku v co nejméně krocích - úspěch za 2 kroky má menší prio / váhu než úspěch za 1 krok
        #Epsilon - kolik % průchodů má být průzkumných (preference průzkumu vs navigace známým směrem)

        q_table[state, action] = new_value

        if reward == -10:
            penalties +=1

        state = next_state
        epochs += 1

    if(verbose):
        if i % 1000 ==0:
            clear_output(wait=True)
            print(f"Episode: {i}")

policy = np.ones([obsSpace,actiSpace]) / actiSpace
for state in range(obsSpace):  #for each states
    best_act = np.argmax(q_table[state]) #find best action
    policy[state] = np.eye(actiSpace)[best_act]  #update 
    
print("Training finished.\n")