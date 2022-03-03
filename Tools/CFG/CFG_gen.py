import angr
from angrutils import *
from cfgexplorer import cfg_explore
import os

def get_all_filepath(dir):
    parents = os.listdir(dir)
    for parent in parents:
        child = os.path.join(dir,parent)
        if os.path.isdir(child):
            get_all_filepath(child)
            # continue
        else:
            suffix = os.path.splitext(child)[1]
            #print(suffix)
            if suffix ==".out":
                all_file_list.append(child)

all_file_list=[]
CFG_Path="/Path/To/The/Directory/That/Need/To/Generate/CFGs"
get_all_filepath(CFG_Path)

for path in all_file_list:

    print(path)
    proj = angr.Project(path, load_options={'auto_load_libs':False},
                        use_sim_procedures=True,
                        default_analysis_mode='symbolic')

    main = proj.loader.main_object.get_symbol("main")
    start_state = proj.factory.blank_state(addr=main.rebased_addr)
    cfg = proj.analyses.CFGEmulated(context_sensitivity_level=2,fail_fast=True, starts=[main.rebased_addr], initial_state=start_state,keep_state=True,state_add_options=angr.sim_options.refs,normalize=True)
    plot_cfg(cfg, path,format="dot", asminst=True, remove_imports=True, remove_path_terminator=True)  
