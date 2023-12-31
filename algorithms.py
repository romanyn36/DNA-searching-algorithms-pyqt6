
from BoyerMoore import  boyer_moore_algo
from kmp import KMPSearch
from naive import naive
from suffixAarrays import suffixAarrays
from kmer import find_valid_pairs,compute_suffix_array


def chooseAlgorithm(p,t,option,k = 2):
    if option==0:
         result = naive(p,t)
    elif option==1:
         result=boyer_moore_algo(p,t) 
    elif option==2:
        result=suffixAarrays(t)
    elif option==3:
         suffix_arr = compute_suffix_array(t)
         result =find_valid_pairs(suffix_arr, k)
    elif option==4:
        result=KMPSearch(p,t)
    return result




# def approximate_match(p,t,matches,n=1):
#     segment_len = int(round(len(p) / (n+1)))
#     all_matches =set()
#     for i in range(n+1):
#         start = i * segment_len
#         end = min((i+1)*segment_len,len(p))
#         for m in matches:
#             if (m < start) or (m -start+len(p) > len(t)) : continue
#             mismatches = 0
#             for j in range(0,start):
#                 if not p[j] == t[m-start+j]:
#                     mismatches +=1 
#                     if (mismatches > n): break
#             for  j in range(end,len(p)):
#                 if not p[j] == t[m-start+j ] :
#                     mismatches +=1 
#                     if (mismatches > n): break
#             if mismatches <= n :
#                 all_matches.add(m-start)
#     return list (all_matches)

 
# # how use
# p='ABAB'
# t='ABABDABACDABABCABAB'
# print(approximate_match(p,t,indx_matched_boyermoore,n=2))

 
# print(approximate_match(p,t,indx_matched_naive))

 
# print(approximate_match(p,t,indx_matched_KMP,n=1))


