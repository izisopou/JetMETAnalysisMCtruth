# JetMETAnalysis-MC-truth

<!-- MarkdownTOC depth=0 -->

- [Overview](#overview)
- [Setup CMSSW release](#setup-cmssw)
- [Instructions on how to run ntuples from MINIAOD](#ntuples-miniaod)
 	- [Important codes for producing ntuples](#important-codes)
 	- [How to produce JRA ntuples](#produce-ntuples)
- [Instructions on how to derive MC-truth JECs](#JEC)
  - [Histograms for PU Reweighting](#PU-reweight)
  - [Pileup Offset Corrections (L1)](#L1)
  - [Relative & Absolute Corrections (L2L3)](#L2L3)
- [Instructions on how to plot the correction factors](#Corr-Factors)

<!-- /MarkdownTOC -->

<a name="overview"></a>
## Overview

The code contained in this package is used for creating and analyzing the L1FastJet and L2Relative MC truth jet energy corrections. The code is used by the Jet Energy Resolution and Corrections (JERC) subgroup. This is a dedicated workflow for the MC-truth jet energy corrections used by the Athens group. The main code is located at https://github.com/cms-jet/JetMETAnalysis .

<a name="setup-cmssw"></a>
## Setup CMSSW release

mkdir MC-truth-JEC/ \
cd MC-truth-JEC/ \
tcsh \
cmsrel CMSSW_12_4_3 \
cd CMSSW_12_4_3/src \
cmsenv \
git-cms-init \
git clone https://github.com/izisopou/JetMETAnalysis-MC-truth.git 

Then compile:

scram b -j 4 

If there are no compilation errors then the code setup was successful. 


<a name="ntuples-miniaod"></a>
## Instructions on how to run ntuples from MINIAOD

In this section instructions are provided on how to produce a JRA ntuple which contains a tree with event and matched reco-gen jet variables, needed for the JEC derivation.

<a name="important-codes"></a>
## Important codes for producing ntuples

1) JetMETAnalysis-MC-truth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py \
L25-26: Specify the jet collection to be saved in the JRA trees \
L51: Insert global tag of sample to be processed \
L69: Specify how many events to be processed, -1 stands for all events in the sample \
L79: Specify which MiniAOD root file to be processed for a local test \
This code calls the addAlgorithm.py one

2) JetMETAnalysis-MC-truth/JetAnalyzers/python/addAlgorithm.py \
L383: Specify the raw jet pT cut with which the reco-gen matching will be performed and jets will be saved in the JRA trees \
L386-397: While reconstructing PUPPI jets the code takes as input the customizePuppiTune_cff_V15.py file

3) JetMETAnalysis-MC-truth/JetAnalyzers/python/customizePuppiTune_cff_V15.py \
This is the configuration file for applying the V15 PUPPI tune recipe \
L12-13: If "useExistingWeights" is set to False then apply the v15 recipe, recalculating PUPPI weights on the fly. If "useExistingWeights" is set to True then use the existing/stored PUPPI weights in MiniAOD and do not apply the recipe

4) JetMETAnalysis-MC-truth/JetAnalyzers/python/Defaults_cff.py \
L33: Change the maximum R with which the reco-gen deltaR matching will be performed

5) JetMETAnalysis-MC-truth/JetAnalyzers/src/JetResponseAnalyzer.cc, JetMETAnalysis-MC-truth/JetAnalyzers/interface/JetResponseAnalyzer.hh, JetMETAnalysis-MC-truth/JetUtilities/src/JRAEvent.cc, JetMETAnalysis-MC-truth/JetUtilities/interface/JRAEvent.h

<a name="produce-ntuples"></a>
## How to produce JRA ntuples

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetAnalyzers/test/

Before submitting jobs to crab run a **local test** first:

In the code JetMETAnalysis-MC-truth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py specify a MiniAOD root file and a small number of events.

cmsenv \
voms-proxy-init -voms cms \
cmsRun run_JRA_cfg_MCtruth.py

This test will produce a file named JRA.root in the directory you are in, containing the small number of events specified. If there are no errors, the JRA.root is produced, and the trees are filled properly, then CRAB jobs can be submitted in order to process the full MC sample.


How to **submit jobs to CRAB**:

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetAnalyzers/test/

In the code JetMETAnalysis-MC-truth/JetAnalyzers/test/run_JRA_cfg_MCtruth.py put as number of events to process -1

In the code JetMETAnalysis-MC-truth/JetAnalyzers/test/custom_crab_JEC.py:

L4-5: Submitting jobs will create a folder workArea/requestName/ inside $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetAnalyzers/test/
L14: Specify MC sample from DAS to process
L17: Specify how many CRAB jobs to have per MiniAOD root file 
L20: Specify name of directory that will be created in the output directory
L21: Specify output directory where the JRA ntuples will be saved. Note that /eos/cms/ should not be written before /store/group/phys_jetmet/

voms-proxy-init -voms cms \
crab submit -c custom_crab_JEC.py

To check the status of jobs in CRAB while inside JetMETAnalysis-MC-truth/JetAnalyzers/test/:

crab status -d workArea/requestName/

To resubmit jobs if some have failed:

crab resubmit -d workArea/requestName/

When all jobs are in finished status, the output JRA root files, based on the above custom_crab_JEC.py, will be located in a directory with this format:\
/eos/cms/store/group/phys_jetmet/ilias/test/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/outputDatasetTag/yymmdd_hhmmss/0000/

These JRA root files are the input ntuples for the MC-truth jet energy corrections.


<a name="JEC"></a>
## Instructions on how to derive MC-truth JECs

**General tips:**

1) In all the steps of the MC-truth JECs you will be submitting jobs to condor. Once you submit them you can check their status by doing: \
condor_q \
For each job you submit, when it is finished, a corresponding root file should appear in eos. Additionally, in the directory $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor/Log/ for each job 3 files will appear: err,log,out. Check the err ones to see if there was an error in your codes that made the jobs crash. If you have a bug somewhere then the output root files in eos will not be created or they will be created empty, so you can also check them by going to the eos directory and doing ls -lh to see the size of the files and if they have closed properly. If the code does not have any bugs then these files should be a few MB each. \
If there are no bugs and the root files have been created correctly then it is usual that condor did not run all jobs (due to technical issues related to condor). Therefore you should always check how many output root files were created by doing "ls | wc -l": they should be the same number as the jobs you submitted. If they are fewer then you can resubmit the jobs (./SubmitStep*.sh as you did in the first time) until all root files are processed. 

2) Every time there is a change in the codes inside $CMSSW_BASE/src/JetMETAnalysis-MC-truth/ you should then compile the codes doing scram b -j 4.

<a name="PU-reweight"></a>
### Histograms for PU Reweighting

In order to later do PU reweighting when deriving and applying the corrections you need to have 2 input root files with the mu (pileup) distribution; one for data and one for the MC. Note that they should have the same binning (we usually use 100 bins from 0 to 100).

To produce the root file for data:

You need to take the latest Golden JSON (Cert.txt) and pileup_latest.txt files from the JERC Protolab : \
https://gitlab.cern.ch/cms-jetmet/JERCProtoLab/-/tree/master/macros/lumi_PU/InputFiles 

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/MyDataMCHistos/ \
cmsenv \
pileupCalc.py -i Cert.txt --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100  MyDataPUHisto.root 

where Cert.txt is the JSON file for the corresponding epoch you want to process (e.g. Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON_nonAPV.txt for the non-APV UL16 data) and pileup_latest.txt for the corresponding year.

Output file: MyDataPUHisto.root

To produce the root file for MC:

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/ \
root -l \
[0] .x create_MyHist_PU.C

Output file: MyMCPUHisto.root


<a name="L1"></a>
### Pileup Offset Corrections (L1)

Based on which collection you want to process go the respective directory: \
cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4CHS/ \
cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK8CHS/ \
cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4PUPPI/ \
cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK8PUPPI/

Only in the first time do: \
	g++ ListRunLumi.cpp -o RunListRunLumi \
		\`root-config --cflags --libs\`

Copy the MyMCPUHisto.root and MyDataPUHisto.root to $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4CHS/Files/

Make sure that in the script Setup_CMSSW.sh the correct path to the condor_AK4CHS/ folder is written.

Determine the input MC samples and output files in eos: \
Open the Setup_FileLocation.sh code and write the correct paths to the NoPUFiles (NoPU or EpsilonPU MC) and WithPUFiles (FlatPU MC). Moreover, write the output directories in eos where the output root files in the 4 steps of the MC-truth JECs will appear. 

**Step1**

In the first step the events between the NoPU/EpsilonPU and the FlatPU sample are matched one by one: 

./SubmitStep1.sh

This will submit jobs to condor. Once they are done then some text files will appear in the Step1Output in eos, where all the events that are matched are written.

./HarvestStep1.sh

This will take as input the txt files in the Step1Output from eos and will create a file named "MatchedFiles" in the directory $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4CHS/Files/ . In that file all the events that are matched between the NoPU/EpsilonPU and the FlatPU sample will be listed.

**Step2**

In this step, the jets from the matched events will be also matched and the offset will be calculated: offset = jetpT(FlatPU) - jetpT(NoPU/EpsilonPU).\
First do:

./RunPrepareStep2Submission 1 > SubmitStep2.sh

This takes as input the $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4CHS/Files/MatchedFiles file and rewrites the SubmitStep2.sh code. Open the SubmitStep2.sh code to see how it has changed. It should list the directories for the MC samples where the JRA_\*.root are located. In L3 you should write the full path of where the Setup_FileLocation.sh is located. Then, replace L11 with:

echo "+JobFlavour = testmatch" >> $SubmissionFile

and immediately below add the line:

echo "+request_cpus=3">>$SubmissionFile

The above lines will help the jobs to run quicker.

The SubmitStep2.sh code calls the Step2PUMatching.sh one so open it and modify it appropriately. In turn, the Step2PUMatching.sh code calls the $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetAnalyzers/bin/jet_match_x.cc. In L40 of the Step2PUMatching.sh make sure it is false (we do not apply any corrections, we want to derive them).

Once you have modified the above codes, submit the jobs:

./SubmitStep2.sh

Once all jobs are finished and all root files are created in the Step2Output location, open the HarvestStep2.sh code, which in turn calls the $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetAnalyzers/bin/jet_synchfit_x.cc one. In this code, in L425-443 you determine what fit function should be used (L1Complex, L1Simple, L1SemiSimple) so comment out 2 of them and leave the one to be used. In L640-648 you also determine the range of the 2D fit. In the HarvestStep2.sh code in L14 you define if you want to use ak4 or ak8 in the jet_synchfit_x.cc code.

./HarvestStep2.sh

This code does 2 things. First it hadds the Step2Output files in eos and then it will create the **Winter22Run3_L1FastJet_AK4PFchs.txt** file in the directory $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4CHS/Files/ (or the directory you have specified in L9 of the HarvestStep2.sh code), along with some plots concerning the 2D fits.

This hadded root file contains information for the offset (before you apply any correction to the MC). To plot and make useful histograms of the offset from this root file do:

cd $CMSSW_BASE/src/ \
cmsenv \
jet_synchplot_x -inputDir ./ -algo1 ak4pfchs -algo2 ak4pfchs -outDir ./ -outputFormat .png .pdf -fixedRange false -tdr true -npvRhoNpuBinWidth 10 -NBinsNpvRhoNpu 5

where the -inputDir will be the directory where the hadded output_ak4pfchs.root file is located. In the -outDir many .png and .pdf files will be created, along with the canvases_synchplot_ak4pfchs.root file. The above code calls the $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetUtilities/src/SynchFittingProcedure.hh. In it, in L430-529 you determine how the offset will be calculated (mean, median or mode).

In order to plot the offset over pT as a function of pT and eta:

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/ \
python PlotL1OffsetVsPt.py \

which takes as input the canvases_synchplot_ak4pfchs.root file.

You are basically done with the L1 corrections, since you have derived the L1 JEC text file. However, you should check the quality of these L1 corrections and if they actually remove the pileup as intended. You have already plotted the raw offset, and you need to do that again, applying now this text file you have produced. For that, you need to repeat the Step2 procedure but now in the Step2PUMatching.sh code in L40 make sure it is true and immediately below add the line -JECpar Winter22Run3_L1FastJet_AK4PFchs.txt. Then sumbit the jobs again with ./SubmitStep2.sh but make sure that *the output root files are in a different location as before so as to not overwrite anything!* When the jobs are done you should **not** run the HarvestStep2.sh code because you do not want to derive any corrections now. You only need to hadd the root files in eos and now use this new hadded root file as input in order to plot the offset again. The offset now should be ~0 since you have applied the Winter22Run3_L1FastJet_AK4PFchs.txt file in the PU sample.

When you plot the offset, you can use the mean, median or mode (gaussian fits) for the offset distribution (SynchFittingProcedure.hh). To check one-by-one the offset distributions from which the mean, median or mode is calculated:

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/ \
root -l \
[0] .x Plot_GausFit_Offset.C


<a name="L2L3"></a>
### Relative & Absolute Corrections (L2L3)

Edit the $CMSSW_BASE/src/condor/Setup_FileLocation.sh code with the input WithPUFiles which should be the PremixedPU MC sample. The NoPUFiles are not used for the L2L3 corrections.

**Step3**

In this step the L1 correction txt file is applied to the PU MC and the response histos in bins of eta and pT are created. The SubmitStep3.sh code calls the Step3ApplyL1.sh code which in turn calls the jet_response_analyzer_x.cc code. 

For PUPPI jets we do not derive L1 corrections, so we have commented out L19-28 in the Step3ApplyL1.sh code so that the step where the L1 corrections are applied to the MC is skipped.

./SubmitStep3.sh

When all jobs are done edit the HarvestStep3.sh code, which calls the code $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetUtilities/src/L2Creator.cc. When standard+Gaussian options is specified in L20 of HarvestStep3.sh then the inverse of the median response will be fitted with this function (L1076 of L2Creator.cc) for all 82 eta bins. In L1141-1177 the initial parameters for all the fits are specified. Since in some of the eta bins the fits fail to converge, you can change the set of the initial parameters for specific eta bins in L402-490.

./HarvestStep3.sh

This will hadd the output root file of Step3Output and then do the fits in order to derive the L2L3 corrections, thus creating the **Winter22Run3_L2Relative_AK4PFchs.txt** file in the directory $CMSSW_BASE/src/JetMETAnalysis-MC-truth/condor_AK4CHS/Files/, along with the file l2.root that contains the graphs with all fits. When running this command the fit probability for all fits will be printed so you will have to identify which fits have failed, modify the L2Creator.cc code, and rerun until all fits converge and the final txt file has the best quality. 


The Merged.root file in the Step3Output directory contaings a lot of histograms with the response distribution (after having applied the L1 correction and before having applied the L2L3 response corrections) in bins of pTgen and eta. To plot such histograms you can use the Plot_response_before_L2L3JEC.C inside $CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/

The l2.root file that is produced contains histograms with the median(response) as a function of pTgen for all eta bins, and the [median(response)]^-1 as a function of pTreco for all eta bins, along with the standard+gaussian fits. To plot such histograms you can use the Plot_ResponseVsRefPt.C and Plot_InverseOfResponseVsJetPt.C inside $CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/


**Step4**

In this step both JEC text files (L1 + L2L3) are applied to the MC and the response is calculated and plotted as a function of eta and pt. The SubmitStep4.sh code calls the Step4Closure.sh one which in turn calls the jet_correction_analyzer_x.cc. After you edit these codes:

./SubmitStep4.sh

Once all jobs are done edit the HarvestStep4.sh code which calls the $CMSSW_BASE/src/JetMETAnalysis-MC-truth/JetUtilities/src/ClosureMaker.cc code, adn run:

./HarvestStep4.sh

This code produces plots of the corrected response vs pt and eta, along with root files with the histograms saved in them.

In order to plot the above L1L2L3 closure plot vs pt with the stylistics of the JERC group:

cd $CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/ \
cmsenv \
python PlotL1L2L3ClosureVsPt.py

<a name="Corr-Factors"></a>
## Instructions on how to plot the correction factors

The two JEC text files Winter22Run3_L1FastJet_AK4PFchs.txt and Winter22Run3_L2Relative_AK4PFchs.txt can be used as input files in order to plot the overall MC-truth correction factors as a function of eta and pt.

cd $CMSSW_BASE/src/ \
cmsenv \
jet_draw_corrections_x -algs ak4pfchs -path ./ -outputDir ./ -useL1FasCor true -useL2Cor true -era ParallelMCL1

where -path is the directory where the two text files are located. This command will produce some plots in the outputDir along with a root file where the histograms of the corrections vs eta and pt are saved. These kind of root files can be used as input for the following plotting scripts:

$CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/Plot_CorrectionsVsEtaPt.C \
$CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/Plot_CorrectionsVsEtaPt_Comparison_withRatios.C 

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

$CMSSW_BASE/src/JetMETAnalysis-MC-truth/scripts/Plot_L1CorrectionsVsRho.C
