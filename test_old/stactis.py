from libtbx import easy_pickle

dic = easy_pickle.load("n.pkl")
print dic
for k,v in dic:
  print "result" * 39
  for r in v:
    d_AD = r.d_AD
    print d_AD















    '''
    d_AD = v.d_AD
    d_AH = v.d_AH
    a_DHA = v.a_DHA
    print d_AD,d_AH,a_DHA
    '''
