import subprocess
import argparse
import argcomplete
import os
import re
from datetime import date
import glob

#TO DO
# Add in further validation to include gaptools validation checks once gaptools is installed in the VM.
#

parser = argparse.ArgumentParser(
                    prog='CCDI_CDS_Pipeline.py',
                    description='A script to run a pipeline for either a project that is CCDI only, CDS only or from CCDI to CDS.',
                    )

parser.add_argument( '-f', '--filename', help='The input template file', required=True)
parser.add_argument( '-p', '--pipeline', help="The pipeline that will be run, 'CCDI' (only), 'CDS' (only), 'Both'.", required=True, choices=['CCDI','CDS','Both'])
parser.add_argument( '-d', '--ccdi_template', help='The example template for a CCDI project')
parser.add_argument( '-s', '--cds_template', help='The example template for a CDS project')
parser.add_argument( '-b', '--bucket_list', help='The list file for a bucket that was created with Bucket_ls.py (part of the Validation script github repo)', default= "NO_LIST_PULL_FROM_S3")

argcomplete.autocomplete(parser)

args = parser.parse_args()

#pull in args as variables
file_name=args.filename
ccdi_template=args.ccdi_template
cds_template=args.cds_template
pipeline=args.pipeline.lower()
bucket_list=args.bucket_list
file_ext=os.path.splitext(file_name)[1]
working_file_path=os.path.split(os.path.relpath(file_name))[0]

#Correct the file path if your within the working directory of the file.
if working_file_path=='':
    working_file_path="."


#Look down all directories to find the exact script path for the directory structure
script_path=os.path.split(os.path.realpath(__file__))[0]
look_down=glob.glob(f'{script_path}/**/**/**/**/**/**/*',recursive=True)

#remove all endpoints except for R scripts (this was also done to avoid picking up README.md files).
look_down_R=[ldl for ldl in look_down if ldl.endswith('.R')]

#All script paths discovered for calls
#CCDI
CCDI_Submission_ValidatoR = [x for x in look_down_R if re.match(r'.*CCDI-Submission_ValidatoR.R', x)][0]
CCDI_CatchERR = [x for x in look_down_R if re.match(r'.*CCDI-CatchERR.R', x)][0]
CCDI_to_SRA = [x for x in look_down_R if re.match(r'.*CCDI_to_SRA.R', x)][0]
CCDI_to_dbGaP = [x for x in look_down_R if re.match(r'.*CCDI_to_dbGaP.R', x)][0]
CCDI_Stat_GeneratoR = [x for x in look_down_R if re.match(r'.*CCDI-Stat_GeneratoR.R', x)][0]

#CDS
CCDI_to_CDS_ConverteR = [x for x in look_down_R if re.match(r'.*CCDI_to_CDS_converteR.R', x)][0]
CDS_CatchERR = [x for x in look_down_R if re.match(r'.*CDS-CatchERR.R', x)][0]
CDS_Submission_ValidationR = [x for x in look_down_R if re.match(r'.*CDS-Submission_ValidationR.R', x)][0]
CDS_to_SRA = [x for x in look_down_R if re.match(r'.*CDS_to_SRA.R', x)][0]
CDS_to_dbGaP = [x for x in look_down_R if re.match(r'.*CDS_to_dbGaP.R', x)][0]
CDS_Stat_GeneratoR = [x for x in look_down_R if re.match(r'.*CDS-Stat_GeneratoR.R', x)][0]

#Obtain the phsXXXXXX.xlsx template
look_down_phsx=list(set([ldl for ldl in look_down if ldl.endswith('phsXXXXXX.xlsx')]))[0]


#obtain the date
def refresh_date():
    today=date.today()
    today=today.strftime("%Y%m%d")
    return today


###############
#
# CCDI Only
#
###############

if pipeline=="ccdi":
    #if there is not a CCDI submission file and CCDI template file, kill the script.
    if not file_name or not ccdi_template: 
        print("Please include both a CCDI submission file and a CDDI template file.")
        exit()

     #obtain the date
    today=refresh_date()
    today_dir=refresh_date()

    #create dir structure and move files accordingly
    dir_base=f"{working_file_path}/{pipeline}_working_{today_dir}"
    dir_0=f"{dir_base}/0_input_files"
    dir_1=f"{dir_base}/1_CCDI_CatchERR"
    dir_2=f"{dir_base}/2_CCDI_Validator"
    dir_3=f"{dir_base}/3_CCDI_to_dbGaP"
    dir_4=f"{dir_base}/4_CCDI_to_SRA"
    dir_5=f"{dir_base}/5_CCDI_Stats"

    subprocess.run([f'mkdir {dir_base}'], shell=True)
    subprocess.run([f'mkdir {dir_0}'], shell=True)
    subprocess.run([f'mkdir {dir_1}'], shell=True)
    subprocess.run([f'mkdir {dir_2}'], shell=True)
    subprocess.run([f'mkdir {dir_3}'], shell=True)
    subprocess.run([f'mkdir {dir_4}'], shell=True)
    subprocess.run([f'mkdir {dir_5}'], shell=True)

    #move input files to input directory
    subprocess.run([f'cp {file_name} {dir_0}'], shell=True)
    subprocess.run([f'cp {ccdi_template} {dir_0}'], shell=True)
    subprocess.run([f'cp {bucket_list} {dir_0}'], shell=True)

    #create new path for input files
    file_name=dir_0+'/'+os.path.split(file_name)[1]
    ccdi_template=dir_0+'/'+os.path.split(ccdi_template)[1]

    subprocess.run([f"Rscript --vanilla {CCDI_CatchERR} -f {file_name} -t {ccdi_template}"], shell=True)
    
    extra_file_base=file_name
    file_name=os.path.splitext(file_name)[0]+f'_CatchERR{today}{file_ext}'
    file_catcherr_text=os.path.splitext(extra_file_base)[0]+f'_CatchERR{today}.txt'

    #move output files to next directory
    subprocess.run([f'mv {file_name} {dir_1}'], shell=True)
    subprocess.run([f'mv {file_catcherr_text} {dir_1}'], shell=True)

    today=refresh_date()

    #create new path for input files
    file_name=dir_1+'/'+os.path.split(file_name)[1]

    subprocess.run([f"Rscript --vanilla {CCDI_Submission_ValidatoR} -f {file_name} -t {ccdi_template} -b {bucket_list}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_vaildate_text=os.path.splitext(extra_file_base)[0]+f'_Validate{today}.txt'
    subprocess.run([f'mv {file_vaildate_text} {dir_2}'], shell=True)


    subprocess.run([f"Rscript --vanilla {CCDI_to_SRA} -f {file_name} -t {look_down_phsx}"], shell=True)
    #SRA can be skipped in certain data sets, so logic here will allow for its exclusion.
    SRA_folder=list(filter(lambda x: "SRA_submission" in x, os.listdir(dir_1)))
    if len(SRA_folder)!=0:
        SRA_folder=list(filter(lambda x: "SRA_submission" in x, os.listdir(dir_1)))[0]
        SRA_folder=dir_1+"/"+SRA_folder
        subprocess.run([f'mv -f {SRA_folder} {dir_4}'], shell=True)

    file_sra_text=os.path.splitext(extra_file_base)[0]+f'_SRA{today}.txt'
    subprocess.run([f'mv {file_sra_text} {dir_4}'], shell=True)

    subprocess.run([f"Rscript --vanilla {CCDI_to_dbGaP} -f {file_name}"], shell=True)
    dbGaP_folder=list(filter(lambda x: "dbGaP_submission" in x, os.listdir(dir_1)))[0]
    dbGaP_folder=dir_1+"/"+dbGaP_folder
    subprocess.run([f'mv -f {dbGaP_folder} {dir_3}'], shell=True)

    #Pull out files from dbGaP submission for stats generation
    dbGaP_folder=list(filter(lambda x: "dbGaP_submission" in x, os.listdir(dir_3)))[0]
    dbgap_dir= dir_3+"/"+dbGaP_folder+"/"
    dbgap_dir_list=os.listdir(os.path.abspath(dbgap_dir))
    SA_DS= [x for x in dbgap_dir_list if re.match(r'SA_DS.*', x)][0]
    SC_DS= [x for x in dbgap_dir_list if re.match(r'SC_DS.*', x)][0]
    SC_DS= dbgap_dir + SC_DS
    SA_DS= dbgap_dir + SA_DS
        
    subprocess.run([f"Rscript --vanilla {CCDI_Stat_GeneratoR} -f {file_name} -c {SC_DS} -a {SA_DS}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_stat_text=os.path.splitext(extra_file_base)[0]+f'_Stats{today}.txt'
    subprocess.run([f'mv {file_stat_text} {dir_5}'], shell=True)


###############
#
# CDS Only
#
###############

elif pipeline=="cds":
    #if there is not a CCDI submission file and template file for both CCDI and CDS, kill the script.
    if not file_name or not cds_template: 
        print("Please include both a CDS submission file and a CDS template file.")
        exit()

     #obtain the date
    today=refresh_date()
    today_dir=refresh_date()

    #create dir structure and move files accordingly
    dir_base=f"{working_file_path}/{pipeline}_working_{today_dir}"
    dir_0=f"{dir_base}/0_input_files"
    dir_1=f"{dir_base}/1_CDS_CatchERR"
    dir_2=f"{dir_base}/2_CDS_Validation"
    dir_3=f"{dir_base}/3_CDS_to_dbGaP"
    dir_4=f"{dir_base}/4_CDS_to_SRA"
    dir_5=f"{dir_base}/5_CDS_Stats"

    subprocess.run([f'mkdir {dir_base}'], shell=True)
    subprocess.run([f'mkdir {dir_0}'], shell=True)
    subprocess.run([f'mkdir {dir_1}'], shell=True)
    subprocess.run([f'mkdir {dir_2}'], shell=True)
    subprocess.run([f'mkdir {dir_3}'], shell=True)
    subprocess.run([f'mkdir {dir_4}'], shell=True)
    subprocess.run([f'mkdir {dir_5}'], shell=True)

    #move input files to input directory
    subprocess.run([f'cp {file_name} {dir_0}'], shell=True)
    subprocess.run([f'cp {cds_template} {dir_0}'], shell=True)

    #create new path for input files
    file_name=dir_0+'/'+os.path.split(file_name)[1]
    cds_template=dir_0+'/'+os.path.split(cds_template)[1]

    subprocess.run([f"Rscript --vanilla {CDS_CatchERR} -f {file_name} -t {cds_template}"], shell=True)
    
    extra_file_base=file_name
    file_name=os.path.splitext(file_name)[0]+f'_CatchERR{today}{file_ext}'
    file_catcherr_text=os.path.splitext(extra_file_base)[0]+f'_CatchERR{today}.txt'
    file_index=os.path.splitext(extra_file_base)[0]+f'_index{today}.tsv'

    #move output files to next directory
    subprocess.run([f'mv {file_name} {dir_1}'], shell=True)
    subprocess.run([f'mv {file_catcherr_text} {dir_1}'], shell=True)
    subprocess.run([f'mv {file_index} {dir_1}'], shell=True)

    today=refresh_date()

    #create new path for input files
    file_name=dir_1+'/'+os.path.split(file_name)[1]

    subprocess.run([f"Rscript --vanilla {CDS_Submission_ValidationR} -f {file_name} -t {cds_template} -b {bucket_list}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_vaildate_text=os.path.splitext(extra_file_base)[0]+f'_Validate{today}.txt'
    subprocess.run([f'mv {file_vaildate_text} {dir_2}'], shell=True)

    subprocess.run([f"Rscript --vanilla {CDS_to_SRA} -f {file_name} -t {look_down_phsx}"], shell=True)
    #SRA can be skipped in certain data sets, so logic here will allow for its exclusion.
    SRA_folder=list(filter(lambda x: "SRA_submission" in x, os.listdir(dir_1)))
    if len(SRA_folder)!=0:   
        SRA_folder=list(filter(lambda x: "SRA_submission" in x, os.listdir(dir_1)))[0]
        SRA_folder=dir_1+"/"+SRA_folder
        subprocess.run([f'mv -f {SRA_folder} {dir_4}'], shell=True)
    
    file_sra_text=os.path.splitext(extra_file_base)[0]+f'_SRA{today}.txt'
    subprocess.run([f'mv {file_sra_text} {dir_4}'], shell=True)

    subprocess.run([f"Rscript --vanilla {CDS_to_dbGaP} -f {file_name}"], shell=True)
    dbGaP_folder=list(filter(lambda x: "dbGaP_submission" in x, os.listdir(dir_1)))[0]
    dbGaP_folder=dir_1+"/"+dbGaP_folder
    subprocess.run([f'mv -f {dbGaP_folder} {dir_3}'], shell=True)

    # #Pull out files from dbGaP submission for stats generation
    dbGaP_folder=list(filter(lambda x: "dbGaP_submission" in x, os.listdir(dir_3)))[0]
    dbgap_dir= dir_3+"/"+dbGaP_folder+"/"
    dbgap_dir_list=os.listdir(os.path.abspath(dbgap_dir))
    SA_DS= [x for x in dbgap_dir_list if re.match(r'SA_DS.*', x)][0]
    SC_DS= [x for x in dbgap_dir_list if re.match(r'SC_DS.*', x)][0]
    SC_DS= dbgap_dir + SC_DS
    SA_DS= dbgap_dir + SA_DS
        
    subprocess.run([f"Rscript --vanilla {CDS_Stat_GeneratoR} -f {file_name} -c {SC_DS} -a {SA_DS}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_stat_text=os.path.splitext(extra_file_base)[0]+f'_Stats{today}.txt'
    subprocess.run([f'mv {file_stat_text} {dir_5}'], shell=True)


###############
#
# Both
#
###############

elif pipeline=="both":
    #if there is not a CCDI submission file and template file for both CCDI and CDS, kill the script.
    if not file_name or not ccdi_template or not cds_template: 
        print("Please include a CCDI submission file and both a CDDI and CDS template file.")
        exit()

     #obtain the date
    today=refresh_date()
    today_dir=refresh_date()

    #create dir structure and move files accordingly
    dir_base=f"{working_file_path}/{pipeline}_working_{today_dir}"
    dir_0=f"{dir_base}/0_input_files"
    dir_1=f"{dir_base}/1_CCDI_CatchERR"
    dir_2=f"{dir_base}/2_CCDI_Validator"
    dir_3=f"{dir_base}/3_CCDI_to_CDS"
    dir_4=f"{dir_base}/4_CDS_CatchERR"
    dir_5=f"{dir_base}/5_CDS_Validation"
    dir_6=f"{dir_base}/6_CDS_to_dbGaP"
    dir_7=f"{dir_base}/7_CDS_to_SRA"
    dir_8=f"{dir_base}/8_CDS_Stats"

    subprocess.run([f'mkdir {dir_base}'], shell=True)
    subprocess.run([f'mkdir {dir_0}'], shell=True)
    subprocess.run([f'mkdir {dir_1}'], shell=True)
    subprocess.run([f'mkdir {dir_2}'], shell=True)
    subprocess.run([f'mkdir {dir_3}'], shell=True)
    subprocess.run([f'mkdir {dir_4}'], shell=True)
    subprocess.run([f'mkdir {dir_5}'], shell=True)
    subprocess.run([f'mkdir {dir_6}'], shell=True)
    subprocess.run([f'mkdir {dir_7}'], shell=True)
    subprocess.run([f'mkdir {dir_8}'], shell=True)

    #move input files to input directory
    subprocess.run([f'cp {file_name} {dir_0}'], shell=True)
    subprocess.run([f'cp {ccdi_template} {dir_0}'], shell=True)
    subprocess.run([f'cp {cds_template} {dir_0}'], shell=True)

    #create new path for input files
    file_name=dir_0+'/'+os.path.split(file_name)[1]
    ccdi_template=dir_0+'/'+os.path.split(ccdi_template)[1]
    cds_template=dir_0+'/'+os.path.split(cds_template)[1]

    subprocess.run([f"Rscript --vanilla {CCDI_CatchERR} -f {file_name} -t {ccdi_template}"], shell=True)

    extra_file_base=file_name
    file_name=os.path.splitext(file_name)[0]+f'_CatchERR{today}{file_ext}'
    file_catcherr_text=os.path.splitext(extra_file_base)[0]+f'_CatchERR{today}.txt'

    #move output files to next directory
    subprocess.run([f'mv {file_name} {dir_1}'], shell=True)
    subprocess.run([f'mv {file_catcherr_text} {dir_1}'], shell=True)

    today=refresh_date()

    #create new path for input files
    file_name=dir_1+'/'+os.path.split(file_name)[1]

    subprocess.run([f"Rscript --vanilla {CCDI_Submission_ValidatoR} -f {file_name} -t {ccdi_template} -b {bucket_list}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_vaildate_text=os.path.splitext(extra_file_base)[0]+f'_Validate{today}.txt'
    subprocess.run([f'mv {file_vaildate_text} {dir_2}'], shell=True)

    today=refresh_date()
    
    subprocess.run([f"Rscript --vanilla {CCDI_to_CDS_ConverteR} -f {file_name} -t {cds_template}"], shell=True)

    file_name=os.path.splitext(file_name)[0]+f'_CDSTemplate{today}.xlsx'

    #move output files to next directory
    subprocess.run([f'mv {file_name} {dir_3}'], shell=True)

    #create new path for input files
    file_name=dir_3+'/'+os.path.split(file_name)[1]

    today=refresh_date()

    subprocess.run([f"Rscript --vanilla {CDS_CatchERR} -f {file_name} -t {cds_template}"], shell=True)
    
    extra_file_base=file_name
    file_name=os.path.splitext(file_name)[0]+f'_CatchERR{today}.xlsx'
    file_catcherr_text=os.path.splitext(extra_file_base)[0]+f'_CatchERR{today}.txt'
    file_index=os.path.splitext(extra_file_base)[0]+f'_index{today}.tsv'

    #move output files to next directory
    subprocess.run([f'mv {file_name} {dir_4}'], shell=True)
    subprocess.run([f'mv {file_catcherr_text} {dir_4}'], shell=True)
    subprocess.run([f'mv {file_index} {dir_4}'], shell=True)

    today=refresh_date()

    #create new path for input files
    file_name=dir_4+'/'+os.path.split(file_name)[1]

    subprocess.run([f"Rscript --vanilla {CDS_Submission_ValidationR} -f {file_name} -t {cds_template} -b {bucket_list}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_vaildate_text=os.path.splitext(extra_file_base)[0]+f'_Validate{today}.txt'
    subprocess.run([f'mv {file_vaildate_text} {dir_5}'], shell=True)

    subprocess.run([f"Rscript --vanilla {CDS_to_SRA} -f {file_name} -t {look_down_phsx}"], shell=True)
    #SRA can be skipped in certain data sets, so logic here will allow for its exclusion.
    SRA_folder=list(filter(lambda x: "SRA_submission" in x, os.listdir(dir_4)))
    if len(SRA_folder)!=0:
        SRA_folder=list(filter(lambda x: "SRA_submission" in x, os.listdir(dir_4)))[0]
        SRA_folder=dir_4+"/"+SRA_folder
        subprocess.run([f'mv -f {SRA_folder} {dir_7}'], shell=True)

    file_sra_text=os.path.splitext(extra_file_base)[0]+f'_SRA{today}.txt'
    subprocess.run([f'mv {file_sra_text} {dir_7}'], shell=True)

    subprocess.run([f"Rscript --vanilla {CDS_to_dbGaP} -f {file_name}"], shell=True)
    dbGaP_folder=list(filter(lambda x: "dbGaP_submission" in x, os.listdir(dir_4)))[0]
    dbGaP_folder=dir_4+"/"+dbGaP_folder
    subprocess.run([f'mv -f {dbGaP_folder} {dir_6}'], shell=True)

    # #Pull out files from dbGaP submission for stats generation
    dbGaP_folder=list(filter(lambda x: "dbGaP_submission" in x, os.listdir(dir_6)))[0]
    dbgap_dir= dir_6+"/"+dbGaP_folder+"/"
    dbgap_dir_list=os.listdir(os.path.abspath(dbgap_dir))
    SA_DS= [x for x in dbgap_dir_list if re.match(r'SA_DS.*', x)][0]
    SC_DS= [x for x in dbgap_dir_list if re.match(r'SC_DS.*', x)][0]
    SC_DS= dbgap_dir + SC_DS
    SA_DS= dbgap_dir + SA_DS
        
    subprocess.run([f"Rscript --vanilla {CDS_Stat_GeneratoR} -f {file_name} -c {SC_DS} -a {SA_DS}"], shell=True)

    #move output to next directory
    extra_file_base=file_name
    file_stat_text=os.path.splitext(extra_file_base)[0]+f'_Stats{today}.txt'
    subprocess.run([f'mv {file_stat_text} {dir_8}'], shell=True)   


###############
#
# Other
#
###############
   
else :
    print('Please submit a correct pipeline: CCDI, CDS, Both')
    exit()
