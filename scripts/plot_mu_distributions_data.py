import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob


def main():
    usage = 'Example: python3 plot_mu_distributions_data.py'
        
    c = rt.TCanvas('c','',800,700)
    c.SetTickx(1)
    c.SetTicky(1)
    c.SetLogy(0)
    c.SetLogx(0)
    c.SetRightMargin(0.03)
    c.SetLeftMargin(0.12)
    c.SetBottomMargin(0.12)

    frame = c.DrawFrame(0,0,100,0.109)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleOffset(0.90)
    frame.GetXaxis().SetTitle('Number of pileup interactions per crossing (#mu)')
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleOffset(1.1)
    frame.GetYaxis().SetTitle('Normalized to unity')

    cms = rt.TPaveText(0.195,0.918,0.495,0.938,'NDC')
    cms.AddText('#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}')
    cms.SetTextFont(42)
    cms.SetTextSize(0.06)
    cms.SetBorderSize(0)
    cms.SetFillColor(0)
    cms.Draw()

    lumi = rt.TPaveText(0.78,0.918,0.98,0.938,'NDC')
    lumi.SetFillColor(0)
    lumi.SetBorderSize(0)
    lumi.AddText('(13.6 TeV)')
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.05)
    lumi.Draw()
    
    legend = rt.TLegend(0.15,0.60,0.85,0.86, '')
    legend.SetTextSize(0.03)
    legend.SetBorderSize(0)
    legend.SetNColumns(2)
                
    
    eras = ['2022CD', '2022EFG', '2023C', '2023D', '2024CDEFGHI']
    colors = [rt.kBlue-4, rt.kRed-4, rt.kGreen-2, rt.kViolet, rt.kOrange+1]    
    
    for era, color in zip(eras, colors):
    
         minbiasxsec = '75300' if era == '2024CDEFGHI' else '69200'
         file_name = '../Histos_PU/MyDataPUHisto_' + era + '_120Bins_' + minbiasxsec + '.root'
         root_file = rt.TFile(file_name, 'READ')
         
         hist = root_file.Get('pileup')
         
         hist.SetDirectory(0)
         hist.SetFillColorAlpha(color, 0.5)
         hist.SetFillStyle(1001)
         hist.SetLineColor(rt.kBlack)
         hist.SetLineWidth(2)
         hist.SetStats(0)
         hist.SetTitle('')
         hist.Scale(1./hist.Integral())
         
         hist.Draw('HIST SAME')
         
         minbiasxsec_leg = '75.3' if era == '2024CDEFGHI' else '69.2'
         legend.AddEntry(hist, era + ' (#sigma_{MB} = ' + minbiasxsec_leg + ' mb)', 'F')
  
    
    legend.Draw()
    
    output_png = f"../Histos_PU/PUProfiles_{'_'.join(eras)}.png"
    output_pdf = output_png.replace(".png", ".pdf")

    c.SaveAs(output_png)
    c.SaveAs(output_pdf)


if __name__ == '__main__':
    main()
