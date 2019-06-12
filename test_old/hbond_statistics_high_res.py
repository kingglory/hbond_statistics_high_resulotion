from __future__ import division
import iotbx.pdb
import os
import traceback
import logging
import mmtbx.nci.hbond as hbond
import mmtbx.model
from libtbx.utils import null_out
from libtbx import group_args
from libtbx import easy_pickle
from mmtbx.utils import run_reduce_with_timeout
from libtbx.easy_mp import pool_map

def run(file_name):
  pdb_inp = iotbx.pdb.input(file_name = file_name)
  hierarchy = pdb_inp.construct_hierarchy()
  asc = hierarchy.atom_selection_cache()
  sel = asc.selection("not(element H or element D)")
  hierarchy = hierarchy.select(sel)
  rr = run_reduce_with_timeout(
    stdin_lines = hierarchy.as_pdb_string().splitlines(),
    file_name   = None,#"model.pdb.gz",
    parameters  = "-oh -his -flip -keep -allalt -pen9999 -",
    override_auto_timeout_with=None)
  pdb_inp = iotbx.pdb.input(source_info = None, lines = rr.stdout_lines)
  hierarchy = pdb_inp.construct_hierarchy()
  asc = hierarchy.atom_selection_cache()
  sel = asc.selection("protein")
  hierarchy = hierarchy.select(sel)
  model = mmtbx.model.manager(
        model_input      = None,
        pdb_hierarchy    = hierarchy,
        crystal_symmetry = pdb_inp. crystal_symmetry(),
        process_input    = True,
        log              = null_out())
  return hbond.find(model = model)
def foo(f):
  #print f
  pdb_code = None
  result = None
  pdb_inp = iotbx.pdb.input(file_name=f)
  if (pdb_inp.resolution()) <= 1.2:
    pdb_code = os.path.basename(f)[3:7]
    try:
      r = run(f)
      result = r.result
      #print pdb_code
    except Exception as e:
      errorFile = open('log.txt', 'a')
      errorFile.write(f + '\n')
      errorFile.write(traceback.format_exc())
      errorFile.close()
  #print (pdb_code,result)
  return (pdb_code,result)


if __name__ == '__main__':
  path = '/home/wangwensong/PDB/pdb/'
  logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  of = open("".join([path,"INDEX"]),"r")
  files = ["".join([path,f]).strip() for f in of.readlines()]
  for f in files:
    if not os.path.exists(f):
      files.remove(f)
  of.close()
  list_s = pool_map(
    processes = 4,
    func = foo,
    iterable = files
  )
  for r in list_s:
     if r is not None:
      if r[0] or r[1] is not None:
        for i in r[1]:
          print i
          easy_pickle.dump("n.pkl",i)
          s = easy_pickle.load("n.pkl")
          print s
          easy_pickle.dump("1.pkl",i.atom_i)
          STOP()
          print i.atom_i
        s.append(r[1])
  print s
  easy_pickle.dump("1.pkl",s)
  dic = {}
  for r in list_s:
     if r is not None:
      if r[0] or r[1] is not None:
       print "*"*180
       #print r
       dic[r[0]]=r[1]
#       print dic
  easy_pickle.dump("easy.pkl",dic)

  rs  = easy_pickle.load(file_name="easy.pkl")
#  print rs



