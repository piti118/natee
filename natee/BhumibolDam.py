from os.path import dirname
import util
import inspect
class Decisions:
    def __init__(self):
        self.dec = []
    def append(date,decision):
        self.dec.append((date,decision))
    def latest(self):
        return self.dec[-1][1]
    def lastdate(self):
        return self.dec[-1][0]
    def weeksum(self):
        return sum( (x[1] for x in self.dec[-7:]) )

class Simulation:
    def __init__(self,dam,alg):
        #TODO check alg signature
        self.alg = alg
        self.dam = dam
        self.dec = Decisions()
    def run(self):
        waterlvl = 0
        first = True
        for data in self.dam.hist:
            date,influx,lvl = data
            if first :
                first = False
                waterlvl = lvl
            min_ = self.dam.min_flow_for_date(date)
            max_ = self.dam.max_flow_for_date(date)
            outflux = self.alg(date,lvl,influx,min_,max_)
            waterlvl += influx - outflux
            self.dec.append(date,outflux)
            print date, influx, outflux, waterlevel,
            self.dam.run_check(waterlevel,lvl,self.dec)
            print ' pass'

        print 'Yeah you won'
        
class BhumibolDam:
    def __init__(self):
        self.capacity = 13462. #m^3 everything here is m^3/day
        self.max_flow_day = 60. #no spill way
        self.max_flow_rainy = 60. # maximum flow for rainy season because of rain fall in central area already
        #self.max_flow_week = 30*7 #or it will flood
        self.min_flow = 12. #for power
        self.min_flow_napee = 30. 
        self.min_flow_naprang = 15.
        self.rainy_month = set([6,7,8,9,10])
        self.napee_month = set([6,7,8,9,10,11])
        self.naprang_month = set(range(12,1,2))
        #load data file for historical data
        self._init_histdata()
        #_init_weather()

    def _init_histdata(self):
        f = open(dirname(__file__)+'../tools/data/bb.csv','r')
        self.hist = []
        for line in f:
            date,dc,influx,lvl = line.split(',')
            date = util.td2date(date)
            self.hist.append((date,float(influx),float(lvl)))
        f.close()
    
    def max_flow_for_date(self,date):
        if date.month in self.rainy_month: return self.max_flow_rainy
        return self.max_flow
    
    def min_flow_for_date(self,date):
        if date.month in self.napee_month: return self.min_flow_napee
        if date.month in self.naprang_month: return self.max_flow_naprang
        return self.min_flow
    
    def run_check(self,cl,dec):
        self.check_capacity(cl,dec)
        self.check_flow(cl,dec)
    #currentlevel after applying the decision and today incoming water
    def check_capacity(self,cl, dec):
        assert cl < self.capacity,'exceed dam capacity'
        assert cl > 0.,'not enough water'

    def check_flow(self,cl, dec):
        date = dec.latedate()
        flow = dec.latest()
        week_flow = dec.weeksum()
        assert flow > self.min_flow,'less than min flow'
        if date.month in self.napee_month: assert flow > self.min_flow_napee,'not enough water for napee'
        if date.month in self.naprang_month: assert flow > self.min_flow_naprang,'not enough water for naprang'
        #check max flow
        assert flow < self.max_flow_day,'spill way open'
        #assert(week_flow < self.max_flow_week,'too much flow in a week')
def main():
    def avg(date,lvl,influx,max_,min_):
        return (max_+min_)/2
    dam = BhumibolDam()
    sim = Simulation(dam,avg)
    sim.run()
if __name__ == '__main__':
    main()    