from os.path import dirname
import util
import inspect
import reader
from util import Struct
import sys

#simple requirement for Bhumibol Dam
#unit here M-m^3 = million m^3
#water lvl is betwen 13462(capacity) and 4000 M-m^3(historical low)  
#out flow capacity is 60M-m^3/day but in rainy season maximum is 30M-m^3/day so that central part won't be flooded
#min_flow =0.05M-m^3/day (made this up for power i guess)
#but in napee season( 6 7 8 9 10 11) one must flow water out at least 20 M-m^3/day (made this up too)
#and in naprang season(12 1 2) one must flow water out at least 10 M-m^3/day (made this up)

class BhumibolDam:
    def __init__(self):
        self.capacity = 13462. #m^3 everything here is m^3/day
        self.min_capacity = 3500.
        self.max_flow_day = 60. #no spill way
        self.max_flow_rainy = 35. # maximum flow for rainy season because of rain fall in central area already
        #self.max_flow_week = 30*7 #or it will flood
        self.min_flow = 0.1 #for power
        self.min_flow_napee = 20. 
        self.min_flow_naprang = 10.
        self.rainy_month = set([6,7,8,9,10])
        self.napee_month = set([6,7,8,9,10,11])
        self.naprang_month = set([12,1,2])

    #simple bound hint about the requirement
    def max_flow_for_date(self,day,month):
        if month in self.rainy_month: return self.max_flow_rainy
        return self.max_flow_day
    #simple bound hint about the requirement
    def min_flow_for_date(self,day,month):
        if month in self.napee_month: return self.min_flow_napee
        if month in self.naprang_month: return self.min_flow_naprang
        return self.min_flow
    #check all requirement
    #cl include water_in and water_out
    def run_check(self,cl,dec):
        self.check_capacity(cl,dec)
        self.check_flow(cl,dec)
    
    #currentlevel after applying the decision and today incoming water
    def check_capacity(self,cl, dec):
        assert cl < self.capacity,'exceed dam capacity'
        assert cl > self.min_capacity,'reach min water level'
    
    def check_flow(self,cl, dec):
        date = dec.lastdate()
        flow = dec.latest()
        week_flow = dec.weeksum()
        assert flow >= self.min_flow,'less than min flow'
        if date.month in self.napee_month: assert flow >= self.min_flow_napee,'not enough water for napee'
        if date.month in self.naprang_month: assert flow >= self.min_flow_naprang,'not enough water for naprang'
        #check max flow
        assert flow <= self.max_flow_day,'spill way open'
        #assert(week_flow < self.max_flow_week,'too much flow in a week')
