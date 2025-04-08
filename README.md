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
- [HOW TO: derive MC truth JECs](#JEC)
	- [Brief overview](#brief_overview)
	- [General tips for HTCondor](#condor) 
	- [Pileup offset corrections (L1FastJet)](#L1)
	- [Jet response corrections (L2Relative)](#L2L3)
- [Instructions on how to plot the correction factors](#Corr-Factors)

<!-- /MarkdownTOC -->

<a name="introduction"></a>
## Introduction

The code contained in this package is used for creating and analyzing the L1FastJet and L2Relative MC truth jet energy corrections. The code is used by the Jet Energy Resolution and Corrections (JERC) subgroup. This is a dedicated workflow for the MC-truth jet energy corrections used by the Athens group. The main code is located at https://github.com/cms-jet/JetMETAnalysis .

<a name="documentation"></a>
## Documentation

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
## Log book of previous changes

In some cases, when moving to a newer CMSSW version, compilation errors when doing `scram b -j 8` arise. In this section the necessary changes to the framework when migrating from a CMSSW version to a newer one will be presented, for book keeping purposes. None of these need to be repeated by the user. The current version of the framework works for the most recent CMSSW_14_2_X version.

<a name="changes_106Xto126X"></a>
## Changes from CMSSW_10_6_X to CMSSW_12_6_X

1) Open the `JetMETAnalysis/JetAnalyzers/BuildFile.xml` code and in line 20 replace `SimDataFormats/JetMatching` with `DataFormats/JetMatching`
2) Open the codes `JetMETAnalysis/JetAnalyzers/interface/JetResponseAnalyzer.hh` and `JetMETAnalysis/JetAnalyzers/interface/JetResponseAnalyzerProducer.hh` and replace `SimDataFormats/JetMatching` with `DataFormats/JetMatching` in lines 45 and 43 respectively.
3) `cp /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/include/c++/9.3.0/bits/stl_tree.h JetMETAnalysis/JetUtilities/interface/`
4) Open the `JetMETAnalysis/JetUtilities/interface/stl_tree.h` code and comment out lines 778-781 which are responsible for giving the error `static assertion failed: comparison object must be invocable as const`
5) Open the `JetMETAnalysis/JetAnalyzers/bin/jet_match_x.cc` and `JetMETAnalysis/JetAnalyzers/bin/jet_synchtest_x.cc` codes and add *before any other include* the following: `#include "JetMETAnalysis/JetUtilities/interface/stl_tree.h"`
6) Then, open the `../tmp/slc7_amd64_gcc900/src/JetMETAnalysis/JetUtilities/src/JetMETAnalysisJetUtilities/a/JetMETAnalysisJetUtilities_xr.cc` code and do the same -> add *before any other include* the following: `#include "JetMETAnalysis/JetUtilities/interface/stl_tree.h"`
7) Move the `SynchFittingProcedure.hh` code from `JetMETAnalysis/JetUtilities/src/` to the `JetMETAnalysis/JetUtilities/interface/` folder and then open the `JetMETAnalysis/JetAnalyzers/bin/jet_synchplot_x.cc` code and in line 35 replace `src/` with `inteface/` (to provide the new correct path).
8) Modify python files to work with python3: 4 spaces instead of a tab, `algsizetype.items()` instead of `algsizetype.iteritems()`, add parentheses in print commands, `list(genJetsDict.keys()).index(alg_size_type)` instead of `genJetsDict.keys().index(alg_size_type)` 

<a name="changes_126Xto130X"></a>
## Changes from CMSSW_12_6_X to CMSSW_13_0_X and beyond (up to at least CMSSW_14_2_X)

1) Change to `edm::one::EDAnalyzer<>` and `edm::one::EDProducer<>` from `edm::EDAnalyzer` and `edm::EDProducer` respectively. Modify the includes as well.

2) Copy the file `/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/gcc/11.2.1-f9b9dfdd886f71cd63f5538223d8f161/include/c++/11.2.1/bits/stl_tree.h` to the `JetMETAnalysisMCtruth/JetUtilities/interface` directory and comment out lines 768-771

3) In `JetUtilities/src/JetInfo.cc` line 361 change `assert(words>0)` to `assert(words != nullptr)`

4) From CMSSW_12_6_X copy the codes `JetMETCorrections/Objects/interface/JetCorrector.h` and `cmssw/JetMETCorrections/Objects/src/JetCorrector.cc` and paste them to `JetUtilities/interface/` and `JetUtilities/src/` respectively. In `JetCorrector.cc` comment out lines 48-53, and in `JetAnalyzers/src/JetResponseAnalyzer.cc`, `JetAnalyzers/src/JetResponseAnalyzerProducer.cc` write `jetCorrector_ =  0`

5) From CMSSW_12_6_X copy the codes `JetMETCorrections/Configuration/python/JetCorrectionServicesAllAlgos_cff.py` and `JetMETCorrections/Configuration/python/JetCorrectionServices_cff.py` and paste them inside `JetAnalyzers/python/`


<a name="setup-cmssw"></a>
## HOW TO: Setup the framework

Setup the code in the AFS area and not the EOS user area, because HTCondor is used, that is not compatible with EOS.

```
mkdir JEC/ 
cd JEC/ 
cmsrel CMSSW_14_2_2 
cd CMSSW_14_2_2/src 
cmsenv 
git clone -b April2025 https://github.com/izisopou/JetMETAnalysisMCtruth.git 
```

Then compile:

```
scram b -j 8 
```

In the first compilation you will get a compilation error about `is_invocable_v<const _Compare&, const _Key&, const _Key&>`. 

Open the file `CMSSW_14_2_2/tmp/el9_amd64_gcc12/src/JetMETAnalysisMCtruth/JetUtilities/src/JetMETAnalysisMCtruthJetUtilities/lcgdict` and before any other include (among L6 and L7) add the following line:

```
#include "JetMETAnalysisMCtruth/JetUtilities/interface/stl_tree.h"
```

Re-compile and there should be no errors. The above file is autogenerated, so if this error comes back again in any given time, repeat the step above.

**Very important note:** Every time there you change any `.cc` or `.hh` or `.h` code inside `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers` or `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities` you should then re-compile, doing `scram b -j 8` for the changes to take effect.

<a name="ntuples-miniaod"></a>
## HOW TO: Produce ntuples from MINIAOD

In this section instructions are provided on how to produce a JRA ntuple which contains a tree with event and matched reco-gen jet variables, needed for the JEC derivation.

<a name="important-codes"></a>
## Important codes for producing ntuples

1) `JetMETAnalysisMCtruth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py` \
L25-26: Specify the jet collections to be saved in the JRA trees \
L51: Insert global tag of sample to be processed \
L69: Specify how many events to be processed, -1 stands for all events in the sample \
L79: Specify which MiniAOD root file to be processed for a local test \
This code calls the addAlgorithm.py one

2) `JetMETAnalysisMCtruth/JetAnalyzers/python/addAlgorithm.py` \
L382: Specify the raw jet pT cut with which the reco-gen matching will be performed and jets will be saved in the JRA trees (default = 0 GeV) \
L391-407: While reconstructing PUPPI jets the code uses the following commands to take the stored PUPPI weights in the dataset

```
process.puppi.useExistingWeights = True
process.puppiNoLep.useExistingWeights = True
```

3) `JetMETAnalysisMCtruth/JetAnalyzers/python/customizePuppiTune_cff_V15.py` \
This is a configuration file for applying the V15 PUPPI tune recipe \
If one did not want to use the default PUPPI weights in the dataset but wanted to re-calculate on the fly the V15 weights, they should load and call in `addAlgorithm.py` this file. NOT needed anymore.

4) `JetMETAnalysisMCtruth/JetAnalyzers/python/Defaults_cff.py` \
L33: Reco-gen jet pairings are saved in the ntuple, along with their deltaR. Change the maximum deltaR value that is saved (default = 999, i.e. write everything). The `deltaR < 0.2 (0.4)` criterion will be used later in another step.

5) `JetMETAnalysisMCtruth/JetAnalyzers/src/JetResponseAnalyzer.cc`, `JetMETAnalysisMCtruth/JetAnalyzers/interface/JetResponseAnalyzer.hh`, `JetMETAnalysisMCtruth/JetUtilities/src/JRAEvent.cc`, `JetMETAnalysisMCtruth/JetUtilities/interface/JRAEvent.h` \
These codes produce the trees. They do not need any change at the moment.


<a name="produce-ntuples"></a>
## How to produce JRA ntuples

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/test/
```

Before submitting jobs to crab run a **local test** first:

In the code `JetMETAnalysisMCtruth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py` specify a MiniAOD root file and a small number of events.

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

L4-5: Submitting jobs will create a folder `workArea/requestName/` inside `$CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/test/`
L14: Specify MC sample from DAS to process
L17: Specify how many CRAB jobs to have per MiniAOD root file (default = 1 for quicker production)
L20: Specify name of directory that will be created in the output directory
L21: Specify output directory where the JRA ntuples will be saved. Note that `/eos/cms/` should not be written before `/store/group/phys_jetmet/`

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

**Please note**: All Run-3 MC ntuples produced by Ilias (me) are located in: 

```
/eos/cms/store/group/phys_jetmet/ilias/Run3MCtruthSamples/NoRawPtCut/
```

<a name="PU-reweight"></a>
### HOW TO: Create histograms for PU reweighting

The only event weights applied in this analysis are the ones related to the PU reweighting. This is only relevant for the `L2Relative` derivation when the `PremixedPU` MC is used. We need to produce two root files with the mu (true number of pileup interactions per crossing) distribution; one for data and one for MC. Note that they should have the same binning (we usually use 120 bins from 0 to 120).

<a name="PU-reweight-data"></a>
### Histogram for data

To produce the root file for data:
```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/Histos_PU/ 
cmsenv 
pileupCalc.py -i Cert_Collisions2024_erasBCDEFGHI.json --inputLumiJSON pileup_latest_2024.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 120 --numPileupBins 120  MyDataPUHisto_2024CDEFGHI_120Bins_69200.root 
```

where `Cert_Collisions2024_erasBCDEFGHI.json` is the Golden JSON file for the corresponding era you want to process and `pileup_latest_2024.txt` the pileup JSON for the corresponding year (ask around if you cannot find where they have it). The minimum bias cross section of 69.2 mb has been used so far but studies have shown that for 13.6 TeV data a more representative value is 75.3 mb. Please ask around for the recommendation before producing this and proceeding to the next steps.

The output file is `MyDataPUHisto_2024CDEFGHI_120Bins_69200.root` that contains a histogram of the mu distribution named `pileup`.

<a name="PU-reweight-mc"></a>
### Histogram for MC

To produce the corresponding root file for MC:

```
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ 
python3 create_mu_distribution.py --era Run3Winter25
```

The output file is `MyMCPUHisto_Run3Winter25_PremixedPU.root` inside `Histos_PU/` that contains a histogram of the mu distribution named `pileup`.



<a name="JEC"></a>
## HOW TO: derive MC truth JECs

<a name="brief_overview"></a>
## Brief overview

The derivation of MC truth JECs consists of four `Steps` which will be explained in detail in the next sections. Here we present a brief overview of what they are:

`Step1`: Matches events between the `FlatPU` and `EpsilonPU` datasets and produces lists with the matched events.

`Step2`: Matches jets between these events, calculates the offset and produces the `L1FastJet` text file by fitting the `<offset>/Aj` as a function of `<pT>` and `<rho>`. Also produces the necessary plots of the average pileup offset.

`Step3`: Applies the `L1FastJet` text file (if one was derived) and produces histograms of the response distributions vs `pT` and `eta`. Then fits the inverse of the median response as a function of `pT` in fine bins of `eta` and produces the `L2Relative` text file.

`Step4`: Produces 2D histograms of the response vs `pT` and `eta` so as to examine the median response before and after the application of corrections (closure).


<a name="condor"></a>
## General tips for HTCondor

1) Throughout all four steps of the MC truth JECs you will be submitting jobs to HTCondor. You can find more information for HTCondor here: https://batchdocs.web.cern.ch/index.html
2) Once you submit jobs to HTCondor you can check their status by doing
```
condor_q
```
3) This command shows the status of all jobs of all users in the particular `bigbird` scheduler. You can change `bigbird` and move to a less crowded one (eg to `bigbird26`) with the following command:
```
setenv _condor_SCHEDD_HOST bigbird26.cern.ch
```

4) When a job is finished it will disappear from `condor_q`, and a corresponding root file should appear in eos. Additionally, in the directory `$CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/Log/` 3 files will appear for each job: `err`, `log`, `out`. Check the `err` and `out` ones to see if there was an error in your codes that made the jobs crash. If you have a bug somewhere then the output root files in eos will not be created or they will be created empty, so you can also check them by going to the eos directory and doing `ls -lh` to see the size of the files and if they have closed properly. If the code does not have any bugs then these files should be a few MB each.

5) When running some steps you will get the following error:
```
Error in <TTree::SetBranchAddress>: unknown branch -> refpdgid_algorithmicDef
Error in <TTree::SetBranchAddress>: unknown branch -> refpdgid_physicsDef
```
You can safely ignore it as we are not doing flavor corrections and do not care that our trees do not have these related branches.

6) If there are no bugs and the root files have been created correctly then it is usual (especially in `Step2`) that condor did not run all jobs (due to technical issues related to condor, wall time etc). Therefore you should always check how many output root files were created in eos by doing `ls | wc -l`: they should be the same number as the jobs you submitted. If they are fewer then you can resubmit the jobs (`./SubmitStep*.sh` as you did in the first time) until all root files are processed. 


<a name="L1"></a>
### Pileup offset corrections (L1FastJet)

Based on which collection you want to process go the respective directory: \
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/ \
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK8CHS/ \
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4PUPPI/ \
cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK8PUPPI/

Only in the first time do: \
	g++ ListRunLumi.cpp -o RunListRunLumi \
		\`root-config --cflags --libs\`

Copy the MyMCPUHisto.root and MyDataPUHisto.root to $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Files/

Make sure that in the script Setup_CMSSW.sh the correct path to the condor_AK4CHS/ folder is written.

Determine the input MC samples and output files in eos: \
Open the Setup_FileLocation.sh code and write the correct paths to the NoPUFiles (NoPU or EpsilonPU MC) and WithPUFiles (FlatPU MC). Moreover, write the output directories in eos where the output root files in the 4 steps of the MC-truth JECs will appear. 

**Step1**

In the first step the events between the NoPU/EpsilonPU and the FlatPU sample are matched one by one: 

./SubmitStep1.sh

This will submit jobs to condor. Once they are done then some text files will appear in the Step1Output in eos, where all the events that are matched are written.

./HarvestStep1.sh

This will take as input the txt files in the Step1Output from eos and will create a file named "MatchedFiles" in the directory $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Files/ . In that file all the events that are matched between the NoPU/EpsilonPU and the FlatPU sample will be listed.

**Step2**

In this step, the jets from the matched events will be also matched and the offset will be calculated: offset = jetpT(FlatPU) - jetpT(NoPU/EpsilonPU).\
First do:

./RunPrepareStep2Submission 1 > SubmitStep2.sh

This takes as input the $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Files/MatchedFiles file and rewrites the SubmitStep2.sh code. Open the SubmitStep2.sh code to see how it has changed. It should list the directories for the MC samples where the JRA_\*.root are located. In L3 you should write the full path of where the Setup_FileLocation.sh is located. Then, replace L11 with:

echo "+JobFlavour = testmatch" >> $SubmissionFile

and immediately below add the line:

echo "+request_cpus=3">>$SubmissionFile

The above lines will help the jobs to run quicker.

The SubmitStep2.sh code calls the Step2PUMatching.sh one so open it and modify it appropriately. In turn, the Step2PUMatching.sh code calls the $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_match_x.cc. In L40 of the Step2PUMatching.sh make sure it is false (we do not apply any corrections, we want to derive them).

Once you have modified the above codes, submit the jobs:

./SubmitStep2.sh

Once all jobs are finished and all root files are created in the Step2Output location, open the HarvestStep2.sh code, which in turn calls the $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/bin/jet_synchfit_x.cc one. In this code, in L425-443 you determine what fit function should be used (L1Complex, L1Simple, L1SemiSimple) so comment out 2 of them and leave the one to be used. In L640-648 you also determine the range of the 2D fit. In the HarvestStep2.sh code in L14 you define if you want to use ak4 or ak8 in the jet_synchfit_x.cc code.

./HarvestStep2.sh

This code does 2 things. First it hadds the Step2Output files in eos and then it will create the **Winter22Run3_L1FastJet_AK4PFchs.txt** file in the directory $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Files/ (or the directory you have specified in L9 of the HarvestStep2.sh code), along with some plots concerning the 2D fits.

This hadded root file contains information for the offset (before you apply any correction to the MC). To plot and make useful histograms of the offset from this root file do:

cd $CMSSW_BASE/src/ \
cmsenv \
jet_synchplot_x -inputDir ./ -algo1 ak4pfchs -algo2 ak4pfchs -outDir ./ -outputFormat .png .pdf -fixedRange false -tdr true -npvRhoNpuBinWidth 10 -NBinsNpvRhoNpu 5

where the -inputDir will be the directory where the hadded output_ak4pfchs.root file is located. In the -outDir many .png and .pdf files will be created, along with the canvases_synchplot_ak4pfchs.root file. The above code calls the $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/src/SynchFittingProcedure.hh. In it, in L430-529 you determine how the offset will be calculated (mean, median or mode).

In order to plot the offset over pT as a function of pT and eta:

cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ \
python PlotL1OffsetVsPt.py \

which takes as input the canvases_synchplot_ak4pfchs.root file.

You are basically done with the L1 corrections, since you have derived the L1 JEC text file. However, you should check the quality of these L1 corrections and if they actually remove the pileup as intended. You have already plotted the raw offset, and you need to do that again, applying now this text file you have produced. For that, you need to repeat the Step2 procedure but now in the Step2PUMatching.sh code in L40 make sure it is true and immediately below add the line -JECpar Winter22Run3_L1FastJet_AK4PFchs.txt. Then sumbit the jobs again with ./SubmitStep2.sh but make sure that *the output root files are in a different location as before so as to not overwrite anything!* When the jobs are done you should **not** run the HarvestStep2.sh code because you do not want to derive any corrections now. You only need to hadd the root files in eos and now use this new hadded root file as input in order to plot the offset again. The offset now should be ~0 since you have applied the Winter22Run3_L1FastJet_AK4PFchs.txt file in the PU sample.

When you plot the offset, you can use the mean, median or mode (gaussian fits) for the offset distribution (SynchFittingProcedure.hh). To check one-by-one the offset distributions from which the mean, median or mode is calculated:

cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ \
root -l \
[0] .x Plot_GausFit_Offset.C


<a name="L2L3"></a>
### Jet response corrections (L2Relative)

Edit the $CMSSW_BASE/src/condor/Setup_FileLocation.sh code with the input WithPUFiles which should be the PremixedPU MC sample. The NoPUFiles are not used for the L2L3 corrections.

**Step3**

In this step the L1 correction txt file is applied to the PU MC and the response histos in bins of eta and pT are created. The SubmitStep3.sh code calls the Step3ApplyL1.sh code which in turn calls the jet_response_analyzer_x.cc code. 

For PUPPI jets we do not derive L1 corrections, so we have commented out L19-28 in the Step3ApplyL1.sh code so that the step where the L1 corrections are applied to the MC is skipped.

./SubmitStep3.sh

When all jobs are done edit the HarvestStep3.sh code, which calls the code $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/src/L2Creator.cc. When standard+Gaussian options is specified in L20 of HarvestStep3.sh then the inverse of the median response will be fitted with this function (L1076 of L2Creator.cc) for all 82 eta bins. In L1141-1177 the initial parameters for all the fits are specified. Since in some of the eta bins the fits fail to converge, you can change the set of the initial parameters for specific eta bins in L402-490.

./HarvestStep3.sh

This will hadd the output root file of Step3Output and then do the fits in order to derive the L2L3 corrections, thus creating the **Winter22Run3_L2Relative_AK4PFchs.txt** file in the directory $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK4CHS/Files/, along with the file l2.root that contains the graphs with all fits. When running this command the fit probability for all fits will be printed so you will have to identify which fits have failed, modify the L2Creator.cc code, and rerun until all fits converge and the final txt file has the best quality. 


The Merged.root file in the Step3Output directory contaings a lot of histograms with the response distribution (after having applied the L1 correction and before having applied the L2L3 response corrections) in bins of pTgen and eta. To plot such histograms you can use the Plot_response_before_L2L3JEC.C inside $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/

The l2.root file that is produced contains histograms with the median(response) as a function of pTgen for all eta bins, and the [median(response)]^-1 as a function of pTreco for all eta bins, along with the standard+gaussian fits. To plot such histograms you can use the Plot_ResponseVsRefPt.C and Plot_InverseOfResponseVsJetPt.C inside $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/


**Step4**

In this step both JEC text files (L1 + L2L3) are applied to the MC and the response is calculated and plotted as a function of eta and pt. The SubmitStep4.sh code calls the Step4Closure.sh one which in turn calls the jet_correction_analyzer_x.cc. After you edit these codes:

./SubmitStep4.sh

Once all jobs are done edit the HarvestStep4.sh code which calls the $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetUtilities/src/ClosureMaker.cc code, adn run:

./HarvestStep4.sh

This code produces plots of the corrected response vs pt and eta, along with root files with the histograms saved in them.

In order to plot the above L1L2L3 closure plot vs pt with the stylistics of the JERC group:

cd $CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/ \
cmsenv \
python PlotL1L2L3ClosureVsPt.py

<a name="Corr-Factors"></a>
## Instructions on how to plot the correction factors

The two JEC text files Winter22Run3_L1FastJet_AK4PFchs.txt and Winter22Run3_L2Relative_AK4PFchs.txt can be used as input files in order to plot the overall MC-truth correction factors as a function of eta and pt.

cd $CMSSW_BASE/src/ \
cmsenv \
jet_draw_corrections_x -algs ak4pfchs -path ./ -outputDir ./ -useL1FasCor true -useL2Cor true -era ParallelMCL1

where -path is the directory where the two text files are located. This command will produce some plots in the outputDir along with a root file where the histograms of the corrections vs eta and pt are saved. These kind of root files can be used as input for the following plotting scripts:

$CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/Plot_CorrectionsVsEtaPt.C \
$CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/Plot_CorrectionsVsEtaPt_Comparison_withRatios.C 

Moreover, only the L1 corrections or only the L2L3 corrections can be also plotted:

cd $CMSSW_BASE/src/ \
cmsenv \
jet_draw_corrections_x -algs ak4pfchs -path ./ -outputDir ./ -useL1FasCor true -era ParallelMCL1 \
or \
jet_draw_corrections_x -algs ak4pfchs -path ./ -outputDir ./ -useL2Cor true -era ParallelMCL1

where -path is the directory where the Winter22Run3_L1FastJet_AK4PFchs.txt or the Winter22Run3_L2Relative_AK4PFchs.txt is located. 

Finally, the L1 corrections can be also plotted as a function of rho. For this you need to edit the $CMSSW_BASE/src/JetMETAnalysis/JetAnalyzers/bin/jet_draw_corrections_x.cc code, based on the instructions in the beginning of the code. Then do:

cd $CMSSW_BASE/src/ \
cmsenv \
jet_draw_corrections_x -algs ak4pfchs -path ./ -outputDir ./ -useL1FasCor true -era ParallelMCL1

where -path is the directory where the Winter22Run3_L1FastJet_AK4PFchs.txt is located. Then, with the output root files of the above command you can plot the L1 corrections as a function of rho for a fixed value of pt with the following code:

$CMSSW_BASE/src/JetMETAnalysisMCtruth/scripts/Plot_L1CorrectionsVsRho.C
