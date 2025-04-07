import glob, os, ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
from array import array
import numpy as np
from tdrstyle_JERC import *
import tdrstyle_JERC as TDR
TDR.extraText  = 'Simulation'
TDR.extraText2  = 'Preliminary'

class L1OffsetVsPt():
    def __init__(self, radius, algo, prefix):
        self.doCleaning = True
        self.radius = radius
        self.algo = algo
        self.inputPath = 'Inputs/'
        self.outputPath = 'Pdfs/'
        os.system('mkdir -p '+self.outputPath)
        self.filename = 'Offset'+prefix+'L1SemiSimpleSmallerRangesVsPt_AK'+self.radius+self.algo+'_default'
        self.years = ['Summer22EE_V2']
        self.etabins = ['BB', 'EI', '1EO', '2EO','FF']
        self.mubins = ['0','0to20', '20to40', '40to60', '60to80', '80to100']
        self.Hists = {
            '0': {'legend': '#mu #approx 0',
                  'color':  ROOT.kBlack,
                  'marker': ROOT.kFullSquare,
                  'msize':  1.0,
                  'hname':  'histograms/OffMeantnpuRef_default_Mu0',
                  },
            '0to20': {'legend': '0 #leq #mu < 20',
                  'color':  ROOT.kRed+1,
                  'marker': ROOT.kFullSquare,
                  'msize':  1.0,
                  'hname':  'histograms/OffMeantnpuRef_default_0',
                  },
            '20to40': {'legend': '20 #leq #mu < 40',
                   'color':  ROOT.kBlue-4,
                   'marker': ROOT.kFullSquare,
                   'msize':  1.0,
                   'hname':  'histograms/OffMeantnpuRef_default_1',
                   },
            '40to60': {'legend': '40 #leq #mu < 60',
                   'color':  ROOT.kGreen-3,
                   'marker': ROOT.kFullSquare,
                   'msize':  1.0,
                   'hname':  'histograms/OffMeantnpuRef_default_2',
                   },
            '60to80': {'legend': '60 #leq #mu < 80',
                   'color':  ROOT.kOrange+1,
                   'marker': ROOT.kFullSquare,
                   'msize':  1.0,
                   'hname':  'histograms/OffMeantnpuRef_default_3',
                   },
            '80to100': {'legend': '80 #leq #mu < 100',
                   'color':  ROOT.kViolet,
                   'marker': ROOT.kFullSquare,
                   'msize':  1.0,
                   'hname':  'histograms/OffMeantnpuRef_default_4',
                   },       

            }
    def Plot(self):
        PlotXMin = 8
        PlotXMax = 5500
        for year in self.years:
            f_ = ROOT.TFile(os.path.join(self.inputPath,self.filename+'.root').replace('default',year).replace('Summer20UL16nonAPV','Summer20UL16'))
            for eta in self.etabins:
                TDR.cms_lumi = TDR.commonScheme['legend'][year]
                TDR.extraText3 = []
                TDR.extraText3.append('AK'+self.radius+' '+self.algo.replace('CHS','PF+CHS'))
                if eta=='BB':   TDR.extraText3.append('0.0 < |#eta| < 1.3')
                elif eta=='EI': TDR.extraText3.append('1.3 < |#eta| < 2.4')
                elif eta=='1EO': TDR.extraText3.append('2.4 < |#eta| < 2.7')
                elif eta=='2EO': TDR.extraText3.append('2.7 < |#eta| < 3.0')
                elif eta=='FF': TDR.extraText3.append('3.0 < |#eta| < 5.0')
                

                PlotYMin = -5
                if eta=='BB':   PlotYMax =  60 if self.radius=='4' else 100
                elif eta=='EI': PlotYMax =  60 if self.radius=='4' else 100
                elif eta=='1EO': PlotYMax = 130 if self.radius=='4' else 100
                elif eta=='2EO': PlotYMax = 130 if self.radius=='4' else 100
                elif eta=='FF': PlotYMax = 130 if self.radius=='4' else 100
                if 'After' in self.filename:
                    PlotYMin = -9.9
                    PlotYMax = 20
                    if eta=='2EO' : PlotYMax = 40
                if 'Before' in self.filename:
                    PlotYMin = -14.9
                    PlotYMax = 50
                    #if eta=='EO': PlotYMax = 160
                if 'Without' in self.filename:
                    PlotYMin = -9.9
                    PlotYMax = 20
                    if eta=='2EO' : PlotYMax = 40
                canv = tdrCanvas('L1OffsetVsPt', PlotXMin, PlotXMax, PlotYMin, PlotYMax, 'p_{T}^{ptcl}[GeV]', 'Average Offset [GeV]', square=kSquare, isExtraSpace=True)
                canv.SetLogx(True)
                GettdrCanvasHist(canv).GetXaxis().SetNoExponent(True)
                leg = tdrLeg(0.60,0.62,0.89,0.91, textSize=0.04)

                legPuppiVersion = tdrLeg(0.6,0.11,0.89,0.31, textSize=0.05)
                #legPuppiVersion.SetHeader('Default v15 tune')
                #legPuppiVersion.SetHeader('L1OffsetV1 tune')

                latex = rt.TLatex()
                latex.SetTextFont(42)
                latex.SetTextSize(0.05)
                latex.SetTextAlign(23)
                # for xbin in [30,100,300,1000, 3000]:
                for xbin in [30,300,3000]:
                    latex.DrawLatex(xbin, PlotYMin-0.018*(PlotYMax-PlotYMin),str(xbin))

                lines = {}
                #self.shifts = [0.00, -2, 2]  if ('After' in self.filename) else [0.00]
                self.shifts = [0.00]
                for shift in self.shifts:
                    lines[shift] = ROOT.TLine(PlotXMin, shift, PlotXMax, shift)
                    lines[shift].SetLineWidth(1)
                    lines[shift].SetLineStyle(ROOT.kDotted if shift != 0 else ROOT.kDashed)
                    lines[shift].SetLineColor(ROOT.kBlack)
                    lines[shift].Draw('same')

                verline = rt.TLine(30,PlotYMin,30,PlotYMax*0.5)
                verline.SetLineWidth(2)
                verline.SetLineStyle(ROOT.kDashed)
                verline.SetLineColor(ROOT.kBlack)
                #verline.Draw('same')

                for bin in self.mubins:
                    if bin=='80to100': continue
                    color  = self.Hists[bin]['color']
                    marker = self.Hists[bin]['marker']
                    self.Hists[bin]['hist'] = f_.Get(self.Hists[bin]['hname'].replace('default',eta))
                    self.Hists[bin]['hist'].SetDirectory(0)
                    self.Hists[bin]['hist'].SetMarkerSize(self.Hists[bin]['msize'])
                    #self.Hists[bin]['hist'].Scale(100)
                    if self.doCleaning:
                        # print ('FIXME: Is cleaning really needed?')
                        for x in range(1,self.Hists[bin]['hist'].GetNbinsX()+1):
                            bin_center = self.Hists[bin]['hist'].GetBinCenter(x)
                            bin_width = self.Hists[bin]['hist'].GetBinWidth(x)
                            if(self.Hists[bin]['hist'].GetBinError(x)>2): self.Hists[bin]['hist'].SetBinContent(x,-999)
                            if (bin_center-bin_width/2)<10: self.Hists[bin]['hist'].SetBinContent(x,-999)
                            if self.radius=='8':
                                if bin_center<10: self.Hists[bin]['hist'].SetBinContent(x,-999)
                    tdrDraw(self.Hists[bin]['hist'], 'P', marker=marker, mcolor=color )
                    leg.AddEntry(self.Hists[bin]['hist'], self.Hists[bin]['legend'], 'lp')

                #canv.SaveAs(os.path.join(self.outputPath, self.filename.replace('default', year+'_'+eta)+'.png'))
                canv.SaveAs(os.path.join(self.outputPath, self.filename.replace('default', year+'_'+eta)+'.pdf'))
                canv.Close()
            f_.Close()

def main():
    prefixes =['After']
    #prefixes =['Without']    
    #radii = ['4', '8']
    radii = ['4']
    #algos = ['CHS', 'PUPPI']
    algos = ['PUPPI']
    for radius in radii:
        for algo in algos:
            if '8' in radius and 'CHS' in algo: continue
            for prefix in prefixes:
                L1OffsetVsPt(radius=radius, algo=algo, prefix=prefix).Plot()

if __name__ == '__main__':
    main()
