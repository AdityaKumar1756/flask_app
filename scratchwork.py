def longestIncSubseq(lst):
        # [1, 3, 12, 10, 2, 4, 5, 6, 11]
        # base case is that there is nothing in the list itself
        # for some list s[1, ... i], when we encounter s[j],
        
        endlis = [1] * len(lst)
        endlis_i = [-1] * len(lst)
        for i in range(len(lst)):
            m = 0
            mi = -1
            for j in range(i):
                if lst[j] < lst[i] and endlis[j] > m:
                    m = endlis[j]
                    mi = j
            endlis[i] = 1 + m
            endlis_i[i] = mi 
        
        # return max(endlis)
        res = []
        
        m = 0
        mi = -1
        for i in range(len(lst)):
            if endlis[i] > m:
                m = endlis[i]
                mi = i
        
        i = mi
        while (i > -1):
            res.append(lst[i])
            i = endlis_i[i]
        
        res.reverse()   
        return res

t1 = [1, 3, 12, 10, 2, 4, 5, 6, 11]
print(longestIncSubseq(t1))