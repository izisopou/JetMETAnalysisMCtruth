#!/bin/sh

source $CMSSW_BASE/src/JetMETAnalysisMCtruth/condor_AK8PUPPI/Setup_FileLocation.sh

Input=$WithPUFiles
Output=$Step4Output

mkdir -p $Step4Output

mkdir -p Log
SubmissionFile=Step4.condor

echo "Universe   = vanilla" > $SubmissionFile
echo "Executable = `pwd`/Step4Closure.sh" >> $SubmissionFile
echo "+JobFlavour = microcentury" >> $SubmissionFile
echo "requirements = (TARGET.OpSysAndVer =?= \"AlmaLinux9\")" >> $SubmissionFile
echo "should_transfer_files = NO" >> $SubmissionFile
# echo "transfer_output_files = DONE.txt" >> $SubmissionFile
echo >> $SubmissionFile

Count=0
for File in `ls $Input | ./Columnize 5 | tr ' ' ':'`
do
   echo $File

   echo "Arguments = `pwd` $File $Output $Count" >> $SubmissionFile
   echo 'Output    = Log/Step4.out.$(Process)' >> $SubmissionFile
   echo 'Error     = Log/Step4.err.$(Process)' >> $SubmissionFile
   echo 'Log       = Log/Step4.log.$(Process)' >> $SubmissionFile
   echo 'Queue' >> $SubmissionFile
   echo >> $SubmissionFile

   let Count=Count+1
done

condor_submit $SubmissionFile
