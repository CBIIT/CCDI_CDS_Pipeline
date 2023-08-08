import os,shutil, subprocess
## This function copies files from source to destination keeping the metadata of the files intact
def curator_copy_file(source:str, dest:str):
    if((source==None) or (dest==None)):
       print("Please specify source and destination l.")
       exit()
    try:
        shutil.copy2(source,dest)
    except Exception as e:
         print('Error copying file: ',e)

## This function moves directories from source to destination
def curator_move_file(source:str, dest:str):
    if((source==None) or (dest==None)):
       print("Please specify source and destination l.")
       exit()
    try:
        source_abs=os.path.abspath(source)
        dest_abs= os.path.abspath(dest)
        print('Source Path: ', source)
        print('Source Path Abs: ', source_abs)
        # Commence Only if Source Path exists
        if os.path.exists(source_abs):
            print('Source exists : ',source_abs)
            # Check if Destination Path exists
            if os.path.exists(dest_abs):
                 # Check if Destination Path is a directory
                if os.path.isdir(dest_abs):
                    # Get the filename from the relative path
                    file_name=os.path.basename(source_abs)
                    # Get the destination absolute path
                    dest_file_path=os.path.join(dest_abs,file_name)
                    print('The path is a directory ', dest_abs)
                    print('Existing Path location: ', dest_file_path)
                    # If the file exists remove it
                    if os.path.isfile(dest_file_path):
                        print('Removing Pre-existing file: ', dest_file_path)                        
                        os.remove(dest_file_path) 
                    else:
                        # If the directory exists remove it
                        print('Removing pre-existing Directory ', dest_file_path)
                        shutil.rmtree(dest_file_path)    
                else:
                    print('The Path is a file: , dest_abs') 
                    os.remove(dest_abs)   


        shutil.move(source_abs,dest_abs)

    except Exception as e:
         print('Error moving file: ',e)

## This function executes an R script that is provided and catches an error
def curator_execute_rscript(cmd):
    if((cmd==None) or (cmd==[])):
       print("Please specify a proper R script to execute.")
       exit()

    try:
       x = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
       print(e.output)

# This function copies the stats files
def copy_stats_png_files(source_dir, target_dir):
    try:
        os.makedirs(target_dir, exist_ok=True)
        for filename in os.listdir(source_dir):
            if filename.endswith("_stats.png"):
                source_path = os.path.join(source_dir, filename)
                target_path = os.path.join(target_dir, filename)
                shutil.move(source_path, target_path)
                print(f"Copying {filename} to {target_dir}")
        print("Copying complete.")
    except Exception as e:
        print(f"An error occurred: {e}")