perm_s = '-rw-r-xrwx'
permits = dict()
perm_grps = ('user','group', 'other')
permits = {gp: perm_s[start:stop].replace('-', '') for (gp, start, stop) in zip(perm_grps, range(1,10,3), range(4,13,3))}
perms = ('read', 'write', 'execute')
permits2 = {gp: perm_s[start:stop].replace('-', '') for (gp, start, stop) in zip(perms, range(1,10,3), range(4,13,3))}
print(permits, permits2)

# for key, value in permits.items():
#     print(value, key)
#



# 45 wayne st, jc
# nari
# liberty realty