#Env Init:
from lib.TaxiEnv import TaxiEnv
import numpy as np
from time import time
from lib.utilities import getInverseAction

def bfs (env, start):
    #WE don't want it to print while algo is running - huge slowdown
    env.print = False
    env.setState(start)

    #Action hopper - Hopper1 is "current itteration", Hopper2 is "nextStep" 
    actionHopper = []
    actionHopper2 = []

    #Just a basic "Been here before" paths pruning
    states=[]


    #First manual Itteration - needs to make main cycle more generic
    startState = env.getLastState()
    actionMask = env.getLastActionMask()
    #print(actionMask)
    #Whole path, states, costs and also actions
    returnVal = []

    akceId = 0
    for i in actionMask:
                #If action is possible:
                if(i == 1):
                    actionHopper.append((startState,akceId,0))
                    states.append(startState)
                    if(akceId >= 4):
                        returnVal.append([startState,akceId,0,[]])
                akceId += 1
    col, row = env.getPos(startState)
    #env.printCurState()
    # print(actionHopper)

    #Values used for return - "we got to the result" flag
    dontReturn = True
    #Basic heuristics - make sure we didn't ran into an infinite cycle
    counter = 0

    #Have we already solved it in first itter?
    if(len(returnVal) == 0):
        #While result doesn't exist and we still got some actions to do:
        while (dontReturn and len(actionHopper) > 0):
            #Check if we are not Too deep
            if(counter > 15):
                break
            counter += 1
            #For all actions in list:
            for i in actionHopper:
                    
                    #Set the state from action
                    try:
                        env.setState(i[0])
                    except Exception as e:
                        # print(i)
                        print(e)
                        #print(actionHopper)
                        #print(returnVal)
                    #Make a move
                    (next_state, reward, done, info1, info2) = env.move(i[1])
                    #If we have already visited this state - go for next action
                    if(next_state in states):
                        continue

                    #Check if we didn't put him in bad place
                    if(reward == -10):
                        break

                    if(i[1]== 5):
                        print("NOPE")
                        #If last action was valid "put him down" - return result
                        returnVal = [next_state,-1,i[2]+1,i]
                        dontReturn = False
                        break

                    #Get possible actions of current state
                    actionMask = info2["action_mask"]
                    akceId = 0
                    #For all possible actions:

                    for j in actionMask:
                        #If the action is possible
                        if(j == 1):
                            #If action is not reverse of the current one:
                            #(we really don't want to go back - efficiency)
                            if(akceId != getInverseAction(i[1])):
                                #Append that action to the hopper
                                actionHopper2.append([next_state,akceId,i[2]+1,i])
                                #If the action is final - we got a target so return it
                                if(akceId >= 4):
                                    #This because we don't want to put the user back again right after pickup
                                    if( i[1]!= 4):
                                        #print(i[1])
                                        if(akceId == 5):
                                            #print(reward)
                                            #dontReturn = False
                                            returnVal = [next_state,akceId,i[2]+1,i]
                                        #We got to the first or second target - reset old states
                                        actionHopper2 = [actionHopper2[-1]]
                                        states = []
                                        #print(actionHopper2)
                                        break
                        akceId += 1
                    #Mark this state as completed
                    states.append(i[0])
                    #Check if we should return something
                    if(not dontReturn):
                        break
            actionHopper = actionHopper2
            actionHopper2 = []

    stateList = []
    actionList = []
    try:
        next_state = returnVal       
        while(True):
            stateList.append(next_state[0])
            actionList.append(next_state[1])
            next_state = next_state[3]            
    except :    
        stateList.reverse()
        actionList.reverse()
    return stateList

        
    #Indexy akcí: 0 - down, 1 - up, 2 - right, 3 - left, 4 - pick, 5 - put. 