import datetime
def td2date(dmy):
    #convert thai date of the form dd/mm/yyyy to date object
    d,m,y = dmy.split('/')
    y = int(y)-543
    return datetime.date(int(y),int(m),int(d))