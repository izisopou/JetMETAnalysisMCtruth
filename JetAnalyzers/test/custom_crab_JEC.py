from WMCore.Configuration import Configuration
config = Configuration()
config.section_("General")
config.General.requestName = 'requestName'
config.General.workArea = 'workArea'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_JRA_cfg_MCtruth.py'
config.JobType.allowUndistributedCMSSW = True
#config.JobType.inputFiles = ['']

config.section_("Data")
config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCP5_Flat2018_13p6TeV_pythia8/Run3Winter22MiniAOD-FlatPU0to70_122X_mcRun3_2021_realistic_v9-v2/MINIAODSIM'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter/'
config.Data.outputDatasetTag = 'outputDatasetTag'
config.Data.outLFNDirBase = '/store/group/phys_jetmet/<personal_folder>/'
#config.Data.ignoreLocality = True
config.Data.ignoreLocality = False

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'