from os.path import dirname
import util
import inspect
import reader
from util import Struct
try:
    from matplotlib import pyplot as plt
except: pass
from Decisions import Decisions
import sys
class Simulation:
    def __init__(self,dam,sit,alg):
        self.alg = alg #algorithm
        self.dam = dam #dam requirement
        self.dec = Decisions() #historical decision
        self.sit = sit # situation (just some array of something with date and water_in field )
    
    def run(self,cont=False):
        water_lvl = 0
        first = True
        success = True
        for data in self.sit:
            if first :
                first = False
                water_lvl = data.water_lvl
            out = self.alg(
                day=data.date.day,
                month=data.date.month,
                water_lvl=water_lvl,
                water_in=data.water_in,
                req = self.dam)
            water_lvl += data.water_in - out
            print util.date2td(data.date), data.water_in, out, water_lvl
            status = 'OK'
            self.dec.append(data.date,out,water_lvl,data.water_in,status)
            
            try:
                self.dam.run_check(water_lvl,self.dec)
            except AssertionError as e:
                status=str(e)
                #replace the status
                self.dec.pop()
                self.dec.append(data.date,out,water_lvl,data.water_in,status)
                success = False
                print util.date2td(data.date),e
            if not cont and status != 'OK': break
        return self.dec.dec
    
    def plot(self,histdata=None):
        dec = self.dec
        fig = plt.figure()
        ax = fig.add_subplot(111)
        out = [x.out*50 for x in dec.dec]
        date = [x.date for x in dec.dec]
        lvl = [x.lvl for x in dec.dec]
        water_in = [x.water_in*50 for x in dec.dec]
        ax.plot(date,out,lw=2,color='magenta')
        ax.plot(date,lvl,color='red',lw=2)
        ax.plot(date,water_in,color='green')
        if histdata is not None:
            hist_lvl = [x.water_lvl for x in histdata]
            hist_date = [x.date for x in histdata]
            hist_out = [x.out*50 for x in histdata]
            ax.plot(hist_date,hist_lvl,color='blue')
            ax.plot(hist_date,hist_out,color='black')
        ax.grid(True)
        ax.set_ylim(ymin=0)
        return fig,ax