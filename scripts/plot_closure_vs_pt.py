import glob, os, ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
from array import array
import numpy as np
from tdrstyle_JERC import *
import tdrstyle_JERC as TDR
TDR.extraText  = 'Simulation'
TDR.extraText2 = 'Preliminary'

class L1L2L3ClosureVsPt():
    def __init__(self, radius, algo, year):
        self.doCleaning = True
        self.radius = radius
        self.algo = algo
        self.year = year
        self.inputPath = 'Inputs/'
        self.outputPath = 'Pdfs/'
        os.system('mkdir -p '+self.outputPath)
        self.histfolder = 'ak'+self.radius+'pf'+self.algo.lower()
        if 'puppi' in self.algo.lower(): self.histfolder = self.histfolder.replace('pfpuppi','puppi')
        self.filename = 'L1L2L3ClosureVsPt_AK'+self.radius+self.algo+'_default'
        self.etabins = ['1.3','2.4','2.7','3.0','5.0']
        #self.etabins = ['3.0', '5.0']
        self.Hists = {
            '1.3': {'legend': '0.0 < |#eta| < 1.3',
                    'color':  ROOT.kGreen+3,
                    'marker': ROOT.kFullCircle,
                    'msize':  1.0,
                    'hname':  self.histfolder+'/ClosureVsRefPt_JetEta0to1.3',
                  },
            '2.4': {'legend': '1.3 < |#eta| < 2.4',
                    'color':  ROOT.kBlue-4,
                    'marker': ROOT.kFullStar,
                    'msize':  1.3,
                    'hname':  self.histfolder+'/ClosureVsRefPt_JetEta1.3to2.4',
            },
            '2.7': {'legend': '2.4 < |#eta| < 2.7',
                    'color':  ROOT.kViolet,
                    'marker': ROOT.kFullSquare,
                    'msize':  0.8,
                    'hname':  self.histfolder+'/ClosureVsRefPt_JetEta2.4to2.7',
            },
            '3.0': {'legend': '2.7 < |#eta| < 3.0',
                    'color':  ROOT.kRed+1,
                    'marker': ROOT.kFullTriangleUp,
                    'msize':  1.0,
                    'hname':  self.histfolder+'/ClosureVsRefPt_JetEta2.7to3',
            },
            '5.0': {'legend': '3.0 < |#eta| < 5.0',
                    'color':  ROOT.kOrange+1,
                    'marker': ROOT.kFullTriangleDown,
                    'msize':  1.0,
                    'hname':  self.histfolder+'/ClosureVsRefPt_JetEta3to5',
            },
        }


    def Plot(self):
        PlotXMin = 8
        PlotXMax = 5500
        PlotYMin = 0.92
        PlotYMax = 1.08
        TDR.cms_lumi = TDR.commonScheme['legend'][self.year]
        if 'UL' in self.year:
            TDR.cms_lumi +=' Legacy'
        TDR.extraText3 = []
        TDR.extraText3.append('AK'+self.radius+' '+self.algo.replace('CHS','PF+CHS'))
        canv = tdrCanvas('L1L2L3ClosureVsPt'+self.year, PlotXMin, PlotXMax, PlotYMin, PlotYMax, 'p_{T}^{ptcl}[GeV]', 'Median response', square=kSquare, isExtraSpace=True)
        canv.SetLogx(True)
        GettdrCanvasHist(canv).GetXaxis().SetNoExponent(True)
        leg = tdrLeg(0.60,0.70,0.89,0.89, textSize=0.04)

        latex = rt.TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.05)
        latex.SetTextAlign(23)
        # for xbin in [30,100,300,1000, 3000]:
        for xbin in [30,300, 3000]:
            latex.DrawLatex(xbin, PlotYMin-0.018*(PlotYMax-PlotYMin),str(xbin))

        lines = {}
        f_ = ROOT.TFile(os.path.join(self.inputPath,self.filename+'.root').replace('default',self.year).replace('Summer20UL16nonAPV','Summer20UL16'))
        for shift in [+0.01, 0.00, -0.01, +0.001, -0.001]:
        #for shift in [0.00]:        
            lines[shift] = ROOT.TLine(PlotXMin, 1+shift, PlotXMax, 1+shift)
            lines[shift].SetLineWidth(1)
            lines[shift].SetLineStyle(ROOT.kDotted if shift != 0 else ROOT.kDashed)
            lines[shift].SetLineColor(ROOT.kBlack)
            lines[shift].Draw('same')

        verline = rt.TLine(30,0.92,30,1.035)
        verline.SetLineWidth(2)
        verline.SetLineStyle(ROOT.kDashed)
        verline.SetLineColor(ROOT.kBlack)
        #verline.Draw('same')

        for bin in self.etabins:
            color  = self.Hists[bin]['color']
            marker = self.Hists[bin]['marker']
            self.Hists[bin]['hist'] = f_.Get(self.Hists[bin]['hname'])
            self.Hists[bin]['hist'].SetDirectory(0)
            self.Hists[bin]['hist'].SetMarkerSize(self.Hists[bin]['msize'])
            if self.doCleaning:
                #Need to remove point outside provided phase-space
                for x in range(1,self.Hists[bin]['hist'].GetNbinsX()+1):
                    bin_center = self.Hists[bin]['hist'].GetBinCenter(x)
                    bin_width = self.Hists[bin]['hist'].GetBinWidth(x)
                    bin_content = self.Hists[bin]['hist'].GetBinContent(x)
                    bin_error = self.Hists[bin]['hist'].GetBinError(x)
                    if bin_content==0: continue
                    if bin_error>0.025: self.Hists[bin]['hist'].SetBinContent(x,0)
                    #if bin_error>0.005 or bin_error/bin_content>0.002: self.Hists[bin]['hist'].SetBinContent(x,0)
                    if (bin_center-bin_width/2)<10: self.Hists[bin]['hist'].SetBinContent(x,0)
                    #if bin == "5.0" and bin_center>600: self.Hists[bin]['hist'].SetBinContent(x,0)
                    #if self.radius=='8':
                     #   if (bin_center-bin_width/2)<30: self.Hists[bin]['hist'].SetBinContent(x,0)
            tdrDraw(self.Hists[bin]['hist'], 'P', marker=marker, mcolor=color )
            leg.AddEntry(self.Hists[bin]['hist'], self.Hists[bin]['legend'], 'lp')

        tdrDraw(self.Hists['2.4']['hist'], 'P', marker=self.Hists['2.4']['marker'], mcolor=self.Hists['2.4']['color'] )

        canv.SaveAs(os.path.join(self.outputPath, self.filename.replace('default', self.year)+'.pdf'))
        canv.Close()
        f_.Close()

def main():
    #radii = ['4', '8']
    radii = ['4']
    #algos = ['CHS', 'PUPPI']
    algos = ['PUPPI']
    years = ['RunIII2024Summer24_V1_WithBPixAndFPixVetoMaps']
    for radius in radii:
        for algo in algos:
            for year in years:
                L1L2L3ClosureVsPt(radius=radius, algo=algo, year=year).Plot()

if __name__ == '__main__':
    main()
