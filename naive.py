def naive(pat, txt):
    result = []
    alignments = 0  # Variable to count alignments
    M = len(pat)
    N = len(txt)

    # A loop to slide pat[] one by one
    for i in range(N - M + 1):
        j = 0
        
        # For current index i, check for pattern match
        while j < M:
            alignments += 1  # Increment alignments for each comparison
            if txt[i + j] != pat[j]:
                break
            j += 1

        if j == M:
            result.append(i)

    return result,alignments