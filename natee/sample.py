from BhumibolDam import BhumibolDam
from Simulation import Simulation
import reader
from os.path import dirname,abspath
import datetime
try:
    from matplotlib import pyplot as plt
except: pass
#argument is passed by name so just copy this
def avg_alg(day,month,water_lvl,water_in,req):
    min_ = req.min_flow_for_date(day,month)
    max_ = req.max_flow_for_date(day,month)
    return (max_+min_)/2
#always trying to min it
def min_alg(day,month,water_lvl,water_in,req):
    min_ = req.min_flow_for_date(day,month)
    max_ = req.max_flow_for_date(day,month)
    return min_
#simple algorithm trying to get back to 8000
def simple_alg(day,month,water_lvl,water_in,req):
    target = 8000.
    min_ = req.min_flow_for_date(day,month)
    max_ = req.max_flow_for_date(day,month)
    if water_lvl<target: return min_
    if water_lvl>target: return max(min(max_,water_lvl-target),min_)
    return min_

def main():
    #situation
    sit = reader.read(dirname(abspath(__file__))+'/../tools/data/bb.csv') #load data file for historical situation
    #requirement
    dam = BhumibolDam() #simple bhumibol dam requirement
    sim = Simulation(dam,sit,simple_alg) #make simulation with dam requirement, situation, and your chosen algorithm
    result = sim.run(True) #use sim.run() or sim.run(False) to abort when there is an error
    #it also returns the array or struct of bookkeeping result
    #try printing the result[0] to see what each element contain
    fig,ax = sim.plot(sit)
    ax.set_xlim(xmin=datetime.date(2009,01,01))
    plt.show()

if __name__ == '__main__':
    main()