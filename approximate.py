# matches passed from result of algorithm : in gui -> button to call 
# and n parameter passed from gui ( text box with check validation )

def approximate_match_pigeonhole(p,t,matches,holes=1):
    segment_len = int(round(len(p) / (holes+1)))
    all_matches =set()
    for i in range(holes+1):
        start = i * segment_len
        end = min((i+1)*segment_len,len(p))
        for m in matches:
            if (m < start) or (m -start+len(p) > len(t)) : continue
            mismatches = 0
            for j in range(0,start):
                if not p[j] == t[m-start+j]:
                    mismatches +=1 
                    if (mismatches > holes): break
            for  j in range(end,len(p)):
                if not p[j] == t[m-start+j ] :
                    mismatches +=1 
                    if (mismatches > holes): break
            if mismatches <= holes :
                all_matches.add(m-start)
    return list (all_matches) , mismatches

# ==============================================

def naiveHamming(p,t,maxDist):
    occ = []
    for i in range( len(t) -len(p) +1):
        nmm=0
        match=True
        for j in range(len(p)):
            if t[i+j] != p[j]:
                nmm+=1
                if nmm > maxDist:
                    break
        if nmm <= maxDist:
            occ.append(i)
    return occ



# ==============================================
def edit_distance_dp(x, y):
    D = []
    # init with zeros
    for i in range(len(x) + 1):
        D.append([0] * (len(y) + 1))
    # init epsilon col and row
    for i in range(len(x) + 1):
        D[i][0] = i
    for i in range(len(y) + 1):
        D[0][i] = i

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            indx_Hor = D[i][j - 1] + 1
            indx_Ver = D[i - 1][j] + 1
            # for diagonal
            if x[i - 1] == y[j - 1]:
                indx_Diag = D[i - 1][j - 1]
            else:
                indx_Diag = D[i - 1][j - 1] + 1

            D[i][j] = min(indx_Diag, indx_Hor, indx_Ver)

    # Backtrack to reconstruct modified strings x and y
    i, j = len(x), len(y)
    modified_x, modified_y = [], []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and x[i - 1] == y[j - 1]:
            modified_x.append(x[i - 1])
            modified_y.append(y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            modified_x.append(x[i - 1])
            modified_y.append('_')  # Placeholder for insertion in y
            i -= 1
        else:
            modified_x.append('_')  # Placeholder for insertion in x
            modified_y.append(y[j - 1])
            j -= 1

    modified_x.reverse()
    modified_y.reverse()

    # Return minimum edit distance and modified strings
    return D[-1][-1], ''.join(modified_x), ''.join(modified_y)


