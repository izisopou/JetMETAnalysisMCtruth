////////////////////////////////////////////////////////////////////////////////
//
// jet_inspect_graphs_x
// --------------------
//
//            07/20/2009 Philipp Schieferdecker <philipp.schieferdecker@cern.ch>
////////////////////////////////////////////////////////////////////////////////


#include "JetMETAnalysisMCtruth/JetUtilities/interface/CommandLine.h"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/ObjectLoader.h"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/RootStyle.h"
#include "JetMETAnalysisMCtruth/JetUtilities/interface/Style.h"

#include <TApplication.h>
#include <TStyle.h>
#include <TFile.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TLatex.h>
#include <TMultiGraph.h>
#include <TGraphErrors.h>
#include <TH1F.h>
#include <TF1.h>
#include <TText.h>
#include <TLine.h>
#include <TPaveStats.h>
#include <Math/Interpolator.h>
#include <TSpline.h>

#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <cmath>
#include <fstream>
#include <algorithm>

using namespace std;


////////////////////////////////////////////////////////////////////////////////
// declare local functions
////////////////////////////////////////////////////////////////////////////////
void   draw_range(const string& range,const int residual=-1);

string get_range(const ObjectLoader<TGraphErrors>& gl,
		 const vector<unsigned int>& indices,
		 bool  addFixedVars=true,string refpt="");
string get_legend_label_from_alg(const string& alg);
string get_legend_label_from_input(const string& input);
void   set_graph_style(TGraphErrors* g,unsigned int ngraph,bool nocolor,
		       const vector<unsigned int>& vcolors,
		       const vector<unsigned int>& vmarkers,
		       const vector<unsigned int>& vlstyles,
		       const vector<float>& vsizes,
		       const vector<float>& vlsizes);

void   set_axis_titles(TH1*h,const string& quantity,float ymin,float ymax,
		       string xtitle,string ytitle,string refpt="",bool tdr=false);

void   draw_graph_residual(TPad* pad,TMultiGraph* mg,
			   const int errMode,
			   const bool resmcdata,
			   const vector<int>& defmcdata,
			   const float yresmax=-1.,
			   const string& restitle="",
			   const float restitlesize=.11,
			   float xmin=-1.,
			   float xmax=-1.,
			   float ymin=-1.,
			   float ymax=-1.,
			   int fullfit=-1,
               bool tdr=false,
               bool interpolate=false);

TH1F*  set_axis_range(TMultiGraph* mg, 
		       float xmin=-1., float xmax=-1.,
		       float ymin=-1., float ymax=-1.);


void   draw_zline(TH1* h1,float xmin=-1.,float xmax=-1.,float y=0.);

void   draw_extrapolation(TMultiGraph* mg,int fullfit=-1,
			  float xmin=-1.,float xmax=-1.);

void draw_labels(const vector<string>& labels,bool leginplot,bool tdrautobins);

////////////////////////////////////////////////////////////////////////////////
// main
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
int main(int argc,char** argv)
{
  CommandLine cl;
  if (!cl.parse(argc,argv)) return 0;

  vector<string> inputs    = cl.getVector<string>("inputs");
  vector<string> algs      = cl.getVector<string>("algs",           "ak5calo");
  vector<string> variables = cl.getVector<string>("variables","RelRspVsRefPt");

  vector<string> leglabels = cl.getVector<string>("leglabels",             "");

  vector<string> tdrlabels = cl.getVector<string>("tdrlabels",             "");
  bool           tdrautobins=cl.getValue<bool>   ("tdrautobins",        false);
  bool           drawrange = cl.getValue<bool>   ("drawrange",           true);


  bool           leginplot = cl.getValue<bool>   ("leginplot",           true);

  bool           drawlegend= cl.getValue<bool>   ("drawlegend",          true);
  double         legx      = cl.getValue <double>("legx",                 0.5);
  double         legy      = cl.getValue <double>("legy",                 0.9);
  double         legw      = cl.getValue <double>("legw",                 0.4);
  int            extraleglabels = cl.getValue<int>("extraleglabels",        0);

  string         xtitle    = cl.getValue<string> ("xtitle",                "");
  string         ytitle    = cl.getValue<string> ("ytitle",                "");
  string         refpt     = cl.getValue<string> ("refpt",                 "");

  vector<unsigned int>colors = cl.getVector<unsigned int>("colors",        "");
  vector<unsigned int>markers= cl.getVector<unsigned int>("markers",       "");
  vector<unsigned int>lstyles= cl.getVector<unsigned int>("lstyles",       "");
  vector<float>       sizes  = cl.getVector<float>       ("sizes",         "");
  vector<float>       lsizes = cl.getVector<float>       ("lsizes",        "");


  string         text      = cl.getValue<string> ("text",                  "");
  bool           logx      = cl.getValue<bool>   ("logx",               false);
  bool           logy      = cl.getValue<bool>   ("logy",               false);
  float          ymin      = cl.getValue<float>  ("ymin",                -1.0);
  float          ymax      = cl.getValue<float>  ("ymax",                -1.0);
  bool           nocolor   = cl.getValue<bool>   ("nocolor",            false);
  bool           overlay   = cl.getValue<bool>   ("overlay",             true);
  int            fullfit   = cl.getValue<int>    ("fullfit",               -1);
  string         prefix    = cl.getValue<string> ("prefix",                "");
  string         suffix    = cl.getValue<string> ("suffix",                "");
  string         opath     = cl.getValue<string> ("opath",                 "");
  vector<string> formats   = cl.getVector<string>("formats",               "");
  bool           batch     = cl.getValue<bool>   ("batch",              false);
  bool           latex     = cl.getValue<bool>   ("latex",              false);
  bool           latexcndf = cl.getValue<bool>   ("latexcndf",           true);
  bool           fittofile = cl.getValue<bool>   ("fittofile",          false);

  int            residual  = cl.getValue<int>    ("residual",              -1);
  string         restitle  = cl.getValue<string> ("restitle",              "");
  float          restitlesize=cl.getValue<float> ("restitlesize",         .11); 
  float          yresmax   = cl.getValue<float>  ("yresmax",               -1);
  bool           resmcdata = cl.getValue<bool>   ("resmcdata",          false);
  vector<int>    defmcdata = cl.getVector<int>   ("defmcdata",             "");
  bool           interpolate=cl.getValue<bool>   ("interpolate",        false);

  float          xmin      = cl.getValue<float>  ("xmin",                -1.0);
  float          xmax      = cl.getValue<float>  ("xmax",                -1.0);
  string         mgname    = cl.getValue<string> ("mgname",                "");
  bool           verbose   = cl.getValue<bool>   ("verbose",            false);
  bool           tdr       = cl.getValue<bool>   ("tdr",                false);
  bool           doFlavor  = cl.getValue<bool>   ("doFlavor",           false);
  bool           override  = cl.getValue<bool>   ("override",           false);
  bool           removeFit = cl.getValue<bool>   ("removeFit",          false);
  bool           drawSpline= cl.getValue<bool>   ("drawSpline",         false);


  if (!cl.check()) return 0;
  cl.print();
  
  // sanity check
  if (!override && ((inputs.size()>1&&algs.size()>1)||
      (algs.size()>1&&variables.size()>1)||
      (inputs.size()>1&&variables.size()>1))) {
    cout<<"Provide more than one value only for one of inputs/algs/variables!"
	<<endl;
    return 0;
  }

  if (resmcdata && defmcdata.size()!=2 && !interpolate) {
    cout<<"If using residual for MC to data comparison you MUST provide"<<endl
	<<"in defmcdata: 1) number of graph with MC (+fit) 2) number of data graph"<<endl;
    return 0;
  }
  
  if (!text.empty()){cout<<"option -text depreciated; use -tdrlabels!"<<endl;return 0;}
  if (0==tdrlabels.size()&&tdrautobins) {
    cout<<"Found no tdrlabels - resetting tdrautobins = false"<<endl;
    tdrautobins = false;
  }
  
  if (ymin<0.0&&logy) ymin = 0.01;

  if (batch&&formats.size()==0) formats.push_back("pdf");
  
  argc = (batch) ? 2 : 1; if (batch) argv[1] = (char*)"-b";
  TApplication* app=new TApplication("jet_inspect_graphs",&argc,argv);
  
  if(tdr) {
    setTDRStyle();

    gStyle->SetOptStat(0);
    gStyle->SetOptFit(0);
  }
  else {
    set_root_style();
  
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(0);
  }
  
  // is the *same* quantity compared for several (e.g. eta-) ranges?
  set<string> quantities;
  for (unsigned int i=0;i<variables.size();i++) {
    size_t pos = variables[i].find(':');
    if(doFlavor) {
      size_t startEndPos = variables[i].find("Abs");
      quantities.insert(variables[i].substr(startEndPos,pos-startEndPos));
    }
    else {
      quantities.insert(variables[i].substr(0,pos));
    }
  }
  if (!override && quantities.size()!=1) {
    cout<<"ERROR: don't try to compare different quantities!"<<endl;
    return 0;
  }
  
  // determine legend labels
  if (algs.size()>1) {
    if (leglabels.size()>0) {
      if (leglabels.size()-extraleglabels!=algs.size()) {
	cout<<"ERROR: leglabels / algs mismatch!"<<endl;
	return 0;
      }
    }
    else {
      for (unsigned int ialg=0;ialg<algs.size();ialg++)
	leglabels.push_back(get_legend_label_from_alg(algs[ialg]));
    }
  }
  else if (inputs.size()>1) {
    if (leglabels.size()>0) {
      if (leglabels.size()-extraleglabels!=inputs.size()) {
	cout<<"ERROR: leglabels / inputs mismatch!"<<endl;
      }
    }
    else {
      for (unsigned int iinput=0;iinput<inputs.size();iinput++)
	leglabels.push_back(get_legend_label_from_input(inputs[iinput]));
    }
  }
  else if (variables.size()>1) {
    if (leglabels.size()>0) {
      if (leglabels.size()-extraleglabels!=variables.size()) {
	cout<<"ERROR: leglabels / variables mismatch!"<<endl;
	return 0;
      }
    }
  }
  else {
    leglabels.push_back(get_legend_label_from_alg(algs[0]));
  }

  TMultiGraph*          mg(0);
  TLegend*              leg(0);
  TLegend*              leg2(0);
  vector<TGraphErrors*> graphs;
  vector<string>        ranges;
  string                quantity=(*quantities.begin());
  
  /// LOOP OVER FILES
  for (unsigned int iinput=0;iinput<inputs.size();iinput++) {
    
    string input=inputs[iinput].substr(0,inputs[iinput].find(':'));
    TFile* file=new TFile(input.c_str(),"READ");
    if (!file->IsOpen()) {cout<<"Can't open "<<file->GetName()<<endl;return 0;}
    
    /// LOOP OVER ALGORITHMS
    for (unsigned int ialg=0;ialg<algs.size();ialg++) {

      string alg=algs[ialg];
      
      TDirectory* dir =(TDirectory*)file->Get(alg.c_str());
      if (0==dir && override) {
        continue;
      }
      else if(0==dir) {
        cout<<"No dir "<<algs[ialg]<<" found"<<endl;
        return 0;
      }

      /// LOOP OVER VARIABLES
      for (unsigned int ivar=0;ivar<variables.size();ivar++) {
	
	string variable=variables[ivar];
  if (verbose)
    cout << "Doing variable " << variable << " ... " << endl;

	ObjectLoader<TGraphErrors> gl;
	gl.load_objects(dir,variable);
  if (verbose)
    cout << "\tNumber of TGraphErrors loaded = " << gl.nobjects() << endl;
	
	gl.begin_loop();
	vector<unsigned int> indices;
	TGraphErrors* g(0);
	while ((g=gl.next_object(indices))) {

	  graphs.push_back(g);
	  ranges.push_back(get_range(gl,indices,variables.size()==1,refpt));

	  if (0==mg) {
	    stringstream sscname;
	    if (!prefix.empty()) sscname<<prefix<<"_";
	    sscname<<quantity;
	    for (unsigned int i=0;i<gl.nvariables();i++) {
	      if (variables.size()>1&&gl.nobjects(i)==1) continue; //??
	      sscname<<"_"<<gl.variable(i)
		     <<gl.minimum(i,indices[i])<<"to"
		     <<gl.maximum(i,indices[i]);
	    }
	    if (!suffix.empty()) sscname<<"_"<<suffix;
	    int nleglabels=(leglabels.size()>0)?leglabels.size():variables.size();
      if (mgname.empty()) mgname = sscname.str();
	    //mg=new TMultiGraph(sscname.str().c_str(),"");
      mg=new TMultiGraph(mgname.c_str(),"");

	    //double ymax=(quantity.find("Rsp")==string::npos)?0.85:0.4;

	    double legxmin = (leginplot) ? legx : 0.825;
	    double legymin = (residual>=0) ? legy-0.045 : legy;
      if(residual>=0 && tdr) legymin += 0.03;
	    double legxmax = (leginplot) ? legx+legw : 1.03;
	    double legymax = (override && algs.size()>1 && variables.size()>1) ? 
                       legymin - (nleglabels)*0.075 : legymin - (nleglabels)*0.055;

	    leg = new TLegend(legxmin,legymin,legxmax,legymax);
	    //leg->SetFillColor(10); leg->SetLineColor(10); leg->SetBorderSize(0);
      leg->SetFillColor(0); leg->SetLineColor(0); leg->SetBorderSize(0);
      if(override && algs.size()>1 && variables.size()>1) {
        leg2 = new TLegend(legxmin-0.08,legymin,legxmax-0.08,legymax);
        leg2->SetFillColor(0); leg2->SetLineColor(0); leg2->SetBorderSize(0);
      }
      for(int el=0; el<extraleglabels;el++) {
         leg->AddEntry((TObject*)0,leglabels[el].c_str(),"");
      }

	    //leg=new TLegend(0.5,ymax,0.9,ymax-nleglabels*0.06);
	    //range=get_range(gl,indices,variables.size()==1);
	  }

	  //cout<<"indices back: "<<indices.back()<<endl;

	  int   ilabel=(inputs.size()>1) ? 
	                iinput : (algs.size()>1) ? 
	                ialg   : (variables.size()>1) ? 
	                ivar   : (indices.size()>0) ? indices.back() : 0;
      ilabel+=extraleglabels;
	  string label=(variables.size()>1&&leglabels.size()==0) ?
	    get_range(gl,indices,true,refpt) : (leglabels.size()>(unsigned)ilabel) ? 
	    leglabels[ilabel] : "error";

	  mg->Add(g); 
	  set_graph_style(g,overlay*(graphs.size()-1),nocolor,colors,markers,lstyles,sizes,lsizes);
    if(override && algs.size()>1 && variables.size()>1) {
      TString header = variables[ivar].substr(0,3);
      header.ToLower();
      if(header.EqualTo("eta") || header.EqualTo("phi")) {
        header = "#kern[0.3]{ #" + header+"}";
      }

      if(!leg->GetHeader() && ivar==0)
        leg->SetHeader(header);
      if(leg2 && !leg2->GetHeader() && ivar==1)
        leg2->SetHeader(header);

      if(ivar==0)
        leg->AddEntry(g,label.c_str(),"lp");
      else if(leg2)
        leg2->AddEntry(g," ","lp");
    }
    else if(doFlavor && (ivar==0||ivar==variables.size()-1))
      continue;
    else
  	  leg->AddEntry(g,label.c_str(),"lp");

	  // print fit parameters
	  TF1* fitfnc = (TF1*)g->GetFunction("fit");
	  if (0!=fitfnc) {
	    for (int ipar=0;ipar<fitfnc->GetNpar();ipar++)
	      cout<<fitfnc->GetParameter(ipar)<<" +- "
		  <<fitfnc->GetParError(ipar)<<endl;
	    if (latexcndf) {
	      cout<<"->Chi2/NDF: "
		  <<fitfnc->GetChisquare()<<"/"
		  <<fitfnc->GetNDF()<<endl;
	    }
	  }

	  // end print fit parameters

	  // save latex table //hh
	  
	  if (latex&&(0!=fitfnc)) {

	    ofstream texfile; stringstream texfilename; stringstream texinput;
	    
	    if (!opath.empty()) texfilename<<opath<<"/";
	    texfilename<<alg<<"_"<<mg->GetName()<<".tex";
	    texfile.open(texfilename.str().c_str(),ofstream::trunc);
	    if (!texfile.is_open()) {
	      cout<<"tex-ERROR: Could not create "<<texfilename.str()<<endl;continue;
	    }
	    texinput<<"%%fitfnc: "<<fitfnc->GetExpFormula()<<endl;

	    if (alg.find("pf")!=string::npos)texinput<<"\\pfjets & ";
	    else if (alg.find("calo")!=string::npos)texinput<<"\\calojets & ";
	    else if (alg.find("jpt")!=string::npos)texinput<<"\\jptjets & ";
	    else if (alg.find("btag")!=string::npos)texinput<<"\\btag & ";
	    else {
	      cout<<"tex-ERROR: Did not recognize alg "<<alg<<endl;continue;
	    }

	    for (int ipar=0;ipar<fitfnc->GetNpar()-1;ipar++) {
	      texinput<<"$ ("<<setprecision(5)<<fixed
		      <<fitfnc->GetParameter(ipar)
		      <<" $ & $ \\pm $ & "
		      <<"$ "<<setprecision(5)<<fixed
		      <<fitfnc->GetParError(ipar)<<") $ & ";
	    }
	    texinput<<"$ ("<<setprecision(5)<<fixed
		    <<fitfnc->GetParameter(fitfnc->GetNpar()-1)
		    <<" $ & $ \\pm $ & "
		    <<"$ "<<setprecision(5)<<fixed
		    <<fitfnc->GetParError(fitfnc->GetNpar()-1)<<") $";
	    //...last not least chi2/ndf
	    if (latexcndf) {
	      texinput<<" & $ ("<<setprecision(1)<<fixed
		      <<fitfnc->GetChisquare()
		      <<"/"
		      <<fitfnc->GetNDF()<<") $";
	    }
	    texfile<<texinput.str().c_str()<<" \\\\ "<<endl; texfile.close();
	    cout<<"Created tex file with fit table: "<<texfilename.str()<<endl<<endl;
	  }
	  else cout<<endl;

	  // end latex table //hh

	  if (fittofile&&0!=fitfnc) {

	    ofstream fitfile; stringstream fitfilename; stringstream fitinput;

	    if (!opath.empty()) fitfilename<<opath<<"/";
	    fitfilename<<alg<<"_"<<mg->GetName()<<".txt";
	    fitfile.open(fitfilename.str().c_str(),ofstream::trunc);
	    if (!fitfile.is_open()) {
	      cout<<"txt-ERROR: Could not create "<<fitfilename.str()<<endl;continue;
	    }
	    fitinput<<fitfnc->GetExpFormula()<<" "<<fitfnc->GetNpar()<<endl;
	    for (int ipar=0;ipar<fitfnc->GetNpar();ipar++) {
	      fitinput<<setprecision(10)<<fixed
		      <<fitfnc->GetParameter(ipar)<<" ";
	    }
	    fitinput<<endl;
	    fitfile<<fitinput.str().c_str(); fitfile.close();
	    cout<<"Created fit file with fit table: "<<fitfilename.str()<<endl<<endl;	    
	  }


	  
	} // graphs
      } // variables
    } // algorithms
  } // inputs

  if (0==mg) { cout<<"ERROR: No data points in the graph!"<<endl; return 0; }

  TCanvas* c;
  
  if (overlay) {
    if(tdr) {
      TH1D* frame = new TH1D();
      frame->GetXaxis()->SetLimits(xmin,xmax);
      frame->GetXaxis()->SetMoreLogLabels(logx);
      frame->GetXaxis()->SetNoExponent(logx);
      frame->GetYaxis()->SetRangeUser(ymin,ymax);
      set_axis_titles(frame,quantity,ymin,ymax,xtitle,ytitle,refpt,tdr);
      TH1D* frameRatio = new TH1D();
      frameRatio->GetXaxis()->SetLimits(xmin,xmax);
      frameRatio->GetXaxis()->SetMoreLogLabels(logx);
      frameRatio->GetXaxis()->SetNoExponent(logx);
      float ratioMin = 0.9;
      float ratioMax = 1.1;
      frameRatio->GetYaxis()->SetRangeUser(ratioMin,ratioMax);
      set_axis_titles(frameRatio,quantity,ratioMin,ratioMax,xtitle,restitle,refpt,tdr);
      frameRatio->GetYaxis()->SetTitleSize(0.049);
      
      if(residual>=0) {
        c = tdrDiCanvas(mg->GetName(),frame,frameRatio,14,11);
        frameRatio->GetYaxis()->SetRangeUser(ratioMin,ratioMax);
        c->GetPad(1)->SetLogx(logx);
        c->GetPad(1)->SetLogy(logy);
        c->GetPad(2)->SetLogx(logx);
      }
      else {
        c = tdrCanvas(mg->GetName(),frame,14,0,true);
        frame->GetXaxis()->SetTitleOffset(frame->GetXaxis()->GetTitleOffset()+0.05);
        if(TString(variables[0]).Contains("RelResVsRefPt"))
          frame->GetYaxis()->SetTitleOffset(1.16);
        c->GetPad(0)->SetLogx(logx);
        c->GetPad(0)->SetLogy(logy);
      }

      //This is a hack because TMultiGraph will always clear the pad
      c->cd(1);
      TGraphErrors *bounds = 0;
      TSpline3* spline = 0;
      int ngraphs = mg->GetListOfGraphs()->GetSize();
      for(int i=0;i<ngraphs; i++) {
        TGraphErrors* tmp = (TGraphErrors*)mg->GetListOfGraphs()->At(i);
        if(residual<0 && removeFit) {
          tmp->GetListOfFunctions()->Clear();
        }
        // This is a hack to reduce the x-axis range for calo to pT>30 GeV
        // It requires removing all of the points less than 30 GeV
        //if(algs.size()>1 && variables.size()==1 &&
        //   mg->GetListOfGraphs()->GetSize()==int(algs.size()) &&
        //   TString(algs[i]).Contains("calo",TString::kIgnoreCase) && 
        //   TString(variables[0]).Contains("VsRefPt")) {
        if(
           (algs.size()>1 && variables.size()==1 &&
           mg->GetListOfGraphs()->GetSize()==int(algs.size()) &&
           TString(algs[i]).Contains("calo",TString::kIgnoreCase) && 
           TString(variables[0]).Contains("VsRefPt")) ||
           (algs.size()>1 && variables.size()>1 && override && i<2 &&
            TString(tmp->GetName()).Contains("VsRefPt"))
           ) {
          Double_t* xVals = tmp->GetX();
          int nPoints = tmp->GetN();
          cout << "***SPECIAL CASE***" << endl
               << "alg=" << algs[i] << endl
               << "variable=" << variables[0] << endl;
          for(int ipoint=0; ipoint<nPoints; ipoint++) {
            if(xVals[ipoint]<20) {
              cout << "\tRemoving point " << ipoint << " at x=" << xVals[ipoint] << endl;
              tmp->RemovePoint(ipoint);
              ipoint--;
              xVals = tmp->GetX();
              nPoints = tmp->GetN();
            }
            else
              continue;
          }
        }
        if(drawSpline) {
          spline = new TSpline3(Form("%s_spline",tmp->GetName()),tmp);
          spline->SetLineColor(tmp->GetLineColor());
          //spline->SetLineWidth(tmp->GetLineWidth());
          spline->SetLineWidth(1.0);
        }
        // This is do that I can draw qJ and gJ first and last of the
        //  graphs as an envelope surrounding other flavours (no markers)
        if(doFlavor && (i==0 || i==ngraphs-1)) {
          if(i==0) {
            int n = tmp->GetN();
            TGraphErrors* tmpEnd = (TGraphErrors*)mg->GetListOfGraphs()->At(ngraphs-1);
            bounds = new TGraphErrors(n*2);
            Double_t* xVals = tmp->GetX();
            Double_t* yVals = tmp->GetY();
            Double_t* xValsEnd = tmpEnd->GetX();
            Double_t* yValsEnd = tmpEnd->GetY();
            for(int ipoint=0; ipoint<tmp->GetN(); ipoint++) {
              bounds->SetPoint(ipoint,xVals[ipoint],yVals[ipoint]);
              bounds->SetPoint(n+ipoint,xValsEnd[n-ipoint-1],yValsEnd[n-ipoint-1]);
            }
            tdrDraw(bounds,"f",kNone,kNone,kSolid,kYellow+1,1001,kYellow+1);
            draw_zline(frame,xmin,xmax,1.0);
          }
          else if(i==ngraphs-1)
            leg->AddEntry(bounds,"qg","f");
        }
        else {
          if(drawSpline) {
            spline->Draw("same");
          }
          tdrDraw(tmp,"P",tmp->GetMarkerStyle(),tmp->GetMarkerColor(),
                  tmp->GetLineStyle(),tmp->GetLineColor());
          draw_extrapolation(mg,fullfit,xmin,xmax);
        }
      }
      if(residual>=0) {
        draw_extrapolation(mg,fullfit,xmin,xmax);
        c->cd(2);
        draw_zline(frameRatio,xmin,xmax,1.0);
        draw_graph_residual(c,mg,residual,
                            resmcdata,defmcdata,yresmax,restitle,restitlesize,
                            xmin,xmax,ymin,ymax,fullfit,tdr,interpolate);
      }

      c->cd(1);
      for(int i=0;i<mg->GetListOfGraphs()->GetSize(); i++) {
        TGraphErrors* tmp = (TGraphErrors*)mg->GetListOfGraphs()->At(i);
        gPad->Modified(); gPad->Update(); // make sure it's (re)drawn
        TPaveStats *s = ((TPaveStats *)(tmp->FindObject("stats")));
        if (s) { s->SetX1NDC(-1); s->SetX2NDC(-1); } // get out of sight
        gPad->Modified(); gPad->Update(); // make sure it's (re)drawn
      }

      if(override && drawlegend && leg2) {
        leg2->SetLineColor(0);
        leg2->SetFillColor(0);
        leg2->SetBorderSize(0);
        leg2->SetTextSize(0.045);
        leg2->Draw(); 
      }
      leg->SetLineColor(0);
      leg->SetFillColor(0);
      leg->SetBorderSize(0);
      leg->SetTextSize(0.045);
      if (drawlegend) leg->Draw();
      if (drawrange) draw_range(ranges.front(),residual);
      if (tdrautobins) tdrlabels.push_back(ranges.front());
      draw_labels(tdrlabels,leginplot,tdrautobins);
      if (tdrautobins) tdrlabels.pop_back();

      c->Update();
      fixOverlay();
    }
    else {
      c = new TCanvas(mg->GetName(),mg->GetName(),600,600);
      gPad->SetLeftMargin(0.18);
      gPad->SetRightMargin(0.05);
      gPad->SetTopMargin(0.08);
      gPad->SetBottomMargin(0.14);
      gPad->SetLogx(logx);
      gPad->SetLogy(logy);

      mg->Draw("AP");
      set_axis_titles(mg->GetHistogram(),quantity,ymin,ymax,xtitle,ytitle,refpt,tdr);

      if (0!=mg->GetHistogram()) {
        mg->GetHistogram()->GetXaxis()->SetMoreLogLabels(logx);
        mg->GetHistogram()->GetXaxis()->SetNoExponent(logx);
      }

      set_axis_range(mg,xmin,xmax,ymin,ymax);
      draw_extrapolation(mg,fullfit,xmin,xmax);
      draw_graph_residual((TPad*)gPad,mg,residual,
                          resmcdata,defmcdata,yresmax,restitle,restitlesize,
                          xmin,xmax,ymin,ymax,fullfit,tdr,interpolate);

      //leg->SetLineColor(10);
      leg->SetLineColor(0);
      //leg->SetFillColor(10);
      leg->SetFillColor(0);
      leg->SetBorderSize(0);
      if (drawlegend) leg->Draw();
      if (drawrange) draw_range(ranges.front(),residual);
      if (tdrautobins) tdrlabels.push_back(ranges.front());
      draw_labels(tdrlabels,leginplot,tdrautobins);
      if (tdrautobins) tdrlabels.pop_back();
    }
  }
  else {
    c = new TCanvas(mg->GetName(),mg->GetName(),600,600);
    unsigned nx = (unsigned)std::sqrt((float)graphs.size());
    unsigned ny = nx;
    if (nx*ny<graphs.size()) nx++;
    if (nx*ny<graphs.size()) ny++;
    c->Divide(nx,ny);
    for (unsigned i=0;i<graphs.size();i++) {
      c->cd(i+1);
      gPad->SetLeftMargin(0.18);
      gPad->SetRightMargin(0.05);
      gPad->SetTopMargin(0.08);
      gPad->SetBottomMargin(0.14);
      gPad->SetLogx(logx);
      gPad->SetLogy(logy);

      stringstream ssmgindname;
      ssmgindname<<"ind_"<<i<<mg->GetName();
      TMultiGraph* mgind = new TMultiGraph(ssmgindname.str().c_str(),
					   ssmgindname.str().c_str());
      mgind->Add(graphs[i]);
      //graphs[i]->Draw("AP");
      mgind->Draw("AP");
      //set_axis_titles(graphs[i]->GetHistogram(),quantity,ymin,ymax);
      set_axis_titles(mgind->GetHistogram(),quantity,ymin,ymax,xtitle,ytitle,refpt,tdr);

      if (0!=mg->GetHistogram()) {
	mg->GetHistogram()->GetXaxis()->SetMoreLogLabels(logx);
	mg->GetHistogram()->GetXaxis()->SetNoExponent(logx);
      }

      set_axis_range(mgind,xmin,xmax,ymin,ymax);
      draw_extrapolation(mgind,fullfit,xmin,xmax);
      draw_graph_residual((TPad*)gPad,mgind,residual,
			  resmcdata,defmcdata,yresmax,restitle,restitlesize,
                          xmin,xmax,ymin,ymax,fullfit,tdr,interpolate);
      
      if (drawrange) draw_range(ranges[i],residual);
      if (tdrautobins) tdrlabels.push_back(ranges[i]);
      draw_labels(tdrlabels,leginplot,tdrautobins);
      if (tdrautobins) tdrlabels.pop_back();
      set_axis_titles(graphs[i]->GetHistogram(),quantity,ymin,ymax,xtitle,ytitle,refpt,tdr);

      if (algs.size()>1||inputs.size()>1) {
	TLatex tex;
	tex.SetNDC();
	tex.SetTextFont(42);
	tex.SetTextSize(0.05);
	string txt = (algs.size()>1) ?
	  get_legend_label_from_alg(algs[i]) :
	  get_legend_label_from_input(inputs[i]);
	tex.DrawLatex(0.6,0.85,txt.c_str());
      }

    }
  }
  
  string output = c->GetName();
  if (!opath.empty()) output = opath + "/" + output;
  for (unsigned int iformat=0;iformat<formats.size();iformat++)
    c->Print((output+"."+formats[iformat]).c_str());
  
  
  if (!batch) app->Run();
  
  return 0;
}


////////////////////////////////////////////////////////////////////////////////
// implement local functions
////////////////////////////////////////////////////////////////////////////////
//______________________________________________________________________________

void draw_labels(const vector<string>& labels,bool leginplot,bool tdrautobins)
{
  for (unsigned ilabel=0;ilabel<labels.size();ilabel++) {
    string tmp(labels[ilabel]);
    size_t pos;
    if (tdrautobins&&ilabel>0&&(ilabel==labels.size()-1)) tmp=labels[ilabel-1];
    pos = tmp.find(':'); assert(pos!=string::npos);
    string x_as_str = tmp.substr(0,pos); tmp = tmp.substr(pos+1);
    pos = tmp.find(':'); assert(pos!=string::npos);
    string y_as_str = tmp.substr(0,pos); tmp = tmp.substr(pos+1);
    pos = tmp.find(':');
    string font_as_str;
    string size_as_str;
    string text;
    if (pos==string::npos) {
      font_as_str = "42";
      size_as_str = "0.04";
      text = tmp;
    }
    else {
      font_as_str = tmp.substr(0,pos); tmp = tmp.substr(pos+1);
      pos = tmp.find(':');
      if (pos==string::npos) {
	size_as_str = "0.04";
	text = tmp; 
      }
      else {
	size_as_str = tmp.substr(0,pos);
	text = tmp.substr(pos+1);
      }
    }
    
    stringstream ssx; ssx<<x_as_str;    double x; ssx>>x;
    stringstream ssy; ssy<<y_as_str;    double y; ssy>>y;
    stringstream ssf; ssf<<font_as_str; int    f; ssf>>f;
    stringstream sss; sss<<size_as_str; double s; sss>>s;

    if (tdrautobins&&ilabel>0&&(ilabel==labels.size()-1)) { 
      y -= 0.05;
      text = labels[labels.size()-1]; 
    } 
   
    if (!leginplot) { double scale = 800.0*0.93/1000./0.82;  x *= scale; }

    TLatex tex;
    tex.SetTextSize(s);
    tex.SetTextFont(f);
    tex.SetNDC(true);
    tex.DrawLatex(x,y,text.c_str());
  }
}


//______________________________________________________________________________
void draw_extrapolation(TMultiGraph* mg,int fullfit,float xmin,float xmax)
{
  if (fullfit<1||fullfit>3) return;
  TIter next(mg->GetListOfGraphs());
  TGraphErrors* g(0);vector<TGraphErrors*> vg;vector<TF1*>vf;

  while (( g = (TGraphErrors*)next() )) {
    vg.push_back(g);
    vf.push_back((TF1*)g->GetListOfFunctions()->Last());
  }
  assert (vg.size()==vf.size());

  if (0==vf.size()) return;



  for (unsigned i(0);i<vf.size();i++) {

    if (0==vf[i]) continue;

    double ffmin(0.0),ffmax(0.0);
    vf[i]->GetRange(ffmin,ffmax);
    
    if (1==fullfit||2==fullfit)
      ffmin = (xmin!=-1.) ? xmin : mg->GetHistogram()->GetXaxis()->GetXmin(); 
    if (1==fullfit||3==fullfit)
      ffmax = (xmax!=-1.) ? xmax : mg->GetHistogram()->GetXaxis()->GetXmax();

    stringstream ssffname;
    ssffname<<"ff_"<<mg->GetName()<<"_"<<i;
    TF1* ff = (TF1*)vf[i]->Clone(ssffname.str().c_str());
   
    ff->SetRange(ffmin,ffmax);
    ff->SetLineColor(vf[i]->GetLineColor());
    ff->SetLineStyle(kDashed);
    ff->SetLineWidth(1);
    ff->Draw("SAME");
  }
}

//______________________________________________________________________________
TH1F* set_axis_range(TMultiGraph* mg, 
		      float xmin, float xmax,
		      float ymin, float ymax)
{
  if (0==mg) return 0;
  if (0==mg->GetHistogram()) return 0;

  TH1F* holdaxis = mg->GetHistogram(); TH1F* hnewaxis(0);
  if (xmin==-1.&&xmax==-1.&&ymin==-1.&&ymax==-1.) return holdaxis;

  vector<float> borders;
  borders.push_back(holdaxis->GetXaxis()->GetXmin());
  borders.push_back(holdaxis->GetMinimum());
  borders.push_back(holdaxis->GetXaxis()->GetXmax());
  borders.push_back(holdaxis->GetMaximum());

  if (xmin!=-1.0) borders[0]=xmin;
  if (ymin!=-1.0) borders[1]=ymin;
  if (xmax!=-1.0) borders[2]=xmax;
  if (ymax!=-1.0) borders[3]=ymax;

  if (xmin!=-1.0 || xmax!=-1.0 || ymin!=-1.0 || ymax!=-1.0)
    hnewaxis = gPad->DrawFrame(borders[0],borders[1],borders[2],borders[3]);

  // copy settings

  hnewaxis->SetTitle(holdaxis->GetTitle());

  hnewaxis->SetXTitle(holdaxis->GetXaxis()->GetTitle());
  hnewaxis->GetXaxis()->CenterTitle(holdaxis->GetXaxis()->GetCenterTitle());
  hnewaxis->GetXaxis()->SetTitleSize(holdaxis->GetXaxis()->GetTitleSize());
  hnewaxis->GetXaxis()->SetLabelSize(holdaxis->GetXaxis()->GetLabelSize());
  hnewaxis->GetXaxis()->SetTitleOffset(holdaxis->GetXaxis()->GetTitleOffset());
  hnewaxis->GetXaxis()->SetLabelOffset(holdaxis->GetXaxis()->GetLabelOffset());
  hnewaxis->GetXaxis()->SetNdivisions(holdaxis->GetXaxis()->GetNdivisions());
  hnewaxis->GetXaxis()->SetTickLength(holdaxis->GetXaxis()->GetTickLength());  
  hnewaxis->GetXaxis()->SetMoreLogLabels(holdaxis->GetXaxis()->GetMoreLogLabels());
  hnewaxis->GetXaxis()->SetNoExponent(holdaxis->GetXaxis()->GetNoExponent());
  hnewaxis->GetXaxis()->SetLabelSize(holdaxis->GetXaxis()->GetLabelSize());
  hnewaxis->GetXaxis()->SetLabelOffset(holdaxis->GetXaxis()->GetLabelOffset());

  hnewaxis->SetYTitle(holdaxis->GetYaxis()->GetTitle());
  hnewaxis->GetYaxis()->CenterTitle(holdaxis->GetYaxis()->GetCenterTitle());
  hnewaxis->GetYaxis()->SetTitleSize(holdaxis->GetYaxis()->GetTitleSize());
  hnewaxis->GetYaxis()->SetLabelSize(holdaxis->GetYaxis()->GetLabelSize());
  hnewaxis->GetYaxis()->SetTitleOffset(holdaxis->GetYaxis()->GetTitleOffset());
  hnewaxis->GetYaxis()->SetLabelOffset(holdaxis->GetYaxis()->GetLabelOffset());
  hnewaxis->GetYaxis()->SetNdivisions(holdaxis->GetYaxis()->GetNdivisions());
  hnewaxis->GetYaxis()->SetTickLength(holdaxis->GetYaxis()->GetTickLength());  
  hnewaxis->GetYaxis()->SetMoreLogLabels(holdaxis->GetYaxis()->GetMoreLogLabels());
  hnewaxis->GetYaxis()->SetNoExponent(holdaxis->GetYaxis()->GetNoExponent());
  hnewaxis->GetYaxis()->SetLabelSize(holdaxis->GetYaxis()->GetLabelSize());
  hnewaxis->GetYaxis()->SetLabelOffset(holdaxis->GetYaxis()->GetLabelOffset());

  mg->Draw("P");
  return hnewaxis;
}


//______________________________________________________________________________
void draw_graph_residual(TPad* pad,TMultiGraph* mg,
			 const int errMode,
			 const bool resmcdata,const vector<int>& defmcdata,
			 const float yresmax, const string& restitle,
			 const float restitlesize,
			 float xmin,float xmax,float ymin,float ymax,
             int fullfit, bool tdr, bool interpolate)
{
  if (errMode<0) return;
  else if (errMode>5){
    cout<<"ERROR: draw_graph_residual() invalid error mode"<<endl;return;
  }
  if (0==pad) return;

  // make sure nobody uses wrong methods...
  if (errMode==1 || errMode==2){
    cout<<"DAMN: residual "<<errMode<<" not implemented:/"<<endl;return;
  }



  TIter next(mg->GetListOfGraphs());
  TGraphErrors* g(0);vector<TGraphErrors*> vg;vector<TF1*>vf;
  
  while (( g = (TGraphErrors*)next() )) {
    vg.push_back(g);
    vf.push_back((TF1*)g->GetListOfFunctions()->Last());
  }
  assert (vg.size()==vf.size());

  bool nofits = true;
  for (unsigned i=0;i<vf.size()&&nofits;i++) {
    if (0!=vf[i]) nofits = false;
  }
  if(nofits && interpolate) {
     cout<<"draw_graph_residual() did not find ANY fits, but using TSpline3 interpolation instead"<<endl;
  }
  else if (nofits) {
    cout<<"draw_graph_residual() did not find ANY fits..., skipping"<<endl;
    return;
  }

  if (resmcdata) {
    if(!interpolate) {
    if (defmcdata.size()!=2) {
      cout<<"DAMN: resmcdata==1, but defmcdata.size()!=2 -> skipping!"<<endl;return;
    }
    // now this is pretty nasty, but should do the job...

    if (vg.size()<(unsigned)std::max(defmcdata[0],defmcdata[1])) {
      cout<<"DAMN: defmcdata contains graphs which DO NOT EXIST in this multigraph!"<<endl;
      return;
    }

    if (0==vg[defmcdata[0]]) {
      cout<<"DAMN: the MC-graph defined in defmcdata[0] does not have a fit -> skipping!"<<endl;
      return;
    }

    TF1* mcfit(0);

    vf.clear();
    for (unsigned i=0;i<(unsigned)defmcdata[1];i++) vf.push_back(mcfit);
    mcfit = (TF1*)vg[defmcdata[0]]->GetListOfFunctions()->Last();
    vf.push_back(mcfit);

    mcfit = 0;
    for (unsigned i=defmcdata[1]+1;i<vg.size();i++) vf.push_back(mcfit);

    assert(vg.size()==vf.size());
    }
    else {
      if (vg.size()<(unsigned)*std::max_element(defmcdata.begin(),defmcdata.end())) {
        cout<<"DAMN: defmcdata contains graphs which DO NOT EXIST in this multigraph!"<<endl;
        return;
      }
      if (*std::min_element(defmcdata.begin(),defmcdata.end())<-1) {
        cout<<"DAMN: defmcdata contains graphs which DO NOT EXIST in this multigraph or do not indicate data!"<<endl;
        return;
      }
      vf.clear();
      TF1* mcfit(0);
      for (unsigned i=0;i<vg.size();i++) vf.push_back(mcfit);
      assert(vg.size()==vf.size());
    }
  }

  
  stringstream rmgname;
  rmgname<<"rmg_"<<mg->GetName();
  TMultiGraph* rmg = new TMultiGraph(rmgname.str().c_str(),
				     rmgname.str().c_str());

  //vector<TGraphErrors*> vrGraph;

  for (unsigned i(0);i<vg.size();i++){
    if (defmcdata[i] == -1) continue;
    if(!tdr) {
      //divide this pad
      if (0==i) pad->Divide(1,2,0.01,0.0);

      // make default settings
      if (0==i) pad->GetPad( 1 )->SetFillColor( 0 );
      if (0==i) pad->GetPad( 2 )->SetFillColor( 0 );
      if (0==i) pad->GetPad( 1 )->SetPad( 0.0,0.25,1.0, 1.0 );
      if (0==i) pad->GetPad( 2 )->SetPad( 0.0, 0.0,1.0,0.25 );

      if (0==i) pad->cd(1);
      if (0==i && pad->GetLogx()) gPad->SetLogx();
      if (0==i && pad->GetLogy()) gPad->SetLogy();
      if (0==i) gPad->SetTopMargin(0.1);
      if (0==i) gPad->SetLeftMargin(0.15);
      if (0==i) gPad->SetRightMargin(0.05);
    
      if (0==i) pad->cd(2);
      if (0==i && pad->GetLogx())gPad->SetLogx();
      if (0==i) gPad->SetBottomMargin(0.375);
      if (0==i) gPad->SetLeftMargin(0.15);
      if (0==i) gPad->SetRightMargin(0.05);
    }

    // define residual graph
  
    TGraphErrors* rGraph = new TGraphErrors(0);

    // Go through all points now...

    for(int ip(0);ip<vg[i]->GetN();ip++) {

      double y  = vg[i]->GetY()[ip];
      double ey = vg[i]->GetEY()[ip];

      double x  = vg[i]->GetX()[ip];
      double ex = vg[i]->GetEX()[ip];
      
      double ffxmin(0.0),ffxmax(0.0);

      if (0==vf[i] && !interpolate) continue;
      else if(vf[i] && !interpolate) vf[i]->GetRange(ffxmin,ffxmax);
      else {
         ffxmin = vg[i]->GetX()[0];
         ffxmax = vg[i]->GetX()[vg[i]->GetN()-1];
      }
      if (x<ffxmin || x>ffxmax) continue;

      double fy = (0==vf[i]) ? (interpolate) ? vg[defmcdata[i]]->Eval(x,0,"s") :  0.0 : vf[i]->Eval(x);

      double resy(0.0),resey(0.0);

      if (0==y) continue;
  
      if (errMode==3) {
	resy  = (y-fy)/y*100.;
	resey = fy/y/y*ey*100.;
      }
      else if (errMode==0) {
	resy  = (y-fy)/sqrt(y)*100.;
      }
      else if (errMode==4) { 
        resy  = (y-fy)/fy*100.;
        resey = 1.0/fy*ey*100.;
      }
      else if (errMode==5) {
        resy = (y)/(fy);
        resey = 1.0/fy*ey;
      }

      int n = rGraph->GetN();

      rGraph->SetPoint(n,x,resy);
      rGraph->SetPointError(n,ex,resey);
    }

    rGraph->SetTitle("");
    if (errMode==3 || errMode==4 || errMode==5) rGraph->SetMarkerStyle(20); else rGraph->SetMarkerStyle(2);
    if (errMode==3 || errMode==4 || errMode==5) rGraph->SetMarkerSize(.75); else rGraph->SetMarkerSize(1.);
    if (0!=vf[i]) rGraph->SetMarkerColor(vf[i]->GetLineColor());
    if (0!=vf[i]) rGraph->SetLineColor(vf[i]->GetLineColor());
    if (resmcdata)  rGraph->SetMarkerColor(vg[defmcdata[i]]->GetMarkerColor());
    if (resmcdata)  rGraph->SetMarkerStyle(vg[defmcdata[i]]->GetMarkerStyle());
    if (resmcdata)  rGraph->SetLineColor(vg[defmcdata[i]]->GetLineColor());

    rGraph->SetLineWidth(1);
      
    if (rGraph->GetN()!=0) rmg->Add(rGraph);
  }
  
  if(!tdr) {    
    pad->cd(1);
    mg->Draw("AP");

    mg->GetHistogram()->GetYaxis()->SetTitleOffset(1.2);
    if (0!=mg->GetHistogram()) {
      mg->GetHistogram()->GetXaxis()->SetMoreLogLabels(pad->GetLogx());
      mg->GetHistogram()->GetXaxis()->SetNoExponent(pad->GetLogx());
      mg->GetHistogram()->GetXaxis()->SetLabelSize( 0.15 );
      mg->GetHistogram()->GetXaxis()->SetLabelOffset( 0.005 );
    }
    if(!tdr) set_axis_range(mg,xmin,xmax,ymin,ymax);
    draw_extrapolation(mg,fullfit,xmin,xmax);

    xmin = (xmin!=-1.) ? xmin: mg->GetHistogram()->GetXaxis()->GetXmin();
    xmax = (xmax!=-1.) ? xmax: mg->GetHistogram()->GetXaxis()->GetXmax();
  }

  pad->cd(2);
  //  rmg->SaveAs("residual.root");

  if(!tdr) {
    rmg->Draw("AP");

    float rmgymax = std::max(TMath::Abs(rmg->GetHistogram()->GetMinimum()),
       TMath::Abs(rmg->GetHistogram()->GetMaximum()));

    rmgymax = (rmgymax>50.) ? 50. : rmgymax;
    rmgymax = (yresmax>0. ) ? yresmax : (rmgymax*1.15);

    rmg->GetHistogram()->SetMinimum(-1.*rmgymax);
    rmg->GetHistogram()->SetMaximum( 1.*rmgymax);

    rmg->GetHistogram()->SetTitle("");

    rmg->GetHistogram()->GetYaxis()->CenterTitle(1);
    rmg->GetHistogram()->GetYaxis()->SetTitleSize( restitlesize );
    rmg->GetHistogram()->GetYaxis()->SetTitleOffset( 0.6 );
    rmg->GetHistogram()->GetYaxis()->SetLabelSize( 0.13 );
    rmg->GetHistogram()->GetYaxis()->SetNdivisions( 505 );

    rmg->GetHistogram()->SetXTitle(mg->GetHistogram()->GetXaxis()->GetTitle());
    rmg->GetHistogram()->GetXaxis()->SetTitleSize( 0.16 );
    rmg->GetHistogram()->GetXaxis()->SetLabelSize( 0.16 );
    rmg->GetHistogram()->GetXaxis()->SetTitleOffset( 1 );
    rmg->GetHistogram()->GetXaxis()->SetLabelOffset( 0.006 );
    rmg->GetHistogram()->GetXaxis()->SetNdivisions( 505 );
    rmg->GetHistogram()->GetXaxis()->SetTickLength(mg->GetHistogram()->GetXaxis()->GetTickLength()*3.);

    rmg->GetHistogram()->GetXaxis()->SetMoreLogLabels(pad->GetLogx());
    rmg->GetHistogram()->GetXaxis()->SetNoExponent(pad->GetLogx());
    rmg->GetHistogram()->GetXaxis()->SetLabelSize( 0.15 );
    rmg->GetHistogram()->GetXaxis()->SetLabelOffset( 0.005 );

      if (restitle.empty()){
      if (!resmcdata) {
        if ( errMode == 0 )
    rmg->GetHistogram()->SetYTitle( "#frac{(point - fit)}{#sqrt{point}} [%]" );
        else if ( errMode == 1 )
    rmg->GetHistogram()->SetYTitle( "#frac{(point - fit)}{#sqrt{fit}} [%]" );
        else if (errMode == 2)
    rmg->GetHistogram()->SetYTitle( "#frac{(point - fit)}{binerror} [%]" );
        else if (errMode == 4)
    rmg->GetHistogram()->SetYTitle( "#frac{(point-fit)}{fit} [%]" );
        else 
    rmg->GetHistogram()->SetYTitle( "#frac{(point-fit)}{point} [%]" );
      }
      else {
        if ( errMode == 0 )
    rmg->GetHistogram()->SetYTitle( "#frac{(data - MC)}{#sqrt{data}} [%]" );
        else if ( errMode == 1 )
    rmg->GetHistogram()->SetYTitle( "#frac{(data - MC)}{#sqrt{MC}} [%]" );
        else if (errMode == 2)
    rmg->GetHistogram()->SetYTitle( "#frac{(data - MC)}{binerror} [%]" );
        else if (errMode == 4)
    rmg->GetHistogram()->SetYTitle( "#frac{(data-MC)}{MC} [%]" );
        else if (errMode == 5)
    rmg->GetHistogram()->SetYTitle( "#frac{data}{MC}" );
        else 
    rmg->GetHistogram()->SetYTitle( "#frac{(data-MC)}{data} [%]" );
      }
    }
    else rmg->GetHistogram()->SetYTitle( restitle.c_str() );  
  }
  else {
    for(int i=0;i<rmg->GetListOfGraphs()->GetSize(); i++) {
        TGraphErrors* tmp = (TGraphErrors*)rmg->GetListOfGraphs()->At(i);
        tdrDraw(tmp,"P",tmp->GetMarkerStyle(),tmp->GetMarkerColor(),
                tmp->GetLineStyle(),tmp->GetLineColor());
      }
  }

  if(!tdr) set_axis_range(rmg,xmin,xmax);
  draw_zline(rmg->GetHistogram(),xmin,xmax,0);

  pad->cd(1);
}

//______________________________________________________________________________
void draw_zline(TH1* h1,float xmin,float xmax,float y)
{
  if (0==h1) return;
  float min = (xmin!=-1.) ? xmin : h1->GetXaxis()->GetXmin();
  float max = (xmax!=-1.) ? xmax : h1->GetXaxis()->GetXmax();

  TLine* zline = new TLine(min,y,max,y);
  zline->SetLineStyle(kDashed);
  zline->SetLineWidth(1);
  zline->Draw("SAME");
}


//______________________________________________________________________________
void draw_range(const string& range, const int residual)
{
  TLatex tex;
  tex.SetNDC(true);
  tex.SetTextAlign(13);
  tex.SetTextSize(0.055);
  tex.SetTextFont(42);     
  if (residual<0) tex.DrawLatex(0.18,0.98,range.c_str());
  else tex.DrawLatex(0.15,0.96,range.c_str());
}


//______________________________________________________________________________
string get_range(const ObjectLoader<TGraphErrors>& gl,
		 const vector<unsigned int>& indices,
		 bool  addFixedVars, string refpt)
{
  string varnameEta = "#eta";
  for (unsigned int i=0;i<gl.nvariables();i++)
    if (gl.variable(i)=="JetEta"&&gl.minimum(i,0)>=0) varnameEta="|#eta|";
    
  string varnameY = "y";
  for (unsigned int i=0;i<gl.nvariables();i++)
    if (gl.variable(i)=="JetY"&&gl.minimum(i,0)>=0) varnameY="|y|";


  stringstream ssrange;

  for (unsigned int i=0;i<gl.nvariables();i++) {
    
    if (gl.nobjects(i)==1&&!addFixedVars) continue;
    
    string varname = gl.variable(i);
    string unit    = "";
    double varmin  = gl.minimum(i,indices[i]);
    double varmax  = gl.maximum(i,indices[i]);
    bool   threshold(false);

    if (varname=="RefPt")    { varname = refpt.empty() ? "p_{T}^{REF}" : refpt.c_str(); 
                                                        unit = " GeV"; }
    if (varname=="JetPt")    { varname = "p_{T}";       unit = " GeV"; }
    if (varname=="JetEta")   { varname = varnameEta;    unit =     ""; }
    if (varname=="JetY")     { varname = varnameY;      unit =     ""; }
    if (varname=="JetPhi")   { varname = "#varphi";     unit =     ""; }
    if (varname=="PtRel")    { varname = "p_{T}^{rel}"; unit =     ""; }
    if (varname=="RelLepPt") { varname = "p_{T}^{l}/p_{T}^{jet}"; unit =""; }
    if (varname=="ThreshPt") { varname = "p_{T,raw}^{3rd}", unit = " GeV"; 
                               threshold = true; }

    if (threshold) ssrange<<varname<<" < "<<varmax<<unit<<"    ";
    else ssrange<<varmin<<" < "<<varname<<" < "<<varmax<<unit<<"    ";
  }
  
  return ssrange.str();
}


//______________________________________________________________________________
string get_legend_label_from_alg(const string& alg)
{
  string label;
  string tmp(alg);
  if      (alg.find("kt")==0) { label = "k_{T}, R=";      tmp = tmp.substr(2); }
  else if (alg.find("sc")==0) { label = "SISCone, R=";    tmp = tmp.substr(2); }
  else if (alg.find("ic")==0) { label = "ItCone, R=";     tmp = tmp.substr(2); }
  else if (alg.find("mc")==0) { label = "MidCone, R=";    tmp = tmp.substr(2); }
  else if (alg.find("ca")==0) { label = "Cam/Aachen, R="; tmp = tmp.substr(2); }
  else if (alg.find("ak")==0) { label = "Anti k_{T}, R="; tmp = tmp.substr(2); }
  else if (alg.find("gk")==0) { label = "Gen k_{T}, R=";  tmp = tmp.substr(2); }
  else return alg;
  
  string reco[7] = { "gen",  "calo",   "pfchs",    "pf",    "trk",      "jpt",  "puppi"   };
  string RECO[7] = { "(Gen)","(Calo)", "(PF+CHS)", "(PF)", "(Tracks)", "(JPT)", "(Puppi)" };

  size_t pos=string::npos; int ireco=-1;
  while (pos==string::npos&&ireco<7) { pos = tmp.find(reco[++ireco]); }
  if (pos==string::npos) return alg;

  double jet_size; stringstream ss1; ss1<<tmp.substr(0,pos); ss1>>jet_size;
  jet_size/=10.0;  stringstream ss2; ss2<<jet_size;
  
  label += ss2.str() + " " + RECO[ireco];
  
  return label;
}


//______________________________________________________________________________
string get_legend_label_from_input(const string& input)
{
  string label;
  string tmp(input);
  size_t pos=tmp.find(':');
  if (pos!=string::npos) {
    label = tmp.substr(pos+1);
  }
  else {
    pos=tmp.find_last_of('/');
    if (pos!=string::npos) tmp=tmp.substr(pos+1);
    pos=tmp.find(".root");
    if (pos!=string::npos) tmp=tmp.substr(0,pos);
    pos=tmp.find('_');
    label=tmp.substr(0,pos);
  }
  return label;
}


//______________________________________________________________________________
void set_graph_style(TGraphErrors* g, unsigned int ngraph,bool nocolor,
		     const vector<unsigned int>& vcolors,
		     const vector<unsigned int>& vmarkers,
		     const vector<unsigned int>& vlstyles,
		     const vector<float>&        vsizes,
		     const vector<float>&        vlsizes)
{
  Color_t colors[10] = {
    kBlue+1,kRed+1,kGreen+2,kMagenta+2,kCyan+3,
    kViolet+4,kOrange+1,kGreen-1,kMagenta-4,kCyan-2
  };
  Style_t lines[10]   = {
    1,1,1,1,1,1,1,1,1,1
  };
  Style_t markers[10] =
    { kOpenCircle,kOpenSquare,kOpenTriangleUp,kOpenDiamond,kOpenCross,
      kOpenStar,kFullCircle,kFullSquare,kFullTriangleUp,kFullTriangleDown
    };
  
  if (nocolor) {
    markers[0]=kFullCircle;       markers[1]=kOpenCircle;
    markers[2]=kFullSquare;       markers[3]=kOpenSquare;
    markers[4]=kFullTriangleUp;   markers[5]=kOpenTriangleUp;
    markers[6]=kFullStar;         markers[7]=kOpenStar;
    markers[8]=kFullTriangleDown; markers[9]=kOpenCross;
  }
  
  Color_t color = colors[std::min(ngraph,(unsigned)9)];
  Style_t line  = lines[std::min(ngraph,(unsigned)9)];
  Style_t marker = markers[std::min(ngraph,(unsigned)9)];
  Float_t msize (0.8);

  if (ngraph<vcolors.size())  color   = vcolors[ngraph];
  //if (ngraph<vmarkers.size()) markers = vmarkers[ngraph];
  if (ngraph<vsizes.size())   msize   = vsizes[ngraph];

  if (nocolor) color = kBlack;
  
  g->SetLineColor(color);
  g->SetMarkerColor(color);
  g->SetMarkerStyle(marker);
  if (ngraph<vmarkers.size()) g->SetMarkerStyle(vmarkers[ngraph]);
  g->SetMarkerSize(msize);
  
  TF1* f(0);
  if (g->GetListOfFunctions()->GetEntries()>0) {
    for(int i=0; i<g->GetListOfFunctions()->GetEntries(); i++) {
      //f=(TF1*)(g->GetListOfFunctions()->At(0));
      f=(TF1*)(g->GetListOfFunctions()->At(i));
      f->SetLineColor(color);
      f->SetLineStyle(line);
      if (ngraph<vlstyles.size()) f->SetLineStyle(vlstyles[ngraph]);
      f->SetLineWidth(1);
      if (ngraph<vlsizes.size()) f->SetLineWidth((Width_t)vlsizes[ngraph]);
    }
  }
  
  return;
}


//______________________________________________________________________________
void set_axis_titles(TH1* h,const string& quantity,float ymin,float ymax,
		     string xtitle,string ytitle,string refpt,bool tdr)
{
  if (0==h) {
    cout<<"set_axis_title ERROR: h is NULL!"<<endl;
    return;
  }
  h->SetTitle("");
  
  ymin = (ymin<0.0) ? 0.0 : ymin;
  h->SetMinimum(ymin);
  
  //string xtitle("");
  //string ytitle("");
  size_t pos = quantity.find("Vs");
  if (pos!=string::npos) {

    if (ytitle.empty()) {
      string ystr=quantity.substr(0,pos);
      if (ystr=="Rsp"||ystr=="RelRsp"||ystr=="AbsRsp") {
	ytitle=refpt.empty() ? "p_{T} / p_{T}^{REF}" : ("p_{T} / "+refpt).c_str();
	ymax = (ymax<0.0) ? 1.2 : ymax;
	h->SetMaximum(ymax);
      }
      else if (ystr=="Res"||ystr=="RelRes"||ystr=="AbsRes") {
	ytitle= refpt.empty() ? "#sigma(p_{T}/p_{T}^{REF}) / <p_{T}/p_{T}^{REF}>" :
	  ("#sigma(p_{T}/"+refpt+") / <p_{T}/"+refpt+">").c_str();
	if (ymax>0.0) h->SetMaximum(ymax);
      }
      else if (ystr=="Asym") {
	ytitle="#sqrt{2}#sigma_{A}";
	ymax = (ymax<0.0) ? 1.3*h->GetMaximum() : ymax;
	h->SetMaximum(ymax);
      }
      else if (ystr=="AbsSlb") {
	ytitle="p^{(e/#mu)}_{T,jet}/p^{(e/#mu+#nu)}_{T,jet}";
	ymax = (ymax<0.0) ? 1.2 : ymax;
	h->SetMaximum(ymax);
      }
      else if (ystr=="Aone") {
	ytitle="a_{1}";
      }
      else if (ystr=="Atwo") {
	ytitle="a_{2}";
      }
      else if (ystr=="Pone") {
	ytitle="p_{1}";
      }
      else if (ystr=="Ptwo") {
	ytitle="p_{2}";
      }
    }

    if (xtitle.empty()) {
      string xstr=quantity.substr(pos+2);    
      if (xstr=="RefPt")    xtitle=refpt.empty() ? "p_{T}^{REF} [GeV]" : (refpt+" [GeV]").c_str();
      if (xstr=="JetPt")    xtitle="p_{T} [GeV]";
      if (xstr=="JetEta")   xtitle="#eta";
      if (xstr=="JetPhi")   xtitle="#varphi";
      if (xstr=="JetY")     xtitle="y";
      if (xstr=="PtRel")    xtitle="p_{T}^{rel} [GeV]";
      if (xstr=="RelLepPt") xtitle="p_{T}^{(e/#mu)} / p_{T,jet}^{(e/#mu)}";
      if (xstr=="ThreshPt") xtitle="p_{T,max}^{3^{rd}}";
    }
  }
  
  h->SetXTitle(xtitle.c_str());
  h->SetYTitle(ytitle.c_str());
  if(!tdr) {
    h->GetXaxis()->SetTitleOffset(1.1);
    h->GetYaxis()->SetTitleOffset(1.4);
    h->GetYaxis()->CenterTitle();
  }
  h->GetYaxis()->SetNdivisions(505);
  return;
}
