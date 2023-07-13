import itertools
import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
import mpl_toolkits
mpl_toolkits.__path__.append('C:/Python27/Lib/site-packages/mpl_toolkits/')
import random


import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as patches
from scipy.stats import gaussian_kde
from scipy.stats import norm

fig = plt.figure(figsize=(8,6))
ax01= plt.subplot2grid((1, 1), (0, 0))


img = mpimg.imread('RAxML_bipartitions.tree2.png')
imgplot = ax01.imshow(img)

ax01.text(8100,350,'$P. intricata$',color = 'k',fontsize = 4.5)
ax01.plot((7950,7950),(80,470),'k-',linewidth=0.4)
ax01.text(8010,640,'- $P. rubi$',color = 'k',fontsize = 4)
ax01.text(8010,810,'- $P. fragariae$',color = 'k',fontsize = 4)
ax01.text(8000,1150,'$P. formosa$',color = 'k',fontsize = 4.5)
ax01.plot((7950,7950),(890,1280),'k-',linewidth=0.4)
ax01.text(8230,1450,'- $P. xmultiformis$',color = 'k',fontsize = 4)
ax01.text(8450,1780,'$P. cambivora$',color = 'k',fontsize = 4.5)
ax01.plot((8370,8370),(1520,1920),'k-',linewidth=0.4)
ax01.text(8940,2300,'$P. uniformis$',color = 'k',fontsize = 4.5)
ax01.plot((8850,8850),(2030,2430),'k-',linewidth=0.4)
ax01.text(8400,2600,'- $P. xalni$',color = 'k',fontsize = 4)
ax01.text(8650,2770,'- $P. cambivora$',color = 'k',fontsize = 4)
ax01.text(7710,3200,'$P. flexuosa$',color = 'k',fontsize = 4.5)
ax01.plot((7600,7600),(2850,3400),'k-',linewidth=0.4)
ax01.text(7700,3650,'$P. europea$',color = 'k',fontsize = 4.5)
ax01.plot((7625,7625),(3480,3720),'k-',linewidth=0.4)
ax01.text(7500,4150,'$P. uliginosa$',color = 'k',fontsize = 4.5)
ax01.plot((7400,7400),(3820,4390),'k-',linewidth=0.4)
ax01.text(7400,4750,'$P. tyrrhenica$',color = 'k',fontsize = 4.5)
ax01.plot((7300,7300),(4490,4870),'k-',linewidth=0.4)
ax01.text(7200,5200,'$P. vulcanica$',color = 'k',fontsize = 4.5)
ax01.plot((7100,7100),(4980,5340),'k-',linewidth=0.4)
ax01.text(9000,6600,'$P. cinnamomi$',color = 'k',fontsize = 4.5)
ax01.plot((8900,8900),(5930,7110),'k-',linewidth=0.4)
ax01.text(8050,5540,'PR15',fontsize = 3.5,weight='bold')
ax01.text(8050,5695,'PP15-01',fontsize = 3.5,weight='bold')
ax01.text(8050,5850,'PP15-02',fontsize = 3.5,weight='bold')
ax01.text(9580,7270,' - $P. mediterranea$',color = 'k',fontsize = 4)
ax01.text(10700,7600,'$P. parvispora$',color = 'k',fontsize = 4.5)
ax01.plot((10600,10600),(7390,7770),'k-',linewidth=0.4)
ax01.text(2000,8100,'$P. niederhauserii$',color = 'k',fontsize = 4.5)
ax01.plot((1850,1850),(7850,8220),'k-',linewidth=0.4)
ax01.text(2710,8610,'$P. pistaciae$',color = 'k',fontsize = 4.5)
ax01.plot((2550,2550),(8350,8740),'k-',linewidth=0.4)
ax01.text(3770,8930,'- $P. melonis$',color = 'k',fontsize = 4)
ax01.text(3450,9280,'$P. cajani$',color = 'k',fontsize = 4.5)
ax01.plot((3350,3350),(9010,9390),'k-',linewidth=0.4)
ax01.text(3800,9750,'$P. vignae$',color = 'k',fontsize = 4.5)
ax01.plot((3700,3700),(9500,9860),'k-',linewidth=0.4)
ax01.text(1800,10230,'$P. sojae$',color = 'k',fontsize = 4.5)
ax01.plot((1700,1700),(9950,10350),'k-',linewidth=0.4)
ax01.text(2000,10770,'$P. pisi$',color = 'k',fontsize = 4.5)
ax01.plot((1850,1850),(10430,11000),'k-',linewidth=0.4)
ax01.text(1350,11340,'$P. asiatica$',color = 'k',fontsize = 4.5)
ax01.plot((1250,1250),(11100,11450),'k-',linewidth=0.4)
ax01.axis('off')
ax01.plot((9000,9600),(10300,10300),'k-',linewidth=0.5)
ax01.text(8860,10200,'0.02 subst./site',fontsize = 3.5)
plt.savefig('Figure_1.pdf',dpi=800,  format='pdf')


