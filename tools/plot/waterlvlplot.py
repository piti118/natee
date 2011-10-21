import csv
from os.path import dirname
from matplotlib import pyplot as plt
from math import sin,pi
fname = 'bb.csv'
reader = csv.reader(open(dirname(__file__)+'../data/'+fname),delimiter=',')

data = [(x[0],float(x[3]),float(x[2])*50) for x in reader]
date,lvl,influx = zip(*data)
period = 365
ur = [sin(2*pi*x/365)*906+12555 for x in range(len(lvl))]#luckily the shift is 0 for bb dam
lr = [sin(2*pi*x/365)*323+10031 for x in range(len(lvl))]
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(range(len(influx)),influx,label = 'incoming water per day scaled up by 50',alpha=0.7,color ='green')
ax.plot(range(len(lvl)),lvl,label = 'water level',lw=2,alpha=0.7,color='red')
ax.plot(range(len(ur)),ur,color='blue',label="upper/lower rule")
ax.plot(range(len(lr)),lr,color='blue')
xticks = range(0,7500,365)
ax.set_xticks(xticks)

xticklabels = [ date[i] if i < len(date) else '' for i in xticks ]
ax.set_xticklabels(xticklabels,rotation = 45)
locs = ax.get_xticks()
ax.set_title('Water Level in Bhumibol Dam')
ax.set_ylabel('million m^3')
ax.legend(loc=2)
print locs
ax.grid(True)
plt.show()
