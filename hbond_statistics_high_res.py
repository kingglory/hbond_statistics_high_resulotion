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

if __name__ == '__main__':
  i = 0
  path = '/home/wangwensong/PDB/pdb/'
  of = open("".join([path,"INDEX"]),"r")
  files = ["".join([path,f]).strip() for f in of.readlines()]
  of.close()
  dict = {}
  logging.basicConfig(filename='log.txt',level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s - %(message)s')

  for f in files:
    print f
    pdb_inp = iotbx.pdb.input(file_name=f)
    if (pdb_inp.resolution()) > 1.2: continue
    pdb_code = os.path.basename(f)[3:7]
    try:
      r = run(f)
      dict[pdb_code] = (r.result)
      i = i + 1
      print i
    except Exception as e:
      errorFile = open('log.txt','a')
      errorFile.write(f+'\n')
      errorFile.write(traceback.format_exc())
      errorFile.close()
  easy_pickle.dump("high_res_hbond.pickle",dict)

