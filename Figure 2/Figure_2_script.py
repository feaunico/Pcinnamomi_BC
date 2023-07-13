import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt

fx = open('GrowthData.txt')
ct = fx.readlines()
fx.close()

test = []
App15, Apr15, Spp15, Spr15 = [], [], [], []
temp = ['5','10','15','20','25','30','35']
for x in temp:
    pp, pr = [], []
    for y in ct:
        if y.split('\t')[2] == x:
            if y.split('\t')[0] =='PP15-01':
                pp.append(float(y.split('\t')[-1].replace('\n','')))
            else:
                pr.append(float(y.split('\t')[-1].replace('\n', '')))
    App15.append(np.mean(pp))
    Apr15.append(np.mean(pr))
    Spp15.append(np.std(pp))
    Spr15.append(np.std(pr))
    try:
        print scipy.stats.kruskal(pp,pr)
        test.append((scipy.stats.kruskal(pp,pr)[0],scipy.stats.kruskal(pp,pr)[1]))
    except:
        test.append((1000,1000))
print test

fig = plt.figure(figsize=(8.,5))
ax01= plt.subplot2grid((1, 1), (0, 0))
N = 7
ind = np.arange(N)  # the x locations for the groups
width = 0.3       # the width of the bars
rects1 = ax01.bar(ind, Apr15, width,yerr= Spr15, color='grey', alpha = 1.0,capsize=7)
#rects1[0].set_color('g',alpha=0.5)
rects2 = ax01.bar(ind+width, App15, width,  yerr= Spp15, color='grey', alpha = 0.7,capsize=7)
ax01.set_ylabel("Growth rate (mm/day)" )
tks = [0.15,1.15,2.15,3.15,4.15,5.15,6.15]
ax01.set_xticks(tks)
ax01.set_xticklabels(['5$^\circ$C','10$^\circ$C','15$^\circ$C','20$^\circ$C','25$^\circ$C','30$^\circ$C','35$^\circ$C'])
ax01.set_yticks([0,1,2,3,4,5,6])
ax01.set_yticklabels(['0','1','2','3','4','5',''])

k = 0
for n in test:
    if n[1] <= 0.001:
        ax01.text(tks[k]-0.05,App15[k] + 0.3,'***')
    elif n[1] <= 0.01:
        ax01.text(tks[k]-0.05,App15[k] + 0.3,'**')
    elif n[1] <= 0.05:
        ax01.text(tks[k]-0.05,App15[k] + 0.3,'*')
    k = k + 1
ax01.legend((rects1[0], rects2[0]), ('PR15', 'PP15-01'),frameon=False)


ax01.set_xlabel("Temperature")
plt.savefig('Figure_2.pdf',dpi=600,  format='pdf')