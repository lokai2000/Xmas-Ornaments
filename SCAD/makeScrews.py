import math
import screwGenLib

height = 15
diameter = 30
screwTol = 0.6

P = 3.0
N = int(0.5+2*height/P)


R2 = (diameter)/2.0
R1 = R2 - 1.0
SCREW = screwGenLib.screwDef(R2,R1,P,N,"./screwOuterInset.stl")
screwGenLib.buildScrew(SCREW)

R2 += screwTol
R1 += screwTol
SCREW = screwGenLib.screwDef(R2,R1,P,N,"./screwOuterOutset.stl")
screwGenLib.buildScrew(SCREW)


