# JetMETAnalysisMCtruth

<!-- MarkdownTOC depth=0 -->

- [Introduction](#introduction)
- [Documentation](#documentation)
- [Log book of previous changes](#logbook)
	- [Changes from CMSSW_10_6_X to CMSSW_12_6_X](#changes_106Xto126X) 
	- [Changes from CMSSW_12_6_X to CMSSW_13_0_X and beyond (up to at least CMSSW_14_2_X)](#changes_126Xto130X)
- [HOW TO: Setup the framework](#setup-cmssw)
- [HOW TO: Produce ntuples from MINIAOD](#ntuples-miniaod)
 	- [Important codes for producing ntuples](#important-codes)
 	- [How to produce JRA ntuples](#produce-ntuples)
- [HOW TO: Create histograms for PU reweighting](#PU-reweight)
	- [Histogram for data](#PU-reweight-data)
 	- [HIstogram for MC](#PU-reweight-mc) 
	- [Plotting and validation of PU reweighting](#PU-reweight-validation)      
- [HOW TO: Jet veto maps](#jet-veto-maps)
- [HOW TO: Gen pT spectrum](#gen-pt-spectrum)
- [HOW TO: derive MC truth JECs, perform sanity checks and validations](#JEC)
	- [Getting started](#getting_started)
	- [Brief overview](#brief_overview)
	- [General tips for HTCondor](#condor) 
	- [Pileup offset corrections (`L1FastJet`) and pileup offset monitoring](#L1)
		- [Step1 -- event matching between `EpsilonPU` and `FlatPU` MC datasets](#step1)
		- [Step2 -- derivation of `L1FastJet` corrections](#step2-derivation)
		- [Pileup offset monitoring and plotting](#step2-plotting)
	- [Jet response corrections (`L2Relative`)](#L2L3)
	    - [Step3 -- derivation of `L2Relative` corrections](#step3)
		- [Step4 -- plotting of jet response](#step4)
		- [Dedicated JECs for the BPix and FPix regions](#bpix-fpix)
    - [Correction factors](#corr-factors)

<!-- /MarkdownTOC -->

<a name="introduction"></a>
# Introduction

The code contained in this package is used for creating and analyzing the `L1FastJet` and `L2Relative` MC truth jet energy corrections. The code is used by the Jet Energy Resolution and Corrections (JERC) subgroup. This is a dedicated workflow for the MC-truth jet energy corrections used by the Athens group. The original code is located at https://github.com/cms-jet/JetMETAnalysis .

<a name="documentation"></a>
# Documentation

1) CMS-AN-2023/061, "MC truth jet energy corrections using the 2022, 2023 and 2024 Run-3 simulations": \
https://cms.cern.ch/iCMS/user/noteinfo?cmsnoteid=CMS%20AN-2023/061

3) CMS-AN-2021/148, "MC truth jet energy corrections using the Legacy 2016 simulations": \
https://cms.cern.ch/iCMS/user/noteinfo?cmsnoteid=CMS%20AN-2021/148 

4) CMS-AN-2020/151, "MC truth jet energy corrections using the Legacy 2017 and 2018 simulations": \
https://cms.cern.ch/iCMS/user/noteinfo?cmsnoteid=CMS%20AN-2020/151

5) CMS-AN-2020/049, "2018 Relative and Absolute MC Truth Jet Energy Corrections": \
https://cms.cern.ch/iCMS/user/noteinfo?cmsnoteid=CMS%20AN-2020/049

6) CMS-AN-2019/230, "2016 Relative and Absolute MC Truth Jet Energy Corrections": \
https://cms.cern.ch/iCMS/user/noteinfo?cmsnoteid=CMS%20AN-2019/230


<a name="logbook"></a>
# Log book of previous changes

In some cases, when moving to a newer CMSSW version, compilation errors when doing `scram b -j 8` arise. In this section the necessary changes to the framework when migrating from a CMSSW version to a newer one will be presented, for book keeping purposes. None of these need to be repeated by the user. The current version of the framework works for the most recent CMSSW_14_2_X version.

<a name="changes_106Xto126X"></a>
# Changes from CMSSW_10_6_X to CMSSW_12_6_X

1) Open the `JetMETAnalysis/JetAnalyzers/BuildFile.xml` code and in line 20 replace `SimDataFormats/JetMatching` with `DataFormats/JetMatching`
2) Open the codes `JetMETAnalysis/JetAnalyzers/interface/JetResponseAnalyzer.hh` and `JetMETAnalysis/JetAnalyzers/interface/JetResponseAnalyzerProducer.hh` and replace `SimDataFormats/JetMatching` with `DataFormats/JetMatching` in lines 45 and 43 respectively.
3) `cp /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/include/c++/9.3.0/bits/stl_tree.h JetMETAnalysis/JetUtilities/interface/`
4) Open the `JetMETAnalysis/JetUtilities/interface/stl_tree.h` code and comment out lines 778-781 which are responsible for giving the error `static assertion failed: comparison object must be invocable as const`
5) Open the `JetMETAnalysis/JetAnalyzers/bin/jet_match_x.cc` and `JetMETAnalysis/JetAnalyzers/bin/jet_synchtest_x.cc` codes and add *before any other include* the following: `#include "JetMETAnalysis/JetUtilities/interface/stl_tree.h"`
6) Then, open the `../tmp/slc7_amd64_gcc900/src/JetMETAnalysis/JetUtilities/src/JetMETAnalysisJetUtilities/a/JetMETAnalysisJetUtilities_xr.cc` code and do the same -> add *before any other include* the following: `#include "JetMETAnalysis/JetUtilities/interface/stl_tree.h"`
7) Move the `SynchFittingProcedure.hh` code from `JetMETAnalysis/JetUtilities/src/` to the `JetMETAnalysis/JetUtilities/interface/` folder and then open the `JetMETAnalysis/JetAnalyzers/bin/jet_synchplot_x.cc` code and in line 35 replace `src/` with `inteface/` (to provide the new correct path).
8) Modify python files to work with python3: 4 spaces instead of a tab, `algsizetype.items()` instead of `algsizetype.iteritems()`, add parentheses in print commands, `list(genJetsDict.keys()).index(alg_size_type)` instead of `genJetsDict.keys().index(alg_size_type)` 

<a name="changes_126Xto130X"></a>
# Changes from CMSSW_12_6_X to CMSSW_13_0_X and beyond (up to at least CMSSW_14_2_X)

1) Change to `edm::one::EDAnalyzer<>` and `edm::one::EDProducer<>` from `edm::EDAnalyzer` and `edm::EDProducer` respectively. Modify the includes as well.

2) Copy the file `/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/gcc/11.2.1-f9b9dfdd886f71cd63f5538223d8f161/include/c++/11.2.1/bits/stl_tree.h` to the `JetMETAnalysisMCtruth/JetUtilities/interface` directory and comment out lines 768-771

3) In `JetUtilities/src/JetInfo.cc` line 361 change `assert(words>0)` to `assert(words != nullptr)`

4) From CMSSW_12_6_X copy the codes `JetMETCorrections/Objects/interface/JetCorrector.h` and `cmssw/JetMETCorrections/Objects/src/JetCorrector.cc` and paste them to `JetUtilities/interface/` and `JetUtilities/src/` respectively. In `JetCorrector.cc` comment out lines 48-53, and in `JetAnalyzers/src/JetResponseAnalyzer.cc`, `JetAnalyzers/src/JetResponseAnalyzerProducer.cc` write `jetCorrector_ =  0`

5) From CMSSW_12_6_X copy the codes `JetMETCorrections/Configuration/python/JetCorrectionServicesAllAlgos_cff.py` and `JetMETCorrections/Configuration/python/JetCorrectionServices_cff.py` and paste them inside `JetAnalyzers/python/`


<a name="setup-cmssw"></a>
# HOW TO: Setup the framework

Setup the code in the AFS area and not the EOS user area, because HTCondor is used, that is not compatible with EOS.

```
mkdir MCtruthJEC/ 
cd MCtruthJEC/ 
cmsrel CMSSW_14_2_2 
cd CMSSW_14_2_2/src 
cmsenv 
git clone https://gitlab.cern.ch/cms-analysis/jme/jerc-derivation/JetMETAnalysisMCtruth.git
```

Then compile:

```
scram b -j 8 
```

In the first compilation you will get a compilation error about `is_invocable_v<const _Compare&, const _Key&, const _Key&>`. 

Open the file `CMSSW_14_2_2/tmp/el9_amd64_gcc12/src/JetMETAnalysisMCtruth/JetUtilities/src/JetMETAnalysisMCtruthJetUtilities/lcgdict/JetMETAnalysisMCtruthJetUtilities_xr.cc` and before any other include (among lines 6 and 7) add the following line:

```
#include "JetMETAnalysisMCtruth/JetUtilities/interface/stl_tree.h"
```

Re-compile and there should be no errors. The aforementioned `JetMETAnalysisMCtruthJetUtilities_xr.cc` script is autogenerated, so if this error comes back again in any given time, repeat the step above.

**Very important note:** Every time there you change any `.cc` or `.hh` or `.h` code inside `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers` or `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities` you should then re-compile, doing `scram b -j 8` for the changes to take effect.

<a name="ntuples-miniaod"></a>
# HOW TO: Produce ntuples from MINIAOD

In this section instructions are provided on how to produce a JRA ntuple which contains a tree with event and matched rec-gen jet variables, needed for the JEC derivation.

<a name="important-codes"></a>
# Important codes for producing ntuples

1) `JetMETAnalysisMCtruth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py` \
**Lines 25-26**: Specify the jet collections to be saved in the JRA trees \
**Line 51**: Insert global tag of sample to be processed \
**Line 69**: Specify how many events to be processed, -1 stands for all events in the sample \
**Line 79**: Specify which MiniAOD root file to be processed for a local test 

The `run_JRA_cfg_MCtruth.py` script then uses the `addAlgorithm.py` one:

2) `JetMETAnalysisMCtruth/JetAnalyzers/python/addAlgorithm.py` \
**Line 382**: Specify the raw jet pT cut with which the rec-gen matching will be performed, and jets will be saved in the JRA trees (default = 0 GeV) \
**Lines 391-407**: While reconstructing PUPPI jets the code uses the following commands to consider the stored PUPPI weights in the dataset:

```
process.puppi.useExistingWeights = True
process.puppiNoLep.useExistingWeights = True
```

3) `JetMETAnalysisMCtruth/JetAnalyzers/python/customizePuppiTune_cff_V15.py` \
This is a configuration file for applying the V15 PUPPI tune recipe. If one did not want to use the default PUPPI weights in the dataset but wanted to re-calculate the V15 weights on the fly, they should load and call in `addAlgorithm.py` this file, while turning the options above to `False`. **NOT needed anymore, as the V15 tune is outdated**.

4) `JetMETAnalysisMCtruth/JetAnalyzers/python/Defaults_cff.py` \
**Line 33**: Rec-gen jet pairings are saved in the ntuple, along with their deltaR. Change the maximum deltaR value that is saved (default = 999, i.e. write everything). The `deltaR < 0.2 (0.4)` criterion will be used later in another step, so here we save all of them.

5) `JetMETAnalysisMCtruth/JetAnalyzers/src/JetResponseAnalyzer.cc`, `JetMETAnalysisMCtruth/JetAnalyzers/interface/JetResponseAnalyzer.hh`, `JetMETAnalysisMCtruth/JetUtilities/src/JRAEvent.cc`, `JetMETAnalysisMCtruth/JetUtilities/interface/JRAEvent.h` \
These codes produce the trees. They do not need any change at the moment. If a new variable needs to be added in the tree of the JRA ntuples these are the codes that need to be modified.


<a name="produce-ntuples"></a>
# How to produce JRA ntuples

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/test/
```

Before submitting jobs to crab run a **local test** first:

In the code `JetMETAnalysisMCtruth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py` specify a MiniAOD root file and a small number of events. Then do:

```
cmsenv 
voms-proxy-init -voms cms 
cmsRun run_JRA_cfg_MCtruth.py
```

This test will produce a file named `JRA.root` in the directory you are in, containing the small number of events specified. If there are no errors, the JRA.root is produced, and the trees are filled properly, then CRAB jobs can be submitted in order to process the full MC sample.


How to **submit jobs to CRAB**:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/test/
```

In the code `JetMETAnalysisMCtruth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py` put as number of events to process -1

In the code `JetMETAnalysisMCtruth/JetAnalyzers/test/custom_crab_JEC.py`:

**Lines 4-5**: Submitting jobs will create a folder `workArea/requestName/` inside `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/test/` \
**Line 14**: Specify the MiniAOD MC sample name (from DAS) to process \
**Line 17**: Specify how many CRAB jobs to have per MiniAOD root file (default = 1 for faster production). The larger this number, the fewer the total CRAB jobs, and thus the longer it will take for each job to run \
**Line 20**: Specify name of folder that will be created in the output EOS directory. Here we usually use `PremixedPU` or `FlatPU0to120` or `EpsilonPU` \
**Line 21**: Specify output directory where the JRA ntuples will be saved. Note that `/eos/cms/` should not be written before `/store/group/phys_jetmet/`

Once you are done, submit the CRAB jobs:

```
voms-proxy-init -voms cms 
crab submit -c custom_crab_JEC.py
```

To check the status of jobs in CRAB while inside `JetMETAnalysisMCtruth/JetAnalyzers/test/`:

```
crab status -d workArea/requestName/
```

To resubmit jobs if some have failed:

```
crab resubmit -d workArea/requestName/
```

When all jobs are in finished status, the output JRA root files, based on the above `custom_crab_JEC.py`, will be located in a directory with this format:\
`/eos/cms/store/group/phys_jetmet/ilias/test/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/outputDatasetTag/yymmdd_hhmmss/0000/`

These JRA root files are the input ntuples for the MC-truth jet energy corrections.

**Please note**: All Run-3 MC ntuples so far have been produced by Ilias (me), and are located in: 

```
/eos/cms/store/group/phys_jetmet/ilias/Run3MCtruthSamples/NoRawPtCut/
```

<a name="PU-reweight"></a>
# HOW TO: Create histograms for PU reweighting

The only event weights applied in this analysis are the ones related to the PU reweighting. This is only relevant for the `L2Relative` derivation where the `PremixedPU` MC is used. We need to produce two root files with the mu (true number of pileup interactions per crossing) distribution; one for data and one for MC. Note that they should have the same binning (we usually use 120 bins from 0 to 120).

<a name="PU-reweight-data"></a>
# Histogram for data

To produce the root file for data:
```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/Histos_PU/ 
cmsenv 
pileupCalc.py -i Cert_Collisions2024_erasBCDEFGHI.json --inputLumiJSON pileup_latest_2024.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 120 --numPileupBins 120  MyDataPUHisto_2024CDEFGHI_120Bins_69200.root 
```

where `Cert_Collisions2024_erasBCDEFGHI.json` is the Golden JSON file for the corresponding era you want to process and `pileup_latest_2024.txt` the pileup JSON for the corresponding year (ask around if you cannot find where they have it). The minimum bias cross section of 69.2 mb has been used so far for the 2022, 2023 and 2024 MCs but studies have shown that for 13.6 TeV data a more representative value is 75.3 mb. The value of 75.3 mb will be used for 2025 MCs onwards (and when 2022, 2023 and 2024 MCs are reproduced). In principle, the MC should have been generated with a mu distribution close to the one of data, such that the weights of the PU reweighting are small and effective statistics is not lost.

If not sure, please ask around for the recommendation before producing this and proceeding to the next steps.

The output file is `MyDataPUHisto_2024CDEFGHI_120Bins_69200.root` that contains a histogram of the mu distribution named `pileup`.

<a name="PU-reweight-mc"></a>
# Histogram for MC

To produce the corresponding root file for MC:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ 
python3 create_mu_distribution.py --era RunIII2024Summer24
```

The output file is `MyMCPUHisto_RunIII2024Summer24_PremixedPU.root` inside `Histos_PU/` that contains a histogram of the mu distribution named `pileup`.


<a name="PU-reweight-validation"></a>
# Plotting and validation of PU reweighting

1) Script that plots the mu distribution of various eras in data:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ 
python3 plot_mu_distributions_data.py
```

**Input:** The `MyDataPUHisto_*.root` files for various eras in data \
**Output:** Plot in PDF format of the mu distribution for various eras in data

2) Script that plots the mu distribution of data, and the corresponding mu distribution of the MC before and after the application of the PU reweighting. If the distributions between data and MC after the reweighting match, this validates that that the PU reweighting was performed properly. 


```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ 
python3 plot_mu_distributions_data_vs_mc.py --data 2024CDEFGHI --mc RunIII2024Summer24
```

**Input:** The `MyDataPUHisto_*.root` file for the era in data, the `MyMCPUHisto_*_PremixedPU.root` file for the MC before the PU reweighting, the hadded file of `Step4Output` from [step4](#step4) for the MC after the PU reweighting \
**Output:** Plot in PDF format with the mu distribution of data, MC before and MC after

<a name="jet-veto-maps"></a>
# HOW TO: Jet veto maps

The jet veto map is a root file that contains `TH2D` histograms which define the jet eta-phi zones that should be excluded from your selection. 

Take the most recent jet veto map for the corresponding era/MC campaign from the JERCProtolab (https://gitlab.cern.ch/cms-jetmet/JERCProtoLab) and put it inside `Histos_JetVetoMaps/`

Script that plots the jet veto map:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ 
python3 plot_jet_veto_maps.py --era 2023D
```

**Input:** The `JetVetoMap_*.root` inside `Histos_JetVetoMaps/` \
**Output:** Plot in PDF format with the veto maps for each issue (`hot`, `cold`, `eep`, `bpix`, `fpix`, etc) in each era


<a name="gen-pt-spectrum"></a>
# HOW TO: Gen pT spectrum

This is not necessary for the derivation of the MC truth JECs, but it might be useful to examine the gen pT spectrum. We are using `flatQCD` MC datasets and we do not apply pT reweighting, so this spectrum should be flat.

Script to create the histogram of the gen pT spectrum:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 create_ptgen_distribution.py --era RunIII2024Summer24
```

**Input:** The JRA ntuples of the MC dataset \
**Output:** A root file named `GetPT_RunIII2024Summer24_PremixedPU.root` inside `Histos_Pt/`

Then, to plot this spectrum for various MC datasets:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_ptgen_distributions.py
```

**Input:** The root files named `GetPT_*_PremixedPU.root` for various MC datasets (defined in line 62) inside `Histos_Pt/` \
**Output:** A plot in PDF format with the gen pT spectra of these MC datasets


<a name="JEC"></a>
# HOW TO: derive MC truth JECs, perform sanity checks and validations

Here you will learn how to produce pileup offset and jet response histograms and plots, derive the `L1FastJet` (optional for PUPPI) and `L2Relative` corrections, and plot them.

<a name="getting_started"></a>
# Getting started

Based on the jet collection you want to process, your work area will be one of the following directories:

``` 
$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/ 
$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK8PUPPI/
$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/
```

Given that AK4 PUPPI jets are the main jet collection in Run-3, this README will refer to this jet collection only. However, **nothing** changes technically if one wants to process one of the other two collections.

**Please note** that the `L1FastJet` corrections are not part of the mainstream calibration for AK4 and AK8 PUPPI jets, and are not needed. However, in this README, the instructions on how to derive such corrections will be provided anyway. These instructions are identical for AK4 CHS jets, which do need pileup offset corrections.


**Only for the first time do the following**:

1) Open the `CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Setup_CMSSW.sh` file and put the correct `SCRAM_ARCH` in the first line (e.g. `SCRAM_ARCH=el9_amd64_gcc12`). Then in the second line put the full path leading to `condor_AK4PUPPI/` (e.g. `cd /afs/cern.ch/work/<u>/<username>/public/MCtruthJEC/CMSSW_14_2_2/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/`)

2) Open the `CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/makefile`, copy from it the following part and paste in the terminal, exactly as it is written:

```
	g++ ListRunLumi.cpp -o RunListRunLumi \
		`root-config --cflags --libs`
```


<a name="brief_overview"></a>
# Brief overview

The derivation of MC truth JECs consists of four **steps**, each of which consist of a **submission** part and a **harvest** part. These will be explained in detail in the next sections. Here we present a brief overview of what each step does:

**Step1**: Matches events between the `FlatPU` and `EpsilonPU` datasets and produces lists with the matched events.

**Step2**: Matches jets between these events, calculates the offset and produces the `L1FastJet` text file by fitting the `<offset>/Aj` as a function of `<pT>` and `<rho>`. Also produces the necessary plots of the average pileup offset.

**Step3**: Applies the `L1FastJet` text file (if one was derived) and produces histograms of the response distributions vs `pT` and `eta`. Then fits the inverse of the median response as a function of `pT` in fine bins of `eta` and produces the `L2Relative` text file.

**Step4**: Produces 2D histograms of the response vs `pT` and `eta` so as to examine the median response before and after the application of corrections (closure). This step is not necessarily the last one chronologically: if a new MC dataset is produced and one wants to first examine the behavior of the raw jet response, then this step is needed, with the option that no JECs are applied.


<a name="condor"></a>
# General tips for HTCondor

1) Throughout all four steps of the MC truth JECs you will be submitting jobs to HTCondor. You can find more information for HTCondor here: https://batchdocs.web.cern.ch/index.html

2) Once you submit jobs to HTCondor you can check their status by doing:
```
condor_q
``` 

3) You can also check the priority of your jobs with:

```
condor_userprio
```

4) If many people are using the particular `bigbird` scheduler you are in, you can change `bigbird` and move to a less crowded one with the following commands:
```
tcsh
setenv _condor_SCHEDD_HOST bigbird26.cern.ch
```

5) When a job is finished it will disappear from `condor_q`, and a corresponding root file should appear in EOS. Additionally, in the directory `$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Log/` 3 files will appear for each job: `err`, `log`, `out`. Check the `err` and `out` ones to see if there was an error in your codes that made the jobs crash. If you have a bug somewhere then the output root files in EOS will not be created or they will be created empty, so you can also check them by going to the EOS directory and doing `ls -lh` to see the size of the files and if they have closed properly. If the code does not have any bugs then these files should be a few MB (or at least a few hundred thousand KB) each.

6) When running some steps you will get the following error messages, which you can safely ignore, as we are not doing flavor corrections and do not care that our trees do not have these related branches:
```
Error in <TTree::SetBranchAddress>: unknown branch -> refpdgid_algorithmicDef
Error in <TTree::SetBranchAddress>: unknown branch -> refpdgid_physicsDef
```

7) If there are no bugs and the root files have been created correctly then it is usual (especially in [step2](#step2-derivation)) that condor did not run all jobs (due to technical issues related to condor, wall time etc). Therefore you should always check how many output root files were created in EOS by doing `ls | wc -l`: they should be the same number as the jobs you submitted. If they are fewer then you can resubmit the jobs (`./SubmitStep*.sh` as you did in the first time) until all root files are processed. 


<a name="L1"></a>
# Pileup offset corrections (`L1FastJet`) and pileup offset monitoring

Go to the corresponding work area, make a directory with the name of the MC dataset and version of corrections you want to derive (e.g. `RunIII2024Summer24_V1_PhiIndependent/`) and then create an `L1_output` directory:

```
cd CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/
cd Files/
mkdir RunIII2024Summer24_V1_PhiIndependent/
cd RunIII2024Summer24_V1_PhiIndependent/
mkdir L1_output/ 
```

Copy the jet veto map inside the directory above:

```
cd CMSSW_BASE/src/JetMETAnalysisMCtruth/Histos_JetVetoMaps/
cp JetVetoMaps_2024CDEFGHI.root $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L1_output/
```

Modify the `Setup_FileLocation.sh` script with the paths of the input JRA ntuples, and the output root files in EOS: 

1) In `NoPUFiles` you should have the path to the `EpsilonPU` JRA ntuples, while in `WithPUFiles` you should have the path to the `FlatPU` JRA ntuples. 

2) Modify the `Step1Output` and `Step2Output` paths accordingly: this is where the output root files of these steps will appear.


<a name="step1"></a>
# Step1 -- event matching between `EpsilonPU` and `FlatPU` MC datasets


Run the following script which submits HTCondor jobs:

```
./SubmitStep1.sh
```

**Input:** The `EpsilonPU` and `FlatPU` JRA ntuples \
**Output:** Txt files in `Step1Output` that contain lists of matched events

When all jobs are finished and the `err` files inside `Log/` are empty, proceed with the harvesting step:

```
./HarvestStep1.sh
```

**Input:** The txt files in `Step1Output` \
**Output**: A file named `MatchedFiles` inside `CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files`

Rename and copy the output file with the name of the MC dataset, so that it won't get overwritten in the future e.g.:

```
cd CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/
cp MatchedFiles MatchedFiles_RunIII2024Summer24
```


<a name="step2-derivation"></a>
# Step2 -- derivation of `L1FastJet` corrections

First do:

```
./RunPrepareStep2Submission 1 > SubmitStep2.sh
```

**Input**: The `$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/MatchedFiles` file \
**Output**: Rewrites the `SubmitStep2.sh` script.

Open the `SubmitStep2.sh` script to see how it has changed. It should list the paths with the locations of the JRA_\*.root files. 

In line 3 you should write the full path of where the `Setup_FileLocation.sh` is located, e.g. `source /afs/cern.ch/work/<u>/<username>/public/MCtruthJEC/CMSSW_14_2_2/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Setup_FileLocation.sh` 

Then, replace

```
echo "+JobFlavour = microcentury" >> $SubmissionFile
```

with:

```
echo "+JobFlavour = testmatch" >> $SubmissionFile
echo "+request_cpus=3">>$SubmissionFile
echo "requirements = (TARGET.OpSysAndVer =?= \"AlmaLinux9\")" >> $SubmissionFile
```

The lines above will help the HTCondor jobs to run faster.

The `SubmitStep2.sh` script uses the `Step2PUMatching.sh` one so open it and modify it appropriately. There, you need to specify:

1) `-ApplyJEC false` -> Do not apply any `L1FastJet` JECs for now (we haven't derived them yet!)
2) `-npvRhoNpuBinWidth 20` -> Bin width of the mu bins (relevant for the pileup offset plots)
3) `-NBinsNpvRhoNpu 6` -> Number of mu bins (relevant for the pileup offset plots)
4) `-useweight false` -> We do not apply pT reweighting
5) `-nrefmax 3` -> Consider only the 3 leading gen jets
6) `-doDZcut false` -> We do not usually apply this cut for the pileup offset (but can turn this on if needed)
7) `-doVetoMap true \
   -JetVetoMapRootName JetVetoMap_20234CDEFGHI.root \
   -JetVetoMapHistName jetvetomap_all` -> Apply jet veto map and specify root file name and `TH2D` hist name

In turn, the `Step2PUMatching.sh` code uses the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_match_x.cc` script. This does not need any modifications but here are some relevant snippets: 

1) in line 1386 the offset is calculated
2) in lines 1436-1438 the `TProfile3D` objects are filled for `<offset/Aj>, <rho>, <pTrec>`
3) many more histograms are filled further below (the relevant ones for plotting the pileup offset are the `p_offresVsrefpt_XX_tnpuYY_YY`)


Once you make sure everything is in place, submit the HTCondor jobs:

```
./SubmitStep2.sh
```

**Input:** None, as the script has already been modifed appropriately. \
**Output:** Root files in `Step2Output`

When all jobs are finished properly and all (or most) root files are produced in EOS, proceed with the harvesting step. Modify the `HarvestStep2.sh` script:

1) This scripts hadds the root files in `Step2Output`.
2) If you don't want to derive `L1FastJet` corrections then keep everything else commented out and go immediately to the step where you plot the pileup offset ([here](#step2-plotting))!!!
3) If you want to derive `L1FastJet` corrections, un-comment out the part that uses the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_synchfit_x.cc` script and modify accordingly. 

In the `jet_synchfit_x.cc` script:

1) In lines 425-450 you determine what fit function should be used (`Complex`, `Simple`, `SemiSimple`): default is `SemiSimple`
2) In lines 640-648 you determine the range of the 2D fit.

Once ready, do:

```
./HarvestStep2.sh
```

**Input:** The root files in `Step2Output`, which are hadded \
**Output if `jet_synchfit_x.cc` is commented out:** None besides the hadded root file in `Step2Output` since you don't want to derive `L1FastJet` corrections \
**Output if `jet_synchfit_x.cc` is used:** The **`L1FastJet` JEC text** file will be created inside `$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L1_output/`


<a name="step2-plotting"></a>
# Pileup offset monitoring and plotting

The hadded root file (`output_ak4puppi.root`) in `Step2Output` contains 2D histograms of the pileup offset. There are a ton of 2D histograms, but the ones we want are the `p_offresVsrefpt_XX_tnpuYY_YY` where `XX = BB, EI, 1EO, 2EO, FF` (the 5 detector regions in abs eta) and `YY` are the mu bins, which were determined in `Step2PUMatching.sh`.

In the pileup offset plots we show the following bins in mu: [0-20], [20-40], [40-60], [60-80], [80-100] and mu approximately zero. To produce the necessary histograms for the latter bin, rerun [step2](#step2-derivation) (specifying a different `Step2Output` to avoid overwriting) but this time do `-npvRhoNpuBinWidth 1 \ -NBinsNpvRhoNpu 6 \` . The first of these bins will be [0-1] which is mu approximately 0.

In order to produce 1D histograms of the average offset divided by gen pT do:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/
jet_synchplot_x -inputDir ./ -algo1 ak4puppi -algo2 ak4puppi -outDir ./ -outputFormat .png .pdf -fixedRange false -tdr true -npvRhoNpuBinWidth 20 -NBinsNpvRhoNpu 6
```

**Input:** The hadded root file in `Step2Output` (`output_ak4puppi.root`) \
**Output:** A root file named `canvases_synchplot_ak4puppi.root` inside `outDir`

You need to use the same `-npvRhoNpuBinWidth 20 -NBinsNpvRhoNpu 6` values as the ones used to create the input `output_ak4puppi.root` file.

The script above uses the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/interface/SynchFittingProcedure.hh` script. In it, in lines 463-465 the average offset is divided by get pT. If you do not want to divide by pT, then comment out these lines and use the lines 459-460 instead (make sure to recompile if you change this).

OK, now you have two `canvases_synchplot_ak4puppi.root` files; one with 6 bins in mu with a bin width of 20, and one with 6 bins with a bin width of 1. Use the following script to stitch them in a single root file that contains the mu bins [~0, 0-20, 20-40, 40-60, ...]: 

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 create_input_histos_for_pu_offset.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V1_PhiIndependent --JEC 0 --DivByPt 1
```

Finally, plot the average offset (divided by pT or not) as a function of pT and eta:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ 
python3 plot_pu_offset_vs_ptgen_eta_mu.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --JEC 0 --DivByPt 1
```

**Input:** The root file created from stitching up the `canvases_synchplot_ak4puppi.root` files \
**Output**: Plots in PDF format with the raw pileup offset


**!!! Please note !!!** \
You have now plotted the raw pileup offset because you have used the `output_ak4puppi.root` file that was produced without any JEC applied. If you've derived `L1FastJet` corrections then you will have to rerun the entire [step2](#step2-derivation) chain, but this time in `Step2PUMatching.sh` instead of:

```
-ApplyJEC false \
```

write:

```
-ApplyJEC true \
-JECpar RunIII2024Summer24_V1_MC_L1FastJet_AK4PUPPI.txt \
```

That way, the new `output_ak4puppi.root` file in `Step2Output` (careful not to overwrite, change this path) will contain histograms with the L1 JECs applied. Repeat all steps to produce the pileup offset plots again.


<a name="L2L3"></a>
# Jet response corrections (`L2Relative`)


Go to the corresponding work area, make a directory with the name of the MC dataset and version of corrections you want to derive (e.g. `RunIII2024Summer24_V1_PhiIndependent/`) and then create an `L2L3_output` directory:

```
cd CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/
cd Files/
mkdir RunIII2024Summer24_V1_PhiIndependent/
cd RunIII2024Summer24_V1_PhiIndependent/
mkdir L2L3_output/ 
```

Copy the jet veto map inside the directory above:

```
cd CMSSW_BASE/src/JetMETAnalysisMCtruth/Histos_JetVetoMaps/
cp JetVetoMaps_2024CDEFGHI.root $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L2L3_output/
```

Copy the histograms for PU reweighting inside the directory above:

```
cd CMSSW_BASE/src/JetMETAnalysisMCtruth/Histos_PU/
cp MyDataPUHisto_2024CDEFGHI_120Bins_69200.root $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L2L3_output/
cp MyMCPUHisto_RunIII2024Summer24_PremixedPU.root $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L2L3_output/
```

Modify the `Setup_FileLocation.sh` script with the paths of the input JRA ntuples, and the output root files in EOS:

1) In `WithPUFiles` you should have the path to the `PremixedPU` JRA ntuples (`NoPUFiles` not needed).
2) Modify the `Step3Output` and `Step4Output` paths accordingly: this is where the output root files of these steps will appear.


<a name="step3"></a>
# Step3 -- derivation of `L2Relative` corrections

The `submission` step produces histograms of the jet response and the rec pT in fine bins of gen pT and eta, while the `harvest` step performs the fits and creates the `L2Relative` text file.

Modify the `Step3ApplyL1.sh` script accordingly. There is the following snippet inside this code that applies the `L1FastJet` corrections before producing the histograms:

```
jet_apply_jec_x \
   -input Input.root \
   -output JRA_jecl1.root \
   -jecpath ./ \
   -era RunIII2024Summer24_V1_MC \
   -levels 1 \
   -algs ak4puppi \
   -L1FastJet true \
   -saveitree false
```
In the case of PUPPI jets where we do not produce `L1FastJet` corrections, this is commented out and no JECs are applied.

The `Step3ApplyL1.sh` code calls the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_response_analyzer_x.cc` script and configures it. Below is an explanation of each option:

1) `-MCPUReWeighting MyMCPUHisto_RunIII2024Summer24_PremixedPU.root \
   -MCPUHistoName pileup \
   -DataPUReWeighting MyDataPUHisto_2024CDEFGHI_120Bins_69200.root \
   -DataPUHistoName pileup \` -> PU reweighting root files and histograms
2) `-useweight false` -> We do not apply pT reweighting
3) `-nrefmax 3` -> Consider only the 3 leading gen jets
4) `-drmax 0.2` -> Consider only the matched rec-gen jets, namely those with DR < 0.2
5) `-nbinsrelrsp 60 \ -relrspmin 0.0 \
   -relrspmax 3.0 \` -> Jet response is binned in 60 bins from 0 to 3  
6) `-jtptmin 0` -> No raw jet pT cut 
7) `-doDZcut true` -> Apply the DZ cut 
8) `-doNMcut true` -> Apply the neutral multiplicity > 1 cut to PUPPI jets with abs eta > 3 
9) `-doVetoMap true \
   -JetVetoMapRootName JetVetoMaps_2024CDEFGHI.root \
   -JetVetoMapHistName jetvetomap_all` -> Apply the jet veto map and specify the root file name and `TH2D` hist name. The full veto map (with BPix and FPix areas) should be used


The main loop with all the important stuff is in lines 1468 onwards in `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_response_analyzer_x.cc`.

When ready, submit HTCondor jobs:

```
./SubmitStep3.sh
```

**Input:** The JRA ntuples of the `PremixedPU` MC dataset \
**Output:** Root files in `Step3Output`

When all jobs are finished, edit the `-outputDir` and `-era` of the `HarvestStep3.sh` code, which calls the code `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/src/L2Creator.cc`. 

```
./HarvestStep3.sh
```

**Input:** The root files in `Step3Output` which are hadded \
**Output:** The **`L2Relative` JEC text** file and a root file named `l2.root` will be created inside the output directory (`CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L2L3_output/`)


You will have to run this command many times because it performs 82 fits (for each eta bin, `ieta`) and many of them will **not** converge. Open the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/src/L2Creator.cc` script. In lines 415-542 I have a few sets of alternative initial parameters. Do the following:

1) Run `./HarvestStep3.sh` and based on the printouts of the fit probabilities determine which `ieta` failed (those with fit prob < 0.05).
2) Put all those `ieta` that failed in the first alternative set of initial parameters (line 415), recompile (`scram b -j 8`) and run `./HarvestStep3.sh` again.
3) Some of those `ieta` will fail again, so put those in the second set of parameters (line 437), recompile and re-run `./HarvestStep3.sh`
4) Repeat until no fit fails.
5) In lines 336-343 you can change the starting point of each fit (i.e. each `ieta`).
6) In lines 300-303 we have used a minimum uncertainty of 0.1% for the points of the spectrum that we fit. You can also tweak that for particular `ieta` fits that keep failing.


Once you make sure that all fits have a fair fit probability (usually above 5%), check the `L2Relative` file which contains the post-fit parameters. There should not be any insanely large values like `e+150` or `inf` values.

Then make sure that there is no asymptotic discontinuity in the fits. Use the script below that also plots these 82 fits:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_inverse_median_response_vs_ptrec.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V1_PhiIndependent
```

**Input:** The `CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Files/RunIII2024Summer24_V1_PhiIndependent/L2L3_output/l2.root` file \
**Output:** Plots in PDF format of each fit. Also, if a warning message about asymptotic discontinuity is printed, then fix that fit because it is problematic.

You can also plot these fits for multiple eras, with the following script: 

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_inverse_median_response_vs_ptrec_multiple_sets.py --jetCone 4 --jetAlgo puppi
```
**Input:** The `l2.root` file for various MC datasets (defined in line 116) \
**Output:** Plots in PDF format for each eta bin with the fits superimposed for all these MC datasets


<a name="step4"></a>
# Step4 -- plotting of jet response 

Edit the `Step4Closure.sh` script that uses the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_correction_analyzer_x.cc` script. These produce 2D plots of jet response vs pT and eta. There is the option to either apply JEC or not so that both the raw and corrected jet response can be examined. 

The configuration options of the `jet_correction_analyzer_x.cc` script are similar to the ones of the `jet_response_analyzer_x.cc` script in [step3](#step3). The main loop with all the important stuff is in lines 590 onwards.

Particularly for the application of JEC:

1) If you do not want any JECs applied then only have `-era RunIII2024Summer24_V1_MC \` without the `-levels` option
2) If you want to apply the `L2Relative` text file then have `-era RunIII2024Summer24_V1_MC \ -levels 2 \`
3) If you want to apply both the `L1FastJet` and `L2Relative` text files then have `-era RunIII2024Summer24_V1_MC \ -levels 1 2 \`

Once ready, submit the HTCondor jobs:

```
./SubmitStep4.sh
```

**Input:** The JRA ntuples of the `PremixedPU` MC dataset \
**Output:** Root files in `Step4Output`

Once all jobs are finished, edit the `-outputDir` in the `HarvestStep4.sh` script which calls the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/src/ClosureMaker.cc` code, and run:

```
./HarvestStep4.sh
```

**Input:** The root files in `Step4Output` which are hadded \
**Output:** The `ClosureVsRefPt.root` root file inside `-outputDir`

The `ClosureVsRefPt.root` file contains histograms of the jet response vs pt and eta. 

In order to plot the median response as a function of gen pT for the 5 different detector regions:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_median_response_vs_ptgen_eta_overview.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V1_PhiIndependent --JEC 1 --ymin 0.92 --ymax 1.08
```

**Input:** The `ClosureVsRefPt.root` file which is renamed to the format of `(L1)L2L3ClosureVsPt_AK4PUPPI_RunIII2024Summer24.root` if JECs are applied (`--JEC 1`) or `RawResponseVsPt_AK4PUPPI_RunIII2024Summer24.root` if JECs are not applied (`--JEC 0`). \
**Output:** A plot in PDF format of the median jet response vs gen pT for various abs eta bins


The median jet response can also be plotted for each abs eta bin and compared between two different sets of samples, alongside their ratio:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_median_response_vs_ptgen_with_ratio.py --jetCone 4 --jetAlgo puppi --MC1 Winter24 --MC2 Summer24 --JEC 0
```

**Input:** The `ClosureVsRefPt.root` files for the two MC campaigns, renamed as before \
**Output:** Five plots in PDF format for each abs eta bin with the median jet response vs gen pT and the ratio for the two MCs


The response distributions, from which the median is extracted, can also be plotted using the script below:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_response_distributions.py --jetCone 4 --jetAlgo puppi --JEC 0 --JetPtMin 30 --JetPtMax 35
```

**Input:** The hadded root file in `Step4Output` \
**Output:** Five plots in PDF format for each abs eta bin with the response distribution for various MCs (defined in line 88) and 30 < gen pT < 35 GeV


<a name="bpix-fpix"></a>
# Dedicated JECs for the BPix and FPix regions

The steps for deriving `L2Relative` corrections explained previously refer to the default JECs that are derived with the BPix and FPix regions excluded (i.e. included in the veto map).

After deriving these `V1_PhiIndependent` corrections, you need to derive dedicated ones for the BPix and FPix regions (if these issues are simulated in the MC dataset).

Rerun [step3](#step3) but this time do not apply any veto map (`-doVetoMap false` in `Step3ApplyL1.sh`) and at the same time only consider jets inside the BPix region, by inserting the following inside the jet loop (right after line 1516):

```
//BPix area      
if( !(JRAEvt->jteta->at(iref)>=-1.479 && JRAEvt->jteta->at(iref)<=0.087 && JRAEvt->jtphi->at(iref)>=-1.2217305 && JRAEvt->jtphi->at(iref)<=-0.78539816) ) continue;	    
```

Then, proceed with running `./HarvestStep3.sh` in order to create a dedicated `L2Relative` JEC txt file for the BPix region (eta bins between -1.479 and 0.087).

Then, do exactly the same for the FPix region, where this time use:

```
//FPix area
if( !( (JRAEvt->jteta->at(iref)>=-2.043 && JRAEvt->jteta->at(iref)<=-1.566 && JRAEvt->jtphi->at(iref)>=2.443461 && JRAEvt->jtphi->at(iref)<=2.7925268) || (JRAEvt->jteta->at(iref)>=-2.043 && JRAEvt->jteta->at(iref)<=-1.83 && JRAEvt->jtphi->at(iref)>=2.7925268 && JRAEvt->jtphi->at(iref)<=3.0543262) ) ) continue;	      
```

and derive a dedicated `L2Relative` JEC txt file for the FPix region (eta bins between -2.043 and -1.566).


Lastly, you will have to merge the default `L2Relative` text file with the two dedicated ones for BPix and FPix. Currently, there is no script or automated way to do this, but it is rather simple, as explained below:

1) Modify the first line of the text file:

``` 
Replace 

{1 JetEta 1 JetPt max(0.0001,((x<[10])*([9]))+((x>=[10])*([0]+([1]/(pow(log10(x),2)+[2]))+([3]*exp(-([4]*((log10(x)-[5])*(log10(x)-[5])))))+([6]*exp(-([7]*((log10(x)-[8])*(log10(x)-[8])))))))) Correction L2Relative}

with

{2 JetEta JetPhi 1 JetPt max(0.0001,((x<[10])*([9]))+((x>=[10])*([0]+([1]/(pow(log10(x),2)+[2]))+([3]*exp(-([4]*((log10(x)-[5])*(log10(x)-[5])))))+([6]*exp(-([7]*((log10(x)-[8])*(log10(x)-[8])))))))) Correction L2Relative}
```

2) Modify the eta bins that are not part of the BPix or FPix region, such that they are explicitly valid for phi between -3.1416 and +3.1416. Example below:

```
Replace

   0.261   0.348    13    3.718792   5300.1131     0.5479962617      13.77220075      12.01276268   -0.03938225575      3.566270518      1.078901922    -0.4527825851     0.2572148366     0.8225844628      1.134272805                8

with

   0.261   0.348       -3.1416         3.1416      13    3.718792   5300.1131     0.5479962617      13.77220075      12.01276268   -0.03938225575      3.566270518      1.078901922    -0.4527825851     0.2572148366     0.8225844628      1.134272805                8

```

3) Modify the eta bins that are part of the BPix or FPix region by providing the JEC for all 3 phi bins for each particular eta bin. Example below:

```
If the default JEC txt file (excluding BPix) has:
  -1.131  -1.044    13   3.6936659   3438.1598     0.6239476945       9.89373998      10.16377066    -0.1389986052       2.50916051     0.7450651239     -0.275431022     0.4908949689      1.185593303      1.129665482                8
and the dedicated JEC txt file (inside BPix) has:
  -1.131  -1.044    13   4.5073879   2999.6713     0.6186154427      11.49065069      14.35726889   -0.05773817491      2.463488477      2.060894849    -0.1300350931      4.025267462      1.078775466      1.258965243                8  

then in the merged, phi-dependent JEC txt file write:

  -1.131  -1.044       -3.1416     -1.2217305      13   3.6936659   3438.1598     0.6239476945       9.89373998      10.16377066    -0.1389986052       2.50916051     0.7450651239     -0.275431022     0.4908949689      1.185593303      1.129665482                8
  -1.131  -1.044    -1.2217305    -0.78539816      13   4.5073879   2999.6713     0.6186154427      11.49065069      14.35726889   -0.05773817491      2.463488477      2.060894849    -0.1300350931      4.025267462      1.078775466      1.258965243                8
  -1.131  -1.044   -0.78539816         3.1416      13   3.6936659   3438.1598     0.6239476945       9.89373998      10.16377066    -0.1389986052       2.50916051     0.7450651239     -0.275431022     0.4908949689      1.185593303      1.129665482                8
```

Now that you have a new, phi-dependent `L2Relative` JEC txt file you can run [step4](#step4), as usual, providing this txt file now.


Additionally, in [step4](#step4), you can isolate the BPix and FPix regions by adding the previous snippets to the `jet_correction_analyzer_x.cc` file:

```
//BPix area      
if( !(JRAEvt->jteta->at(iref)>=-1.479 && JRAEvt->jteta->at(iref)<=0.087 && JRAEvt->jtphi->at(iref)>=-1.2217305 && JRAEvt->jtphi->at(iref)<=-0.78539816) ) continue;	    

//FPix area
if( !( (JRAEvt->jteta->at(iref)>=-2.043 && JRAEvt->jteta->at(iref)<=-1.566 && JRAEvt->jtphi->at(iref)>=2.443461 && JRAEvt->jtphi->at(iref)<=2.7925268) || (JRAEvt->jteta->at(iref)>=-2.043 && JRAEvt->jteta->at(iref)<=-1.83 && JRAEvt->jtphi->at(iref)>=2.7925268 && JRAEvt->jtphi->at(iref)<=3.0543262) ) ) continue;	      
```

and apply either the `V1_PhiIndependent` or the `V1_PhiDependent` JEC txt file to see the jet response in those regions.

A relevant script that plots the fits (inverse of median jet response vs pT) for the phi bins inside and outside the BPix or FPix regions can be used:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_inverse_median_response_vs_ptrec_bpix_fpix.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V1 --issue BPix
```

**Input:** The `l2.root` file for the default and the dedicated JECs \
**Output:** Plots in PDF format with the fits to the inverse of median response for the relevant eta bins. Superimposed in each plot is the fit (correction factor) inside and outside the BPix or FPix region


Furthermore, you can plot the median jet response inside the BPix or FPix areas, using the following script:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_median_response_vs_ptptcl_bpix_fpix.py --jetCone 4 --jetAlgo puppi --MC RunIII2024Summer24 --version V1 --DoBPix 1 --DoFPix 1 --JECvsPhi 1
```

**Input:** The hadded root file in `Step4Output` inside the BPix and/or the FPix region. Option `-JECvsPhi` determines what `Step4Output` to consider; the one derived when applying the `V1_PhiIndependent` or `V1_PhiDependent` JECs \
**Output:** Plot in PDF format with the median jet response vs gen pT for jets inside the BPix and/or FPix region


<a name="corr-factors"></a>
# Correction factors

The two JEC text files `L1FastJet` and `L2Relative` can be used as input to plot the correction factors as a function of eta (and as a function of pT but these are already plotted as fits to the inverse of the median response).

First do:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/
jet_draw_corrections_x -algs ak4puppi -path ./ -outputDir ./ -useL2Cor true -era RunIII2024Summer24_V1_MC
```

**Input:** If `-useL2Cor true` then the `L2Relative` text file. If `-useL1FasCor true` then the `L1FastJet` text file. If `-useL1FasCor true -useL2Cor true` then the `L1FastJet * L2Relative` text files. \
**Output:** The `Corrections_Overview_ak4puppi.root` file inside the `outputDir` folder

Inside the `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_draw_corrections_x.cc` script, in lines 307-331 we specify for what raw jet pT values we want to plot the correction factors vs eta. Currently these are: ptraw = [10, 15, 20, 30, 50, 100, 300, 500, 1000, 3000] GeV. 


In order to plot the correction factors vs eta for these raw pT values use the following script:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_correction_vs_eta.py --jetCone 4 --jetAlgo puppi
```

**Input:** The `Corrections_Overview_ak4puppi.root` files for each MC dataset (defined in line 83), renamed in the format `L2L3Correction_AK4PUPPI_RunIII2024Summer24.root`. \
**Output:** Plots in PDF format of the correction factor vs eta for each raw pT value

You can also plot the correction factors of two MC dataset alongside their ratio, using the following script:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/
python3 plot_correction_vs_eta_with_ratio.py --jetCone 4 --jetAlgo puppi --MC1 Winter24 --MC2 RunIII2024Summer24
```

**Input:** The `Corrections_Overview_ak4puppi.root` files for the two MC datasets, renamed in the format `L2L3Correction_AK4PUPPI_RunIII2024Summer24.root`. \
**Output:** Plots in PDF format of the correction factor vs eta for each raw pT value


