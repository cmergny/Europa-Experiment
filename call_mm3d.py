# -*- coding: utf-8 -*-
"""
call mm3d (Micmac) commands
Author: Cyril Mergny
Last update : 26/11/2020
"""

### Imports 

import glob
import os
import subprocess
from laser_process import BrowseFolder

### Functions

def CallCommand(cmd):
    """Type the cmd argument in a terminal shell and print the output"""
    print(f"--- Calling command : {cmd} ---")
    call_result = subprocess.run(cmd, capture_output=True,text=True)
    print(call_result.stderr)
    print(call_result.stdout)
    return(None)

def CreateMasqs(in_dir, master_nbr):
    """"Open the mm3d SaisieMasqQt GUI for all sets in the input folder"""
    for folder_name in glob.glob(in_dir + 'set_*')[:1]:
        ## Change os dir to input directory
        os.chdir(folder_name)
        print(f'Moving to folder : "{folder_name}".')
        # Call command
        cmd = f'mm3d SaisieMasqQT {master_nbr}.JPG'
        CallCommand(cmd)
        ## Change back
        script_dir = os.path.dirname(__file__)
        os.chdir(script_dir)
        print(f"Change os path back to {script_dir}")
    return(None)

def Callmm3d(in_dir):
    
    for folder_name in glob.glob(in_dir + 'set_*')[:1]:
        print(f'Moving to folder : "{folder_name}".')
        os.chdir(folder_name)
    
        cmd = 'mm3d Tapioca All ".*JPG" -1'
        CallCommand(cmd)
        
        cmd = 'mm3d Tapas FraserBasic ".*JPG" Out=Folder'
        CallCommand(cmd)
        
        cmd = 'mm3d AperiCloud ".*JPG" Folder '
        CallCommand(cmd)
        
        cmd = 'mm3d Malt GeomImage ".*JPG" Folder Master={}.JPG ZoomF=2'.format(master_nbr)
        CallCommand(cmd)
        
        cmd = 'mm3d Nuage2Ply "MM-Malt-Img-{0}/NuageImProf_STD-MALT_Etape_7.xml" Attr="{0}.JPG" Out=7.ply RatioAttrCarte=2'.format(master_nbr)
        CallCommand(cmd)
        
        cmd = 'mm3d GrShade MM-Malt-Img-{}/Z_Num7_DeZoom2_STD-MALT.tif ModeOmbre=IgnE Mask=AutoMask_STD-MALT_Num_6.tif FZ=2 Out=depth7.tif'.format(master_nbr)
        CallCommand(cmd)
        
        cmd = 'meshlabserver -i 7.ply -o output.ply -s script.mlx'
        CallCommand(cmd)
        
    return(None)
    

#### Main

if __name__ == '__main__':
    
    user_friendly = True
    
    if user_friendly:
        ## Find input folder  
        in_dir = BrowseFolder(user_friendly)
        master_nbr = int(input("master_nbr = "))
    else:
        ## Manual Definition 
        in_dir = "C:/Users/Cyril/Documents/EuropaExp/photos" # input dir
        in_dir = BrowseFolder(user_friendly, in_dir)
        master_nbr = 3
        
    CreateMasqs(in_dir, master_nbr)
    Callmm3d(in_dir)
    
    

    


