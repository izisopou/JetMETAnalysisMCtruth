#!/bin/sh --login

#BSUB -q 1nh

WorkDir=$1
Files=$2
Output=$3
ID=$4

source $WorkDir/Setup_CMSSW.sh

cp $WorkDir/Files/Summer23_V1/L2L3_output/*.txt .
cp $WorkDir/Files/Summer23_V1/L2L3_output/*.root .

echo Input files are: $Files

hadd -k -f Input.root `echo $Files | tr ':' ' '`

# We do not have L1 corrections for PUPPI so the following lines are commented out
# but if you have derived  them you need to un-comment them.

#jet_apply_jec_x \
#   -input Input.root \
#   -output JRA_jecl1.root \
#   -jecpath ./ \
#   -era Summer23_V1_MC \
#   -levels 1 \
#   -algs ak8puppi \
#   -L1FastJet true \
#   -saveitree false

cp $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/config/jra_dr_finebinning.config jra.config
#cp $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/config/jra_dr_coarsebinningeta.config jra.config

# if you want to apply an L1 txt file and have the above lines un-commented out
# then you need to have the following lines below:
#
# -input JRA_jecl1.root
# -algs ak8puppil1

jet_response_analyzer_x jra.config \
   -input Input.root \
   -nbinsabsrsp 0 \
   -nbinsetarsp 0 \
   -nbinsphirsp 0 \
   -nbinsrelrsp 60 \
   -doflavor false \
   -flavorDefinition phys \
   -MCPUReWeighting MyMCPUHisto_Run3Summer23_PremixedPU.root \
   -MCPUHistoName pileup \
   -DataPUReWeighting MyDataPUHisto_2023_erasC_100Bins.root \
   -DataPUHistoName pileup \
   -output jra.root \
   -useweight false \
   -nrefmax 3 \
   -algs ak8puppi \
   -drmax 0.4 \
   -relrspmin 0.0 \
   -relrspmax 3.0 \
   -jtptmin 0 \
   -doDZcut true \
   -doNMcut true \
   -doVetoMap true \
   -JetVetoMapName JetVetoMap_2023C.root

cp jra.root ${Output}/JRA_jecl1${ID}.root

rm *.root


