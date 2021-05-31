import numpy as np
import pandas as pd
import matplotlib
import pulp


path= r'C:\Users\CATHERINE\Desktop\data_center_scenarios.csv'
df=pd.read_csv(path,sep=';')
#print(df.head)
df_scenar1=df[df["scenario"]==1].copy()
#print(df_scenar1['cons (kW)'][1])

##création de la data_nf

    
np.random.seed(7)
pt=0.5
#print(df_scenar1)
random_lambda = np.random.rand(48)
random_price=np.random.rand(48)
#print(random_lambda)

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
        return 0
        #return self.sol[time]*(self.cop_hp-1)*pt/(self.cop_cs*pt*self.data['cons (kW)'][time])
        
    # TO BE COMPLETED
        
    
    def compute_flex_cons(self):
        self.flex_cons=np.zeros(self.horizon)
        for i in range(self.horizon):
            self.flex_cons[i]=self.alpha[i]*self.excess_thpower[i]/((self.cop_hp-1)*pt)
            
    def compute_hotwater(self):
        self.hotwater=np.zeros(self.horizon)
        for i in range(self.horizon):
            self.hot_water[i]=self.cop_hp*self.flex_cons[i]
    
    
    def global_decision(self):
        self.alphao=np.zeros(48)
        
        lp = pulp.LpProblem('data_center', pulp.LpMinimize)
        lp.setSolver()
        add_cons = {}
        for t in range(self.horizon):
            var_name='lhp'+str(t)
            add_cons[t]=pulp.LpVariable(var_name, 0.0, 1.0)
            constraint_name = "limitation_" + str(t)
    		
            lp+=self.cop_hp*self.deltat*self.alphao[t]*self.lIT[t]*(self.cop_cs/self.eer)/((self.cop_hp-1)*self.deltat)<=10
            constraint_name = "puissancemax_" + str(t)
            lp+=self.lIT[t]+self.lIT[t]*(1.0+1.0/(self.eer*self.deltat))+self.alphao[t]*self.lIT[t]*self.cop_cs/self.eer/((self.cop_hp -1)*self.deltat)< self.pmax[t]
        
        lp.setObjective(pulp.lpSum([self.prices[t]*(self.nonflex[t]+add_cons[t]) for t in range(self.horizon)])\
        -pulp.lpSum([self.prices_hw[t]*self.cop_hp*add_cons[t] for t in range(self.horizon)])  )
        lp.solve()
        model=pd.Model(lp,add_cons)
        pd.solve(model,'data_center')
        results=pd.getResultsModel(lp,model,'data_center')
        pd.printResults(lp, model, 'data_center',[],results)
        for t in range(self.horizon):
            self.alpha[t] = self.alphao[t].varValue
            return results
            
     

    def compute_load(self, time):
        self.set_lNF()
        self.compute_HR()
        self.global_decision()
        self.compute_lHP()
        self.compute_HDC()
        self.compute_bill()
        load = np.zeros(self.horizon)
        for time in range(self.horizon):
            load[time]= self.lIT[time]+self.lNF[time]+self.lHP[time]
            return load

    def reset(self):
        # reset all observed data
        pass
        
    
    
_name__='main'
    
#####test
if _name__=='main':
    X=Player()
    load=X.compute_load()
    X.set_scenario(df_scenar1)
    X.set_prices(random_lambda)
    X.set_nonflexible()
    #print(X.cop_hp)
    X.global_decision()
    print(X.bill)
    print(X.alpha)
    print(X.horizon)
    
