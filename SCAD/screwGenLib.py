import math
import numpy
from stl import mesh


def lsin(ang):

  phase = ang%(2.0*math.pi)
  if (phase <= math.pi/2.0):
    #print "1: phase {0:f}\n".format(phase)
    return phase/(math.pi/2.0)
  elif (phase <= math.pi):
    #print "2: phase {0:f}\n".format(phase)
    return 1.0-(-1.0+phase/(math.pi/2.0))
  elif (phase <= 3.0*math.pi/2.0):
    #print "3: phase {0:f}\n".format(phase)
    return -(-2.0+phase/(math.pi/2.0))
  else:
    #print "4: phase {0:f}\n".format(phase)
    return -(1.0-(-3.0+phase/(math.pi/2.0)))


class screwDef:

  def __init__(self, R2, R1, P, N, fN, fR=128, fS=8):
    self.R2 = R2
    self.R1 = R1
    self.P  = P
    self.N  = N
    self.fN = fN
    self.fR = fR
    self.fS = fS



def buildScrew(screw,verbose=0):

  #Outer Raius of Screw (mm)
  R2 = screw.R2

  #Inner Radius of Screw (mm)
  R1 = screw.R1

  #Distance Between Teeth (mm)
  P = screw.P

  #Number of teeth at R1
  N = screw.N


  #----------------------------

  #number of cylinder radial segments
  fNR = screw.fR

  #number of cylinder vertical segemnts per tooth
  fNT = screw.fS

  #verbose = 1

  #-----------------------------
  #Build the point cloud

  worm = []

  zStep = P/float(fNT)

  fNR_angle = 2.0 * math.pi / fNR

  phaseStep = (2.0*math.pi) / fNT

  dR = (R2 - R1)/2.0

  for tooth in range(N):

    for layer in range(fNT):

      z  = (tooth * P) + (layer * zStep)

      if verbose:
        print "Base Height: {0:f}".format((layer * zStep))
        print "Z: {0:f}".format(z)

      dS = 1.0
      dT = dR

      for outer in range(fNR):

        offset = ((2.0*math.pi)/fNR)*outer

        #Fixme
        R = R1 + dT + dS*dR*lsin(layer*phaseStep-offset)
        x = R * math.cos(outer*fNR_angle)
        y = R * math.sin(outer*fNR_angle)
        
        worm.append( [x,y,z] )


  layerCnt = fNT * (N)

  #-----------------------------
  #Generate the worm model

  finalz  = (N-1)*P + ((fNT) * zStep)

  if verbose:
    print "Final Z: {0:f}".format(finalz)


  pointA = len(worm)
  pointB = pointA + 1
  worm.append( [0,0,0] )
  worm.append( [0,0,finalz] )

  vertices = numpy.array(worm)


  faceList=[]

  #sides
  for lA in range(layerCnt-1):

    lB = lA + 1

    for oA in range(fNR):

      oB = (oA+1)%fNR

      p00 = oA + lA * fNR
      p01 = oB + lA * fNR
      p02 = oA + lB * fNR
      p03 = oB + lB * fNR

      triangA = [p00,p01,p02]
      triangB = [p01,p03,p02]

      faceList.append(triangA)
      faceList.append(triangB)

  #bottom
  for oA in range(fNR):

    oB = (oA+1)%fNR

    p00 = oA 
    p01 = oB
    p02 = pointA

    triangA = [p00,p02,p01]

    faceList.append(triangA)

  #top
  lA = layerCnt-1
  for oA in range(fNR):

    oB = (oA+1)%fNR

    p00 = oA + lA * fNR
    p01 = oB + lA * fNR
    p02 = pointB

    triangA = [p00,p01,p02]

    faceList.append(triangA)


      
  faces = numpy.array(faceList)


  wormgear = mesh.Mesh(numpy.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
  for i, f in enumerate(faces):
    for j in range(3):
      wormgear.vectors[i][j] = vertices[f[j],:]

  #print "Generating model {0:s}:".format(fields[4])
  wormgear.save(screw.fN)



