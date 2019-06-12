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
  pdb_code = None
  result = None
  pdb_inp = iotbx.pdb.input(file_name=f)
  if (pdb_inp.resolution()) <= 1.2:
    pdb_code = os.path.basename(f)[3:7]
    try:
      r = run(f)
      result = r.result
    except Exception as e:
      errorFile = open('log.txt', 'a')
      errorFile.write(f + '\n')
      errorFile.write(traceback.format_exc())
      errorFile.close()
  return (pdb_code,result)


if __name__ == '__main__':
  logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  path = '/home/wensong/pdb_bob/'
  of = open("".join([path,"INDEX"]),"r")
  files = ["".join([path,f]).strip() for f in of.readlines()]
  for f in files:
    if not os.path.exists(f):
      files.remove(f)
  of.close()
  list_pdbcode_result = pool_map(
    processes=60,
    func=foo,
    iterable=files)
  dict = {}
  for r in list_pdbcode_result:
    if r is not None:
      if r[0] or r[1] is not None:
        dict[r[0]] = r[1]
  easy_pickle.dump("high_res_hbond.pickle",dict)

