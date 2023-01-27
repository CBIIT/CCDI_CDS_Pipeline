import subprocess

#Func to git pull repos for pipeline.
def cbiit_git_puller(repos, dir):
    cbiit="https://github.com/CBIIT/"
    for repo in repos:
        subprocess.run(f'git clone {cbiit}{repo}.git {dir}{repo}', shell=True)

#Make directory structure for scripts
subprocess.run(['mkdir Scripts'], shell=True)
subprocess.run(['mkdir Scripts/CCDI'], shell=True)
subprocess.run(['mkdir Scripts/CDS'], shell=True)

#Current CCDI repos required for pipeline
ccdi_repos=[
'ChildhoodCancerDataInitiative-CatchERR',
'ChildhoodCancerDataInitiative-Submission_ValidatoR',
'ChildhoodCancerDataInitiative-CCDI_to_dbGaP', 
'ChildhoodCancerDataInitiative-Stat_GeneratoR', 
'ChildhoodCancerDataInitiative-CCDI_to_SRA'
]

#Current CDS repos required for pipeline
cds_repos=[
'CancerDataServices-Stat_GeneratoR',
'CancerDataServices-CDS_to_dbGaP', 
'CancerDataServices-CCDI_to_CDS_ConverteR', 
'CancerDataServices-SubmissionValidationR', 
'CancerDataServices-CDS_to_SRA', 
'CancerDataServices-CatchERR', 
]

#Clone repos
cbiit_git_puller(ccdi_repos, 'Scripts/CCDI/')
cbiit_git_puller(cds_repos, 'Scripts/CDS/')
