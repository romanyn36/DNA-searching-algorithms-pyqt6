def getLPS(pattern):
    lps = [0] * len(pattern)
    j = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def KMPSearch(pat, txt):
    result = []
    alignments = 0  # Counter for alignments
    skips = 0  # Counter for skips

    M = len(pat)
    N = len(txt)

    lps = [0] * M
    j = 0

    lps = getLPS(pat)

    i = 0
    while (N - i) >= (M - j):
        if pat[j] == txt[i]:
            i += 1
            j += 1
            alignments += 1  # Increment alignment count

        if j == M:
            index = i - j
            result.append(index)
            j = lps[j - 1]
            skips += 1  # Increment skip count

        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                skips += 1  # Increment skip count

    return result, alignments, skips