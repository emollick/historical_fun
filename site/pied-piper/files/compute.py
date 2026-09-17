import math
def jdn_julian(y,m,d):
    if m<=2: y-=1; m+=12
    return int(365.25*(y+4716))+int(30.6001*(m+1))+d-1524.5
def weekday(jd): return ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][int((jd+1.5)%7)]
def easter_julian(y):
    a,b,c=y%4,y%7,y%19; d=(19*c+15)%30; e=(2*a+4*b-d+34)%7
    return (d+e+114)//31,((d+e+114)%31)+1
def hav(a,b):
    R=6371.0; la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
if __name__=="__main__":
    print("26 June 1284 (Julian):",weekday(jdn_julian(1284,6,26)))
    print("Easter 1284:",easter_julian(1284))
    H=(52.104,9.357)
    for k,v in {"Coppenbrügge":(52.118,9.55),"Stendal":(52.607,11.859),"Pritzwalk":(53.150,12.174),"Prenzlau":(53.316,13.862),"Stettin":(53.429,14.553),"Kolberg":(54.176,15.583),"Olomouc":(49.594,17.251),"Erfurt":(50.978,11.029),"Lüneburg":(53.250,10.414)}.items():
        d=hav(H,v); print(f"{k:14s}{d:6.0f} km  road~{d*1.25:5.0f} km  {d*1.25/25:4.1f} days")
