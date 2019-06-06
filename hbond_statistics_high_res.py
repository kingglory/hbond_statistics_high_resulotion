from __future__ import division,absolute_import,print_function
import iotbx.pdb
import os
import mmtbx.model
from libtbx import easy_pickle
import mmtbx.nci.hbond as hbond
import mmtbx.model
from libtbx.utils import null_out
from mmtbx.utils import run_reduce_with_timeout

def run():
  rr = run_reduce_with_timeout(
    stdin_lines = None,
    file_name   = "pdb35c8.ent.gz",
    parameters  = "-oh -his -flip -keep -allalt -pen9999",
    override_auto_timeout_with=None)
  pdb_inp = iotbx.pdb.input(source_info = None, lines = rr.stdout_lines)
  hierarchy = pdb_inp.construct_hierarchy()
  asc = hierarchy.atom_selection_cache()
  sel = asc.selection("protein")
  hierarchy = hierarchy.select(sel)
  model = mmtbx.model.manager(
    model_input      = None,
    pdb_hierarchy    = hierarchy,
    crystal_symmetry = pdb_inp.crystal_symmetry(),
    process_input    = True,
    log              = null_out())
  return hbond.find(model = model)


  






if __name__ == '__main__':

    r = run()
    dict = {}
    dict[1] = r.result
    easy_pickle.dump("1nym.pickle",dict)

    """
    path ='/home/wangwensong/PDB/pdb/'
    of = open("".join([path,"INDEX"]),"r")
    files = ["".join([path,f]).strip() for f in of.readlines()]
    of.close()
    i = 0
    dict = {}
    for f in files:
      pdb_code = os.path.basename(f)[3:7]
      file_name = f
      print (file_name)
      r = run(file_name)
      dict[pdb_code] = r.result
    easy_pickle.dump("high_res_hbond.pickle",dict)
    """
    

