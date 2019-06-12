#BSUB -L /bin/bash
#BSUB -J hbond
#BSUB -q highcpu
#BSUB -n 28
#BSUB -o job.out
#BSUB -e job.err
source  /home/wensong/phenix-dev-3525/phenix_env.sh intel64 > /dev/null 2>&1
phenix.python hbond_statistics_high_res.py > test_o.log
