# hbond_statistics_high_resulotion

/hbond_statistics_high_resulotion/hbond_statistics_high_resulotion/

1:"high_res_hbond.pickle" is the pickle file of hbond results dictionary{pdb_code:result_hbond}

2:"hbond_statistics_high_res.py " is the python script to get the high_res_hbond.pickle base on pdb library

3:"log.txt" contains the error or warning informations after running the "hbond_statistics_high_res.py "

4: "statistics.py" is going to load the "high_res_hbond.pickle" to dictionary ,the drawn statistics pictures
But there are problem when load the pickle file!!!!!!!!!!!!!!!

the error information is as follow:


Traceback (most recent call last):
  File "stactis.py", line 3, in <module>
    dic = easy_pickle.load("n.pkl")
  File "/home/wangwensong/phenix-dev-3525/modules/cctbx_project/libtbx/easy_pickle.py", line 82, in load
    return pickle.loads(_open(file_name, "rb").read())
TypeError: No to_python (by-value) converter found for C++ type: scitbx::af::tiny<bool, 3ul>
