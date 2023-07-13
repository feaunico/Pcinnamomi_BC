

import random, matplotlib, os, sys, glob, time

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.datasets import make_classification

from sklearn.svm import LinearSVC


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def _training_(header, _snp_, listeSNP):   #67
    snp = []
    k = 0
    for x in _snp_:
        if x.split('\t')[0] + '|' + x.split('\t')[1] in listeSNP:
            k = k + 1

            if x not in snp:
                snp.append(x)
    loci = []
    matrix = []
    for x in snp:
        if x.split('\t')[0] != '\n' and x.split('\t')[0] != '':
            ls = []
            Line = x.split('\t')
            Line = Line[4:]

            for y in Line:
                y = y.replace('\n', '').replace('\r', '')
                y = y.replace('0|0', '1').replace('0|1', '2').replace('1|1', '3').replace('2|2', '3').replace('3|3',
                                                                                                              '3').replace(
                    '4|4', '3').replace('5|5', '3').replace('6|6', '3').replace('7|7', '3').replace('8|8', '3').replace(
                    '9|9', '3').replace('.|.', '1')
                ls.append(int(y))
            matrix.append(ls)

            loci.append(x.split('\t')[0] + '|' + x.split('\t')[1])

    matrix = np.array(matrix)
    matrix = matrix.transpose()
    return matrix, header

def linSVC(matrix, header):
    clf = make_pipeline(StandardScaler(),LinearSVC(random_state=0, tol=1e-5,C = 1))
    clf.fit(matrix, header)
    return clf


def firstCheck(q,mx):
        os.system('samtools depth Rs_mapped_sort.bam -Q 60 -q ' + str(q) + ' > depth')
        fsam = open('depth')
        dpt = fsam.readlines()
        fsam.close()

        dmapped = {}
        for x in dpt:
            if int(x.split('\t')[-1].replace('\n','')) >= 1:  #should be 2
                if x.split('\t')[0] not in dmapped:
                    dmapped[x.split('\t')[0]] = []
                dmapped[x.split('\t')[0]].append(x.split('\t')[1])
        sLsAl = []
        k, b = 0, 0
        for x in allsnp[1:]:
            b = b +1
            try:
                if x.split('\t')[1] in dmapped[x.split('\t')[0]]:
                    sLsAl.append(x)
                    k = k + 1
            except:
                pass

        return sLsAl


def runSNPs(listeAL,fnn,raw):
    Outls, LIST_loci = [], []
    total = 0
    done = []
    random.shuffle(listeAL)
    j = 0
    while j < len(listeAL):
        if total < nb_snps:
            SNP = listeAL[j]
            #print SNP
            print('total found', total)
            print(len(done) , len(listeAL) - 1)
            done.append(SNP)
            sc = SNP.split('\t')[0]
            pos = int(SNP.split('\t')[1])
            REF = SNP.split('\t')[2]
            ALT = SNP.split('\t')[3]
            res = os.popen('bcftools mpileup -Ou -r ' + sc + ':' + str(pos) + '-' + str(pos) + ' -f ' + ref + ' ' + nom + '.bam | bcftools call -m').readlines()
            try:
                MQ = res[-1].split('MQ=')[1].split('\t')[0]
                if MQ == '.':
                    MQ = 0.0
                DP4 = res[-1].split('DP4=')[1].split(';')[0]
                DP4 = DP4.split(",")
                DP = 0
                for g in DP4:
                    DP = DP + int(g)
                dicoVal = {'DP': DP, 'MQ': MQ, 'MQ0F': float(res[-1].split('MQ0F=')[1].split(';')[0])}
                genot = res[-1].split('\t')[-1].replace('\n','')
                genot = genot.split(':')[0]
            except:
                genot = './.'
                pass
            try:
                dp = int(dicoVal['DP'])
            except:
                dp = 0
            if genot == '1/1' or genot == '0/1':
                if dicoVal['DP'] >= 2:  
                    fnn.write(res[-1])
                    obref, obalt = res[-1].split('\t')[3], res[-1].split('\t')[4]
                    if obref == REF and obalt == ALT:
                        Outls.append(sc + '|' + str(pos) + '|' + genot)
                        LIST_loci.append(sc + '|' + str(pos))
                        total = total + 1
                        raw.write(SNP.replace('\n','')  + '\t' + str(res[-1]) )
            elif genot == '0/0' and dicoVal['DP'] >= 2:   
                obref, obalt = res[-1].split('\t')[3], res[-1].split('\t')[4]
                if len(obref) == 1 and len(obalt)==1:
                    total = total + 1
                    fnn.write(res[-1])
                    Outls.append(sc + '|' + str(pos) + '|' + genot)
                    LIST_loci.append(sc + '|' + str(pos))
                    raw.write(SNP.replace('\n','') + '\t' + str(res[-1]) )
        else:
            j = len(listeAL)
        j = j + 1
    return total, Outls, LIST_loci


start_time = time.time()



#
#  command line => python ASSIGN_Pcinna.py Phyci1_AssemblyScaffolds.fasta All_SNPs.xls barcode01 50000"




print(len(sys.argv), sys.argv)

if len(sys.argv) == 6:
    reads_folder = sys.argv[3] + ' ' + sys.argv[4]
    training_set = sys.argv[2]
    ref = sys.argv[1]
    nb_snps = int(sys.argv[5])
elif len(sys.argv) == 5:
    reads_folder = sys.argv[3]
    training_set = sys.argv[2]
    ref = sys.argv[1]
    nb_snps = int(sys.argv[4])


else:
    print('usage: python2.7 ASSIGN.py <ref_genome> <training_set> <folder with ON fastq files> <max_nb_of_SNPs')
    exit()



os.system('touch reads.fastq')
for x in glob.glob(reads_folder + '/*.gz'):
    os.system('gzip -d ' + x)

line = ""
for x in glob.glob(reads_folder + '/*.fastq'):
    line = line + x + ' '
os.system('cat ' + line  + ' > reads.fastq')





fx = open(ref)
ct = fx.read().split('>')
fx.close()
ct = ct[1:]

dico = {}
for x in ct:
    dico[x.split('\n',1)[0]] = x.split('\n',1)[1].replace('\n','').replace('\r','') + 'N'*500


########################################################
##                                                    ##
#     training set  - 187 SNPs from Shakya et a. 2021  #
##                                                    ##
########################################################

fx = open(training_set)
allsnp = fx.readlines()
fx.close()

head = allsnp[0].split('\t')[4:-1] + [allsnp[0].split('\t')[-1].replace('\n', '').replace('\r', '')]

print(head)



####################################################################
##                                                                ##
#     Alignment of the reads on the  reference genome              #
##                                                                ##
####################################################################

print("running samtools")

nom = os.path.split(reads_folder)[-1]

#os.system('minimap2 -ax map-ont ' + ref + ' reads.fastq -o Rs.sam')
#os.system('samtools view -b -F 4 Rs.sam > Rs_mapped.bam')
#os.system('samtools sort Rs_mapped.bam -o ' + nom + '.bam')
#os.system('samtools index ' + nom + '.bam')
#os.system('samtools sort Rs_mapped.bam > Rs_mapped_sort.bam')
#os.system('samtools stats Rs_mapped_sort.bam > stats')

############## BWA MAPPING #########
os.system('samtools faidx ' + ref )
os.system('bwa index ' + ref)
#os.system('bwa mem -T 24 ' + ref  + reads + ' > Rs.sam')
os.system('bwa mem -x ont2d -T 14 ' + ref + ' reads.fastq > Rs.sam')   #oxford nanopore 1D
os.system('samtools view -b -F 4 Rs.sam > Rs_mapped.bam')
os.system('samtools sort Rs_mapped.bam -o ' + nom + '.bam')
os.system('samtools index ' + nom + '.bam')
os.system('samtools sort Rs_mapped.bam > Rs_mapped_sort.bam')
os.system('samtools stats Rs_mapped_sort.bam > stats')


ssAl = firstCheck(15,1)
print(len(ssAl))
print(ssAl)

FNN = open('calls.xls', 'w')
RAW = open('raw_calls.txt', 'w')
tot, outls, list_loci = runSNPs(ssAl,FNN,RAW)
FNN.close()
RAW.close()


fx = open('raw_calls.txt')
ctt = fx.readlines()
fx.close()

matrix = []
ls = []

probas = {'pop1':[],'pop2':[],'pop3':[],'pop4':[],'pop5':[]}

for line in ctt:
    LINE = line.split('\t')[4:187]
    smx = []
    for m in LINE:
        smx.append(m.replace('0|0','1').replace('0|1','2').replace('1|1','3'))

    matrix.append(smx)
    if ':' not in line.split('\t')[-1]:
        ls.append(line.split('\t')[-1].replace('\n','').replace('0/0','1').replace('0/1','2').replace('1/1','3'))
    else:
        ls.append(line.split('\t')[-1].split(':')[0].replace('0/0','1').replace('0/1','2').replace('1/1','3'))

    #calculate allele freq in pop1:
    diallele = {'pop1':'','pop2':'','pop3':'','pop4':'','pop5':''}
    PopgenotypeS = [LINE[0:63],LINE[63:99],LINE[99:153],LINE[153:163],LINE[163:182]]
    for gen,pop in zip(PopgenotypeS,diallele):
        #print(gen,pop)

        all0, all1 = 0, 0
        for genotype in gen:
            if genotype == "0|0":
                all0 = all0 + 2
            elif genotype == "0|1":
                all0 = all0 + 1
                all1 = all1 + 1
            else :
                all1 = all1 + 2
        diallele[pop] = (all0,all1)

    #allele frequencies
    print(diallele)
    #print(probas)
    for x in ls:
        if x == '1':  #0|0
            probas['pop1'].append((float(diallele['pop1'][0]) / (diallele['pop1'][0] + diallele['pop1'][1])) ** 2)
            probas['pop2'].append((float(diallele['pop2'][0]) / (diallele['pop2'][0] + diallele['pop2'][1])) ** 2)
            probas['pop3'].append((float(diallele['pop3'][0]) / (diallele['pop3'][0] + diallele['pop3'][1])) ** 2)
            probas['pop4'].append((float(diallele['pop4'][0]) / (diallele['pop4'][0] + diallele['pop4'][1])) ** 2)
            probas['pop5'].append((float(diallele['pop5'][0]) / (diallele['pop5'][0] + diallele['pop5'][1])) ** 2)

        elif x == '3':
            probas['pop1'].append((float(diallele['pop1'][1]) / (diallele['pop1'][0] + diallele['pop1'][1])) ** 2)
            probas['pop2'].append((float(diallele['pop2'][1]) / (diallele['pop2'][0] + diallele['pop2'][1])) ** 2)
            probas['pop3'].append((float(diallele['pop3'][1]) / (diallele['pop3'][0] + diallele['pop3'][1])) ** 2)
            probas['pop4'].append((float(diallele['pop4'][1]) / (diallele['pop4'][0] + diallele['pop4'][1])) ** 2)
            probas['pop5'].append((float(diallele['pop5'][1]) / (diallele['pop5'][0] + diallele['pop5'][1])) ** 2)

        elif x == '2':
            probas['pop1'].append((float(diallele['pop1'][1]) / (diallele['pop1'][0] + diallele['pop1'][1])) * (diallele['pop1'][0] / (diallele['pop1'][0] + diallele['pop1'][1])) * 2)
            probas['pop2'].append((float(diallele['pop2'][1]) / (diallele['pop2'][0] + diallele['pop2'][1])) * (diallele['pop2'][0] / (diallele['pop2'][0] + diallele['pop2'][1])) * 2)
            probas['pop3'].append((float(diallele['pop3'][1]) / (diallele['pop3'][0] + diallele['pop3'][1])) * (diallele['pop3'][0] / (diallele['pop3'][0] + diallele['pop3'][1])) * 2)
            probas['pop4'].append((float(diallele['pop4'][1]) / (diallele['pop4'][0] + diallele['pop4'][1])) * (diallele['pop4'][0] / (diallele['pop4'][0] + diallele['pop4'][1])) * 2)
            probas['pop5'].append((float(diallele['pop5'][1]) / (diallele['pop5'][0] + diallele['pop5'][1])) * (diallele['pop5'][0] / (diallele['pop5'][0] + diallele['pop5'][1])) * 2)

#print('probas',probas)    #proba based on allelic frequencies - not reliable
print(np.mean(probas['pop1']))
print(np.mean(probas['pop2']))
print(np.mean(probas['pop3']))
print(np.mean(probas['pop4']))
print(np.mean(probas['pop5']))

matrix = np.array(matrix)
matrix = matrix.transpose()

ls = np.array(ls)

print(ls)
print(matrix)
print(len(matrix))
print(len(head))


clf = linSVC(matrix, head)
pred = clf.predict([ls])
print('linearSVC', pred)
predict_proba_dist = clf.decision_function([ls])
pred_probability = []
for eachArr in predict_proba_dist:
    pred_probability.append(softmax(eachArr))
print(pred[0],pred_probability)  #probabilities for linearSVC