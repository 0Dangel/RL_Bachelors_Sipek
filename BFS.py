#Env Init:
from lib.TaxiEnv import TaxiEnv
import numpy as np
from time import time
from lib.utilities import getInverseAction

def bfs (env, start, moreResults = False):
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
        
            i = statesTisTurn.pop(0)
            #print(i,end=",")
            state, actionMask = env.setState(i, True)
            if not (state in states):
                states[state] = [False,[]]
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
                    onBoard = True
                    #statesNextTurn = [nxtState]
                #If I am done - return with the path
                if(done):
                    finalPath = states[state].copy()
                    finalPath[1].append(state)
                    finalPath[1].append(nxtState)
                    gotResult = True
                    break
                #If we have the passenger onboard but the action doesn't make it "done" - end
                elif(actionId == 5):
                    continue
                #If next state hasn't been checked - add an empty array
                if not (nxtState in states):
                    states[nxtState] = [False,[]]
                    goThrough = True
                #If the nextState hasn't been searched or shorter path has been found
                if goThrough or onBoard != states[nxtState][0]  or (len(states[nxtState][1]) > len(states[state][1])+1 ) :
                    goThrough = False
                    #print(rew)
                    states[nxtState][1] = states[state][1].copy()
                    states[nxtState][1].append(state)
                    states[nxtState][0] = onBoard
                    statesNextTurn.append(nxtState)
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
    return finalPath[1]     
