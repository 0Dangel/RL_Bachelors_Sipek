from lib.TaxiEnv import TaxiEnv
from IPython.display import clear_output
from time import sleep

def getInverseAction(action):
    if(action == 0):
        return 1    
    if(action == 1):
        return 0    
    if(action == 2):
        return 3    
    if(action == 3):
        return 2
    return 1000


def renderStates(stateList, animSpeed = 0.42):
    env = TaxiEnv()
    for state in stateList:
        env.setState(state)
        clear_output()
        env.printCurState()
        sleep(animSpeed)



def renderActions(actionList, startState, animSpeed = 0.42):
    env = TaxiEnv()
    env.setState(startState)
    env.print = True
    for action in actionList:
        clear_output()
        env.move(action)

        #env.printCurState()
        sleep(animSpeed)
    
    
