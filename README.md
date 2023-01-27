# CCDI_CDS_Pipeline
This is a pipeline script that will run either or both CCDI and CDS scripts for validation and release.

This script needs to be place at the top directory structure that contains all of the following scripts, found in the setup_repo.py script.

> Please run the setup_repo.py script first to ensure that all repos are present in the directory tree.

For information on how to run the CCDI_CDS_Pipeline.py please run `python CCDI_CDS_Pipeline.py -h`

```
usage: CCDI_CDS_Pipeline.py [-h] [-f FILENAME] [-p PIPELINE] [-d CCDI_TEMPLATE] [-s CDS_TEMPLATE]

A script to run a pipeline for either a project that is CCDI only, CDS only or from CCDI to CDS.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        The input template file
  -p PIPELINE, --pipeline PIPELINE
                        The pipeline that will be run, 'CCDI' (only), 'CDS' (only), 'Both'.
  -d CCDI_TEMPLATE, --ccdi_template CCDI_TEMPLATE
                        The example template for a CCDI project
  -s CDS_TEMPLATE, --cds_template CDS_TEMPLATE
                        The example template for a CDS project
```                        
  
For keeping the pipeline scripts up to date, please run the `repo_update.py` script before using the pipeline. This script will perform `git pull` on all repos within the `Scripts/` directory.
