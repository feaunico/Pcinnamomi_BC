import numpy as np
import matplotlib.pyplot as plt

def create_mortality(temp):
    fx = open('june5_R_PythonInput.txt')
    ct = fx.readlines()
    fx.close()
    ctl, pear, root = [], [], []
    dpi = ['8','15','28','37','45','56']
    for day in dpi:
        m, n = 0.0, 0.0
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'P15_Root':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        n = n + 1
                        if x.split('\t')[4].replace('\n','') == '5' or x.split('\t')[4].replace('\n','') == '4':
                            m = m + 1
        root.append(m/n*100)
    for day in dpi:
        m, n = 0.0, 0.0
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'P15_Pear':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        n = n + 1
                        if x.split('\t')[4].replace('\n','') == '5' or x.split('\t')[4].replace('\n','') == '4':
                            m = m + 1
        pear.append(m / n * 100)

    for day in dpi:
        m, n = 0.0, 0.0
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'Ctl':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        n = n + 1
                        if x.split('\t')[4].replace('\n','') == '5' or x.split('\t')[4].replace('\n','') == '4':
                            m = m + 1
        ctl.append(m / n * 100)
    return root, pear, ctl


def create_symptomatic(temp):   #severity >=2
    fx = open('june5_R_PythonInput.txt')
    ct = fx.readlines()
    fx.close()
    ctl, pear, root = [], [], []
    dpi = ['8','15','28','37','45','56']
    for day in dpi:
        m, n = 0.0, 0.0
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'P15_Root':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        n = n + 1
                        if int(x.split('\t')[4].replace('\n','')) >= 2:
                            m = m + 1
        root.append(m/n*100)
    for day in dpi:
        m, n = 0.0, 0.0
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'P15_Pear':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        n = n + 1
                        if int(x.split('\t')[4].replace('\n','')) >= 2:
                            m = m + 1
        pear.append(m / n * 100)

    for day in dpi:
        m, n = 0.0, 0.0
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'Ctl':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        n = n + 1
                        if int(x.split('\t')[4].replace('\n','')) >= 2:
                            m = m + 1
        ctl.append(m / n * 100)
    return root, pear, ctl

def create_severity(temp):
    fx = open('june5_R_PythonInput.txt')
    ct = fx.readlines()
    fx.close()

    ctl, pear, root = [], [], []
    ctlstd, pearstd, rootstd = [], [], []

    dpi = ['8','15','28','37','45','56']
    for day in dpi:
        tp = []
        for x in ct:

            if x.split('\t')[0] == 'P15_Root':
                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        tp.append(int(x.split('\t')[4].replace('\n','')))
        root.append(np.mean(tp))
        rootstd.append(np.std(tp))

    for day in dpi:
        tp = []
        for x in ct:
            if x.split('\t')[0] == 'P15_Pear':

                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        tp.append(int(x.split('\t')[4].replace('\n','')))
        pear.append(np.mean(tp))
        pearstd.append(np.std(tp))

    for day in dpi:
        tp = []
        for x in ct:
            if x.split('\t')[0] == 'Ctl':
                if x.split('\t')[1] == temp:
                    if x.split('\t')[3] == day:
                        tp.append(int(x.split('\t')[4].replace('\n','')))
        ctl.append(np.mean(tp))
        ctlstd.append(np.std(tp))
    print root, rootstd, pear, pearstd, ctl, ctlstd
    return root, rootstd, pear, pearstd, ctl, ctlstd







fig = plt.figure(figsize=(9,8.5))
ax00 = plt.subplot2grid((3, 2), (0, 0))
ax01 = plt.subplot2grid((3, 2), (0, 1))
ax10 = plt.subplot2grid((3, 2), (1, 0))
ax11 = plt.subplot2grid((3, 2), (1, 1))
ax20 = plt.subplot2grid((3, 2), (2, 0))
ax21 = plt.subplot2grid((3, 2), (2, 1))




y = [8,15,28,37,45,56]
a,b, c,d, e,f = create_severity('15')
ax00.errorbar(y, a, yerr=b, fmt='bo-',capsize=5)
ax00.errorbar(y, c, yerr=d, fmt='go-',capsize=5)
ax00.errorbar(y, e, yerr=f, fmt='ro-',capsize=5)
ax00.set_ylabel('Severity index')
ax00.text(8,1.2,'ns',ha='center',fontsize=8)
ax00.text(14.5,-0.4,'a,',ha='center', color = 'r', fontsize=8)
ax00.text(16,-0.4,'a',ha='center',color = 'b', fontsize=8)
ax00.text(15,1.3,' b',ha='center',color = 'g', fontsize=8)

ax00.text(28,-0.4,'a',ha='center', color = 'r', fontsize=8)
ax00.text(27.5,1.3,'b,',ha='center', color = 'g', fontsize=8)
ax00.text(29,1.3,'b',ha='center', color = 'b', fontsize=8)

ax00.text(37,-0.4,'a',ha='center', color = 'r', fontsize=8)
ax00.text(36.5,1.85,'b,',ha='center', color = 'g', fontsize=8)
ax00.text(38,1.85,'b',ha='center', color = 'b', fontsize=8)

ax00.text(45,-0.4,'a',ha='center', color = 'r', fontsize=8)
ax00.text(44.5,2.1,'b,',ha='center', color = 'g', fontsize=8)
ax00.text(46,2.1,'b',ha='center', color = 'b', fontsize=8)

ax00.text(56,-0.2,'a',ha='center', color = 'r', fontsize=8)
ax00.text(55.5,3.1,'b,',ha='center', color = 'g', fontsize=8)
ax00.text(57,3.1,'b',ha='center', color = 'b', fontsize=8)



a,b, c,d, e,f = create_severity('25')
ax01.errorbar(y, a, yerr=b, fmt='bo-',capsize=5)
ax01.errorbar(y, c, yerr=d, fmt='go-',capsize=5)
ax01.errorbar(y, e, yerr=f, fmt='ro-',capsize=5)

ax01.text(8,1.2,'ns',ha='center',fontsize=8)
ax01.text(15,0.5,'a',ha='center', color = 'r', fontsize=8)
ax01.text(14.5,2.2,'b,',ha='center',color = 'b', fontsize=8)
ax01.text(16,2.2,' b',ha='center',color = 'g', fontsize=8)

ax01.text(28,-0.3,'a',ha='center', color = 'r', fontsize=8)
ax01.text(27.5,4.05,'b,',ha='center', color = 'g', fontsize=8)
ax01.text(29,4.05,'b',ha='center', color = 'b', fontsize=8)

ax01.text(37,-0.3,'a',ha='center', color = 'r', fontsize=8)
ax01.text(36.5,4.1,'b,',ha='center', color = 'g', fontsize=8)
ax01.text(38.0,4.1,'b',ha='center', color = 'b', fontsize=8)

ax01.text(45,-0.25,'a',ha='center', color = 'r', fontsize=8)
ax01.text(44.5,4.3,'b,',ha='center', color = 'g', fontsize=8)
ax01.text(46.0,4.3,'b',ha='center', color = 'b', fontsize=8)

ax01.text(56,-0.1,'a',ha='center', color = 'r', fontsize=8)
ax01.text(55.5,3.7,'b,',ha='center', color = 'g', fontsize=8)
ax01.text(57.0,3.7,'b',ha='center', color = 'b', fontsize=8)








ax00.set_ylim(-0.5,5.5)
ax01.set_ylim(-0.5,5.5)
ax00.set_xticks(y)
ax01.set_xticks(y)
ax00.set_title("15" + "$^\circ$" + "C",fontsize = 16)
ax01.set_title("25$^\circ$C",fontsize = 16)


a, b, c = create_symptomatic('15')
X = np.arange(6)
ax10.bar(X + 0.00, a, color = 'b', width = 0.25)
ax10.bar(X + 0.25, b, color = 'g', width = 0.25)
ax10.bar(X + 0.50, c, color = 'r', width = 0.25)
ax10.set_xticks(X + 0.25)
ax10.set_xticklabels(['8', '15', '28', '37', '45', '56'])
ax10.set_ylabel('% symptomatic seedlings\n(severity index > 1)')

a, b, c = create_symptomatic('25')
X = np.arange(6)
ax11.bar(X + 0.00, a, color = 'b', width = 0.25)
ax11.bar(X + 0.25, b, color = 'g', width = 0.25)
ax11.bar(X + 0.50, c, color = 'r', width = 0.25)
ax11.set_xticks(X + 0.25)
ax11.set_xticklabels(['8', '15', '28', '37', '45', '56'])

a, b, c = create_mortality('25')
X = np.arange(6)
ax21.bar(X + 0.00, a, color = 'b', width = 0.25)
ax21.bar(X + 0.25, b, color = 'g', width = 0.25)
ax21.bar(X + 0.50, c, color = 'r', width = 0.25)
ax21.set_xticks(X + 0.25)
ax21.set_xticklabels(['8', '15', '28', '37', '45', '56'])
ax21.set_ylabel('% dead seedlings')


ax20.axis('off')
#ax20.spines['bottom'].set_visible(False)
#ax20.spines['left'].set_visible(False)

ax20.plot((0.01,0.95),(0.95,0.95),'k-',linewidth=0.4)
ax20.plot((0.95,0.95),(-0.06,0.95),'k-',linewidth=0.4,clip_on=False)
ax20.plot((0.01,0.01),(-0.06,0.95),'k-',linewidth=0.4,clip_on=False)
ax20.plot((0.01,0.95),(-0.06,-0.06),'k-',linewidth=0.4,clip_on=False)


ax20.plot((0.2,0.2),(0.845,0.845),'s',color = 'blue',markersize = 6)
ax20.plot((0.2,0.2),(0.725,0.725),'s',color = 'green',markersize = 6)
ax20.plot((0.2,0.2),(0.605,0.605),'s',color = 'red',markersize = 6)

ax20.text(0.25, 0.82, '$P. cinnamomi$' + ' - PR15')
ax20.text(0.25, 0.7, '$P. cinnamomi$' + ' - PP15-01')
ax20.text(0.25, 0.58, 'Control')

ax20.text(0.05, 0.43, 'Severity index:')

ax20.text(0.05, 0.0, '    1, >20% needles pale-green;\n    2, >20% needles yellow;\n    3, <50% needles brown;\n    4, >50% needles brown;\n    5, all needles brown - seedling dead')

ax00.text(-7.5,5.5,'A',fontsize=15.5)

ax10.text(-2.2,100,'B',fontsize=15.5)

ax20.text(1.01,0.96,'C',fontsize=15.5)
ax10.set_xlabel('days post inoculation')
ax21.set_xlabel('days post inoculation')

ax20.set_ylim([0,1])
ax20.set_xlim([0,1])
ax20.set_xticks([])
ax20.set_yticks([])




plt.savefig('Figure_3.pdf',dpi=600,  format='pdf')