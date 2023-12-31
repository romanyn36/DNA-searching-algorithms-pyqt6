def suffixAarrays(T):
    l=[]
    for i in range(len(T)):
        l.append(T[i:])
    l2=l.copy()
    l.sort()
    dec={}
    for i in range(len(l)):
        dec[l[i]]=i
    table=[]
    for i in range(len(l)):
        table.append([l2[i],i,dec[l2[i]]])
    return table