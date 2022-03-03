This repository contains the tools and scripts for running SCAGuard.

## File Tree

```
├── README.md
├── SCAGuard
│   ├── Analyze
│   ├── Detect
│   ├── Normalize.py
│   ├── xprint.py
│   ├── SCAGuard_AC.sh
│   ├── SCAGuard_VC.sh
│   └── SCAGuard.conf
└── Tools
    ├── bingraphvis
    ├── CacheSimulator
    ├── CFG
    ├── Intel PT
    └── Perf
```

- SCAGuard: contains the SCAGuard and its configuration file.
- Tools: contains the necessary tools to help running SCAGuard.
  - bingraphvis: A  tool for dumping the CFG, here is a bug-fix version from  https://github.com/axt/bingraphvis.
  - CacheSimulator:  A Cache simulator for generating Cache State Transition.
  - Intel PT: The scripts and pintool for collecting memory addresses.
  - Perf: The script for collecting HPC data. 

## Requirements

- Python3.7
- numpy 1.19.2
- pydotplus 2.0.2
- angr 9.0.5034
- angr-utils  0.5.0
- cfg-explorer  0.0.1
- bingraphvis (our bug-fix version)
- beautifulsoup4   4.9.3
- capstone 4.0.2
- pyvex  9.0.5034
- gensim 4.0.1
- tslearn  0.5.0.5

## Preparation

#### Preparation for Pintool instrumentation

We use *Intel pin* version 3.13-98189-g60a6ef199-gcc-linux.

For building and running the pintool for memory access collection, do:

```
cp Tools/Intel PT/dtrace.cpp /Path/TO/pin-3.13-98189-g60a6ef199-gcc-linux/source/tools/ManualExamples/
cp Tools/Intel PT/acompile.sh /Path/TO/pin-3.13-98189-g60a6ef199-gcc-linux/source/tools/ManualExamples/
cd pin-3.13-98189-g60a6ef199-gcc-linux/source/tools/ManualExamples/
./acompile.sh
```

#### Preparation for HPC Data Collection

We use *perf* version 5.9.10.

To use perf, do:

`sudo sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'`

`sudo sh -c "echo 0 > /proc/sys/kernel/kptr_restrict"`

#### Preparation for CFG Collection

We need to set a specific directory that contains the binaries need to generate CFGs.

1. Open `Tools/CFG/CFG_gen.py`

2. Set the specific directory at `CFG_Path`. 

#### Preparation for SCAGuard

Before use the SCAGuard, we need to set the paths of the necessary data and tools for SCAGuard.

1. Open `SCAGuard/SCAGuard.conf`
2. Set a path that contains samples at `file_path` . The samples could be selected from https://github.com/SCAGuard/DataSet.
3. Set a path to store log files at  `log_path`.
4. Set the path of Intel Pin at `intelpin_path`.
5. Set the path of Cache Simulator at `cachetool_path`.
6. Set the directory that contains PoCs at  `POC_dir`.
7. We also need to set the path for each PoC. The path of Flush+Reload/ Prime+Probe/ Flush+Reload with Spectre/ Prime+Probe with Spectre should be filled at `POC_fr`/`POC_pp`/`POC_frspectre`/`POC_ppspectre` respectively.
8. Similarly, the path to the target programs also needs to be set. The path of Flush+Reload/ Prime+Probe/ Flush+Reload with Spectre/ Prime+Probe/Benign Programs can be set at `FR_dir`/ `PP_dir` / `FRSpectre_dir`/ `PPSpectre_dir`/ `Benign_dir`respectively.

## How to use SCAGuard

#### Data Collection

1. Leverage the script `Tools/Perf/collect.sh`  to collect the HPC data of each sample.  Then you will get the HPC data file `*.out.txt` for each sample.
2. Use `Python3.7 Tools/CFG/CFG_gen.py` to generate the CFGs of the samples. Then the CFG data file `*.out.dot`  is generated for each sample.

#### Data Analysis

3. To extract the attack-related basic blocks for attack modeling, Data Analysis is necessary by executing `./SCAGuard/Analyze`.

#### Attack Detection and Classification

4. To get the data  in Table 5, use:

   `./SCAGuard/SCAGuard_AC.sh`

#### Variants Detection and Classification

5. To get the data  in Figure 8, use:

​     `./SCAGuard/SCAGuard_VC.sh`
