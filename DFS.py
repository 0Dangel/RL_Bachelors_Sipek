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
    #for k in range(env.allStatesCount):
    statesTisTurn = []

    statesTisTurn.append(start)
    states = {}
    genericMaskLen = len(env.getLastActionMask())
    gotResult = False
    goThrough = False
    onBoard = False
    done = False
    solDepth = float("inf")
    finalPath = None
    pickupState = [] 
    stuckCounter = 0
    #For every pre-fetched actions
    while not gotResult:
        #print(statesTisTurn)
        #print("")

        #If we are stuck in this cycle
        if(stuckCounter > 3):
            return finalPath

        while len(statesTisTurn) > 0:
        
            i = statesTisTurn.pop()
            #print(i,end=",")
            state, actionMask = env.setState(i, True)
            if not (state in states):
                states[state] = [False,0,[]]
            #If we got to the max depth, end this turn

            print("----------------")
            print(states)
            print(state)
            if(states[state][1] > maxDepth or states[state][1] > solDepth):
                continue
            
            # For each action:
            print(actionMask)
            for actionId in range(genericMaskLen):
                actionId = 5 - actionId        
                
                #If action is not viable skip
                if(actionMask[actionId]) == 0:
                    continue
                print(actionId)
                #Else :
                #Set the previous state:
                env.setState(i)
                #Make a move
                nxtState, rew, done ,_,_ = env.move(actionId)
                #If the action was "pickup" - start from here next itteration
                if(actionId == 4):
                    # statesTisTurn = []
                    # statesNextTurn = []
                    pickupState = nxtState
                    #Reset current Depth:

                    solDepth = states[state][1]+1
                    #states[state][1] = 0
                    
                    #onBoard = True
                    #statesNextTurn = [nxtState]
                #If I am done - return with the path
                if(done):
                    #print(2)
                    pickupState = nxtState
                    finalPath = states[state].copy()
                    finalPath[2].append(state)
                    finalPath[2].append(nxtState)
                    gotResult = True
                    # if(moreResults):    
                    #     return finalPath
                    # return finalPath[2]    
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
            if(gotResult):
                break
            #print("yes")
            #break
            #statesTisTurn = statesNextTurn.copy()
            #print(statesNextTurn)q
            onBoard = True
            solDepth = float("inf")
            statesTisTurn = [pickupState]
            print(states)
            print(pickupState)
            states[pickupState][1] = 0
        stuckCounter += 1

    
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