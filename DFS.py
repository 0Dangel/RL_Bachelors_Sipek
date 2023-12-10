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


def dfs (env, start, maxDepth = 15 ,moreResults = False):
    errStates = []
    #for k in range(env.allStatesCount):
    statesTisTurn = []
    statesNextTurn = []

    statesTisTurn.append(start)
    states = {}
    genericMaskLen = len(env.getLastActionMask())
    gotResult = False
    goThrough = False
    onBoard = False
    done = False

    finalPath = []
    #For every pre-fetched actions
    while not gotResult:
        #print(statesTisTurn)
        #print("")

        while len(statesTisTurn) > 0:
        
            i = statesTisTurn.pop()
            #print(i,end=",")
            state, actionMask = env.setState(i, True)
            if not (state in states):
                states[state] = [False,0,[]]
            #If we got to the max depth, end this turn
            if(states[state][1] > maxDepth):
                continue
            # For each action:
            for actionId in range(genericMaskLen):        
                #If action is not viable skip
                if(actionMask[actionId]) == 0:
                    continue
                #Else :
                #Set the previous state:
                env.setState(i)
                #Make a move
                nxtState, rew, done ,_,_ = env.move(actionId)
                #If the action was "pickup" - start from here next itteration
                if(actionId == 4):
                    statesTisTurn = []
                    statesNextTurn = []
                    #Reset current Depth:
                    states[state][1] = 0
                    onBoard = True
                    #statesNextTurn = [nxtState]
                #If I am done - return with the path
                if(done):
                    #print(2)
                    finalPath = states[state].copy()
                    finalPath[2].append(state)
                    finalPath[2].append(nxtState)
                    gotResult = True
                    break
                #If we have the passenger onboard but the action doesn't make it "done" - end
                elif(actionId == 5):
                    continue
                #If next state hasn't been checked - add an empty array
                if not (nxtState in states):
                    states[nxtState] = [False,0,[]]
                    goThrough = True
                #If the nextState hasn't been searched or shorter path has been found
                if goThrough or onBoard != states[nxtState][0]  or (len(states[nxtState][2]) > len(states[state][2])+1 ) :
                    goThrough = False
                    #print(rew)
                    states[nxtState][2] = states[state][2].copy()
                    states[nxtState][2].append(state)
                    states[nxtState][1] = states[state][1]+1
                    states[nxtState][0] = onBoard
                    statesTisTurn.append(nxtState)
                #else:
                    #print("Not updated - " + str(nxtState) + " from state " + str(state))
        else:
            #print("yes")
            #break
            statesTisTurn = statesNextTurn.copy()
            #print(statesNextTurn)
            statesNextTurn = []
    if(moreResults):
        return finalPath
    return finalPath[2]               




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