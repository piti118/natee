from util import Struct
class Decisions:
    def __init__(self):
        self.dec = []
    def append(self,date,out,lvl,water_in,status):
        self.dec.append(Struct(
            date=date,
            out=out,
            lvl=lvl,
            water_in=water_in,
            status=status))
    def latest(self):
        return self.dec[-1].out
    def lastdate(self):
        return self.dec[-1].date
    def weeksum(self):
        return sum( (x.out for x in self.dec[-7:]) )
    def pop(self):
        self.dec.pop()
