import numpy as np
import itertools

def decomposeStates(thr, st_table):
        n = st_table.shape[0]
        count = 1
        for i, j in itertools.product(range(n), range(n)):
            if st_table[i][j] > thr:
                st_table[i][j] = count
                count += 1
            else:
                st_table[i][j] = 0

        #print("\n____table with increasing numbers ____")
        #print(st_table)

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

        #print("\n____table with group numbers ____")
        #print(st_table)

        group_keys = []
        for i, j in itertools.product(range(n), range(n)):
            if st_table[i][j] > 0:
                group_keys.append(st_table[i][j])
        keys_dict = dict.fromkeys(group_keys)

        #print("\n____keys dictionary____")
        #print(keys_dict)
        
        for k in keys_dict.keys():
            keys_dict[k] = list(dict.fromkeys(np.nonzero(st_table == k)[0]))

        #print(keys_dict)

        return list(keys_dict.values())

def main():
    arr = np.array([[1, 0, 0]
                   ,[0, 1, 0]
                   ,[0, 0, 1]])
    groups = decomposeStates(0.01, arr)
    print(groups)

if __name__ == "__main__":
    main()