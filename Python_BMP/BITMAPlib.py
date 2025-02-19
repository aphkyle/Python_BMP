#
#Copyright 2022 by Joel C. Alcarez /joelalcarez1975@gmail.com
#
#We make no warranty of any kind, expressed or implied.
#
#The primary author and any subsequent code contributors shall not
#be liable in any event for incidental or consquential damages
#in connection with, or arising out of the use of this code
#in current form or with modifications.
#
#Contact primary author if you plan to use this in a commercial product at
# joelalcarez1975@gmail.com.

#Educational or hobby use highly encouraged.
#
#ps:created out of extreme boredom during the COVID-19 pandemic.
#
#This graphics library outputs to a bitmap file

from array import array
from os.path import isfile
from tests.proctimer import functimer
from Python_BMP.mathlib import sin,cos,cosaffin,radians,random,distance,vmag,iif,roundvect,addvect,addvectinlist,subvect,setminmax,isinrange,swapif,setmin,setmax,anglebetween2Dlines,polar2rectcoord2D,range2baseanddelta,mirror,xorvect,andvect,rotatebits,LSMslope,LSMYint,trans,intscalarmulvect
from Python_BMP.primitives2D import iterline,iterparallelogram,itercirclepartlineedge,itercirclepartvertlineedge,itercircle,itercirclepart,iterellipserot,iterellipsepart,iterellipse,iterbeziercurve,iterbspline,recvert,horizontalvert,verticalvert,arcvert,rectboundarycoords,regpolygonvert,bsplinevert
from Python_BMP.solids3D import gensides,perspective,getshapesidedict,tetrahedravert,cubevert,hexahedravert,octahedravert,decahedvertandsurface,dodecahedvertandsurface,fillpolydata,polyboundary,surfplot3Dvertandsurface,cylindervertandsurface,spherevertandsurface,rotvec3D,conevertandsurface
from Python_BMP.fonts import font8x8,font8x14,getcharfont
from Python_BMP.colors import bmpvalidcolorbits,isvalidcolorbit,bmpstdpal,getdefaultbitpal,colormix,RGBtoBGRarr,int2RGBlist,RGBfactors2RGB,int2BGRarr,RGB2int,int2RGBarr,int2RGB,getcolorname2RGBdict,getdefaultlumrange,getRGBfactors,matchRGBtopal,brightnessadjust,monochromepal,colorfiltertoBGRbuf,gammaBGRbuf,applymonochromefiltertoBGRbuf,applycolorfiltertoBGRbuf,applygammaBGRbuf,probplotRGBto1bit,thresholdadjust,colorfilter,monochrome,gammacorrect,monochromefiltertoBGRbuf,RGBfactorstoBaseandRange,invertbitsinbuffer,applybrightnessadjtoBGRbuf,applythresholdadjtoBGRbuf
from Python_BMP.messages import sysmsg

# BMP constants do not edit!!!
bmpheaderid,bmpfilesize,bmphdrsize,bmpcolorbits,bmpx,bmpy,bmppal=array('B',[66,77]),2,10,28,18,22,54
bmpheadersize={1:62,4:118,8:1078,24:54}
        
def checklink(func):
    def callf(*args,**kwargs):
        if isfile(args[0]):  return(func(*args,**kwargs))
        else: print(sysmsg['filenotexist'])
    return(callf)

def checklinks(func):
    def callf(*args,**kwargs):
        if isfile(args[0]) and isfile(args[1]):  return(func(*args,**kwargs))
        else: print(sysmsg['filenotexist'])
    return(callf)

def intcircleparam(func):
    def callf(*args,**kwargs):
        if (type(args[1])==int and type(args[2])==int) and type(args[3])==int: return(func(*args,**kwargs))
        else:  print(sysmsg['inttypereq'])
    return(callf)

def intcircleparam24bitonly(func):
    def callf(*args,**kwargs):
        if args[0][bmpcolorbits]!=24 : print(sysmsg['not24bit'])
        else:
            if (type(args[1])==int and type(args[2])==int) and type(args[3])==int: return(func(*args,**kwargs))
            else:  print(sysmsg['inttypereq'])
    return(callf)

def func24bitonly(func):
    def callf(*args,**kwargs):
        if args[0][bmpcolorbits]!=24 : print(sysmsg['not24bit'])
        else: return(func(*args,**kwargs))
    return(callf)

def func24bitonlyandentirerectinboundary(func):
    def callf(*args,**kwargs):
        bmp,x1,y1,x2,y2=args[0],args[1],args[2],args[3],args[4]
        if bmp[bmpcolorbits]!=24 : print(sysmsg['not24bit'])
        else:
            if (type(x1)==int and type(x2)==int) and (type(y1)==int and type(y2)==int):
                if not (isinBMPrectbnd(bmp,x1,y1) and isinBMPrectbnd(bmp,x2,y2)):print(sysmsg['regionoutofbounds'])
                else: return(func(*args,**kwargs))
            else:  print(sysmsg['inttypereq'])
    return(callf)

def func24bitonlyandentirecircleinboundary(func):
    def callf(*args,**kwargs):
        bmp,x,y,r=args[0],args[1],args[2],args[3]
        if bmp[bmpcolorbits]!=24 : print(sysmsg['not24bit'])
        else:
            if (type(x)==int and type(y)==int) and type(r)==int:
                if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r): return(func(*args,**kwargs))
                else: print(sysmsg['regionoutofbounds'])
            else:  print(sysmsg['inttypereq'])
    return(callf)

def func8and24bitonlyandentirecircleinboundary(func):
    def callf(*args,**kwargs):
        bmp,x,y,r=args[0],args[1],args[2],args[3]
        if bmp[bmpcolorbits] not in [24,8]: print(sysmsg['not24or8bit'])
        else:
            if (type(x)==int and type(y)==int) and type(r)==int:
                if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r): return(func(*args,**kwargs))
                else: print(sysmsg['regionoutofbounds'])
            else:  print(sysmsg['inttypereq'])
    return(callf)

def func8and24bitonly(func):
    def callf(*args,**kwargs):
        if args[0][bmpcolorbits] not in [24,8]: print(sysmsg['not24or8bit'])
        else: return(func(*args,**kwargs))
    return(callf)

def func8and24bitonlyandentirerectinboundary(func):
    def callf(*args,**kwargs):
        bmp,x1,y1,x2,y2=args[0],args[1],args[2],args[3],args[4]
        if bmp[bmpcolorbits] not in [24,8]: print(sysmsg['not24or8bit'])
        else:
            if (type(x1)==int and type(x2)==int) and (type(y1)==int and type(y2)==int):
                if not (isinBMPrectbnd(bmp,x1,y1) and isinBMPrectbnd(bmp,x2,y2)):print(sysmsg['regionoutofbounds'])
                else: return(func(*args,**kwargs))
            else:  print(sysmsg['inttypereq'])
    return(callf)

def entirerectinboundary(func):
    def callf(*args,**kwargs):
        bmp,x1,y1,x2,y2=args[0],args[1],args[2],args[3],args[4]
        if (type(x1)==int and type(x2)==int) and (type(y1)==int and type(y2)==int):
            if not (isinBMPrectbnd(bmp,x1,y1) and isinBMPrectbnd(bmp,x2,y2)):print(sysmsg['regionoutofbounds'])
            else: return(func(*args,**kwargs))
        else:  print(sysmsg['inttypereq'])
    return(callf)

def entirecircleinboundary(func):
    def callf(*args,**kwargs):
        bmp,x,y,r=args[0],args[1],args[2],args[3]
        if (type(x)==int and type(y)==int) and type(r)==int:
            if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r): return(func(*args,**kwargs))
            else: print(sysmsg['regionoutofbounds'])
        else:  print(sysmsg['inttypereq'])
    return(callf)

def writeint(offset,cnt,arr,value):
    j=cnt-1
    for i in range(0,j):
        b=value&0xff
        arr[offset+i]=b
        value=value>>8

def readint(offset,cnt,arr):
    v,j=0,cnt-1
    for i in range(0,j): v+=arr[offset+i]<<(i<<3)
    return v

def int2buf(cnt,value): return array('B',[(value>>(i*8))&0xff for i in range(0,cnt)])

def buf2int(buf):
    v,j=0,len(buf)-1
    for i in range(0,j): v+=buf[i]<<(i<<3)
    return v

def adjustbufsize(bufsize,bits):
    if bits==24: bufsize*=3
    elif bits==4: bufsize=bufsize>>1
    elif bits==1:  bufsize=bufsize>>3
    return bufsize

def setmaxx(bmp,xmax): writeint(bmpx,4,bmp,xmax)

def getmaxx(bmp): return readint(bmpx,4,bmp)

def setmaxy(bmp,ymax): writeint(bmpy,4,bmp,ymax)

def getmaxy(bmp): return readint(bmpy,4,bmp)

def getmaxxy(bmp): return (readint(bmpx,4,bmp),readint(bmpy,4,bmp))

def bottomrightcoord(bmp): return [readint(bmpx,4,bmp)-1,readint(bmpy,4,bmp)-1]

def centercoord(bmp): return [(readint(bmpx,4,bmp)-1)>>1,(readint(bmpy,4,bmp)-1)>>1]

def isinBMPrectbnd(bmp,x,y): return (x<readint(bmpx,4,bmp) and y<readint(bmpy,4,bmp)) and (x>-1 and y>-1)

def listinBMPrecbnd(bmp,xylist):
    retval=True
    for v in xylist:
        if isinBMPrectbnd(bmp,v[0],v[1])==False: break
    return retval

def setcolorbits(bmp,bits): bmp[bmpcolorbits]=bits

def getcolorbits(bmp): return bmp[bmpcolorbits]

def getxcharcount(bmp): return computexbytes(readint(18,4,bmp),bmp[bmpcolorbits])

def setfilesize(bmp,size): writeint(bmpfilesize,8,bmp,size)

def getfilesize(bmp): return readint(bmpfilesize,8,bmp)

def sethdrsize(bmp,hdsize): writeint(bmphdrsize,4,bmp,hdsize)

def gethdrsize(bmp): return readint(bmphdrsize,4,bmp)

def getimageinfo(bmp): return readint(bmpy,4,bmp),bmp[bmpcolorbits],getxcharcount(bmp),readint(bmphdrsize,4,bmp)

def getmaxcolors(bmp): return 1<<bmp[bmpcolorbits]

def compute24bitBMPoffset(bmp,x,y): return (x*3)+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),24))

def compute24bitBMPoffsetwithheader(bmp,x,y): return (x*3)+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),24))+54

def compute8bitBMPoffset(bmp,x,y): return x+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),8))

def compute8bitBMPoffsetwithheader(bmp,x,y): return x+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),8))+1078

def compute4bitBMPoffset(bmp,x,y): return (x>>1)+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),4))

def compute1bitBMPoffset(bmp,x,y): return (x>>3)+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),1))

def compute4bitBMPoffsetwithheader(bmp,x,y): return (x>>1)+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),4))+118

def compute1bitBMPoffsetwithheader(bmp,x,y): return (x>>3)+((readint(bmpy,4,bmp)-y-1)*computexbytes(readint(bmpx,4,bmp),1))+62

def getcomputeBMPoffsetwithheaderfunc(bmp): return {24:compute24bitBMPoffsetwithheader,8:compute8bitBMPoffsetwithheader,4:compute4bitBMPoffsetwithheader,1:compute1bitBMPoffsetwithheader}[bmp[bmpcolorbits]]

def getcomputeBMPoffsetfunc(bmp): return {24:compute24bitBMPoffset,8:compute8bitBMPoffset,4:compute4bitBMPoffset,1:compute1bitBMPoffset}[bmp[bmpcolorbits]]

def computeBMPoffset(bmp,x,y):
    f=getcomputeBMPoffsetfunc(bmp)
    return f(bmp,x,y)

def computeBMPoffsetwithheader(bmp,x,y):
    f=getcomputeBMPoffsetwithheaderfunc(bmp)
    return f(bmp,x,y)

def getmaxxyandbits(bmp): return (((readint(bmpx,4,bmp),readint(bmpy,4,bmp)),bmp[bmpcolorbits]))

def computeuncompressedbmpfilesize(bmp): return computeBMPfilesize(getmaxx(bmp),getmaxy(bmp),bmp[bmpcolorbits])

def isbmpcompressed(bmp): return computeuncompressedbmpfilesize(bmp)>getfilesize(bmp)

def compute24bitoffset(x,y,mx,my): return (x*3)+((my-y-1)*computexbytes(mx,24))

def computexbytes(x,bits):
    if bits<=8:
        xperbyte=8//bits
        xbytes,rem=divmod(x,xperbyte)
        if rem>0: xbytes+=1
    if bits==24:xbytes=x*3
    rem=xbytes&3
    if rem>0: xbytes=xbytes+(4-rem)
    return xbytes

def computepadbytes(x,bits):
    if bits<=8:
        xperbyte=8//bits
        xbytes,rem=divmod(x,xperbyte)
        if rem>0: xbytes+=1
    if bits==24:xbytes=x*3
    rem=xbytes&3
    return iif(rem>0,4-rem,0)

def getdefaultBMPhdrsize(bits): return bmpheadersize[bits]

def computeBMPfilesize(x,y,bits): return computexbytes(x,bits)*y+bmpheadersize[bits]

def compute_bmpmetadata(x,y,bits): return (computeBMPfilesize(x,y,bits),bmpheadersize[bits],x,y,bits)

def isdefaultpal(bmp): return getdefaultbitpal(getcolorbits(bmp))==getallRGBpal(bmp)

def getBMPimgbytes(bmp): return bmp[gethdrsize(bmp):getfilesize(bmp)]

def setBMPimgbytes(bmp,buf): bmp[gethdrsize(bmp):getfilesize(bmp)]=buf

def centerpoint(x1,y1,x2,y2): return ((x2-x1)>>1)+x1,((y2-y1)>>1)+y1

def isinrectbnd(x,y,xmin,ymin,xmax,ymax): return (x<xmax and y<ymax) and (x>xmin and y>ymin)

def listinrecbnd(xylist,xmin,ymin,xmax,ymax):
    retval=True
    for v in xylist:
        if isinrectbnd(v[0],v[1],xmin,ymin,xmax,ymax)==False: break
    return retval

def swapxy(v): return [v[1],v[0]]

def getIFSparams(): return {'fern':(((0,0,0,.16,0,0),(.2,-.26,.23,.22,0,1.6),(-.15,.28,.26,.24,0,.44),(.85,.04,-.04,.85,0,1.6)),(.009,.073,.137,1)),'tree':(((0,.2,0,.5,0,0),(.1,0,0,.1,0,.2),(.42,-.42,.42,.42,0,.2),(.42,.42,-.42,.42,0,.2)),(.05,.2,.6,1)),'cantortree':(((1/3,0,0,1/3,0,0),(1/3,0,0,1/3,1,0),(2/3,0,0,2/3,0.5,0.5),(0,0,0,0,0,0)),(1/3,2/3,1,1)),'sierpinskitriamgle':(((.5,0,0,.5,0,0),(.5,0,0,.5,1,0),(.5,0,0,.5,.5,.5),(0,0,0,0,0,0)),(1/3,2/3,1,1))}

def mandelparamdict(): return {'maxdefault':(1.75,-1.75,1.5,-1.5),'maxeqdim':(1.75,-1.75,1.75,-1.75),'middefault':(.75,-1.25,1.25,-1.25),'mindefault':(.75,-.75,.5,-.5),'mineqdim':(.5,-.5,.5,-.5),'custom1':(-.5,-.7,-.5,-.7)}

def mandelbrot(bmp,x1,y1,x2,y2,mandelparam,RGBfactors,maxiter):
    maxcolors=getmaxcolors(bmp)
    mcolor=maxcolors-1
    Pmax,Pmin,Qmax,Qmin=mandelparam[0],mandelparam[1],mandelparam[2],mandelparam[3]
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    maxx,maxy=x2-x1,y2-y1
    dp,dq,max_size=(Pmax-Pmin)/maxx,(Qmax-Qmin)/maxy,4
    for y in range(y1,y2,1):
        Q=Qmin+(y-y1)*dq
        for x in range(x1,x2,1):
            P,xp,yp,c,Xsq,Ysq=Pmin+(x-x1)*dp,0,0,0,0,0
            while (Xsq+Ysq)<max_size:
                 xp,yp=Xsq-Ysq+P,2*xp*yp+Q
                 Xsq,Ysq=xp*xp,yp*yp
                 c+=1
                 if c>maxiter: break
            if bmp[bmpcolorbits]==24:c=colormix(((255-c)*20)%256,RGBfactors)
            else: c=mcolor-c%maxcolors
            plotxybit(bmp,x,y,c)

def IFS(bmp,IFStransparam,x1,y1,x2,y2,xscale,yscale,xoffset,yoffset,color,maxiter):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    af,p,x,y=IFStransparam[0],IFStransparam[1],x1,y1
    dy,i=y2-y1,0
    while i<maxiter:
        j=random()
        t=af[iif(j<p[0],0,iif(j<p[1],1,iif(j<p[2],2,3)))]
        nx=t[0]*x+t[1]*y+t[4]
        x,y=nx,t[2]*x+t[3]*y+t[5]
        px,py=int(x*xscale+xoffset+x1),int((dy-y*yscale+yoffset)+y1)
        if isinrectbnd(px,py,x1,y1,x2,y2): plotxybit(bmp,px,py,color)
        i+=1

def plotflower(bmp,cx,cy,r,petals,angrot,lumrange,RGBfactors):
    maxcolors=getmaxcolors(bmp)
    mcolor=maxcolors-1
    lum1,dlum=range2baseanddelta(lumrange)
    p,angmax,angrot=petals/2,360*petals,radians(angrot)
    for a in range(0,angmax):
        ang=radians(a/petals)
        f,rang=cos(p*ang)**2,ang+angrot
        x,y=int(cx-r*sin(rang)*f),int(cy-r*cos(rang)*f)
        c=colormix(setmax(abs(int(lum1+dlum*(distance([x,y],[cx,cy])/r))),255),RGBfactors)
        if bmp[bmpcolorbits]!=24: c=mcolor-c%maxcolors
        plotxybit(bmp,x,y,c)

def plotfilledflower(bmp,cx,cy,r,petals,angrot,lumrange,RGBfactors):
    for nr in range (r,2,-1): plotflower(bmp,cx,cy,nr,petals,angrot,lumrange,RGBfactors)

def plotbitsastext(bits):
    mask=128
    while mask>0:
        if (mask & bits)==0: print(' ',end='')
        else: print('*',end='')
        mask=mask>>1

def plotbmpastext(bmp):#cant output 24 bit bmp
    bits,my,r,offset=getcolorbits(bmp),getmaxy(bmp)-1,getxcharcount(bmp),gethdrsize(bmp)
    for y in range(my,0,-1):
        for x in range(0,r):
            if bits==1: plotbitsastext(bmp[offset+r*y+x])
            if bits==4:
                c0,c1=divmod(bmp[offset+r*y+x],16)
                print(chr(97+c0)+chr(97+c1),end='')
            if bits==8: print(chr(bmp[offset+r*y+x]),end='')
        print()

def plot8bitpatternastext(bitpattern,onechar,zerochar):
    s=""
    for bits in bitpattern:
        mask=128
        while mask>0:
            s+=iif(mask & bits>0,onechar,zerochar)
            mask=mask>>1
        s+='\n'
    return s

def enumletters(st):
    c,i=len(st),0
    while i<c:
        yield st[i:i+1]
        i+=1

def enumreverseletters(st):
    i=len(st)-1
    while i>-1:
        yield st[i:i+1]
        i-=1

def char2int(charcodestr):
    place,strhash=0,0
    for c in enumletters(charcodestr):
        strhash=strhash+ord(c)*(256**place)
        place+=1
    return strhash

def setbmppal(bmp,pallist):
    c=0
    if len(pallist)==getmaxcolors(bmp):
        for p in pallist:
            setRGBpal(bmp,c,p[0],p[1],p[2])
            c+=1

def getallRGBpal(bmp):
    colors=getmaxcolors(bmp)
    return [getRGBpal(bmp,c) for c in range(0,colors)]

def getRGBpal(bmp,c):
    i=bmppal+(c<<2)
    return [bmp[i+2],bmp[i+1],bmp[i]]

def setRGBpal(bmp,c,r,g,b):
    start=bmppal+(c<<2)
    end=start+3
    bmp[start:end]=RGBtoBGRarr(r,g,b)

def dict2descorderlist(d):
    l=[]
    for k in d: l.append([d[k],k])
    l.sort()
    l.reverse()
    return l

def colorhistorgram(bmp):
    d={}
    for v in iterimagecolor(bmp,sysmsg['colorhist'],'*',sysmsg['done']):
        c=v[1]
        if c not in d: d.setdefault(c,1)
        else: d[c]+=1
    return  dict2descorderlist(d)

def makenewpalfromcolorhist(chist,colors,similaritythreshold):
    newpal,palcnt,colorcount=[[0,0,0]],1,len(chist)
    for i in range(0,colorcount):
        rgb=int2RGBlist(chist[i][1])
        addcl=True
        for palentry in newpal:
            if distance(palentry,rgb)<similaritythreshold: addcl=False
        if addcl:
            print(palcnt, '=' ,rgb)
            newpal.append(rgb)
            palcnt+=1
        if palcnt==colors: break
    return newpal

def copyBMPhdr(bmp):
    hdrsize,newbmp=gethdrsize(bmp),array('B',[0]*getfilesize(bmp))
    newbmp[0:hdrsize]=bmp[0:hdrsize]
    return newbmp

def copyRGBpal(sourceBMP,destBMP):
    hdl=gethdrsize(sourceBMP)
    destBMP[bmppal:hdl]=sourceBMP[bmppal:hdl]

def setbmp_properties(bmpmeta):
    bmp,filesize,hdrsize,x,y,bits=array('B'),bmpmeta[0],bmpmeta[1],bmpmeta[2],bmpmeta[3],bmpmeta[4]
    bmp.frombytes(b'\x00'*(filesize))
    bmp[0:2]=bmpheaderid
    setfilesize(bmp,filesize)
    sethdrsize(bmp,hdrsize)
    setmaxx(bmp,x)
    setmaxy(bmp,y)
    bmp[bmpcolorbits]=bits
    bmp[14]=40 #required
    if bits<24: setbmppal(bmp,getdefaultbitpal(bits))
    return bmp

def setnewpalfromsourcebmp(sourcebmp,newbmp,similaritythreshold):
    newpal=makenewpalfromcolorhist(colorhistorgram(sourcebmp),getmaxcolors(newbmp),similaritythreshold)
    setbmppal(newbmp,newpal)
    return newpal

def RGBpalbrightnessadjust(bmp,percentadj): return [brightnessadjust(c,percentadj) for c in getallRGBpal(bmp)]

def setBMP2monochrome(bmp,RGBfactors):
    newpal=monochromepal(getcolorbits(bmp),RGBfactors)
    setbmppal(bmp,newpal)
    return newpal

def altsplitbuf(buf):
    m=len(buf)
    if m%2==0: m-=m&1
    return [buf[0:m-1:2],buf[1:m:2]]

def altsplitbuf3way(buf):
    m=len(buf)
    if m%3==0: m-=m&1
    return [buf[0:m-2:3],buf[1:m-1:3],buf[2:m:3]]

def altsplitbufnway(buf,n):
    retval,m,j,i=[],len(buf),n-1,0
    if m%n==0: m-=m&1
    while i<n:
        retval+=[buf[i:m-j:n]]
        i+=1
        j-=1
    return retval

def newBMP(x,y,colorbits): return setbmp_properties(compute_bmpmetadata(x,y,colorbits))

def CopyBMPxydim2newBMP(bmp,newbits): return newBMP(getmaxx(bmp),getmaxy(bmp),newbits)

@checklink
def loadBMP(filename):#loads bitmap to array very fast
    a=array('B')
    with open(filename,'rb') as f: #ucompressed BMP only
        hd=f.read(2)
        if hd!=b'BM': print(sysmsg['notBMP'])
        else:
            fsize=char2int(f.read(8))
            f.seek(0)
            a.frombytes(f.read(fsize))
        f.close()
    return a

def saveBMP(filename,bmp):
    with open(filename,'wb') as f:
        f.write(bmp)
        f.close()

def BMPbitBLTput(bmp,offset,arraybuf):
    hdrsize,bufsize=gethdrsize(bmp),len(arraybuf)
    startoff=hdrsize+offset
    endoff=startoff+bufsize
    if offset>=0 and endoff<=getfilesize(bmp): bmp[startoff:endoff]=arraybuf
    else: print (sysmsg['invalidoffset'])

def BMPbitBLTget(bmp,offset,bufsize):
    hdrsize,retval=gethdrsize(bmp),array('B',[])
    startoff=hdrsize+offset
    endoff=startoff+bufsize
    if (offset>=0 and bufsize>0 ) and endoff<=getfilesize(bmp): retval=bmp[startoff:endoff]
    else: print (sysmsg['invalidoffset'])
    return retval

def vertBMPbitBLTget(bmp,x,y1,y2):
    bits=bmp[bmpcolorbits]
    r,m,c=getxcharcount(bmp),getmaxxy(bmp),getcomputeBMPoffsetwithheaderfunc(bmp)
    if isinrange(x,m[0],-1):
        y1,y2=swapif(y1,y2,y1>y2)
        y1,y2=setmin(y1,0),setmax(y2,m[1]-1)
        s,e=c(bmp,x,y2),c(bmp,x,y1)+r
        if bits==24: return makeBGRbuf(bmp[s:e-2:r],bmp[s+1:e-1:r],bmp[s+2:e:r])
        else: return bmp[s:e:r]
    else: print(sysmsg['lineoutofbnd'])

def applyfuncwithparam2vertBMPbitBLTget(bmp,x,y1,y2,func,funcparam):
    bits=bmp[bmpcolorbits]
    r,m,c=getxcharcount(bmp),getmaxxy(bmp),getcomputeBMPoffsetwithheaderfunc(bmp)
    if isinrange(x,m[0],-1):
        y1,y2=swapif(y1,y2,y1>y2)
        y1,y2=setmin(y1,0),setmax(y2,m[1]-1)
        s,e=c(bmp,x,y2),c(bmp,x,y1)+r
        if bits==24: bmp[s:e-2:r],bmp[s+1:e-1:r],bmp[s+2:e:r]=func(bmp[s:e-2:r],funcparam),func(bmp[s+1:e-1:r],funcparam),func(bmp[s+2:e:r],funcparam)
        else: bmp[s:e:r]=func(bmp[s:e:r],funcparam)
    else: print(sysmsg['lineoutofbnd'])

def plotRGBxybit(bmp,x,y,rgb):
    if isinBMPrectbnd(bmp,x,y):
        if bmp[bmpcolorbits]==24:
            offset=compute24bitBMPoffsetwithheader(bmp,x,y)
            endoffset=offset+3
            bmp[offset:endoffset]= array('B',[rgb[2],rgb[1],rgb[0]])
        else: plotxybit(bmp,x,y,matchRGBtopal(rgb,getallRGBpal(bmp)))

def plotxybit(bmp,x,y,c):
    if isinBMPrectbnd(bmp,x,y):
        offset,bits=computeBMPoffsetwithheader(bmp,x,y),bmp[bmpcolorbits]
        if bits==24:bmp[offset:offset+3]=int2BGRarr(c)
        elif bits==8:bmp[offset]=c&0xff
        elif bits==4:
            if c>15: c&=0xf
            if x&1==1: bmp[offset]=(bmp[offset] & 0xf0)+c
            else: bmp[offset]=(c<<4)+(bmp[offset] & 0xf)
        elif bits==1:
            b,mask=bmp[offset],1<<(7-(x%8))
            if c>1: c=1
            if c==1: b=b | mask
            else:
                if b & mask>0: b=b ^ mask
            bmp[offset]=b

def getxybit(bmp,x,y):
    retval=0
    if isinBMPrectbnd(bmp,x,y):
        offset,bits=computeBMPoffsetwithheader(bmp,x,y),bmp[bmpcolorbits]
        if bits==1:
            mask=7-(x%8)
            retval=(bmp[offset] & (1<<mask))>>mask
        elif bits==4:
            if x&1==1: retval=(bmp[offset] & 0xf)
            else: retval=(bmp[offset] & 0xf0)>>4
        elif bits==8: retval=bmp[offset]
        elif bits==24:retval=RGB2int(bmp[offset+2],bmp[offset+1],bmp[offset])
    else: retval=-1
    return retval

def getRGBxybitvec(bmp,v): return getRGBxybit(bmp,v[0],v[1])

def getRGBxybit(bmp,x,y):
    retval=[]
    if isinBMPrectbnd(bmp,x,y):
        if getcolorbits(bmp)==24:
            i=compute24bitBMPoffsetwithheader(bmp,x,y)
            retval=[bmp[i+2],bmp[i+1],bmp[i]]
        else: retval=getRGBpal(bmp,getxybit(bmp,x,y))
    return retval

def getxybitvec(bmp,v): return getxybit(bmp,v[0],v[1])

def intplotvecxypoint(bmp,v,c): plotxybit(bmp,v[0],v[1],c)

def plotvecxypoint(bmp,v,c):
    v=roundvect(v)
    plotxybit(bmp,v[0],v[1],c)

def plotRGBxybitvec(bmp,v,rgb): plotRGBxybit(bmp,v[0],v[1],rgb)

def plotxypointlist(bmp,vlist,penradius,color):
    for v in vlist: roundpen(bmp,v,penradius,color)

def roundpen(bmp,point,penradius,color):
    x,y=point[0],point[1]
    if penradius<=1: plotxybit(bmp,x,y,color)
    else: circle(bmp,x,y,penradius,color,True)

def swapcolors(bmp,p1,p2):
    c=getxybitvec(bmp,p1)
    intplotvecxypoint(bmp,p1,getxybitvec(bmp,p2))
    intplotvecxypoint(bmp,p2,c)

def line(bmp,x1,y1,x2,y2,color):
    m=getmaxxy(bmp)
    mx,my=m[0]-1,m[1]-1
    x1,x2,y1,y2=setminmax(x1,0,mx),setminmax(x2,0,mx),setminmax(y1,0,my),setminmax(y2,0,my)
    if x1==x2: vertline(bmp,x1,y1,y2,color)
    elif y1==y2: horiline(bmp,y1,x1,x2,color)
    else:
        bits=bmp[bmpcolorbits]
        c=getcomputeBMPoffsetwithheaderfunc(bmp)
        if bits==24:
            buf=int2BGRarr(color)
            for p in iterline((x1,y1),(x2,y2)):
                s=c(bmp,p[0],p[1])
                bmp[s:s+3]=buf
        elif bits==8:
            color&=0xff
            for p in iterline((x1,y1),(x2,y2)): bmp[c(bmp,p[0],p[1])]=color
        elif bits==4:
            if color>15: color&=0xf
            for p in iterline((x1,y1),(x2,y2)):
                s=c(bmp,p[0],p[1])
                if p[0]&1==1: bmp[s]=(bmp[s]&0xf0)+color
                else: bmp[s]=(color<<4)+(bmp[s]&0xf)
        elif bits==1:
            if color>1: color&=0x1
            for p in iterline((x1,y1),(x2,y2)):
                s=c(bmp,p[0],p[1])
                b,mask=bmp[s],1<<(7-(p[0]%8))
                if color==1: b=b | mask
                else:
                    if b & mask>0: b=b ^ mask
                bmp[s]=b

def horiline(bmp,y,x1,x2,color):
    bits,m=bmp[bmpcolorbits],getmaxxy(bmp)
    if isinrange(y,m[1],-1):
        x1,x2=swapif(x1,x2,x1>x2)
        x1,x2=setmin(x1,0),setmax(x2,m[0]-1)
        dx=x2-x1+1
        s=computeBMPoffsetwithheader(bmp,x1,y)
        if bits==24:
            e=s+(dx*3)
            rgb=int2RGBlist(color)
            bmp[s:e]=array('B',[rgb[2],rgb[1],rgb[0]]*dx)
        elif bits==8:
            e=s+dx
            color&=0xff
            bmp[s:e]=array('B',[color]*dx)
        elif bits==4:
            dx>>=1
            e=s+dx
            color&=0xf
            c1,c2=-1,(color<<4)+color
            if x1&1==1: c1=(bmp[s] & 0xf0)
            bmp[s:e]=array('B',[c2]*dx)
            if c1!=-1: bmp[s]=c1+(bmp[s] & 0xf)
            if x2&1==1: plotxybit(bmp,x2-1,y,color)
        elif bits==1:
            x2+=1
            for x in range(x1,x2): plotxybit(bmp,x,y,color)
    else: print(sysmsg['lineoutofbnd'])

def vertline(bmp,x,y1,y2,color):
    bits=bmp[bmpcolorbits]
    if bits not in [24,8]:
        y1,y2=swapif(y1,y2,y1>y2)
        y2+=1
        for y in range(y1,y2): plotxybit(bmp,x,y,color)
    else:
        r,m,c=getxcharcount(bmp),getmaxxy(bmp),getcomputeBMPoffsetwithheaderfunc(bmp)
        if isinrange(x,m[0],-1):
            y1,y2=swapif(y1,y2,y1>y2)
            y1,y2=setmin(y1,0),setmax(y2,m[1]-1)
            dy,rgb=y2-y1+1,int2RGBlist(color)
            s,e=c(bmp,x,y2),c(bmp,x,y1)+r
            if bits==24: bmp[s:e-2:r],bmp[s+1:e-1:r],bmp[s+2:e:r]=array('B',[rgb[2]]*dy),array('B',[rgb[1]]*dy),array('B',[rgb[0]]*dy)
            elif bits==8: bmp[s:e:r]=array('B',[color%256]*dy)
        else: print(sysmsg['lineoutofbnd'])

def fillbackgroundwithgrad(bmp,lumrange,RGBfactors,direction): filledgradrect(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,lumrange,RGBfactors,direction)

@func8and24bitonlyandentirerectinboundary
def filledgradrect(bmp,x1,y1,x2,y2,lumrange,RGBfactors,direction):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)   
    dx,dy=x2-x1+1,y2-y1+1
    base,lrange=RGBfactorstoBaseandRange(lumrange,RGBfactors)
    if direction==0:
        xlim=x2+1
        for x in range(x1,xlim):
            f=x/dx
            c=RGB2int(round(base[0]+lrange[0]*f),round(base[1]+lrange[1]*f),round(base[2]+lrange[2]*f))
            if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
            vertline(bmp,x,y1,y2,c)
    else:
        ylim=y2+1
        for y in range(y1,ylim):
            f=y/dy
            c=RGB2int(round(base[0]+lrange[0]*f),round(base[1]+lrange[1]*f),round(base[2]+lrange[2]*f))
            if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
            horiline(bmp,y,x1,x2,c)

@entirerectinboundary            
def itercopyrect(bmp,x1,y1,x2,y2):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    bufsize,r=adjustbufsize(x2-x1+1,bmp[28]),getxcharcount(bmp)
    offset=computeBMPoffset(bmp,x1,y2)
    lim=computeBMPoffset(bmp,x2,y1)+r
    while (offset+bufsize)<=lim:
        yield BMPbitBLTget(bmp,offset,bufsize)
        offset+=r
    
def intlinevec(bmp,u,v,color): line(bmp,u[0],u[1],v[0],v[1],color)

def linevec(bmp,u,v,color): intlinevec(bmp,roundvect(u),roundvect(v),color)

def filledparallelogram(bmp,p1,p2,p3,color):
    for v in iterparallelogram(p1,p2,p3): linevec(bmp,v[0],v[1],color)

def drawvec(bmp,u,v,headsize0fordefault,color):
    vm,anginc=vmag(subvect(u,v)),0.39269908169872414
    hm=iif(headsize0fordefault==0,vm/5,headsize0fordefault)
    a=anglebetween2Dlines(u,v)
    a1,a2=a-anginc,a+anginc
    linevec(bmp,u,v,color)
    def hdaddvect(bmp,v,hm,a1,a2):
        linevec(bmp,v,addvect(v,polar2rectcoord2D([hm,a1])),color)
        linevec(bmp,v,addvect(v,polar2rectcoord2D([hm,a2])),color)
    def hdsubvect(bmp,v,hm,a1,a2):
        linevec(bmp,v,subvect(v,polar2rectcoord2D([hm,a1])),color)
        linevec(bmp,v,subvect(v,polar2rectcoord2D([hm,a2])),color)
    if u[0]<v[0] and u[1]<v[1]: hdsubvect(bmp,v,hm,a1,a2)
    elif u[0]>v[0] and u[1]>v[1]: hdaddvect(bmp,v,hm,a1,a2)
    elif v[1]==u[1] and u[0]<v[0]: hdsubvect(bmp,v,hm,a1,a2)
    elif v[1]==u[1] and u[0]>v[0]: hdaddvect(bmp,v,hm,a1,a2)
    elif v[0]==u[0] and u[1]>v[1]: hdsubvect(bmp,v,hm,a1,a2)
    elif v[0]==u[0] and u[1]<v[1]: hdaddvect(bmp,v,hm,a1,a2)
    elif u[0]<v[0] and u[1]>v[1]: hdsubvect(bmp,v,hm,a1,a2)
    else: hdaddvect(bmp,v,hm,a1,a2)

def thickroundline(bmp,p1,p2,penradius,color):
    for p in iterline(p1,p2): circle(bmp,p[0],p[1],penradius,color,True)

def gradthickroundline(bmp,p1,p2,penradius,lumrange,RGBfactors):
    lum1,lumrang=range2baseanddelta(lumrange)
    for i in range(penradius,0,-1):
        c=colormix(int(lum1+(lumrang*i/penradius)),RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        thickroundline(bmp,p1,p2,i,c)

@intcircleparam24bitonly        
def applynoparam24bitfunctocircregion(bmp,x,y,r,func):
    c=getcomputeBMPoffsetwithheaderfunc(bmp)
    if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r):
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
            bmp[s1:e1]=func(bmp[s1:e1])
            if y1!=y2: bmp[s2:e2]=func(bmp[s2:e2])
    else:
        xmax,ymax=getmaxx(bmp),getmaxy(bmp)
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            x1,x2=setmin(x1,0),setmax(x2,xmax-1)
            if isinrange(y2,ymax,-1):
                s2,e2=c(bmp,x1,y2),c(bmp,x2,y2)
                bmp[s2:e2]=func(bmp[s2:e2])
            if isinrange(y1,ymax,-1) and y2!=y1:
                s1,e1=c(bmp,x1,y1),c(bmp,x2,y1)
                bmp[s1:e1]=func(bmp[s1:e1])

@intcircleparam24bitonly       
def apply24bitfunctocircregion(bmp,x,y,r,func,funcparam):
    c=getcomputeBMPoffsetwithheaderfunc(bmp)
    if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r):
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
            bmp[s1:e1]=func(bmp[s1:e1],funcparam)
            if y2!=y1: bmp[s2:e2]=func(bmp[s2:e2],funcparam)
    else:
        xmax,ymax=getmaxx(bmp),getmaxy(bmp)
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            x1,x2=setmin(x1,0),setmax(x2,xmax-1)
            if isinrange(y2,ymax,-1):
                s2,e2=c(bmp,x1,y2),c(bmp,x2,y2)
                bmp[s2:e2]=func(bmp[s2:e2],funcparam)
            if isinrange(y1,ymax,-1) and y2!=y1:
                s1,e1=c(bmp,x1,y1),c(bmp,x2,y1)
                bmp[s1:e1]=func(bmp[s1:e1],funcparam)

@entirecircleinboundary
def copycircregion2buf(bmp,x,y,r):
    copybuf,c=[getcolorbits(bmp),r],getcomputeBMPoffsetwithheaderfunc(bmp)
    for v in itercirclepartlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        copybuf+=[[bmp[c(bmp,x1,y1):c(bmp,x2,y1)],bmp[c(bmp,x1,y2):c(bmp,x2,y2)]]]
    return copybuf

def pastecirularbuf(bmp,x,y,circbuf):
    if circbuf!=None:
        r,c=circbuf[1],getcomputeBMPoffsetwithheaderfunc(bmp)
        if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r):
            if getcolorbits(bmp)!=circbuf[0]: raise(sysmsg['bitsnotequal'])
            else:
                i=2
                for v in itercirclepartlineedge(r):
                    x1,x2=mirror(x,v[0])
                    y1,y2=mirror(y,v[1])
                    bmp[c(bmp,x1,y1):c(bmp,x2,y1)],bmp[c(bmp,x1,y2):c(bmp,x2,y2)]=circbuf[i][0],circbuf[i][1]
                    i+=1
        else: print(sysmsg['regionoutofbounds'])
    else: print(sysmsg['invalidbuf'])

def copycircregion(bmp,x,y,r,newxy): pastecirularbuf(bmp,newxy[0],newxy[1],copycircregion2buf(bmp,x,y,r))

@intcircleparam
def applynoparamfunctocircregion(bmp,x,y,r,func):
    c=getcomputeBMPoffsetwithheaderfunc(bmp)
    if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r):
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
            bmp[s1:e1]=func(bmp[s1:e1])
            if y1!=y2: bmp[s2:e2]=func(bmp[s2:e2])
    else:
        xmax,ymax=getmaxx(bmp),getmaxy(bmp)
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            x1,x2=setmin(x1,0),setmax(x2,xmax-1)
            if isinrange(y2,ymax,-1):
                s2,e2=c(bmp,x1,y2),c(bmp,x2,y2)
                bmp[s2:e2]=func(bmp[s2:e2])
            if isinrange(y1,ymax,-1) and y2!=y1:
                s1,e1=c(bmp,x1,y1),c(bmp,x2,y1)
                bmp[s1:e1]=func(bmp[s1:e1])

def RGB2BGRbuf(buf):
    m=len(buf)
    buf[0:m-2:3],buf[2:m:3]=buf[2:m:3],buf[0:m-2:3]

@entirecircleinboundary        
def flipXYcircregion(bmp,x,y,r):
    bits,c=bmp[bmpcolorbits],getcomputeBMPoffsetwithheaderfunc(bmp)
    if bits not in [24,8]:
        n=flipXY(bmp)
        for v in itercirclepartlineedge(r):
            x3,x4=mirror(y,v[0])
            y3,y4=mirror(x,v[1])
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            bmp[c(bmp,x1,y1):c(bmp,x2,y1)],bmp[c(bmp,x1,y2):c(bmp,x2,y2)]=n[c(n,x3,y3):c(n,x4,y3)],n[c(n,x3,y4):c(n,x4,y4)]
    else:
        c,buf=getcomputeBMPoffsetwithheaderfunc(bmp),[]
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            x2+=1
            x3,x4=mirror(x,v[1])
            y3,y4=mirror(y,v[0])
            buf+=[[x1,y1,x2,y2,vertBMPbitBLTget(bmp,x3,y3,y4),vertBMPbitBLTget(bmp,x4,y3,y4)]]
        for b in buf:
            x1,y1,x2,y2=b[0],b[1],b[2],b[3]
            bmp[c(bmp,x1,y1):c(bmp,x2,y1)],bmp[c(bmp,x1,y2):c(bmp,x2,y2)]=b[4],b[5]

def fliphoricircregion(bmp,x,y,r): horitransformincircregion(bmp,x,y,r,'F')

@func8and24bitonlyandentirecircleinboundary
def horitransformincircregion(bmp,x,y,r,trans):
    def flip24():  bmp[s1:e1-2:k],bmp[s2:e2-2:k],bmp[s1+1:e1-1:k],bmp[s2+1:e2-1:k],bmp[s1+2:e1:k],bmp[s2+2:e2:k]=bmp[s2:e2-2:k],bmp[s1:e1-2:k],bmp[s2+1:e2-1:k],bmp[s1+1:e1-1:k],bmp[s2+2:e2:k],bmp[s1+2:e1:k]
    def flip8(): bmp[s1:e1:k],bmp[s2:e2:k]=bmp[s2:e2:k],bmp[s1:e1:k]
    def mirror24R(): bmp[s1:e1-2:k],bmp[s1+1:e1-1:k],bmp[s1+2:e1:k]=bmp[s2:e2-2:k],bmp[s2+1:e2-1:k],bmp[s2+2:e2:k]
    def mirror8R(): bmp[s1:e1:k]=bmp[s2:e2:k]
    def mirror24L(): bmp[s2:e2-2:k],bmp[s2+1:e2-1:k],bmp[s2+2:e2:k]=bmp[s1:e1-2:k],bmp[s1+1:e1-1:k],bmp[s1+2:e1:k]
    def mirror8L(): bmp[s2:e2:k]=bmp[s1:e1:k]
    bits,c=bmp[bmpcolorbits],getcomputeBMPoffsetwithheaderfunc(bmp)
    if trans=='L':
        if bits==24: f=mirror24L
        elif bits==8: f=mirror8L
    elif trans=='R':
        if bits==24: f=mirror24R
        elif bits==8: f=mirror8R
    elif trans=='F':
        if bits==24: f=flip24
        elif bits==8: f=flip8
    for v in itercirclepartvertlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        k=getxcharcount(bmp)
        s1,e1,s2,e2=c(bmp,x1,y2),c(bmp,x1,y1)+k,c(bmp,x2,y2),c(bmp,x2,y1)+k
        f()
    
def mirrorleftincircregion(bmp,x,y,r): horitransformincircregion(bmp,x,y,r,'L')

def mirrorrightincircregion(bmp,x,y,r): horitransformincircregion(bmp,x,y,r,'R')

def flipvertcircregion(bmp,x,y,r): verttransformincircregion(bmp,x,y,r,'F')

@entirecircleinboundary
def verttransformincircregion(bmp,x,y,r,transform):
    def mirrorT(): bmp[s2:e2]=bmp[s1:e1]
    def mirrorB(): bmp[s1:e1]=bmp[s2:e2]
    def flip(): bmp[s1:e1],bmp[s2:e2]=bmp[s2:e2],bmp[s1:e1]
    if transform=='T': f=mirrorT
    elif transform=='B': f=mirrorB
    elif transform=='F': f=flip
    c=getcomputeBMPoffsetwithheaderfunc(bmp)
    for v in itercirclepartlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
        f()
    
def mirrortopincircregion(bmp,x,y,r): verttransformincircregion(bmp,x,y,r,'T')

def mirrorbottomincircregion(bmp,x,y,r): verttransformincircregion(bmp,x,y,r,'B')

def mirrortopleftincircregion(bmp,x,y,r):
    mirrorleftincircregion(bmp,x,y,r)
    mirrortopincircregion(bmp,x,y,r)

def mirrortoprightincircregion(bmp,x,y,r):
    mirrorrightincircregion(bmp,x,y,r)
    mirrortopincircregion(bmp,x,y,r)

def mirrorbottomleftincircregion(bmp,x,y,r):
    mirrorleftincircregion(bmp,x,y,r)
    mirrorbottomincircregion(bmp,x,y,r)

def mirrorbottomrightincircregion(bmp,x,y,r):
    mirrorrightincircregion(bmp,x,y,r)
    mirrorbottomincircregion(bmp,x,y,r)

@func24bitonlyandentirecircleinboundary  
def vertbrightnessgrad2circregion(bmp,x,y,r,lumrange):
    c,f=getcomputeBMPoffsetwithheaderfunc(bmp),applybrightnessadjtoBGRbuf
    l,dl,b,=lumrange[0],(lumrange[1]-lumrange[0])/(2*r),y-r
    for v in itercirclepartlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        l1,l2=l+(y1-b)*dl,l+(y2-b)*dl
        s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
        bmp[s1:e1],bmp[s2:e2]=f(bmp[s1:e1],l1),f(bmp[s2:e2],l2)

@func24bitonlyandentirecircleinboundary     
def horibrightnessgrad2circregion(bmp,x,y,r,lumrange):
    f=applybrightnessadjtoBGRbuf
    l,dl,b=lumrange[0],(lumrange[1]-lumrange[0])/(2*r),x-r
    for v in itercirclepartvertlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        applyfuncwithparam2vertBMPbitBLTget(bmp,x1,y1,y2,f,l+(x1-b)*dl)
        if x1!=x2: applyfuncwithparam2vertBMPbitBLTget(bmp,x2,y1,y2,f,l+(x2-b)*dl)

@intcircleparam    
def outlinecircregion(bmp,x,y,r):
    bits,c=bmp[bmpcolorbits],getcomputeBMPoffsetwithheaderfunc(bmp)
    if entirecircleisinboundary(x,y,-1,getmaxx(bmp),-1,getmaxy(bmp),r):
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
            if bits==24:
                bmp[s1:e1]=array('B',xorvect(bmp[s1:e1],bmp[s1+3:e1+3]))
                if y1!=y2: bmp[s2:e2]=array('B',xorvect(bmp[s2:e2],bmp[s2+3:e2+3]))
            else:
                bmp[s1:e1]=array('B',xorvect(bmp[s1:e1],bmp[s1+1:e1+1]))
                if y1!=y2: bmp[s2:e2]=array('B',xorvect(bmp[s2:e2],bmp[s2+1:e2+1]))
    else:
        xmax,ymax=getmaxx(bmp),getmaxy(bmp)
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            x1,x2=setmin(x1,0),setmax(x2,xmax-1)
            if isinrange(y2,ymax,-1):
                s2,e2=c(bmp,x1,y2),c(bmp,x2,y2)
                if bits==24:  bmp[s2:e2]=array('B',xorvect(bmp[s2:e2],bmp[s2+3:e2+3]))
                else: bmp[s2:e2]=array('B',xorvect(bmp[s2:e2],bmp[s2+1:e2+1]))
            if isinrange(y1,ymax,-1) and y2!=y1:
                s1,e1=c(bmp,x1,y1),c(bmp,x2,y1)
                if bits==24: bmp[s1:e1]=array('B',xorvect(bmp[s1:e1],bmp[s1+3:e1+3]))
                else: bmp[s1:e1]=array('B',xorvect(bmp[s1:e1],bmp[s1+1:e1+1]))

def monocircle(bmp,x,y,r):applynoparam24bitfunctocircregion(bmp,x,y,r,monochromefiltertoBGRbuf)

def colorfiltercircregion(bmp,x,y,r,rgbfactors):apply24bitfunctocircregion(bmp,x,y,r,colorfiltertoBGRbuf,rgbfactors)

def gammacorrectcircregion(bmp,x,y,r,gamma):apply24bitfunctocircregion(bmp,x,y,r,gammaBGRbuf,gamma)

def brightnessadjcircregion(bmp,x,y,r,percentadj):apply24bitfunctocircregion(bmp,x,y,r,applybrightnessadjtoBGRbuf,percentadj)

def invertbitsincircregion(bmp,x,y,r):applynoparamfunctocircregion(bmp,x,y,r,invertbitsinbuffer)

def circlevec(bmp,v,r,color,isfilled=None):
    v=roundvect(v)
    circle(bmp,v[0],v[1],r,color,isfilled)

def entirecircleisinboundary(x,y,minx,maxx,miny,maxy,r): return (isinrange(x-r,maxx,minx) and isinrange(x+r,maxx,minx)) and (isinrange(y-r,maxy,miny) and isinrange(y+r,maxy,miny))

def entireellipseisinboundary(x,y,minx,maxx,miny,maxy,b,a): return (isinrange(x-b,maxx,minx) and isinrange(x+b,maxx,minx)) and (isinrange(y-a,maxy,miny) and isinrange(y+a,maxy,miny))

def filledcircle(bmp,x,y,r,color):
    bits=bmp[bmpcolorbits]
    if bits<8:
        for v in itercirclepartlineedge(r):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            horiline(bmp,y1,x1,x2,color)
            horiline(bmp,y2,x1,x2,color)
    else:
        m=getmaxxy(bmp)
        if bits==24:
            for v in itercirclepartlineedge(r):
                x1,x2=mirror(x,v[0])
                y1,y2=mirror(y,v[1])
                x1,x2=setmin(x1,0),setmax(x2,m[0]-1)
                dx,ymax=x2-x1+1,m[1]
                rgb=int2RGBlist(color)
                colorbuf=array('B',[rgb[2],rgb[1],rgb[0]]*dx)
                lbuf=dx*3
                if isinrange(y2,ymax,-1):
                    s=compute24bitBMPoffsetwithheader(bmp,x1,y2)
                    bmp[s:s+lbuf]=colorbuf
                if isinrange(y1,ymax,-1):
                    s=compute24bitBMPoffsetwithheader(bmp,x1,y1)
                    bmp[s:s+lbuf]=colorbuf
        elif bits==8:
            for v in itercirclepartlineedge(r):
                x1,x2=mirror(x,v[0])
                y1,y2=mirror(y,v[1])
                x1,x2=setmin(x1,0),setmax(x2,m[0]-1)
                dx,ymax=x2-x1+1,m[1]
                colorbuf=array('B',[color&0xff]*dx)
                if isinrange(y2,ymax,-1):
                    s=compute8bitBMPoffsetwithheader(bmp,x1,y2)
                    bmp[s:s+dx]=colorbuf
                if isinrange(y1,ymax,-1):
                    s=compute8bitBMPoffsetwithheader(bmp,x1,y1)
                    bmp[s:s+dx]=colorbuf

def circle(bmp,x,y,r,color,isfilled=None):
    if isfilled: filledcircle(bmp,x,y,r,color)
    else:
        m,bits,c=getmaxxy(bmp),bmp[bmpcolorbits],getcomputeBMPoffsetwithheaderfunc(bmp)
        dobndcheck=not entirecircleisinboundary(x,y,-1,m[0],-1,m[1],r)
        if bits==24:
            color=int2BGRarr(color)
            if dobndcheck:
                for p in itercircle(x,y,r):
                    px,py=p[0],p[1]
                    if isinBMPrectbnd(bmp,px,py):
                        s=c(bmp,px,py)
                        bmp[s:s+3]=color
            else:
                for p in itercirclepart(r):
                    x1,x2=mirror(x,p[0])
                    y1,y2=mirror(y,p[1])
                    x3,x4=mirror(x,p[1])
                    y3,y4=mirror(y,p[0])
                    s1,s2,s3,s4,s5,s6,s7,s8=c(bmp,x1,y1),c(bmp,x2,y2),c(bmp,x1,y2),c(bmp,x2,y1),c(bmp,x3,y3),c(bmp,x4,y4),c(bmp,x3,y4),c(bmp,x4,y3)
                    bmp[s1:s1+3]=bmp[s2:s2+3]=bmp[s3:s3+3]=bmp[s4:s4+3]=bmp[s5:s5+3]=bmp[s6:s6+3]=bmp[s7:s7+3]=bmp[s8:s8+3]=color
        elif bits==8:
            if dobndcheck:
                for p in itercircle(x,y,r):
                    px,py=p[0],p[1]
                    if isinBMPrectbnd(bmp,px,py): bmp[c(bmp,px,py)]=color
            else:
                for p in itercirclepart(r):
                    x1,x2=mirror(x,p[0])
                    y1,y2=mirror(y,p[1])
                    bmp[c(bmp,x1,y1)]=bmp[c(bmp,x2,y2)]=bmp[c(bmp,x1,y2)]=bmp[c(bmp,x2,y1)]=color
        else:
            for p in itercircle(x,y,r): plotxybit(bmp,p[0],p[1],color)

def thickcircle(bmp,x,y,r,penradius,color):
    for p in itercircle(x,y,r): circle(bmp,p[0],p[1],penradius,color,True)

def gradthickcircle(bmp,x,y,radius,penradius,lumrange,RGBfactors):
    lum1,lumrang=range2baseanddelta(lumrange)
    for i in range(penradius,0,-1):
        c=colormix(int(lum1+(lumrang*i/penradius)),RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        thickcircle(bmp,x,y,radius,i,c)

def gradcircle(bmp,x,y,radius,lumrange,RGBfactors):
    lum1,lumrang=range2baseanddelta(lumrange)
    for r in range(radius-1,0,-1):
        c=colormix(int(lum1+(lumrang*r/radius)),RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        thickcircle(bmp,x,y,r,2,c)

def thickellipserot(bmp,x,y,b,a,degrot,penradius,color):
    for p in iterellipserot(x,y,b,a,degrot): circle(bmp,p[0],p[1],penradius,color,True)

def gradthickellipserot(bmp,x,y,b,a,degrot,penradius,lumrange,RGBfactors):
    lum1,lumrang=range2baseanddelta(lumrange)
    for i in range(penradius,0,-1):
        c=colormix(int(lum1+(lumrang*i/penradius)),RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        thickellipserot(bmp,x,y,b,a,degrot,i,c)

def filledellipse(bmp,x,y,b,a,color):
    bits=bmp[bmpcolorbits]
    if bits<8:
        for v in iterellipsepart(b,a):
            x1,x2=mirror(x,v[0])
            y1,y2=mirror(y,v[1])
            horiline(bmp,y1,x1,x2,color)
            horiline(bmp,y2,x1,x2,color)
    else:
        m=getmaxxy(bmp)
        if bits==24:
            for v in iterellipsepart(b,a):
                x1,x2=mirror(x,v[0])
                y1,y2=mirror(y,v[1])
                x1,x2=setmin(x1,0),setmax(x2,m[0]-1)
                dx,ymax=x2-x1+1,m[1]
                rgb=int2RGBlist(color)
                colorbuf=array('B',[rgb[2],rgb[1],rgb[0]]*dx)
                lbuf=dx*3
                if isinrange(y2,ymax,-1):
                    s=compute24bitBMPoffsetwithheader(bmp,x1,y2)
                    bmp[s:s+lbuf]=colorbuf
                if isinrange(y1,ymax,-1):
                    s=compute24bitBMPoffsetwithheader(bmp,x1,y1)
                    bmp[s:s+lbuf]=colorbuf
        elif bits==8:
            for v in iterellipsepart(b,a):
                x1,x2=mirror(x,v[0])
                y1,y2=mirror(y,v[1])
                x1,x2=setmin(x1,0),setmax(x2,m[0]-1)
                dx,ymax=x2-x1+1,m[1]
                colorbuf=array('B',[color&0xff]*dx)
                if isinrange(y2,ymax,-1):
                    s=compute8bitBMPoffsetwithheader(bmp,x1,y2)
                    bmp[s:s+dx]=colorbuf
                if isinrange(y1,ymax,-1):
                    s=compute8bitBMPoffsetwithheader(bmp,x1,y1)
                    bmp[s:s+dx]=colorbuf

def ellipse(bmp,x,y,b,a,color,isfilled=None):
    if isfilled: filledellipse(bmp,x,y,b,a,color)
    else:
        m,bits,c=getmaxxy(bmp),bmp[bmpcolorbits],getcomputeBMPoffsetwithheaderfunc(bmp)
        dobndcheck=not entireellipseisinboundary(x,y,-1,m[0],-1,m[1],b,a)
        if bits==24:
            color=int2BGRarr(color)
            if dobndcheck:
                for p in iterellipse(x,y,b,a):
                    px,py=p[0],p[1]
                    if isinBMPrectbnd(bmp,px,py):
                        s=c(bmp,px,py)
                        bmp[s:s+3]=color
            else:
                for p in iterellipse(x,y,b,a):
                    s=c(bmp,p[0],p[1])
                    bmp[s:s+3]=color
        elif bits==8:
            if dobndcheck:
                for p in iterellipse(x,y,b,a):
                    px,py=p[0],p[1]
                    if isinBMPrectbnd(bmp,px,py): bmp[c(bmp,px,py)]=color
            else:
                for p in iterellipse(x,y,b,a):bmp[c(bmp,p[0],p[1])]=color
        else:
            for p in iterellipse(x,y,b,a): plotxybit(bmp,p[0],p[1],color)

def ellipsevert(x,y,b,a): return [v for v in iterellipse(x,y,b,a)]

def gradellipse(bmp,x,y,b,a,lumrange,RGBfactors):
    lum1,lumrang=range2baseanddelta(lumrange)
    r=iif(a>b,a,b)
    a-=r
    b-=r
    for i in range(r,0,-1):
        c=colormix(int(lum1+(lumrang*i/r)),RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        ellipse(bmp,x,y,b+i,a+i,c,True)
        
@intcircleparam
def drawarc(bmp,x,y,r,startdegangle,enddegangle,color,showoutline,fillcolor,isfilled):
    av=arcvert(x,y,r,startdegangle,enddegangle,showoutline)
    for p in av: plotxybit(bmp,p[0],p[1],color)
    if isfilled: fillboundary(bmp,fillpolydata(av,getmaxx(bmp),getmaxy(bmp)),fillcolor)

def rectangle(bmp,x1,y1,x2,y2,color): plotpoly(bmp,recvert(x1,y1,x2,y2),color)

def sortrecpoints(x1,y1,x2,y2):
    x1,x2=swapif(x1,x2,x1>x2)
    y1,y2=swapif(y1,y2,y1>y2)
    return x1,y1,x2,y2

@entirerectinboundary    
def filledrect(bmp,x1,y1,x2,y2,color):
    bits=bmp[bmpcolorbits]
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    if bits not in [8,24]:
        y2+=1
        for y in range(y1,y2): horiline(bmp,y,x1,x2,color)
    else:
        dx,r,rgb,c=x2-x1+1,getxcharcount(bmp),int2RGB(color),getcomputeBMPoffsetwithheaderfunc(bmp)
        if bits==24: buf=array('B',[rgb[2],rgb[1],rgb[0]]*dx)
        elif bits==8: buf=array('B',[matchRGBtopal(rgb,getallRGBpal(bmp))]*dx)
        offset,lim,bufsize,fsize=c(bmp,x1,y2),c(bmp,x2,y1),len(buf),getfilesize(bmp)
        while (offset<=lim) and ((offset+bufsize)<=fsize):
            bmp[offset:offset+bufsize]=buf
            offset+=r

def beziercurve(bmp,pntlist,penradius,color):
    for v in iterbeziercurve(pntlist): roundpen(bmp,v,penradius,color)

def bspline(bmp,pntlist,penradius,color,isclosed,curveback):
    for v in iterbspline(pntlist,isclosed,curveback): roundpen(bmp,v,penradius,color)

def plotrotated8bitpattern(bmp,x,y,bitpattern,scale,pixspace,color):
    inc=scale-1-pixspace
    for bits in bitpattern:
        ox,mask=x,128
        bits=rotatebits(bits)
        while mask>0:
            if (mask & bits)>0:
                if scale==1 or inc<=0: plotxybit(bmp,x,y,color)
                else: filledrect(bmp,x,y,x+inc,y+inc,color)
            mask=mask>>1
            x+=scale
        y+=scale
        x=ox

def plot8bitpattern(bmp,x,y,bitpattern,scale,pixspace,color):
    inc=scale-1-pixspace
    for bits in bitpattern:
        ox,mask=x,128
        while mask>0:
            if (mask & bits)>0:
                if scale==1 or inc<=0: plotxybit(bmp,x,y,color)
                else: filledrect(bmp,x,y,x+inc,y+inc,color)
            mask=mask>>1
            x+=scale
        y+=scale
        x=ox

def plot8bitpatternupsidedown(bmp,x,y,bitpattern,scale,pixspace,color):
    inc=scale-1-pixspace
    i=len(bitpattern)-1
    while i>-1:
        bits=bitpattern[i]
        ox,mask=x,128
        while mask>0:
            if (mask & bits)>0:
                if scale==1 or inc<=0: plotxybit(bmp,x,y,color)
                else: filledrect(bmp,x,y,x+inc,y+inc,color)
            mask=mask>>1
            x+=scale
        y+=scale
        x=ox
        i-=1

def plot8bitpatternsideway(bmp,x,y,bitpattern,scale,pixspace,color):
    inc=scale-1-pixspace
    for bits in bitpattern:
        oy,mask=y,128
        while mask>0:
            if (mask & bits)>0:
                if scale==1 or inc<=0: plotxybit(bmp,x,y,color)
                else: filledrect(bmp,x,y,x+inc,y+inc,color)
            mask=mask>>1
            y-=scale
        x+=scale
        y=oy

def plotstringfunc(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf,orderfunc,fontrenderfunc):
    if spacebetweenchar==0:spacebetweenchar=1
    ox,xstep,ypixels=x,(scale<<3)+spacebetweenchar,fontbuf[0] #x factor 8 since 8 bits in byte
    ystep=ypixels*scale+spacebetweenchar #possible to have 8x16 chars
    for c in orderfunc(str2plot):
        if c=='\n':
            y+=ystep
            x=ox
        elif c=='\t': x+=xstep<<2
        else:
            fontrenderfunc(bmp,x,y,getcharfont(fontbuf,c),scale,pixspace,color)
            x+=xstep

def plotstring(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf): plotstringfunc(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf,enumletters,plot8bitpattern)

def plotstringupsidedown(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf): plotstringfunc(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf,enumletters,plot8bitpatternupsidedown)

def plotreversestring(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf): plotstringfunc(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf,enumreverseletters,plotrotated8bitpattern)

def plotstringsideway(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf):
    if spacebetweenchar==0:spacebetweenchar=1
    oy,xstep,ypixels=y,(scale<<3)+spacebetweenchar,fontbuf[0]
    ystep=ypixels*scale+spacebetweenchar
    for c in enumletters(str2plot):
        if c=='\n':
            x+=ystep #we swap x and y since sideways
            y=oy
        elif c=='\t': y-=xstep<<2 #we swap x and y since sideways
        else:
            plot8bitpatternsideway(bmp,x,y,getcharfont(fontbuf,c),scale,pixspace,color)
            y-=xstep

def plotstringvertical(bmp,x,y,str2plot,scale,pixspace,spacebetweenchar,color,fontbuf):
    if spacebetweenchar==0:spacebetweenchar=1
    oy,ypixels=y,fontbuf[0]
    xstep,ystep=(scale<<3)+spacebetweenchar,ypixels*scale+spacebetweenchar
    for c in enumletters(str2plot):
        if c=='\n':
            x+=xstep
            y=oy
        elif c=='\t': y+=ystep<<2
        else:
            plot8bitpattern(bmp,x,y,getcharfont(fontbuf,c),scale,pixspace,color)
            y+=ystep

def fillboundary(bmp,bndfilldic,color):
    for y in bndfilldic:
        yint=len(bndfilldic[y])
        if yint==1: plotxybit(bmp,bndfilldic[y][0],y,color)
        else:
            for j in range(1,yint):
                x1,x2=bndfilldic[y][j-1],bndfilldic[y][j]
                horiline(bmp,y,x1,x2,color)

def plotpolyfill(bmp,vertlist,color):
    fillboundary(bmp,fillpolydata(polyboundary(vertlist),getmaxx(bmp),getmaxy(bmp)),color)

def thickplotpoly(bmp,vertlist,penradius,color):
    vertcount=len(vertlist)
    for i in range(0,vertcount):
        if i>0: thickroundline(bmp,vertlist[i-1],vertlist[i],penradius,color)
    thickroundline(bmp,vertlist[0],vertlist[vertcount-1],penradius,color)

def plotlines(bmp,vertlist,color):
    vertcount=len(vertlist)
    for i in range(0,vertcount):
        if i>0: linevec(bmp,vertlist[i-1],vertlist[i],color)

def plotpoly(bmp,vertlist,color):
    plotlines(bmp,vertlist,color)
    linevec(bmp,vertlist[0],vertlist[len(vertlist)-1],color)

def plotpolylist(bmp,polylist,color):
    for poly in polylist: plotpoly(bmp,poly,color)

def plotpolyfillist(bmp,sides,RGBfactors):
    polylist,normlist,i=sides[0],sides[1],0
    for poly in polylist:
        c=colormix(int(cosaffin(normlist[i],[0,0,1])*128)+127,RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        plotpolyfill(bmp,poly,c)
        i=i+1

def plot3d(bmp,sides,issolid,RGBfactors,showoutline,outlinecolor):
    if issolid: plotpolyfillist(bmp,sides,RGBfactors)
    if showoutline: plotpolylist(bmp,sides[0],outlinecolor)

def plot3Dsolid(bmp,vertandsides,issolid,RGBfactors,showoutline,outlinecolor,rotvect,transvect3D,d,transvect):
    plot3d(bmp,gensides(perspective(vertandsides[0],rotvect,transvect3D,d),transvect,vertandsides[1]),issolid,RGBfactors,showoutline,outlinecolor)

def gradvert(bmp,vertlist,penradius,lumrange,RGBfactors):
    lum1,lumrang=range2baseanddelta(lumrange)
    for i in range(penradius,0,-1):
        c=colormix(int(lum1+(lumrang*i/penradius)),RGBfactors)
        if bmp[bmpcolorbits]!=24:c=matchRGBtopal(int2RGBarr(c),getallRGBpal(bmp))
        for point in vertlist: roundpen(bmp,point,i,c)

@entirerectinboundary        
def xygrid(bmp,x1,y1,x2,y2,xysteps,color):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    xstep,ystep=xysteps[0],xysteps[1]
    for x in range(x1,x2,xstep): vertline(bmp,x,y1,y2,color)
    for y in range(y1,y2,ystep): horiline(bmp,y,x1,x2,color)

def xygridvec(bmp,u,v,steps,gridcolor): xygrid(bmp,u[0],u[1],v[0],v[1],steps,gridcolor)

def spiralcontrolpointsvert(x,y,step,growthfactor,turns):
    v=[[x,y]]
    inc=step
    while turns>0:
        x+=step
        v.append([x,y])
        step+=inc
        y+=step
        v.append([x,y])
        step+=inc
        x-=step
        v.append([x,y])
        step+=inc
        y-=step
        v.append([x,y])
        turns-=1
        step+=inc
        inc*=growthfactor
    return v

def getdatalisttotal(dlist):
    total=0
    for d in dlist: total+=d[0]
    return total

def genpiechartdata(dlist): #[[20,c['red']],[30,c['brightyellow']]...]
    sa,tot=0,getdatalisttotal(dlist)#more date an be addded tolist
    alist,big=[],-1 #but the value and coler must be present
    for d in dlist:
        p=d[0]/tot
        ea=sa+p*360
        p*=100
        alist.append([sa,ea,d[1],d[0],p])
        if p>=50: big=dlist.index(d)
        sa=ea
    return alist,big

def piechart(bmp,x,y,r,dataandcolorlist):
    alist,big=genpiechartdata(dataandcolorlist)
    if big>-1:#for speed more computions in drawarc
            circle(bmp,x,y,r,alist[big][2],True)
    for a in alist:
        if a[4]<50: drawarc(bmp,x,y,r,a[0],a[1],a[2],True,a[2],True)
    return [alist,big]

def numbervert(bmp,vlist,xadj,yadj,scale,valstart,valstep,pixspace,spacebetweenchar,color,fontbuf,suppresszero,suppresslastnum,rightjustify):
    plot,maxv=False,len(vlist)-1
    for v in vlist:
        i=vlist.index(v)
        if i>0:plot=True
        else:plot=not suppresszero
        if i==maxv and suppresslastnum:plot=False
        stval=str(valstart+i*valstep)
        rjust=0
        if rightjustify:rjust=(len(stval)-1)<<3
        if plot: plotstring(bmp,v[0]+xadj-rjust,v[1]+yadj,stval,scale,pixspace,spacebetweenchar,color,fontbuf)

def vertlinevert(bmp,vlist,linelen,yadj,color):
    for v in vlist: vertline(bmp,v[0],v[1],v[1]+linelen+yadj,color)

def horilinevert(bmp,vlist,linelen,xadj,color):
    for v in vlist: horiline(bmp,v[1],v[0],v[0]+linelen+xadj,color)

def XYaxis(bmp,origin,steps,xylimits,xyvalstarts,xysteps,color,textcolor,showgrid,gridcolor):
    hvert=horizontalvert(origin[1],origin[0],xylimits[0],steps[0])
    vvert=verticalvert(origin[0],origin[1],xylimits[1],-steps[1])
    if showgrid:xygridvec(bmp,origin,xylimits,steps,gridcolor)
    drawvec(bmp,origin,[origin[0],xylimits[1]],10,color)
    drawvec(bmp,origin,[xylimits[0],origin[1]],10,color)
    vertlinevert(bmp,hvert,5,-2,color)
    horilinevert(bmp,vvert,-3,0,color)
    font=font8x14
    numbervert(bmp,vvert,-15,-4,1,xyvalstarts[1],xysteps[1],0,0,textcolor,font,False,False,True)
    numbervert(bmp,hvert,-4,7,1,xyvalstarts[0],xysteps[0],0,0,textcolor,font,False,False,False)
    xvalmax,yvalmax=xyvalstarts[0]+(len(hvert)-1)*xysteps[0],xyvalstarts[1]+(len(vvert)-1)*xysteps[1]
    return (origin,steps,xylimits,xyvalstarts,xysteps,(xvalmax,yvalmax))

def userdef2Dcooordsys2screenxy(x,y,lstcooordinfo):
    origin,steps,xylimits,xyvalstarts,xysteps=lstcooordinfo[0],lstcooordinfo[1],lstcooordinfo[2],lstcooordinfo[3],lstcooordinfo[4]
    x,y=[origin[0]+((x-xyvalstarts[0])/xysteps[0])*steps[0],origin[1]-((y-xyvalstarts[0])/xysteps[1])*steps[1]]
    if x>xylimits[0] or y<xylimits[1]:
        x,y=-1,-1
        print(sysmsg['regionoutofbounds'])
    return [x,y]

def XYscatterplot(bmp,XYdata,XYcoordinfo,showLinearRegLine,reglinecolor):
    for v in XYdata:#[[x,y,radius (max rad 5 ),isfilled],...]
        r,w=v[2],userdef2Dcooordsys2screenxy(v[0],v[1],XYcoordinfo)
        if r>1: circlevec(bmp,w,setmax(r,5),v[3],v[4])
        else: plotvecxypoint(bmp,w,v[3])
    if showLinearRegLine:
        m,b=LSMslope(XYdata),LSMYint(XYdata)
        xmin,xmax=XYcoordinfo[3][0],XYcoordinfo[5][0]
        ymin,ymax=xmin*m+b,xmax*m+b
        u=userdef2Dcooordsys2screenxy(xmin,ymin,XYcoordinfo)
        w=userdef2Dcooordsys2screenxy(xmax,ymax,XYcoordinfo)
        if w==[-1,-1]:
            ymax=XYcoordinfo[5][1]
            xmax=(ymax-b)/m
            w=userdef2Dcooordsys2screenxy(xmax,ymax,XYcoordinfo)
        linevec(bmp,u,w,reglinecolor)

def itergetneighbors(v,mx,my,includecenter):
    x,y=v[0],v[1]
    if x>-1 and y>-1:
        lx,ty,rx,by=x-1,y-1,x+1,y+1
        if ty>0: yield [x,ty]
        if includecenter: yield(v)
        if by<my: yield [x,by]
        if lx>0:
            if ty>0: yield [lx,ty]
            yield [lx,y]
            if by<my: yield [lx,by]
        if rx<mx:
            if ty>0: yield [rx,ty]
            yield [rx,y]
            if by<my: yield [rx,by]

def getneighborlist(v,mx,my,includecenter): return [u for u in itergetneighbors(v,mx,my,includecenter)]

def getneighborcolorlist(bmp,v): return [getRGBxybitvec(bmp,u) for u in itergetneighbors(v,getmaxx(bmp),getmaxy(bmp),True)]

def isimgedge(bmp,v,mx,my,similaritythreshold):
    retval,rgb=False,getRGBxybitvec(bmp,v)
    for u in itergetneighbors(v,mx,my,False):
        if distance(getRGBxybitvec(bmp,u),rgb)>similaritythreshold:
            retval=True
            break
    return retval

def iterimagedgevert(bmp,similaritythreshold):
    m=getmaxxy(bmp)
    for v in iterimageRGB(bmp,sysmsg['edgedetect'],'*',sysmsg['done']):
        for u in itergetneighbors(v[0],m[0],m[1],False):
            if distance(getRGBxybitvec(bmp,u),v[1])>similaritythreshold:
                yield u
                break

def iterimageregionvertbyRGB(bmp,rgb,similaritythreshold):
    for v in iterimageRGB(bmp,sysmsg['edgedetect'],'*',sysmsg['done']):
        if distance(rgb,v[1])<similaritythreshold: yield v[0]

def getimageregionbyRGB(bmp,rgb,similaritythreshold): return [v for v in iterimageregionvertbyRGB(bmp,rgb,similaritythreshold)]

def getimagedgevert(bmp,similaritythreshold): return [v for v in iterimagedgevert(bmp,similaritythreshold)]

def plotimgedges(bmp,similaritythreshold,edgeradius,edgecolor): plotxypointlist(bmp,getimagedgevert(bmp,similaritythreshold),edgeradius,edgecolor)

def getBGRpalbuf(bmp): return bmp[bmppal:gethdrsize(bmp)]

def convertbufto24bit(buf,bgrpalbuf,bits):
    retval=[]
    for b in buf:
        if bits==8:
            s=b<<2
            retval+=bgrpalbuf[s:s+3]
        elif bits==4:
            s1,s2=divmod(b,16)
            s1<<=2
            s2<<=2
            retval+=bgrpalbuf[s1:s1+3]+bgrpalbuf[s2:s2+3]
        elif bits==1:
            for i in enumbits(b):
                s=i<<2
                retval+=bgrpalbuf[s:s+3]
    return array('B',retval)

def upgradeto24bitimage(bmp):
    bits=bmp[bmpcolorbits]
    if bits==24:
        print(sysmsg['is24bit'])
        nbmp=bmp
    else:
        nbmp,bgrpal,mx,my=CopyBMPxydim2newBMP(bmp,24),getBGRpalbuf(bmp),getmaxx(bmp)-1,getmaxy(bmp)-1
        offset,r=computeBMPoffset(nbmp,0,my),getxcharcount(nbmp)
        for buf in itercopyrect(bmp,0,0,mx,my):
            BMPbitBLTput(nbmp,offset,convertbufto24bit(buf,bgrpal,bits))
            offset+=r
    return nbmp

def iterimageRGB(bmp,waitmsg,rowprocind,finishmsg):
    if waitmsg!='': print(waitmsg)
    r,y,offset,b=getxcharcount(bmp),getmaxy(bmp)-1,0,getBMPimgbytes(bmp)
    maxoffset,x,mx,bits=len(b),0,getmaxx(bmp),bmp[28]
    if bits<24: 
        p=getallRGBpal(bmp)
        doff=1
    else:doff=3
    while offset<maxoffset:
        if bits==1:
            c=b[offset]
            bit=7
            while bit>-1:
                if x<mx: yield ((x,y),p[(c & 1<<bit)>>bit])
                x+=1
                bit-=1
        elif bits==4:
            c0,c1=divmod(b[offset],16)
            if x<mx: yield ((x,y),p[c0])
            x+=1
            if x<mx: yield ((x,y),p[c1])
            x+=1
        elif bits==8:
            if x<mx: yield ((x,y),p[b[offset]])
            x+=1
        elif bits==24:
            if x<mx: yield ((x,y),(b[offset+2],b[offset+1],b[offset]))
            x+=1
        if offset%r==0:
            x=0
            y-=1
            if rowprocind!='': print(rowprocind,end='')
        offset+=doff
    print('\n')
    if finishmsg!='': print(finishmsg)

def iterimagecolor(bmp,waitmsg,rowprocind,finishmsg):
    if waitmsg!='': print(waitmsg)
    r,y,offset,b=getxcharcount(bmp),getmaxy(bmp)-1,0,getBMPimgbytes(bmp)
    maxoffset,x,mx,bits=len(b),0,getmaxx(bmp),bmp[bmpcolorbits]
    if bits==24: doff=3
    else: doff=1
    while offset<maxoffset:
        if bits==1:
            c=b[offset]
            bit=7
            while bit>-1:
                if x<mx: yield ((x,y),(c & 1<<bit)>>bit)
                x+=1
                bit-=1
        elif bits==4:
            c0,c1=divmod(b[offset],16)
            if x<mx: yield ((x,y),c0)
            x+=1
            if x<mx: yield ((x,y),c1)
            x+=1
        elif bits==8:
            if x<mx: yield ((x,y),b[offset])
            x+=1
        elif bits==24:
            if x<mx: yield ((x,y),(b[offset+2]<<16)+(b[offset+1]<<8)+b[offset])
            x+=1
        if offset%r==0:
            x=0
            y-=1
            if rowprocind!='': print(rowprocind,end='')
        offset+=doff
    print('\n')
    if finishmsg!='': print(finishmsg)

@entirerectinboundary
def copyrect(bmp,x1,y1,x2,y2):
    retval=array('B',[bmp[bmpcolorbits]])
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    retval+=int2buf(2,x2-x1+2)
    retval+=int2buf(2,y2-y1+1)
    retval+=int2buf(2,adjustbufsize(x2-x1+1,bmp[28]))
    for buf in itercopyrect(bmp,x1,y1,x2,y2):
        retval+=buf
    return retval

def pasterect(bmp,buf,x1,y1):
    if bmp[bmpcolorbits]!=buf[0]:print(sysmsg['bitsnotequal'])
    else:
        x2,y2,r=x1+buf2int(buf[1:3]),y1+buf2int(buf[3:5]),getxcharcount(bmp)
        if listinBMPrecbnd(bmp,((x1,y1),(x2,y2))):
            offset=computeBMPoffset(bmp,x1,y2)
            br=buf2int(buf[5:7])
            startoff,endoff,bufsize=7,br+7,len(buf)
            while startoff<bufsize:
                BMPbitBLTput(bmp,offset,buf[startoff:endoff])
                offset+=r
                startoff=endoff
                endoff+=br
        else: print(sysmsg['regionoutofbounds'])

def convertselection2BMP(buf):
    bmp,bits=-1,buf[0]
    if not isvalidcolorbit(bits): print (sysmsg['invalidbuf'])
    else:
        bmp=newBMP(buf2int(buf[1:3])+1,buf2int(buf[3:5])+1,bits)
        pasterect(bmp,buf,0,0)
    return bmp

def invertimagebits(bmp):
    offset,maxoffset=gethdrsize(bmp),getfilesize(bmp)
    while offset<maxoffset:
        bmp[offset]=255^bmp[offset]
        offset+=1

def erasealternatehorizontallines(bmp,int_eraseeverynline,int_eraseNthline,bytepat):
    bufsize,s1=getxcharcount(bmp),gethdrsize(bmp),
    s2=getfilesize(bmp)-bufsize
    bytepat&=0xff
    blank=array('B', [bytepat]*bufsize)
    i=1
    while s2>s1:
        if i%int_eraseeverynline==int_eraseNthline: bmp[s2:s2+bufsize]=blank
        s2-=bufsize
        i+=1

def eraseeverynthhorizontalline(bmp,n): erasealternatehorizontallines(bmp,n,0,0)

@entirecircleinboundary
def erasealternatehorizontallinesincircregion(bmp,x,y,r,int_eraseeverynline,int_eraseNthline,bytepat):
    c=getcomputeBMPoffsetwithheaderfunc(bmp)
    bytepat&=0xff
    for v in itercirclepartlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        s1,e1,s2,e2=c(bmp,x1,y1),c(bmp,x2,y1),c(bmp,x1,y2),c(bmp,x2,y2)
        if y1%int_eraseeverynline==int_eraseNthline:bmp[s1:e1]=array('B', [bytepat]*(e1-s1))
        if y2%int_eraseeverynline==int_eraseNthline:bmp[s2:e2]=array('B', [bytepat]*(e2-s2))

def eraseeverynthhorizontallineinccircregion(bmp,x,y,r,n):erasealternatehorizontallinesincircregion(bmp,x,y,r,n,0,0)

@entirerectinboundary
def erasealternatehorizontallinesinregion(bmp,x1,y1,x2,y2,int_eraseeverynline,int_eraseNthline,bytepat):
    bytepat&=0xff
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    bufsize,r,f=adjustbufsize(x2-x1+1,bmp[28]),getxcharcount(bmp),getcomputeBMPoffsetwithheaderfunc(bmp)
    s1,s2=f(bmp,x1,y2),f(bmp,x1,y1)
    blank=array('B', [bytepat]*bufsize)
    i=1
    while s2>s1:
        if i%int_eraseeverynline==int_eraseNthline: bmp[s2:s2+bufsize]=blank
        s2-=r
        i+=1

def eraseeverynthhorilineinregion(bmp,x1,y1,x2,y2,n): erasealternatehorizontallinesinregion(bmp,x1,y1,x2,y2,n,0,0)

def verttrans(bmp,trans):
    def flip(): bmp[s1:e1],bmp[s2:e2]=bmp[s2:e2],bmp[s1:e1]
    def mirrortop(): bmp[s1:s1+bufsize]=bmp[s2:s2+bufsize]
    def mirrorbottom(): bmp[s2:s2+bufsize]=bmp[s1:s1+bufsize]
    if trans=='F': f=flip
    elif trans=='T': f=mirrortop
    elif trans=='B': f=mirrorbottom
    bufsize,s1=getxcharcount(bmp),gethdrsize(bmp)
    s2=getfilesize(bmp)-bufsize
    while s1<s2:
        e1,e2=s1+bufsize,s2+bufsize
        f()
        s1+=bufsize
        s2-=bufsize

def flipvertical(bmp): verttrans(bmp,'F')

def mirrortop(bmp): verttrans(bmp,'T')

def mirrorbottom(bmp): verttrans(bmp,'B')

@entirerectinboundary
def verttransregion(bmp,x1,y1,x2,y2,trans):
    def flip(): bmp[s1:e1],bmp[s2:e2]=bmp[s2:e2],bmp[s1:e1]
    def mirrortop(): bmp[s1:s1+bufsize]=bmp[s2:s2+bufsize]
    def mirrorbottom(): bmp[s2:s2+bufsize]=bmp[s1:s1+bufsize]
    if trans=='F': f=flip
    elif trans=='T': f=mirrortop
    elif trans=='B': f=mirrorbottom
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    bufsize,r,c=adjustbufsize(x2-x1+1,bmp[28]),getxcharcount(bmp),getcomputeBMPoffsetwithheaderfunc(bmp)
    s1,s2=c(bmp,x1,y2),c(bmp,x1,y1)
    while s1<s2:
        e1,e2=s1+bufsize,s2+bufsize
        f()
        s1+=r
        s2-=r

def flipverticalregion(bmp,x1,y1,x2,y2): verttransregion(bmp,x1,y1,x2,y2,'F')

def mirrorbottominregion(bmp,x1,y1,x2,y2):  verttransregion(bmp,x1,y1,x2,y2,'B')

def mirrortopinregion(bmp,x1,y1,x2,y2):  verttransregion(bmp,x1,y1,x2,y2,'T')
    
@entirerectinboundary        
def fliphorzontalpixelbased(bmp,x1,y1,x2,y2):
    m=x1+((x2-x1)>>1)
    while x1<=m:
        y=y1
        while y<=y2:
            swapcolors(bmp,(x1,y),(x2,y))
            y+=1
        x1+=1
        x2-=1

@entirerectinboundary    
def fliphverticalalpixelbased(bmp,x1,y1,x2,y2):
    m=y1+((y2-y1)>>1)
    while y1<=m:
        x=x1
        while x<=x2:
            swapcolors(bmp,(x,y1),(x,y2))
            x+=1
        y1+=1
        y2-=1

def flipnibbleinbuf(buf): return array('B',[(b>>4)+((b%16)<<4) for b in buf])

def rotatebitsinbuf(buf): return array('B',[ rotatebits(b) for b in buf])

def flipbuf(buf,bits):
    if bits==24: buf=flip24bitbuf(buf)
    else: buf.reverse()
    if bits==4: buf=flipnibbleinbuf(buf)
    if bits==1: buf=rotatebitsinbuf(buf)
    return buf

@entirerectinboundary    
def horizontalbulkswap(bmp,x1,y1,x2,y2,swapfunc):
    dx={24:1,8:1,4:2,1:8}[bmp[bmpcolorbits]]
    c,r=getcomputeBMPoffsetwithheaderfunc(bmp),getxcharcount(bmp)
    y1,y2=swapif(y1,y2,y1>y2)
    x1,x2=swapif(x1,x2,x1>x2)
    while x1<x2:
        swapfunc(bmp,c(bmp,x1,y2),c(bmp,x1,y1)+r,c(bmp,x2,y2),c(bmp,x2,y1)+r,r)
        x1+=dx
        x2-=dx

def fliphorizontalregion(bmp,x1,y1,x2,y2):
    def swap24bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1-2:r],bmp[s2:e2-2:r],bmp[s1+1:e1-1:r],bmp[s2+1:e2-1:r],bmp[s1+2:e1:r],bmp[s2+2:e2:r]=bmp[s2:e2-2:r],bmp[s1:e1-2:r],bmp[s2+1:e2-1:r],bmp[s1+1:e1-1:r],bmp[s2+2:e2:r],bmp[s1+2:e1:r]
    def swap8bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1:r],bmp[s2:e2:r]=bmp[s2:e2:r],bmp[s1:e1:r]
    def swap4bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1:r],bmp[s2:e2:r]=flipnibbleinbuf(bmp[s2:e2:r]),flipnibbleinbuf(bmp[s1:e1:r])
    def swap1bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1:r],bmp[s2:e2:r]=rotatebitsinbuf(bmp[s2:e2:r]),rotatebitsinbuf(bmp[s1:e1:r])
    horizontalbulkswap(bmp,x1,y1,x2,y2,{24:swap24bit,8:swap8bit,4:swap4bit,1:swap1bit}[bmp[bmpcolorbits]])

def mirrorleftinregion(bmp,x1,y1,x2,y2):
    def swap24bit(bmp,s1,e1,s2,e2,r): bmp[s2:e2-2:r],bmp[s2+1:e2-1:r],bmp[s2+2:e2:r]=bmp[s1:e1-2:r],bmp[s1+1:e1-1:r],bmp[s1+2:e1:r]
    def swap8bit(bmp,s1,e1,s2,e2,r): bmp[s2:e2:r]=bmp[s1:e1:r]
    def swap4bit(bmp,s1,e1,s2,e2,r): bmp[s2:e2:r]=flipnibbleinbuf(bmp[s1:e1:r])
    def swap1bit(bmp,s1,e1,s2,e2,r): bmp[s2:e2:r]=rotatebitsinbuf(bmp[s1:e1:r])
    horizontalbulkswap(bmp,x1,y1,x2,y2,{24:swap24bit,8:swap8bit,4:swap4bit,1:swap1bit}[bmp[bmpcolorbits]])

def mirrorrightinregion(bmp,x1,y1,x2,y2):
    def swap24bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1-2:r],bmp[s1+1:e1-1:r],bmp[s1+2:e1:r]=bmp[s2:e2-2:r],bmp[s2+1:e2-1:r],bmp[s2+2:e2:r]
    def swap8bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1:r]=bmp[s2:e2:r]
    def swap4bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1:r]=flipnibbleinbuf(bmp[s2:e2:r])
    def swap1bit(bmp,s1,e1,s2,e2,r): bmp[s1:e1:r]=rotatebitsinbuf(bmp[s2:e2:r])
    horizontalbulkswap(bmp,x1,y1,x2,y2,{24:swap24bit,8:swap8bit,4:swap4bit,1:swap1bit}[bmp[bmpcolorbits]])

def mirrorleft(bmp): mirrorleftinregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1)

def mirrorright(bmp): mirrorrightinregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1)

def mirrortopleftinregion(bmp,x1,y1,x2,y2):
    mirrorleftinregion(bmp,x1,y1,x2,y2)
    mirrortopinregion(bmp,x1,y1,x2,y2)

def mirrortoprightinregion(bmp,x1,y1,x2,y2):
    mirrorrightinregion(bmp,x1,y1,x2,y2)
    mirrortopinregion(bmp,x1,y1,x2,y2)

def mirrorbottomleftinregion(bmp,x1,y1,x2,y2):
    mirrorleftinregion(bmp,x1,y1,x2,y2)
    mirrorbottominregion(bmp,x1,y1,x2,y2)

def mirrorbottomrightinregion(bmp,x1,y1,x2,y2):
    mirrorrightinregion(bmp,x1,y1,x2,y2)
    mirrorbottominregion(bmp,x1,y1,x2,y2)

def mirrortopleft(bmp):
    mirrorleftinregion(bmp,0,0,getmaxx(bmp)-1,(getmaxy(bmp)-1)//2)
    mirrortop(bmp)

def mirrortopright(bmp):
    mirrorrightinregion(bmp,0,0,getmaxx(bmp)-1,(getmaxy(bmp)-1)//2)
    mirrortop(bmp)

def mirrorbottomleft(bmp):
    ymax=getmaxy(bmp)-1
    mirrorleftinregion(bmp,0,ymax//2,getmaxx(bmp)-1,ymax)
    mirrorbottom(bmp)

def mirrorbottomright(bmp):
    ymax=getmaxy(bmp)-1
    mirrorrightinregion(bmp,0,ymax//2,getmaxx(bmp)-1,ymax)
    mirrorbottom(bmp)

def fliphorizontal(bmp): fliphorizontalregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1)

def flipXY(bmp):
    mx,my,bits=getmaxy(bmp),getmaxx(bmp),bmp[bmpcolorbits]
    nbmp=newBMP(mx,my,bits)
    if bits not in [8,24]:
        copyRGBpal(bmp,nbmp)
        for v in iterimagecolor(bmp,sysmsg['flipXY'],'*',sysmsg['done']): plotxybit(nbmp,v[0][1],v[0][0],v[1])
    else:
        r,offset=getxcharcount(nbmp),0
        mx-=1
        if bits<24: copyRGBpal(bmp,nbmp)
        for y in range(0,my):
            BMPbitBLTput(nbmp,offset,array('B',vertBMPbitBLTget(bmp,y,0,mx)))
            offset+=r
    return nbmp

@entirerectinboundary                  
def itergetcolorfromrectregion(bmp,x1,y1,x2,y2):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    x,y=x1,y1
    while y<=y2:
        x=x1
        while x<=x2:
            yield ((x,y),getxybit(bmp,x,y))
            x+=1
        y+=1

@entirerectinboundary              
def crop(bmp,x1,y1,x2,y2):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    bits=bmp[bmpcolorbits]
    nbmp=newBMP(x2-x1+1,y2-y1+1,bits)
    if bits<8:
        copyRGBpal(bmp,nbmp)
        for v in itergetcolorfromrectregion(bmp,x1,y1,x2,y2):
            intplotvecxypoint(nbmp,subvect(v[0],(x1,y1)),v[1])
    else:
        offset,r=0,getxcharcount(nbmp)
        for buf in itercopyrect(bmp,x1,y1,x2,y2):
            BMPbitBLTput(nbmp,offset,buf)
            offset+=r
    return nbmp

@entirerectinboundary    
def invertregion(bmp,x1,y1,x2,y2):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    bits=bmp[bmpcolorbits]
    if bits<8:
        c=getmaxcolors(bmp)-1
        for v in itergetcolorfromrectregion(bmp,x1,y1,x2,y2):
            intplotvecxypoint(bmp,v[0],getxybitvec(bmp,v[0])^c)
    else:
        offset=iif(bits==24,compute24bitBMPoffset(bmp,x1,y2),compute8bitBMPoffset(bmp,x1,y2))
        r=getxcharcount(bmp)
        for buf in itercopyrect(bmp,x1,y1,x2,y2):
            BMPbitBLTput(bmp,offset,invertbitsinbuffer(buf))
            offset+=r

def monofilterto24bitregion(bmp,x1,y1,x2,y2):applybyrefnoparamfuncto24bitregion(bmp,x1,y1,x2,y2,applymonochromefiltertoBGRbuf)

def monofilterto24bitimage(bmp): monofilterto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1)

def horizontalbrightnessgradto24bitimage(bmp,lumrange):horizontalbrightnessgradto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,lumrange)

def flip24bitbuf(buf):
    buf.reverse()
    RGB2BGRbuf(buf)
    return array('B',buf)

def makeBGRbuf(bbuf,gbuf,rbuf):
    buf=[]
    for b,g,r in zip(bbuf,gbuf,rbuf):
        buf+=[b,g,r]
    return array('B',buf)

def unpack4bitbuf(buf):
    retval=[]
    for b in buf:
        retval+=[b//16, b&0xf]
    return retval

def unpack4bitbufresizeNtimesbigger(buf,n):
    retval=[]
    for b in buf:
        retval+=[b>>4]*n
        retval+=[b&0xf]*n
    return retval

def pack4bitbuf(unpackedbuf):
    retval=[]
    j,i=len(unpackedbuf)-1,0
    while i<j:
        retval+=[(unpackedbuf[i]<<4)+unpackedbuf[i+1]]
        i+=2
    return retval

def resize4bitbufNtimesbigger(buf,n): return array('B',pack4bitbuf(unpack4bitbufresizeNtimesbigger(buf,n)))

def resize8bitbufNtimesbigger(buf,n):
    retval=[]
    for b in buf:
        retval+=[b]*n
    return array('B',retval)

def resize24bitbufNtimesbigger(buf,n):
    c,r=altsplitbuf3way(buf),resize8bitbufNtimesbigger
    return makeBGRbuf(r(c[0],n),r(c[1],n),r(c[2],n))

def resize1bitbufNtimesbigger(buf,n):
    retval=[]
    for b in buf: retval+=packbitlisttobuf(resizebitpattenNtimesbigger(b,n))
    return array('B',retval)

def enumbits(byteval):
    bit=7
    while bit>-1:
        yield  ((byteval & (1<<bit))>>bit)
        bit-=1

def resizebitpattenNtimesbigger(byteval,n):
    retval=[]
    for bit in enumbits(byteval): retval+=[bit]*n
    return retval

def packbitlisttobuf(blist):
    retval,j,i,b=[],len(blist)+1,1,0
    while i<j:
        m=i%8
        b+=blist[i-1]<<(7-m)
        if m==0 and i>1:
            retval+=[b]
            b=0
        i+=1
    return retval

def resizebufNtimesbigger(buf,n,bits):
    f={24:resize24bitbufNtimesbigger,8:resize8bitbufNtimesbigger,4:resize4bitbufNtimesbigger,1:resize1bitbufNtimesbigger}[bits]
    return f(buf,n)

def resizeNtimesbigger(bmp,n):
    bits=bmp[bmpcolorbits]
    m=getmaxxy(bmp)
    nx,ny=m[0]*n,m[1]*n
    nbmp,mx,my=newBMP(nx,ny,bits),m[0]-1,m[1]-1
    ny-=1
    if bits<24:copyRGBpal(bmp,nbmp)
    offset,r=computeBMPoffset(nbmp,0,ny),getxcharcount(nbmp)
    for buf in itercopyrect(bmp,0,0,mx,my):
        nbuf=resizebufNtimesbigger(buf,n,bits)
        i=0
        while i<n:
            BMPbitBLTput(nbmp,offset,nbuf)
            offset+=r
            i+=1
    return nbmp

def colorfilterto24bitregion(bmp,x1,y1,x2,y2,rgbfactors): applybyreffuncto24bitregion(bmp,x1,y1,x2,y2,applycolorfiltertoBGRbuf,rgbfactors)

def colorfilterto24bitimage(bmp,rgbfactors): colorfilterto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,rgbfactors)

def brightnesseadjto24bitregion(bmp,x1,y1,x2,y2,percentadj): applyfuncto24bitregion(bmp,x1,y1,x2,y2,applybrightnessadjtoBGRbuf,percentadj)

def thresholdadjto24bitregion(bmp,x1,y1,x2,y2,lumrange): applyfuncto24bitregion(bmp,x1,y1,x2,y2,applythresholdadjtoBGRbuf,lumrange)

def thresholdadjcircregion(bmp,x,y,r,lumrange):apply24bitfunctocircregion(bmp,x,y,r,applythresholdadjtoBGRbuf,lumrange)

def brightnesseadjto24bitimage(bmp,percentadj): brightnesseadjto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,percentadj)

def thresholdadjto24bitimage(bmp,lumrange): thresholdadjto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,lumrange)

def verticalbrightnessgradto24bitimage(bmp,lumrange):verticalbrightnessgradto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,lumrange)

@func24bitonlyandentirerectinboundary
def applybyrefnoparamfuncto24bitregion(bmp,x1,y1,x2,y2,func):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    offset,r=compute24bitBMPoffset(bmp,x1,y2),getxcharcount(bmp)
    for buf in itercopyrect(bmp,x1,y1,x2,y2):
        func(buf)
        BMPbitBLTput(bmp,offset,buf)
        offset+=r
    
@func24bitonlyandentirerectinboundary
def applybyreffuncto24bitregion(bmp,x1,y1,x2,y2,func,funcparam):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    offset,r=compute24bitBMPoffset(bmp,x1,y2),getxcharcount(bmp)
    for buf in itercopyrect(bmp,x1,y1,x2,y2):
        func(buf,funcparam)
        BMPbitBLTput(bmp,offset,buf)
        offset+=r

@func24bitonlyandentirerectinboundary
def applyfuncto24bitregion(bmp,x1,y1,x2,y2,func,funcparam):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    offset,r=compute24bitBMPoffset(bmp,x1,y2),getxcharcount(bmp)
    for buf in itercopyrect(bmp,x1,y1,x2,y2):
        BMPbitBLTput(bmp,offset,func(buf,funcparam))
        offset+=r

@func24bitonlyandentirerectinboundary
def verticalbrightnessgradto24bitregion(bmp,x1,y1,x2,y2,lumrange):
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    offset,r=compute24bitBMPoffset(bmp,x1,y2),getxcharcount(bmp)
    lum=lumrange[1]
    dlum=(lumrange[0]-lumrange[1])/(y2-y1)
    for buf in itercopyrect(bmp,x1,y1,x2,y2):
        BMPbitBLTput(bmp,offset,applybrightnessadjtoBGRbuf(buf,lum))
        offset+=r
        lum+=dlum

@func24bitonlyandentirerectinboundary
def horizontalbrightnessgradto24bitregion(bmp,x1,y1,x2,y2,lumrange):
    r,c=getxcharcount(bmp),getcomputeBMPoffsetwithheaderfunc(bmp)
    x1,y1,x2,y2=sortrecpoints(x1,y1,x2,y2)
    xlim,f=x2+1,applybrightnessadjtoBGRbuf
    l=lumrange[0]
    dl=(lumrange[1]-lumrange[0])/(x2-x1)
    for x in range(x1,xlim):
        s,e=c(bmp,x,y2),c(bmp,x,y1)
        bmp[s:e-2:r],bmp[s+1:e-1:r],bmp[s+2:e:r]=f(bmp[s:e-2:r],l),f(bmp[s+1:e-1:r],l),f(bmp[s+2:e:r],l)
        l+=dl

@func24bitonlyandentirecircleinboundary 
def magnifyNtimescircregion(bmp,x,y,r,n):
    nx,ny,b,c=x*n,y*n,resizeNtimesbigger(bmp,n),computeBMPoffsetwithheader
    for v in itercirclepartlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        x3,x4=mirror(nx,v[0])
        y3,y4=mirror(ny,v[1])
        bmp[c(bmp,x1,y1):c(bmp,x2,y1)],bmp[c(bmp,x1,y2):c(bmp,x2,y2)]=b[c(b,x3,y3):c(b,x4,y3)],b[c(b,x3,y4):c(b,x4,y4)]

@func24bitonlyandentirecircleinboundary 
def pixelizenxncircregion(bmp,x,y,r,n):
    b,c=pixelizenxn(bmp,n),computeBMPoffsetwithheader
    for v in itercirclepartlineedge(r):
        x1,x2=mirror(x,v[0])
        y1,y2=mirror(y,v[1])
        bmp[c(bmp,x1,y1):c(bmp,x2,y1)],bmp[c(bmp,x1,y2):c(bmp,x2,y2)]=b[c(b,x1,y1):c(b,x2,y1)],b[c(b,x1,y2):c(b,x2,y2)]

def resizesmaller24bitbuf(buflist):
    n,a,m,s=len(buflist),addvectinlist,intscalarmulvect,altsplitbufnway
    c,f=altsplitbuf3way(a(buflist)),1/(n*n)
    return  makeBGRbuf(m(a(s(c[0],n)),f),m(a(s(c[1],n)),f),m(a(s(c[2],n)),f))

@func24bitonly
def resizeNtimessmaller(bmp,n):
    bits,nbmp=bmp[bmpcolorbits],-1
    m=getmaxxy(bmp)
    nx,ny=m[0]//n,m[1]//n
    nbmp,mx,my=newBMP(nx,ny,bits),m[0]-1,m[1]-1
    ny-=1
    offset,r=compute24bitBMPoffset(nbmp,0,ny),getxcharcount(nbmp)
    i,bufl,y=1,[],0
    for buf in itercopyrect(bmp,0,0,mx,my):
        j=i%n
        bufl+=[buf]
        if j==0:
            BMPbitBLTput(nbmp,offset,resizesmaller24bitbuf(bufl))
            offset+=r
            bufl=[]
            y+=1
            if y>ny: break
        i+=1
    return nbmp

def pixelizenxn(bmp,n): return resizeNtimesbigger(resizeNtimessmaller(bmp,n),n)

def adjustcolordicttopal(bmp,colordict):
    if getcolorbits(bmp)<24:
        for color in colordict:
            colordict[color]=matchRGBtopal(int2RGBarr(colordict[color]),getallRGBpal(bmp))

def gammaadjto24bitregion(bmp,x1,y1,x2,y2,gamma): applybyreffuncto24bitregion(bmp,x1,y1,x2,y2,applygammaBGRbuf,gamma)

def gammaadjto24bitimage(bmp,gamma): gammaadjto24bitregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1,gamma)

@entirerectinboundary
def compareimglines(bmp,x1,y1,x2,y2,func):
    offset,r=computeBMPoffset(bmp,x1,y2),getxcharcount(bmp)
    oldbuf=[]
    for buf in itercopyrect(bmp,x1,y1,x2,y2):
        if oldbuf!=[]:
            BMPbitBLTput(bmp,offset,array('B',func(buf,oldbuf)))
            offset+=r
        oldbuf=buf
    BMPbitBLTput(bmp,offset,array('B',func(buf,oldbuf)))

def outlineregion(bmp,x1,y1,x2,y2):compareimglines(bmp,x1,y1,x2,y2,xorvect)

def outline(bmp): outlineregion(bmp,0,0,getmaxx(bmp)-1,getmaxy(bmp)-1)

@intcircleparam
def sphere(bmp,x,y,r,rgbfactors): gradcircle(bmp,x,y,r,[255,0],rgbfactors)

@intcircleparam
def thickencirclearea(bmp,x,y,r,rgbfactors): gradthickcircle(bmp,x,y,r,8,[255,0],rgbfactors)

@entirerectinboundary
def fern(bmp,x1,y1,x2,y2,color): IFS(bmp,getIFSparams()['fern'],x1,y1,x2,y2,abs(y2-y1)//10,abs(y2-y1)//10,abs(x2-x1)//2,0,color,100000)

@checklink
def applybyreffuncwithparamtoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,func,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        func(bmp,x1,y1,x2,y2,funcparam)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savedareafunc']%(func.__name__,x1,y1,x2,y2,ExistingBMPfile,NewBMPfile))

@checklink
def applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,func,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24 : print(sysmsg['not24bit'])
        else:
            func(bmp,x1,y1,x2,y2,funcparam)
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savedareafunc']%(func.__name__,x1,y1,x2,y2,ExistingBMPfile,NewBMPfile))

@checklink        
def applybyref24bitfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else:
            func(bmp,x1,y1,x2,y2)
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savedareafunc']%( func.__name__,x1,y1,x2,y2,ExistingBMPfile,NewBMPfile))

@checklink
def applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        func(bmp,x1,y1,x2,y2)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savedareafunc']%( func.__name__,x1,y1,x2,y2,ExistingBMPfile,NewBMPfile))

@checklink    
def applyfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        bmp=func(bmp,x1,y1,x2,y2)
        if bmp!=None:
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savedareafunc']%( func.__name__,x1,y1,x2,y2,ExistingBMPfile,NewBMPfile))

@checklink
def applybyreffuncandsave(ExistingBMPfile,NewBMPfile,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        func(bmp)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savefunc']%(func.__name__ ,ExistingBMPfile,NewBMPfile))

@checklink    
def applybyreffuncwithparamandsave(ExistingBMPfile,NewBMPfile,func,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:    
        func(bmp,funcparam)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savesingleparamfunc']%(func.__name__,str(funcparam),ExistingBMPfile,NewBMPfile))

@checklink
def applyfuncandsave(ExistingBMPfile,NewBMPfile,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        saveBMP(NewBMPfile,func(bmp))
        print(sysmsg['savefunc']%(func.__name__ ,ExistingBMPfile,NewBMPfile))

@checklink
def apply24bitfuncandsave(ExistingBMPfile,NewBMPfile,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else:
            saveBMP(NewBMPfile,func(bmp))
            print(sysmsg['savefunc']%(func.__name__ ,ExistingBMPfile,NewBMPfile))

@checklink
def apply24bitfuncwithparamandsave(ExistingBMPfile,NewBMPfile,func,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else:
            saveBMP(NewBMPfile,func(bmp,funcparam))
            print(sysmsg['savesingleparamfunc']%(func.__name__,str(funcparam),ExistingBMPfile,NewBMPfile))

@checklink
def apply8bitabovefuncandsave(ExistingBMPfile,NewBMPfile,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits] not in [8,24]: print(sysmsg['not24or8bit'])
        else:
            saveBMP(NewBMPfile,func(bmp))
            print(sysmsg['savefunc']%(func.__name__ ,ExistingBMPfile,NewBMPfile))

@checklink
def applyfunctocircregion(ExistingBMPfile,NewBMPfile,func,x,y,r):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        func(bmp,x,y,r)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savecircfunc']%(func.__name__ ,x,y,r,ExistingBMPfile,NewBMPfile))

@checklink
def applyfunctocircregionwithparam (ExistingBMPfile,NewBMPfile,func,x,y,r,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        func(bmp,x,y,r,funcparam)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savecircfuncwithparam']%(func.__name__ ,x,y,r,funcparam,ExistingBMPfile,NewBMPfile))

@checklink
def apply24bitcoloradjfunctocircregion(ExistingBMPfile,NewBMPfile,func,x,y,r):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else:
            func(bmp,x,y,r)
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savecircfunc']%(func.__name__ ,x,y,r,ExistingBMPfile,NewBMPfile))

@checklink
def apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,func,x,y,r,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else: 
            func(bmp,x,y,r,funcparam)
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savecircfuncwithparam']%(func.__name__ ,x,y,r,funcparam,ExistingBMPfile,NewBMPfile))

@checklink
def applycoloradjfunc(ExistingBMPfile,NewBMPfile,func,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: setbmppal(bmp,[func(c,funcparam) for c in getallRGBpal(bmp)])
        else:
            if func.__name__=='colorfilter': colorfilterto24bitimage(bmp,funcparam)
            elif func.__name__=='brightnessadjust':  brightnesseadjto24bitimage(bmp,funcparam)
            elif func.__name__=='gammacorrect': gammaadjto24bitimage(bmp,funcparam)
            elif func.__name__=='thresholdadjust': thresholdadjto24bitimage(bmp,funcparam)
            else:
                for v in iterimageRGB(bmp,sysmsg['coloradj'],'*',sysmsg['done']):  plotRGBxybitvec(bmp,v[0], func(v[1],funcparam))
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savesingleparamfunc']%(func.__name__,str(funcparam),ExistingBMPfile,NewBMPfile))

@checklink
def apply24bitcoloradjfunc(ExistingBMPfile,NewBMPfile,func,funcparam):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else:
            func(bmp,funcparam)
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savesingleparamfunc']%(func.__name__,str(funcparam),ExistingBMPfile,NewBMPfile))

@checklink        
def applynoparamcoloradjfunc(ExistingBMPfile,NewBMPfile,func):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        if bmp[bmpcolorbits]!=24: setbmppal(bmp,[func(c) for c in getallRGBpal(bmp)])
        else:
            if func.__name__=='monochrome': monofilterto24bitimage(bmp)
            else:
                for v in iterimageRGB(bmp,sysmsg['coloradj'],'*',sysmsg['done']):  plotRGBxybitvec(bmp,v[0], func(v[1]))
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savenoparamfunc']%(func.__name__,ExistingBMPfile,NewBMPfile))

@checklink
def cropBMPandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applyfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,crop)

@checklink
def cropBMPandsaveusingrectbnd(ExistingBMPfile,NewBMPfile,rectbnd): applyfunctoregionandsave(ExistingBMPfile,NewBMPfile,rectbnd[0][0],rectbnd[0][1],rectbnd[1][0]+1,rectbnd[1][1]+1,crop)

@checklinks
def imagecomp(inputfile1,inputfile2,diff_file,func):
    bmp1,bmp2=loadBMP(inputfile1),loadBMP(inputfile2)
    if len(bmp1)>54 and len(bmp2)>54:
        s1,s2=getmaxxyandbits(bmp1),getmaxxyandbits(bmp2)
        if s1!=s2: print(sysmsg['cantcomparefiles']%(s1,s2))
        else:
            bits=s1[1]
            nbmp=CopyBMPxydim2newBMP(bmp1,bits)
            if bits<24:
                pal1,pal2=getallRGBpal(bmp1),getallRGBpal(bmp2)
                if pal1!=pal2: print(sysmsg['diffpal'])
                copyRGBpal(bmp1,nbmp)
            setBMPimgbytes(nbmp,array('B',func(getBMPimgbytes(bmp1),getBMPimgbytes(bmp2))))
            saveBMP(diff_file,nbmp)
            print(sysmsg['savdifffile']%diff_file)
    
@checklink
@functimer
def reduce24bitimagebits(Existing24BMPfile,NewBMPfile,newbits,similaritythreshold,usemonopal,RGBfactors):
    sbmp=loadBMP(Existing24BMPfile)
    if len(sbmp)>54:
        if sbmp[bmpcolorbits]!=24: print(sysmsg['not24bit'])
        else:
            bmp=CopyBMPxydim2newBMP(sbmp,newbits)
            if newbits>1:
                if usemonopal: newpal=setBMP2monochrome(bmp,RGBfactors)
                else: newpal=setnewpalfromsourcebmp(sbmp,bmp,similaritythreshold)
            for v in iterimageRGB(sbmp,sysmsg['colorquant'],'*',sysmsg['done']):
                    if newbits==1: c=probplotRGBto1bit(v[1],2)
                    else: c=matchRGBtopal(v[1],newpal)
                    intplotvecxypoint(bmp,v[0],c)
            saveBMP(NewBMPfile,bmp)
            print(sysmsg['savemod']%(Existing24BMPfile,NewBMPfile))

@checklink
@functimer
def imgregionbyRGB2file(ExistingBMPfile,NewBMPfile,edgeradius,edgecolor,rgb,similaritythreshold,showedgeonly):
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54:
        edge=getimageregionbyRGB(bmp,rgb,similaritythreshold)
        if showedgeonly:bmp=copyBMPhdr(bmp)
        plotxypointlist(bmp,edge,edgeradius,edgecolor)
        saveBMP(NewBMPfile,bmp)
        print(sysmsg['savemod']%(ExistingBMPfile,NewBMPfile))

@functimer
def invertbits2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,invertimagebits)

@functimer
def flipvertical2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,flipvertical)

@functimer
def mirrortop2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrortop)

@functimer
def mirrortopleft2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrortopleft)

@functimer
def mirrortopright2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrortopright)

@functimer
def mirrorbottomleft2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrorbottomleft)

@functimer
def mirrorbottomright2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrorbottomright)

@functimer
def mirrorbottom2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrorbottom)

@functimer
def mirrorleft2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrorleft)

@functimer
def mirrorright2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,mirrorright)

@functimer
def fliphorizontal2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,fliphorizontal)

@functimer
def flipXY2file(ExistingBMPfile,NewBMPfile): applyfuncandsave(ExistingBMPfile,NewBMPfile,flipXY)

@functimer
def flipverticalregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,flipverticalregion)

@functimer
def fliphorizontalregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,fliphorizontalregion)

@functimer
def mirrorleftinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrorleftinregion)

@functimer
def mirrorrightinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrorrightinregion)

@functimer
def mirrortopinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrortopinregion)

@functimer
def mirrorbottominregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrorbottominregion)

@functimer
def mirrortopleftinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrortopleftinregion)

@functimer
def mirrortoprightinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrortoprightinregion)

@functimer
def mirrorbottomleftinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrorbottomleftinregion)

@functimer
def mirrorbottomrightinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,mirrorbottomrightinregion)

@functimer
def invertregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,invertregion)

@functimer
def autocropimg2file(ExistingBMPfile,NewBMPfile,similaritythreshold): 
    bmp=loadBMP(ExistingBMPfile)
    if len(bmp)>54: cropBMPandsaveusingrectbnd(ExistingBMPfile,NewBMPfile,rectboundarycoords(getimagedgevert(bmp,similaritythreshold)))

@functimer
def adjustbrightness2file(ExistingBMPfile,NewBMPfile,percentadj): applycoloradjfunc(ExistingBMPfile,NewBMPfile,brightnessadjust,percentadj)

@functimer
def thresholdadjust2file(ExistingBMPfile,NewBMPfile,lumrange): applycoloradjfunc(ExistingBMPfile,NewBMPfile,thresholdadjust,lumrange)

@functimer
def adjustbrightnessinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,percentadj): applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,brightnesseadjto24bitregion,percentadj)

@functimer
def adjustthresholdinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,lumrange): applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,thresholdadjto24bitregion,lumrange)

@functimer
def colorfilter2file(ExistingBMPfile,NewBMPfile,rgbfactors): applycoloradjfunc(ExistingBMPfile,NewBMPfile,colorfilter,rgbfactors)

@functimer
def monochrome2file(ExistingBMPfile,NewBMPfile): applynoparamcoloradjfunc(ExistingBMPfile,NewBMPfile,monochrome)

@functimer
def colorfilterinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,rgbfactors):  applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,colorfilterto24bitregion,rgbfactors)

@functimer
def monofilterinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyref24bitfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,monofilterto24bitregion)

@functimer
def pixelizenxntofile(ExistingBMPfile,NewBMPfile,n): apply24bitfuncwithparamandsave(ExistingBMPfile,NewBMPfile,pixelizenxn,n)

@functimer
def resizeNtimessmaller2file(ExistingBMPfile,NewBMPfile,n): apply24bitfuncwithparamandsave(ExistingBMPfile,NewBMPfile,resizeNtimessmaller,n)

@functimer
def resizeNtimesbigger2file(ExistingBMPfile,NewBMPfile,n): apply24bitfuncwithparamandsave(ExistingBMPfile,NewBMPfile,resizeNtimesbigger,n)

@functimer
def upgradeto24bitimage2file(ExistingBMPfile,NewBMPfile):applyfuncandsave(ExistingBMPfile,NewBMPfile,upgradeto24bitimage)

@functimer
def gammaadj2file(ExistingBMPfile,NewBMPfile,gamma): applycoloradjfunc(ExistingBMPfile,NewBMPfile,gammacorrect,gamma)

@functimer
def gammaadjtoregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,gamma):  applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,gammaadjto24bitregion,gamma)

@functimer
def eraseeverynthhorilineinregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,n): applybyreffuncwithparamtoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,eraseeverynthhorilineinregion,n)

@functimer
def rectangle2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,color): applybyreffuncwithparamtoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,rectangle,color)

@functimer
def fern2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,color): applybyreffuncwithparamtoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,fern,color)

@functimer
def eraseeverynthhoriline2file(ExistingBMPfile,NewBMPfile,n): applybyreffuncwithparamandsave(ExistingBMPfile,NewBMPfile,eraseeverynthhorizontalline,n)

@functimer
def outlineregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2): applybyreffunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2, outlineregion)

@functimer
def outline2file(ExistingBMPfile,NewBMPfile): applybyreffuncandsave(ExistingBMPfile,NewBMPfile,outline)

@functimer
def imagediff(inputfile1,inputfile2,diff_file): imagecomp(inputfile1,inputfile2,diff_file,xorvect)

@functimer
def showsimilarparts(inputfile1,inputfile2,diff_file): imagecomp(inputfile1,inputfile2,diff_file,andvect)

@functimer
def monochromecircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): apply24bitcoloradjfunctocircregion(ExistingBMPfile,NewBMPfile,monocircle,x,y,r)

@functimer
def invertbitsincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,invertbitsincircregion,x,y,r)

@functimer
def colorfiltercircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,rgbfactors): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,colorfiltercircregion,x,y,r,rgbfactors)

@functimer
def thresholdadjcircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,lumrange): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,thresholdadjcircregion,x,y,r,lumrange)

@functimer
def gammacorrectcircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,gamma): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,gammacorrectcircregion,x,y,r,gamma)

@functimer
def sphere2file(ExistingBMPfile,NewBMPfile,x,y,r,rgbfactors): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,sphere,x,y,r,rgbfactors)

@functimer
def filledcircle2file(ExistingBMPfile,NewBMPfile,x,y,r,color): applyfunctocircregionwithparam(ExistingBMPfile,NewBMPfile,filledcircle,x,y,r,color)

@functimer
def circle2file(ExistingBMPfile,NewBMPfile,x,y,r,color): applyfunctocircregionwithparam(ExistingBMPfile,NewBMPfile,circle,x,y,r,color)

@functimer
def thickencirclearea2file(ExistingBMPfile,NewBMPfile,x,y,r,rgbfactors): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,thickencirclearea,x,y,r,rgbfactors)

@functimer
def brightnessadjcircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,percentadj): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,brightnessadjcircregion,x,y,r,percentadj)

@functimer
def vertbrightnessgrad2circregion2file(ExistingBMPfile,NewBMPfile,x,y,r,lumrange): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,vertbrightnessgrad2circregion,x,y,r,lumrange)

@functimer
def horibrightnessgrad2circregion2file(ExistingBMPfile,NewBMPfile,x,y,r,lumrange): apply24bitcoloradjfuncwithparam2circregion(ExistingBMPfile,NewBMPfile,horibrightnessgrad2circregion,x,y,r,lumrange)

@functimer
def flipvertcircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,flipvertcircregion,x,y,r)

@functimer
def eraseeverynthhorilineinccircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,n): applyfunctocircregionwithparam(ExistingBMPfile,NewBMPfile,eraseeverynthhorizontallineinccircregion,x,y,r,n)

@functimer
def mirrortopincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrortopincircregion,x,y,r)

@functimer
def mirrorbottomincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrorbottomincircregion,x,y,r)

@functimer
def mirrorleftincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrorleftincircregion,x,y,r)

@functimer
def mirrorrightincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrorrightincircregion,x,y,r)

@functimer
def mirrortopleftincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrortopleftincircregion,x,y,r)

@functimer
def mirrorbottomleftincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrorbottomleftincircregion,x,y,r)

@functimer
def mirrortoprightincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrortoprightincircregion,x,y,r)

@functimer
def mirrorbottomrightincircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,mirrorbottomrightincircregion,x,y,r)

@functimer
def fliphoricircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,fliphoricircregion,x,y,r)

@functimer
def outlinecircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,outlinecircregion,x,y,r)

@functimer
def flipXYcircregion2file(ExistingBMPfile,NewBMPfile,x,y,r): applyfunctocircregion(ExistingBMPfile,NewBMPfile,flipXYcircregion,x,y,r)

@functimer
def magnifyNtimescircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,intmagfactor): applyfunctocircregionwithparam(ExistingBMPfile,NewBMPfile,magnifyNtimescircregion,x,y,r,intmagfactor)

@functimer
def pixelizenxncircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,intpixsize): applyfunctocircregionwithparam(ExistingBMPfile,NewBMPfile,pixelizenxncircregion,x,y,r,intpixsize)

@functimer
def copycircregion2file(ExistingBMPfile,NewBMPfile,x,y,r,newxycenterpoint): applyfunctocircregionwithparam(ExistingBMPfile,NewBMPfile,copycircregion,x,y,r,newxycenterpoint)

@functimer
def horizontalbrightnessgrad2file(ExistingBMPfile,NewBMPfile,lumrange): apply24bitcoloradjfunc(ExistingBMPfile,NewBMPfile,horizontalbrightnessgradto24bitimage,lumrange)

@functimer
def horizontalbrightnessgradregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,lumrange): applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,horizontalbrightnessgradto24bitregion,lumrange)

@functimer
def verticalbrightnessgrad2file(ExistingBMPfile,NewBMPfile,lumrange): apply24bitcoloradjfunc(ExistingBMPfile,NewBMPfile,verticalbrightnessgradto24bitimage,lumrange)

@functimer
def verticalbrightnessgradregion2file(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,lumrange): applybyref24bitcolorfunctoregionandsave(ExistingBMPfile,NewBMPfile,x1,y1,x2,y2,verticalbrightnessgradto24bitregion,lumrange)
