import gymnasium as gym
import time
from IPython.display import clear_output
import numpy as np
import random
import seaborn as sns


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


    def getMoves(self):
        return self.env.action_space.sample()


    def move(self,action):
        self.actionCount += 1
        (next_state, reward, done, info1, info2) = self.env.step(action)
        if(reward == -10):
            self.penalties += 1
        
        s=self.env.render()
        print(s)

        return (next_state, reward, done, info1, info2) 