#comparison function(for sorting rotations alphabetically. It takes two rotations x and y as input, compares their suffixes, and returns an integer representing their order.)
def cmpfunc(x, y):
    return int(x['suffix'] > y['suffix']) - int(x['suffix'] < y['suffix'])

def compute_suffix_array(input_text):
    len_text = len(input_text)
    suff = [{'index': i, 'suffix': input_text[i:]} for i in range(len_text)] # creates a list of rotations, each rotation represented as a dictionary with an index and a suffix.
    
    # Sort rotations using comparison function
    suff.sort(key=lambda x: x['suffix'])

    suffix_arr = [s['suffix'] for s in suff]

    return suffix_arr

def find_valid_pairs(suffix_arr, k):
    valid_pairs = []
    curr_count = 1
    n = len(suffix_arr)
    prev_suff = ""

    # Iterate over the suffix array, keeping a current count
    for i in range(n):
        # Skip the current suffix if it has length < k
        if len(suffix_arr[i]) < k:
            if i != 0 and len(prev_suff) == k:
                valid_pairs.append((prev_suff, curr_count))
                curr_count = 1
            prev_suff = suffix_arr[i]
            continue

        # Increment curr_count if the first k chars of prev_suff and current suffix are the same
        if prev_suff[:k] == suffix_arr[i][:k]:
            curr_count += 1
        else:
            # Output valid pair when i != 0 and len(prev_suff) == k
            if i != 0 and len(prev_suff) == k:
                valid_pairs.append((prev_suff, curr_count))
                curr_count = 1
                prev_suff = suffix_arr[i][:k]
            else:
                prev_suff = suffix_arr[i][:k]
                continue

        # Modify prev_suff to the current suffix
        prev_suff = suffix_arr[i][:k]

    # Add the last valid pair to the list
    if len(prev_suff) == k:
        valid_pairs.append((prev_suff, curr_count))

    return valid_pairs

