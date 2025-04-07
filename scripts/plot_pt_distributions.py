import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob


def main():
    usage = 'Example: python3 plot_pt_distributions.py'
        
    c = rt.TCanvas('c','',800,700)
    c.SetTickx(1)
    c.SetTicky(1)
    c.SetLogy(1)
    c.SetLogx(1)
    c.SetRightMargin(0.03)
    c.SetLeftMargin(0.12)
    c.SetBottomMargin(0.12)

    frame = c.DrawFrame(3,0.000000005,6800,1)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleOffset(0.90)
    frame.GetXaxis().SetTitle('p_{T}^{ptcl} [GeV]')
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleOffset(1.1)
    frame.GetYaxis().SetTitle('Normalized number of jets to unity')

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
    
    pave = rt.TPaveText(0.185,0.45,0.385,0.55,'NDC')
    pave.AddText("No weights applied")
    pave.AddText("3 leading gen jets considered")
    pave.SetTextFont(42)
    pave.SetTextSize(0.04)
    pave.SetBorderSize(0)
    pave.SetFillColor(0)
    pave.SetTextAlign(11)
    pave.Draw()
    
    legend = rt.TLegend(0.15,0.15,0.55,0.45, '')
    legend.SetTextSize(0.04)
    legend.SetBorderSize(0)
                
    
    eras = ['Run3Summer22', 'Run3Summer22EE', 'Run3Summer23', 'Run3Summer23BPix', 'RunIII2024Summer24']
    colors = [rt.kBlue-4, rt.kRed-4, rt.kGreen-2, rt.kViolet, rt.kOrange+1]  
    markers = [rt.kOpenCircle, rt.kOpenSquare, rt.kOpenTriangleUp, rt.kOpenTriangleDown, rt.kOpenCross]  
    
    for era, color, marker in zip(eras, colors, markers):
         
         file_name = '../Histos_Pt/GenPT_' + era + '_PremixedPU.root'
         root_file = rt.TFile(file_name, 'READ')
         
         hist = root_file.Get('gen_pt_3leading')
         
         hist.SetDirectory(0)
         hist.SetMarkerColor(color)
         hist.SetMarkerStyle(marker)
         hist.SetMarkerSize(1.5 if marker == rt.kOpenCross else 1.2)
         hist.SetLineColor(color)
         hist.SetLineWidth(2)
         hist.SetStats(0)
         hist.SetTitle('')
         hist.Scale(1./hist.Integral())
         
         hist.Draw('PE SAME')
         
         legend.AddEntry(hist, era.replace('RunIII2024', '') + ' (Flat2022)' if era == 'RunIII2024Summer24' else era.replace('Run3', '') + ' (Flat)', 'PE')
  
    
    legend.Draw()
    
    suffixes = [era.replace('Run3', '').replace('RunIII2024', '') for era in eras]

    output_png = f"../Histos_Pt/GenPT_{'_'.join(suffixes)}.png"
    output_pdf = output_png.replace(".png", ".pdf")

    c.SaveAs(output_png)
    c.SaveAs(output_pdf)


if __name__ == '__main__':
    main()
