

def minmax_euclid(z, M, R):
  a = {}
  b = {}
  s = {}
  t = {}
  u = {}
  v = {}
  a[0] = z
  b[0] = M
  s[0] = 1
  t[0] = 0
  u[0] = 0
  v[0] = 1
  i = 0
  while True:
    while b[i] >= a[i]: # Loop A
      b[i+1] = b[i] - a[i]
      u[i+1] = u[i] - s[i]
      v[i+1] = v[i] - t[i]
      a[i+1] = a[i]
      s[i+1] = s[i]
      t[i+1] = t[i]
      i=i+1
      if -u[i] > R :
          return (a[i],b[i])
    if b[i] == 0:
      return(1,M-1)
    while a[i] >= b[i]: # Loop B
      a[i+1] = a[i] - b[i]
      s[i+1] = s[i] - u[i]
      t[i+1] = t[i] - v[i]
      b[i+1] = b[i]
      u[i+1] = u[i]
      v[i+1] = v[i]
      i=i+1
      if s[i] > R:
          return (a[i],b[i])
    if a[i] == 0 :
      return (1,M-1)

def minmax_euclid_brute(z, M, R):
    a = z % M
    b = z % M
    for w in range(1,R):
        v = (w*z)%M
        if v < a:
            a = v
        if v > b:
            b = v
    return a,b

print(minmax_euclid_brute(39,256,10))
print(minmax_euclid(39,256,128))