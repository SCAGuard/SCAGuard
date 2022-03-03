from __future__ import print_function
from multiprocessing import context
from capstone import *
from capstone.x86 import *
from pyvex.lifting import register
from xprint import to_hex, to_x, to_x_32
import angr
from capstone import *
from gensim import corpora
import tslearn.metrics
import numpy as np
import json
import sys, getopt
import os

# Instruction Normalization
# 1.Extract the basic block with angr.
# 2.Parse each instruction in the instruction sequence in such basic block with capstone.
# 3.With the parsed results, we can normalize the instruction sequence.
def common_block(program_path):
    p = angr.Project(program_path, auto_load_libs=False)

    address_list_path=program_path+".block"
    common_addr_list=[]
    with open(address_list_path,'r') as address_list:
        context=address_list.read()
        context=context.replace("[","").replace("]","").replace("\n","")
        context=context.split(",")
        for item in context:
            if item != "":
                common_addr_list.append(int(item,16))


    common_block_list=[]

    for addr in common_addr_list:
        bb = p.factory.block(addr)
        CODE =bb.bytes

        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        str=""
        for insn in md.disasm(CODE, addr):
            str+=insn.mnemonic
            str+=" "

            if len(insn.operands) > 0:
                c = -1
                for i in insn.operands:
                    c += 1
                    if i.type == X86_OP_REG:
                        str+="reg"
                    if i.type == X86_OP_IMM:
                        str+="imm"
                    if i.type == X86_OP_MEM:
                        str+="mem"
                    if c<len(insn.operands)-1:
                        str+=" "
                str+="|"
        common_block_list.append(str)
    return common_block_list
        


# Construct a dictionary for each normalized instruction
def convert2dics(documents,dict):
    items=[]
    for item in documents:
        tmpitems=[]
        res=item.split("|")
        for i in res:
            if i!="":
                tmpitems.append(dict[i])
        items.append(tmpitems)
    return items


# List the files in target directory
def get_all_filepath(dir,ext):
    parents = os.listdir(dir)
    for parent in parents:
        child = os.path.join(dir,parent)
        if os.path.isdir(child):
            get_all_filepath(child,ext)
        else:
            suffix = os.path.splitext(child)[1]
            if suffix ==ext or suffix==".amd64-m64-gcc42-nn":
                all_file_list.append(child)

# Transform a long instruction sequence into a list of instruction
def word_cut(doc):
    seg = [w.split("|") for w in doc]
    return seg


#Encode the noamalized instruction
def ins_encode(file,dictionary):
    file_block_list=common_block(file)
    file_encode=convert2dics(file_block_list,dictionary.token2id)

    str_group=""
    for ises in file_encode:
        # str_group+="["
        
        # for item in ises:
        str_group+=str(ises)
        
        str_group+="\n"

    with open(file+".is","w") as f:
            f.write(str_group)
    


if __name__ == "__main__":

    argvs=sys.argv[1:]
    worktype=""
    try:
      opts, args = getopt.getopt(argvs,"ht:",["help","type="])
      if(len(opts)==0 or len(opts)>=2):
        print('-h help -t type')
        # worktype="AC"
        sys.exit(2)
    except getopt.GetoptError:
        print('-h help -t type')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-h help -t <AC|VC>')
            print('AC:"Attack Classification"')
            print('VC:"Variant Classification"')
            sys.exit()
        elif opt in ("-t", "--type"):
            if arg=="AC" or arg=="VC":
                worktype = arg
                print("WORK TYPE:"+arg)
        else:
            print('-h help -t type')
            sys.exit(2)

    #1. Parse the config.
    config=[]
    with open("./SCAGuard.conf","r") as f:
        config=json.load(f)

    POC_dir=config["POC_dir"]
    POC_fr=config["POC_fr"]
    POC_pp=config["POC_pp"]
    POC_frspectre=config["POC_frspectre"]
    POC_ppspectre=config["POC_ppspectre"]

    FR_dir=config["FR_dir"]
    PP_dir=config["PP_dir"]
    FRSpectre_dir=config["FRSpectre_dir"]
    PPSpectre_dir=config["PPSpectre_dir"]
    Benign_dir=config["Benign_dir"]

    #2. Add the instructions of the POCs into the dictionary 
    all_file_list=[]
    get_all_filepath(POC_dir,".out")
    documents=[]
    for file in all_file_list:
        file_block_list=common_block(file)
        for ins in file_block_list:
            documents.append(ins)

    #3. Add the instructions of the target programs into the dictionary 
    if worktype=="AC":
        paths=[FR_dir,PP_dir,FRSpectre_dir,PPSpectre_dir,Benign_dir]
    else:
        paths =[FRSpectre_dir,PPSpectre_dir,Benign_dir]

    for file_index in range(len(paths)):
        
        all_file_list=[]
        get_all_filepath(paths[file_index],".out")
        print(file_index)

        for file in all_file_list:
            file_block_list=common_block(file) #Instruction Normalization
            for ins in file_block_list:
                documents.append(ins)

    #4. Assign a unique code for each instruction in the dictionary
    texts= word_cut(documents)
    dictionary = corpora.Dictionary(texts)


    #5. Encode the normalized instructions
    all_file_list=[]
    get_all_filepath(POC_dir,".out")
    documents=[]
    for file in all_file_list:
        print(file)
        ins_encode(file,dictionary)


    if worktype=="AC":
        paths=[FR_dir,PP_dir,FRSpectre_dir,PPSpectre_dir,Benign_dir]
    else:
        paths =[FRSpectre_dir,PPSpectre_dir,Benign_dir]

    for file_index in range(len(paths)):

        all_file_list=[]
        get_all_filepath(paths[file_index],".out")

        for file in all_file_list:
            print(file)
            ins_encode(file,dictionary)


            
            
            