# ----------Preprocessing function ----------------------
import string


def z_array(s):
    ''' Use z_array to preprocess s
    ---------------------------------------------------------
    This array provides the lengths of substrings in the string 
    that match the string's prefix starting from each index.
    '''

    # check if s greater one 
    try :
        assert len(s) > 1 
    except :
        print('error in length String Must be greater than one.')

    z= [len(s)] + [0] * (len(s) -1) # build z array [len(s) , 0,0,0,...,len(s-1)]

    # comparison of s with prefix 
    for i in range(1, len(s)):
        if s[i] == s[i-1]: 
            z[1] += 1
    
        else : break
    
    r,l =0,0
    if z[1] > 0 :
        r,l = z[1],1
    
    for k in range (2 , len(s)):
        assert z[k] == 0
        
        # case 1
        if k > r  :
            
            for i in range (k, len(s)):
                if s[i] == s[i-k] :
                    z[k] += 1
                
                else : break
            
            r,l =  k+z[k]-1 , k
        # case 2
        else :
            # calculate len of beta 
            nbeta = r - k + 1
            zkp = z[k-1]
            if nbeta > zkp:
                z[k] = zkp
            else :
                # compare characters just past r
                nmatch =0
                for i in range (r+1 ,len(s)):
                    if s[i] == s[i-k]:
                        nmatch += 1
                    else: break
                r,l = r+nmatch, k
                z[k] = r-k+1
    
    return z

def n_array(s):
    '''
    This array represents the lengths of the longest suffixes of the string
    that match the entire string, starting from each position in the reversed string.
    '''
    return z_array(s[::-1])[::-1] 

def big_l_prime_array(p,n):
    lp =[0] *len(p)
    for j in range(len(p)-1):
        i= len(p) - n[j]
        if i < len(p):
            lp[i] =j+1
    return lp 

def big_l_array(p,lp):
    l=[0]*len(p)
    l[1]= lp[1]
    for i in range(2,len(p)):
        l[i]=max(l[i-1],lp[i])
    return l

def small_l_prime_array(n):
    small_lp = [0]* len(n)
    for i in range(len(n)):
        if n[i] == i+1: # prefix matching suffix
            small_lp[len(n)-i-1]=i+1
    for i in range(len(n)-2 , -1,-1):
        if small_lp[i] == 0:
            small_lp[i] = small_lp[i+1]
    return small_lp



# ----------------------Good suffix function ------------------
def good_suffix_table(p):
    n = n_array(p)
    lp =big_l_prime_array(p,n)
    return lp,big_l_array(p,lp),small_l_prime_array(n)

def good_suffix_mismatch(i,big_l_prime,small_l_prime):
    length = len(big_l_prime)
    assert i < length
    if i == length - 1 : return 0 
    i+=1
    if big_l_prime[i] > 0: return length - big_l_prime[i]
    return length - small_l_prime[i]

def good_suffix_match(small_l_prime):
    return len(small_l_prime) - small_l_prime[1]

# -----------Bad Char table-------------
def dense_bad_char_tab(p,amap):
    tab=[]
    nxt=[0]*len(amap)
    for i in range(0,len(p)):
        c=p[i]
        assert c in amap
        tab.append(nxt[:])
        nxt[amap[c]]=i+1
    return tab

# --------------=== Boyer moore Process ==-------------------

class cBoyerMoore :

    def __init__(self,p,text):
        self.p=p
        self.alphabet="".join(sorted(set(text)))
        # print( self.alphabet)
    # create  map from alphabet characters to integers 
        self.amap ={}
        for i in range (len(self.alphabet)):
            self.amap[self.alphabet[i]]=i

        # Bad characters
        self.bad_char = dense_bad_char_tab(p,self.amap)

        # good suffix 
        _,self.big_l , self.small_l_prime = good_suffix_table(p)

    def bad_char_rule(self,i,c):
        assert c in self.amap
        ci =self.amap[c]
        assert i > (self.bad_char[i][ci]-1)
        return i - (self.bad_char[i][ci]-1)
    
    def good_suffix_rule(self, i):
        '''give mismatch at offset i , return amount to shift as determined by good suffix rule '''
        length = len(self.big_l)
        assert i<length
        if i == length-1:
            return 0
        i+=1
        if self.big_l[i] >0 :
            return length -self.big_l[i]
        return length - self.small_l_prime[i]
    
    def  match_skip(self):
        '''return amount to shift in case where p matches t'''
        return len(self.small_l_prime) - self.small_l_prime[1]

# ----------------=== Build Algorithm ==--------------------------------
def boyer_moore_algo(pattern, text):
    obj_cls_BoyerMoore = cBoyerMoore(pattern, text)
    i = 0
    occurrences = []
    alignments = []

    while i < len(text) - len(pattern) + 1:
        shift = 1
        mismatched = False
        alignment = [' '] * len(text)  # Alignment initialization

        # Case
        for j in range(len(pattern) - 1, -1, -1):
            alignment[i + j] = text[i + j]  # Filling in the alignment
            if not pattern[j] == text[i + j]:
                skip_bad_char = obj_cls_BoyerMoore.bad_char_rule(j, text[i + j])
                skip_good_suffix = obj_cls_BoyerMoore.good_suffix_rule(j)
                shift = max(shift, skip_bad_char, skip_good_suffix)
                mismatched = True
                break

        # Case
        if not mismatched:
            occurrences.append(i)
            alignment[i:i + len(pattern)] = pattern  # Set matched pattern in alignment
            skip_good_suffix = obj_cls_BoyerMoore.match_skip()
            shift = max(shift, skip_good_suffix)

        alignments.append(''.join(alignment))  # Append alignment to alignments list
        i += shift

    return occurrences, len(alignments), obj_cls_BoyerMoore.match_skip()