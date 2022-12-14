#include "JetMETAnalysisMCtruth/JetUtilities/interface/JRAEvent.h"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/TProfileMDF.h"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/PUNtuple.hh"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/JetInfo.hh"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/EvtID.hh"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/TSplineSteffen.hh"

#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/GeometryVector/interface/Point3DBase.h"
#include "DataFormats/GeometryVector/interface/GlobalTag.h"
#include "DataFormats/GeometryVector/interface/Basic3DVector.h"

#include <vector>
#include <map>
#include <utility>

namespace { 
   struct dictionary {
      //JRAEvent jraeventdummy0;
      edm::Wrapper<JRAEvent> dummy1;
      std::vector<JRAEvent> dummy2;
      edm::Wrapper<std::vector<JRAEvent> > dummy3;
      edm::Wrapper<JRAEvent::Flavor> dummy4;
      std::vector<JRAEvent::Flavor> dummy5;
      edm::Wrapper<std::vector<JRAEvent::Flavor> > dummy6;
      evtid dummy7_0;
      edm::Wrapper<evtid> dummy7_1;
      std::vector<evtid> dummy8;
      edm::Wrapper<std::vector<evtid> > dummy9;
      std::map<evtid,std::pair<Long64_t,Long64_t>,evtid> dummy10;
      edm::Wrapper<std::map<evtid,std::pair<Long64_t,Long64_t>,evtid> > dummy11;
      std::vector<std::pair<evtid,std::pair<Long64_t,Long64_t> > > dummy12;
      edm::Wrapper<std::vector<std::pair<evtid,std::pair<Long64_t,Long64_t> > > > dummy13;
      std::pair<Long64_t,Long64_t> dummy14;
      edm::Wrapper<std::pair<Long64_t,Long64_t> > dummy15;
      std::vector<std::pair<Long64_t,Long64_t> > dummy16;
      edm::Wrapper<std::vector<std::pair<Long64_t,Long64_t> > > dummy17;
      std::map<evtid,std::pair<ULong64_t,ULong64_t>,evtid> dummy18;
      edm::Wrapper<std::map<evtid,std::pair<ULong64_t,ULong64_t>,evtid> > dummy19;
      std::vector<std::pair<evtid,std::pair<ULong64_t,ULong64_t> > > dummy20;
      edm::Wrapper<std::vector<std::pair<evtid,std::pair<ULong64_t,ULong64_t> > > > dummy21;
      std::pair<ULong64_t,ULong64_t> dummy22;
      edm::Wrapper<std::pair<ULong64_t,ULong64_t> > dummy23;
      std::vector<std::pair<ULong64_t,ULong64_t> > dummy24;
      edm::Wrapper<std::vector<std::pair<ULong64_t,ULong64_t> > > dummy25;
      edm::Wrapper<Point3DBase<float,GlobalTag> > dummy26;
      
   };
}
