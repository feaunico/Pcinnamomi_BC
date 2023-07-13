

import matplotlib, random, os, sys, glob
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


########################################################
##                                                    ##
#       Validation of the linear SVC model             #
#           with the input SNP dataset                 #
##                                                    ##
###             Generate Supp. Fig S1                  #
########################################################


def linSVC(matrix, header, _C_):
    #build SVC model and fit data to it
    clf = make_pipeline(StandardScaler(),LinearSVC(random_state=0, tol=1e-5, C = _C_))
    clf.fit(matrix, header)
    return clf

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def run_test(error_rate,testC):
    dic = [[],[]]
    ft = open("res_test.xls",'a')
    nbttest = 500                                           #for each k SNPs do 500 random draws
    for g in [2,5,10,15,20,30,40,50, 60, 70, 80, 90, 100]:  # k = 2 to 100 random SNPs :
        nb4test =[]
        for k in range(0,nbttest):                          # do k tests for g SNPs
            cpt = 0
            ssallsnp = allsnp[1:]
            sublist = random.sample(ssallsnp,g)
            pick = random.sample(range(0,183),60)
            matrix = []
            for x in sublist:
                nlin = []
                LINE = x.split('\t')[4:187]
                for y in LINE:
                    nlin.append(y.replace('\n','').replace('0|0','1').replace('0|1','2').replace('1|1','3'))
                matrix.append(nlin)
            matrix = np.array(matrix)
            matrix = matrix.transpose()
            matrix = matrix.astype(float)

            for _pick_ in pick:   #test 60 samples (=1/3 of the individuals of the SNP dataset) with the training set of g SNPs
                test = []
                for x in sublist:
                    LINE = x.split('\t')[4:187]
                    test.append(LINE[_pick_].replace('0|0','1').replace('0|1','2').replace('1|1','3'))
                expected = head[_pick_]
                tochange = random.sample(range(len(test)), int(g * error_rate))
                i = 0
                ntest =[]
                while i < len(test):
                    if i in tochange:
                        if test[i] == '0':
                            ntest.append(random.sample(['1','2'],1)[0])
                        elif test[i] == '1':
                            ntest.append(random.sample(['1','2'],1)[0])
                        else:
                            ntest.append(random.sample(['1','2'],1)[0])
                    else:
                        ntest.append(test[i])
                    i = i + 1
                test = ntest
                test = np.array(test)
                test = test.astype(float)
                clf = linSVC(matrix, head, testC)
                pred = clf.predict([test])
                if pred[0] == expected:
                    cpt = cpt + 1
            nb4test.append(float(cpt)/len(pick))
        dic[0].append(np.mean(nb4test)*100)
        dic[1].append(np.std(nb4test)*100)
        print g, np.mean(nb4test)*100, np.std(nb4test)*100
        print dic
    ft.close()
    return dic


fx = open("All_SNPs.xls")   #tab file that contains the SNPs
allsnp = fx.readlines()
fx.close()

head = allsnp[0].split('\t')[4:-1] + [allsnp[0].split('\t')[-1].replace('\n', '').replace('\r', '')]


dic_0 = run_test(0.0,1)   #no wrong SNPs - all SNP calls are correct
dic_1 = run_test(0.05,1)  #5% of SNPs are wrong


# generate graph with results

fig = plt.figure(figsize=(8,7))
ax1 = plt.subplot2grid((1, 1), (0, 0))

rg = [2,5,10,15,20,30,40,50,60,70,80,90,100]

ax1.errorbar(rg, dic_0[0], yerr=dic_0[1], fmt='bo-', capsize=5)
ax1.errorbar(rg, dic_1[0], yerr=dic_0[1], fmt='go-', capsize=5)
ax1.set_xlim(0,110)
ax1.set_xticks([10,20,30,40,50,60,70,80,90,100])
ax1.set_ylabel('% correct assignment')
ax1.set_xlabel('Number of SNPs')
ax1.plot((72,80),(63,63),'b-')
ax1.text(83,62.8,'No error')
ax1.plot((72,80),(60,60),'g-')
ax1.text(83,59.8,'5% error')


plt.savefig('Figure_supp_1.png',dpi=600,  format='png')