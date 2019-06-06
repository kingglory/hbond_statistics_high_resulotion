from __future__ import division
import iotbx.pdb
import os
import hbond
import mmtbx.model
from libtbx.utils import null_out
from libtbx import group_args
from libtbx import easy_pickle
from libtbx import easy_mp
from libtbx import easy_run
import collections
import math
from iotbx.pdb import remark_2_interpretation
from libtbx import easy_pickle


def get_resolution(pdb_inp):
    resolution = None
    resolutions = iotbx.pdb.remark_2_interpretation.extract_resolution(
      pdb_inp.extract_remark_iii_records(2))
    if (resolutions is not None):
      resolution = resolutions[0]
    return resolution
def core(pdb_inp,pair_proxies = None):
  model = mmtbx.model.manager(
    model_input   = pdb_inp,
    process_input = True,
    log           = null_out())
  #print model.model_as_pdb(),"wwwwwwwwwwww"
  m_sel = model.selection("not protein")
  new_model = model.select(~m_sel)
  #print new_model.model_as_pdb(),"eeeeeeeeeeee"

  return hbond.find(model=new_model, pair_proxies=pair_proxies)



def run(file_name,protein_only = True):
    result = None
    if (protein_only):
      pdb_inp = iotbx.pdb.input(file_name=file_name)
      resolution = get_resolution(pdb_inp=pdb_inp)
      if 0< resolution <= 1.2:
        r = core(pdb_inp=pdb_inp)
        result = r.show()
    return result
        

        
  






if __name__ == '__main__':
    path ='/home/wangwensong/PDB/pdb/'
    of = open("".join([path,"INDEX"]),"r")
    files = ["".join([path,f]).strip() for f in of.readlines()]
    of.close()
    i = 0
    dict = {}
    for f in files:
      pdb_code = os.path.basename(f)[3:7]
      print pdb_code*8
      r = run(f)
      print pdb_code * 8
      dict[pdb_code] = r

    easy_pickle.dump("high_res_hbond.pickle",dict)

    

