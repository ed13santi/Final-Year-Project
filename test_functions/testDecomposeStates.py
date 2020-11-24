import numpy as np
import itertools

def decomposeStates(thr, st_table):
        #assign different number to each entry above threshold, set entries below thr to 0
        n = st_table.shape[0]
        count = 1
        for i, j in itertools.product(range(n), range(n)):
            if st_table[i][j] > thr:
                st_table[i][j] = count
                count += 1
            else:
                st_table[i][j] = 0

        #assign same number to all entries that are part of the same subsystem
        while True:
            st_table_copy = st_table
            for i in range(n):
                if np.max( st_table[i,:] ) > 0:
                    minval = np.min( st_table[i][np.nonzero(st_table[i])] )
                    for j in np.nonzero(st_table[i])[0]:
                        st_table[i][j] = minval
            for j in range(n):
                if np.max( st_table[:,j] ) > 0:
                    minval = np.min( st_table[:,j][np.nonzero(st_table[:,j])] )
                    for i in np.nonzero(st_table[:,j])[0]:
                        st_table[i][j] = minval
            if (st_table_copy == st_table).all() :
                break

        #group states in the same subsystem as list of lists
        group_keys = []
        for i, j in itertools.product(range(n), range(n)):
            if st_table[i][j] > 0:
                group_keys.append(st_table[i][j])
        groups = []
        for k in group_keys:
            groups.append(list(dict.fromkeys(np.nonzero(st_table == k)[0])))

        return groups

def main():
    arr = np.array([[1, 0, 0]
                   ,[0, 1, 0]
                   ,[0, 0, 1]])
    groups = decomposeStates(0.01, arr)
    print(groups)

if __name__ == "__main__":
    main()