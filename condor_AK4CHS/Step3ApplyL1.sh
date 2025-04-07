#!/bin/sh --login

#BSUB -q 1nh

WorkDir=$1
Files=$2
Output=$3
ID=$4

source $WorkDir/Setup_CMSSW.sh

cp $WorkDir/Files/Summer23_V1/L1_output/*.txt .
cp $WorkDir/Files/Summer23_V1/L1_output/*.root .

echo Input files are: $Files

hadd -k -f Input.root `echo $Files | tr ':' ' '`

jet_apply_jec_x \
   -input Input.root \
   -output JRA_jecl1.root \
   -jecpath ./ \
   -era Summer23_V1_MC \
   -levels 1 \
   -algs ak4pfchs \
   -L1FastJet true \
   -saveitree false

cp $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/config/jra_dr_finebinning.config jra.config
#cp $CMSSW_BASE/src/JetMETAnalysisMCtruth/JetAnalyzers/config/jra_dr_coarsebinningeta.config jra.config

jet_response_analyzer_x jra.config \
   -input JRA_jecl1.root \
   -nbinsabsrsp 0 \
   -nbinsetarsp 0 \
   -nbinsphirsp 0 \
   -nbinsrelrsp 60 \
   -doflavor false \
   -flavorDefinition phys \
   -MCPUReWeighting MyMCPUHisto_Run3Summer23_PremixedPU.root \
   -MCPUHistoName pileup \
   -DataPUReWeighting MyDataPUHisto_2023_erasC_100bins.root \
   -DataPUHistoName pileup \
   -output jra.root \
   -useweight false \
   -nrefmax 3 \
   -algs ak4pfchsl1 \
   -drmax 0.2 \
   -relrspmin 0.0 \
   -relrspmax 3.0 \
   -jtptmin 0 \
   -doDZcut true \
   -doNMcut false \
   -doVetoMap true \
   -JetVetoMapName JetVetoMap_2023C.root

cp jra.root ${Output}/JRA_jecl1${ID}.root

rm *.root

