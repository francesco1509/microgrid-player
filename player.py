# python 3
# this class combines all basic features of a generic player

import numpy as np
import pandas
import gurobipy as gp
from gurobipy import GRB

path= r'C:\SERIOUS_GAME\data_center_scenarios.csv'
df=pandas.read_csv(path,sep=';')
print(df.head)
df_scenar1=df[df["scenario"]==1].copy()
print(df_scenar1['cons (kW)'][1])

##création de la data_nf

    
np.random.seed(7)
pt=0.5
print(df_scenar1)
random_lambda = np.random.rand(48)
random_price=np.random.rand(48)
print(random_lambda)

class Player:

    def __init__(self):
    # some  player might not have parameters
        self.parameters = 0
        self.horizon = 48
        self.eer = 4
        self.cop_cs=self.eer+1
        self.cop_hp=0.4*(60+273)/25
        self.prices_hw=np.random.rand(48)
        print("prix",self.prices_hw)

    def set_scenario(self, scenario_data):
         self.data = scenario_data
         
    def set_nonflexible(self):
        df_nf=(self.data).copy()
        nonflex=np.zeros(self.horizon)
        for i in range (len(self.data)):
            nonflex[i]= df_nf['cons (kW)'][i]*(1+1/(self.eer*pt))
            
        self.nonflex=nonflex
            

    def set_prices(self, prices):
         self.prices = prices
    def compute_excess_thpower(self):
        excesspower=np.zeros(self.horizon)
        for i in range(len(self.data)):
            excesspower[i]=self.data['cons (kW)'][i]*self.cop_cs*pt
            
        self.excess_thpoower=excesspower
  

    def take_decision(self, time):
        
        return self.sol[time]*(self.cop_hp-1)*pt/(self.cop_cs*pt*self.data['cons (kW)'][time])
        
    # TO BE COMPLETED
        return 0
    
    def compute_flex_cons(self):
        self.flex_cons=np.zeros(self.horizon)
        for i in range(self.horizon):
            self.flex_cons[i]=self.alpha[i]*self.excess_thpower[i]/((self.cop_hp-1)*pt)
            
    def compute_hotwater(self):
        self.hotwater=np.zeros(self.horizon)
        for i in range(self.horizon):
            self.hot_water[i]=self.cop_hp*self.flex_cons[i]
    
    
    def global_decision(self):
        self.alpha=np.zeros(48)
        
        # lp = pulp.LpProblem('data_center', pulp.LpMinimize)
        # lp.setSolver()
        # add_cons = {}
        # for t in range(self.horizon):
        #     var_name='lhp'+str(t)
        #     add_cons[t]=pulp.LpVariable(var_name, 0.0, 10/self.cop_hp )
        
        # lp.setObjective(pulp.lpSum([self.prices[t]*(self.nonflex[t]+add_cons[t]) for t in range(self.horizon)])\
        # -pulp.lpSum([self.prices_hw[t]*self.cop_hp*add_cons[t] for t in range(self.horizon)])  )
        # model=Model(lp,add_cons)
        # solve(model,'data_center')
        # results=getResultsModel(pb,model,pb_name)
        # printResults(pb, model, 'data_center',[],results)
        m=gp.Model()
        vars = m.addVars(self.horizon,lb=0.0,ub=10/(self.cop_hp*pt),vtype=GRB.CONTINUOUS, name='e')
        m.setObjective(sum(self.prices[t]*(self.nonflex[t]+vars[t])-self.prices_hw[t]*self.cop_hp*vars[t] for t in range(self.horizon)), GRB.MINIMIZE)
        m.optimize()
        self.sol=np.zeros(48)
        for j in range(self.horizon):
            print(j,vars[j].X)
            self.sol[j]=vars[j].X
            
        return self.sol
    def compute_all_load(self):
        load = self.global_decision(self)
            # for time in range(self.horizon):
             # 	load[time] = self.compute_load(time)
        return load
            
            
            
        

    def compute_load(self, time):
        load = self.take_decision(time)
         # do stuff ?
        return load

    def reset(self):
        # reset all observed data
        pass
    
    
    
    
    
#####test
if __name__=='__main__':
    X=Player()
    X.set_scenario(df_scenar1)
    X.set_prices(random_lambda)
    X.set_nonflexible()
    print(X.cop_hp)
    test=X.global_decision()
    
    print(X.horizon)

