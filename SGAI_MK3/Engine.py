import random as rd
class Engine():
    role = ""
    gamma = 0
    alpha = 0
    epsilon = 0
    budget = 0
    QTable = []
    rand = False
    ACTION_SPACE = ["moveUp","moveDown","moveLeft","moveRight","heal","bite"]
    '''
    Role is either Government or Zombie
    Budget = how far your ML model thinks ahead- mainly used for Monte Carlo Tree Search but can be applied
    to other areas
    QTable = given your model- remove if not q-learning
    '''
    def __init__(self,r,b,learning,BoardSize, ra) -> None:
        self.role = r
        self.budget = b
        self.gamma = learning[0]
        self.alpha = learning[1]
        self.epsilon = learning[2]
        self.rand = ra
        
        
        self.QTable = [0] * BoardSize
        #Board size is totalrows*totalcolumns. Remove if not QTable
        pass
    def think(self,GameBoard):
        '''
        This is where you put your ML Function
        Returns array with [action, coordinate, reward]
        '''
        i = 0
        r = rd.uniform(0.0, 1.0)
        st = rd.randint(0, len(GameBoard.States) - 1)
        state = self.QTable[st]
        if r < self.gamma or self.rand:
            while GameBoard.States[st].person is None:
                st = rd.randint(0, len(GameBoard.States) - 1)
            
        else:
            biggest = None
            for x in range(len(GameBoard.States)):
                arr = self.QTable[x]
                exp = sum(arr) / len(arr)
                if biggest is None:
                    biggest = exp
                    i = x
                elif biggest < exp and self.role == "Government":
                    biggest = exp
                    i = x
                elif biggest > exp and self.role != "Government":
                    biggest = exp
                    i = x
                    state = self.QTable[i]
                    b = 0
                    j = 0
                    ind = 0
                for v in state:
                    if v > b and self.role == "Government":
                        b = v
                        ind = j
                    elif v < b and self.role != "Government":
                        b = v
                        ind = j
                    j += 1
                action_to_take = self.ACTION_SPACE[ind]
                old_qval = b
                old_state = i
            
            return [action_to_take, old_state, old_qval]
                   
    def update_q_table(self,NewBoard, action_info):
        # action_info: exactly what is returned in think function with reward and nextstate qvalue at the end * 
        idx = self.ACTION_SPACE.index(action_info[0])
        self.QTable[action_info[1]][idx] = self.QTable[action_info[1]][idx] + self.alpha * (action_info[3] + self.gamma * action_info[4]) -  self.QTable[action_info[1]][idx]
        # GameBoard.QTable[i] = GameBoard.QTable[i] + alpha * (reward[0] + gamma * NS) - GameBoard.QTable[i]