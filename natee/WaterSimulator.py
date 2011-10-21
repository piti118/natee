from os.path import dirname
import util
import inspect
import reader
from util import Struct
try:
    from matplotlib import pyplot as plt
except: pass
import sys
class Simulation:
    def __init__(self,req,sit,alg):
        #TODO check alg signature
        self.alg = alg
        self.dam = req
        self.data = sit
        self.dec = Decisions() #historical decision
        
    def run(self,ignore_error=False):
        waterlvl = 0
        first = True
        for data in self.dam.hist:
            if first :
                first = False
                water_lvl = data.water_lvl
            min_ = self.req.min_flow_for_date(data.date)
            max_ = self.req.max_flow_for_date(data.date)
            out = self.alg(day=data.date.day,month=data.date.month,lvl=water_lvl,water_in=data.water_in,min_=min_,max_=max_)
            waterlvl += data.water_in - out
            self.dec.append(date,out,water_lvl,data.water_in)
            print util.date2td(date), data.water_in, out, water_lvl
            try:
                self.req.run_check(waterlvl,self.dec)
            except Exception as e:
                print e 
                break
    
    def plot(self,dec):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        out = [x.out*50 for x in dec.dec]
        date = [x.date for x in dec.dec]
        lvl = [x.lvl for x in dec.dec]
        water_in = [x.water_in*50 for x in dec.dec]
        hist_lvl = [x.water_lvl for x in self.dam.hist]
        hist_date = [x.date for x in self.dam.hist]
        ax.plot(date,out,lw=2,color='magenta')
        ax.plot(date,lvl,color='red',lw=2)
        ax.plot(date,water_in,color='green')
        ax.plot(hist_date,hist_lvl,color='blue')
        ax.grid(True)
        ax.set_ylim(ymin=0)
        plt.show()
