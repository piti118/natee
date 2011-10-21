import datetime

def date2td(date):
    newyear = date.year+543
    return '/'.join([str(date.day),str(date.month),str(newyear)])

def td2date(dmy):
    #convert thai date of the form dd/mm/yyyy to date object
    d,m,y = dmy.split('/')
    y = int(y)-543
    return datetime.date(int(y),int(m),int(d))
    
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
    def __str__(self):
        return str(self.__dict__)