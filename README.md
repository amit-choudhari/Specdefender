<img src="https://github.com/amit-choudhari/Specdefender/blob/main/images/icon.png" width=20% height=20%>
# Specdefender
Static defences against spectre such as load barriers, Retpoline, etc suffers the performance of the process. And dynmaic defences mostly attempt to kill the process. We propose a tool that aims to bring a balance between performance, security and availability. SpecDefender is a tool that dynamically defend against spectre attack.
![Modules](https://github.com/amitsirius/Specdefender/blob/main/images/specdefender\_modules.png?raw=true)
## Table of contents
* [General info](#general-info)
* [Core components](#core-components)
* [Working](#working)
* [TODO](#todo)

## General info



## Core components
There are three major components of this tool.
1. Counter (Counter.py): Collects HPC data of the process under observation for 100ms. 
2. Detector (detector.py): Detects the presense of Spectre using a pre-trained multi-class model.
3. Patching (patch.py): Restart the program with spectre defence (load barriers) instrumented in the binary.
![Class Diagram](https://github.com/amitsirius/Specdefender/blob/main/images/specdefender\_class\_diagram.png?raw=true)

#### Working:
When a process is under spectre attack, the attacker tries to continuously mistrain the branch predictor and perform cache attack. This behaviour causes an unusual number of cache misses and speculative loads. Specdefender detects these abnormalities using a pre-trained model and restarts the process with spectre defences.
![Working Diagram](https://github.com/amitsirius/Specdefender/blob/main/images/specdefender\_working.PNG?raw=true)

In presence of SpecDefender, when a process is attacked by spectre it transitions through 4 states. 
1. Normal: Spectre-unsafe high performance program
2. Attack: Spectre-unsafe high performance program under attack [transient state]
3. safe under attack: Spectre-safe slow program under attack
4. safe: Spectre-safe slow program not under attack
![State Diagram](https://github.com/amitsirius/Specdefender/blob/main/images/specdefender\_state.PNG?raw=true)
## Usage
Run the detector.py file along with sample spectre test code from /test directory.
![usage](https://github.com/amitsirius/Specdefender/blob/main/images/specdefender\_usage.PNG?raw=true)
## Original paper

```
@inproceedings{10.1145/3560834.3563830,
author = {Choudhari, Amit and Guilley, Sylvain and Karray, Khaled},
title = {SpecDefender: Transient Execution Attack Defender Using Performance Counters},
year = {2022},
isbn = {9781450398848},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3560834.3563830},
doi = {10.1145/3560834.3563830},
booktitle = {Proceedings of the 2022 Workshop on Attacks and Solutions in Hardware Security},
pages = {15–24},
numpages = {10},
keywords = {efficient mitigation, speculative execution, spectre, transient execution attack},
location = {Los Angeles, CA, USA},
series = {ASHES'22}
}
```

## TODO
- [-] Add support for DBI

**Free Software, Hell Yeah!**


