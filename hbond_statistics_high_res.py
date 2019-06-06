from __future__ import division
import iotbx.pdb
import os
from libtbx import group_args
from libtbx import easy_pickle
from libtbx import easy_mp
from libtbx import easy_run
import collections
import math
from iotbx.pdb import remark_2_interpretation


def get_resolution(pdb_inp):
    resolution = None
    resolutions = iotbx.pdb.remark_2_interpretation.extract_resolution(
      pdb_inp.extract_remark_iii_records(2))
    if (resolutions is not None):
      resolution = resolutions[0]
    return resolution




def run(file_name,protein_only = True):
    if (protein_only):
      pdb_inp = iotbx.pdb.input(file_name=file_name)
      resolution = get_resolution(pdb_inp=pdb_inp)
      if 0< resolution <= 1.2:
        easy_run("phenix.hbond pdb_inp")

        
  






if __name__ == '__main__':
    path ='/home/wangwensong/PDB/pdb/'
    of = open("".join([path,"INDEX"]),"r")
    files = ["".join([path,f]).strip() for f in of.readlines()]
    of.close()
    args = []
    i = 0
    for f in files:
     run(f)
    

