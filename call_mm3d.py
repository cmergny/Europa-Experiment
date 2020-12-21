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
    global in_dir
    """Type the cmd argument in a terminal shell and print the output"""
    print(f"--- Calling command : {cmd} ---")
    call_result = subprocess.run(cmd, capture_output=True,text=True)
    #print(call_result.stderr)
    print(call_result.stdout)
    with open(f'{in_dir}/callmm3d-log.txt', 'a') as f:
        f.write(f"--- Calling command : {cmd} --- \n")
        f.write(call_result.stderr)
        f.write(call_result.stdout)
    return(None)

def CreateMasqs(in_dir, master_nbr):
    """"Open the mm3d SaisieMasqQt GUI for all sets in the input folder"""
    for folder_name in glob.glob(in_dir + '/set_***'):
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
    
    for folder_name in glob.glob(in_dir + '/set_***'):
        print(f'Moving to folder : "{folder_name}".')
        os.chdir(folder_name)
        folder_name = folder_name.split('\\')[-1]
        
        # cmd = 'mm3d SaisieAppuisInitQT ".*.JPG" Folder1 Dico-Appuis.xml Mesure-Appuis.xml'
        # CallCommand(cmd)
        # cmd = 'mm3d GCPBascule ".*.JPG" Folder1 Etape_ini Dico-Appuis.xml Mesure-Appuis-S2D.xml'
        # CallCommand(cmd)
        # cmd = 'mm3d Campari ".*.JPG" Etape_ini Folder'
        # CallCommand(cmd)
        # cmd = 'mm3d AperiCloud ".*.JPG" Folder'
        # CallCommand(cmd)

        
        # cmd = 'mm3d Tapioca All ".*JPG" -1'
        # CallCommand(cmd)
        # cmd = 'mm3d Tapas FraserBasic ".*JPG" Out=Folder'
        # CallCommand(cmd)
        # cmd = 'mm3d AperiCloud ".*JPG" Folder '
        # CallCommand(cmd)
        # cmd = f'mm3d Malt GeomImage ".*JPG" Folder Master={master_nbr}.JPG ZoomF=1'
        # CallCommand(cmd)
        cmd = f'mm3d Nuage2Ply "MM-Malt-Img-{master_nbr}/NuageImProf_STD-MALT_Etape_8.xml" Attr="{master_nbr}.JPG" Out=8.ply RatioAttrCarte=1'
        CallCommand(cmd)
        
        #cmd = f'mm3d Nuage2Ply "MM-Malt-Img-{master_nbr}/NuageImProf_STD-MALT_Etape_7.xml" Attr="{master_nbr}.JPG" Out=7.ply RatioAttrCarte=2'
        #CallCommand(cmd)


        
        #cmd = f'mm3d GrShade MM-Malt-Img-{master_nbr}/Z_Num7_DeZoom2_STD-MALT.tif ModeOmbre=IgnE Mask=AutoMask_STD-MALT_Num_6.tif FZ=2 Out={in_dir}/depth_maps/{folder_name}.JPG'
        #CallCommand(cmd)

        #cmd = f'meshlabserver -i 7.ply -o mesh_{folder_name[-3:]}.ply -s {in_dir}\script.mlx'
        #CallCommand(cmd)
        
        
    return(None)
    

#### Main

if __name__ == '__main__':
    
    user_friendly = False
    
    if user_friendly:
        ## Find input folder  
        in_dir = BrowseFolder(user_friendly)
        master_nbr = int(input("master_nbr = "))
    else:
        ## Manual Definition 
        in_dir = "C:/Users/Arnaud/EuropaExp/XP1612/Stereo" # input dir
        in_dir = BrowseFolder(user_friendly, in_dir)
        master_nbr = 3
    
    # Create a log file for shell outputs
    f = open(f'{in_dir}/callmm3d-log.txt', 'w')
    f.close()
    print(glob.glob(in_dir + '/set_***'))
    
    #CreateMasqs(in_dir, master_nbr)
    Callmm3d(in_dir)
    

# mm3d SaisieAppuisInitQT ".*.JPG" Folder Dico-Appuis.xml Mesure-Appuis.xml
    
# mm3d GCPBascule ".*.JPG" Folder1 Etape_ini Dico-Appuis.xml Mesure-Appuis-S2D.xml
# mm3d Campari ".*.JPG" Etape_ini Etape_inter
# mm3d AperiCloud ".*.JPG" Folder
