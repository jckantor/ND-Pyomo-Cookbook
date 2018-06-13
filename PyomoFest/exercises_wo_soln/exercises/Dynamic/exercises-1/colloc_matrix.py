import numpy

cp = [0, 0.155051, 0.644949, 1]

a = []

print('[')
for i in range(len(cp)):
    ptmp = []
    tmp = 0
    for j in range(len(cp)):
        if j != i:
            row = []
            row.insert(0,1/(cp[i]-cp[j]))
            row.insert(1,-cp[j]/(cp[i]-cp[j]))
            ptmp.insert(tmp,row)
            tmp += 1
    p=[1]
    for j in range(len(cp)-1):
        p = numpy.convolve(p,ptmp[j])
    pder = numpy.polyder(p,1)
    arow = []
    for j in range(len(cp)):
        arow.append(numpy.polyval(pder,cp[j]))
    a.append(arow)
    print(str(arow)+',')
print(']')


                                                              
