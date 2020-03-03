def getsug_id():
  import random
  sug_id=[]
  for i in range(3):
    n = random.randrange(1, 5000)
    sug_id.append(n)
  return(sug_id)
