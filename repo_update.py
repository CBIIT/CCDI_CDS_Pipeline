import subprocess

# Perform a git pull on all directories that are one directory below the organizing directories.
subprocess.run('find ./Scripts -mindepth 2 -maxdepth 2 -type d -print -exec git -C {} pull \;', shell=True)
