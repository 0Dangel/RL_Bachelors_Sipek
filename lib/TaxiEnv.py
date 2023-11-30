import gymnasium as gym
import time
from IPython.display import clear_output
import numpy as np
import random
import seaborn as sns
import math

class TaxiEnv:

    def __init__(self, print = False):
        #self.value = value
        self.env = gym.make("Taxi-v3", render_mode="ansi").env
        self.lastState = self.env.reset()
        self.actionCount = 0
        self.penalties = 0
        self.reward = 0
        self.print = print

    def getSize(self):
        return (self.env.observation_space.n, self.env.action_space.n)

    def getLastState(self):
        return self.lastState[0]
    
    def getLastActionMask(self):
        return self.lastState[1]["action_mask"]
    
    #Returns the "Column, Row" tuple
    def getPos(self,stav = None):
        if(stav == None):
            stav = self.getLastState()
        stav
        vysl = list(self.env.unwrapped.decode(stav))
        # stav = self.getLastState()
        # col = math.floor((stav%100)/20)
        # row = math.floor(stav/100)
        return(vysl[1],vysl[0])
    
    def getRandomMove(self):
        return self.env.action_space.sample()


    def move(self,action):
        self.actionCount += 1
        (next_state, reward, done, info1, info2) = self.env.step(action)
        if(reward == -10):
            self.penalties += 1
        if(self.print == True):
            self.printCurState()

        return (next_state, reward, done, info1, info2) 
    
    def printCurState(self):
        s=self.env.render()
        print(s)

    def setState(self,stateNum):
        pNum =self.env.P[stateNum]
        actionMask =self.env.action_mask(stateNum)
        self.lastState = (stateNum,{'prob' : 1.0,'action_mask':actionMask})
        self.env.unwrapped.s = stateNum
        #self.printCurState()

    def render(self):
        self.env.render()