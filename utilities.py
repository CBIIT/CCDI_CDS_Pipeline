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


def curator_move_file(source:str, dest:str):
    if((source==None) or (dest==None)):
       print("Please specify source and destination l.")
       exit()

          
    source_path = os.path.abspath(source)
    destination_path = os.path.abspath(dest)
    
    print('Source: ',source)
    print('Source Path Abs: ', source_path)
    print('Dest: ',dest)
    print('Dest Path Abs: ', destination_path)            
    try:
        if os.path.exists(destination_path):
            if os.path.isdir(source_path):
                # Remove destination directory if it exists
                source_base_dir=os.path.abspath(source_path).split(os.path.sep)[-1]
                        # ReCalculate the abspath of the destination directory
                destination_path = os.path.join(destination_path,source_base_dir)
                if os.path.isdir(destination_path):
                    print('Removing pre-existing Directory ', destination_path)
                    shutil.rmtree(destination_path)
            else:
                # Remove destination file if it exists
                file_name=os.path.basename(source_path)
                dest_file_path=os.path.join(destination_path,file_name)
                if os.path.exists(dest_file_path):
                    print('Removing pre-existing File ', dest_file_path)
                    os.remove(dest_file_path)

        shutil.move(source_path, destination_path)
        print(f"Moved '{source_path}' to '{destination_path}'")
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