import csv
from os.path import dirname
from matplotlib import pyplot as plt
from math import sin,pi
import sys
sys.path.append(dirname(__file__)+'../../natee/')
import reader
import util
fname = 'bb.csv'
data = reader.read(dirname(__file__)+'../data/'+fname)

data = [(x.date,x.water_lvl,x.water_in*50) for x in data]
date,lvl,influx = zip(*data)
period = 365
ur = [sin(2*pi*x/365)*262+13379 for x in range(len(lvl))]#luckily the shift is 0 for bb dam
lr = [(sin(2*pi*x/365)*2.5+237.5)*13462./260. for x in range(len(lvl))]
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(range(len(influx)),influx,label = 'incoming water per day scaled up by 50',alpha=0.7,color ='green')
ax.plot(range(len(lvl)),lvl,label = 'water level',lw=2,alpha=0.7,color='red')
ax.plot(range(len(ur)),ur,color='blue',label="upper/lower rule")
ax.plot(range(len(lr)),lr,color='blue')
xticks = range(0,7500,365)
ax.set_xticks(xticks)

xticklabels = [ util.date2td(date[i]) if i < len(date) else '' for i in xticks ]
ax.set_xticklabels(xticklabels,rotation = 45)
locs = ax.get_xticks()
ax.set_title('Water Level in Bhumibol Dam')
ax.set_ylabel('million m^3')
ax.legend(loc=2)
print locs
ax.grid(True)
plt.show()
