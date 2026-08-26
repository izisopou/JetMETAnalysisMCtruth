import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob


def main():
    usage = 'Example: python3 plot_jet_veto_maps.py --era 2023D'

    parser = ArgumentParser(description='Script that plots the jet veto map',epilog=usage)
    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")         

    args = parser.parse_args()
        
    c = rt.TCanvas('c','',800,800)
    c.SetTickx(1)
    c.SetTicky(1)
    c.SetRightMargin(0.04)
    c.SetLeftMargin(0.12)
    c.SetTopMargin(0.09)
    c.SetBottomMargin(0.12)

    frame = c.DrawFrame(-5.19,-3.15,5.19,3.15)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleOffset(0.9)
    frame.GetXaxis().SetTitle('#eta_{jet}')
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleOffset(1.1)
    frame.GetYaxis().SetTitle('#phi_{jet}')

    cms = rt.TPaveText(0.20,0.93,0.35,0.95,'NDC')
    cms.AddText('#bf{CMS} #scale[0.7]{#it{Preliminary}}')
    cms.SetTextFont(42)
    cms.SetTextSize(0.055)
    cms.SetBorderSize(0)
    cms.SetFillColor(0)
    cms.Draw()

    lumi = rt.TPaveText(0.80,0.915,0.965,0.935,'NDC')
    lumi.SetFillColor(0)
    lumi.SetBorderSize(0)
    lumi.AddText(args.era + ' (13.6 TeV)')
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.045)
    lumi.SetTextAlign(31)
    lumi.Draw()
    
    xminleg = 0.70 if args.era == '2024' else 0.16
    xmaxleg = 0.90 if args.era == '2024' else 0.36
    yminleg = 0.50 if args.era == '2024' else 0.78
    ymaxleg = 0.66 if args.era == '2024' else 0.88
    
    legend = rt.TLegend(xminleg, yminleg, xmaxleg, ymaxleg, '');
    legend.SetTextSize(0.03);
    legend.SetBorderSize(0);
            
    filename = '../Histos_JetVetoMaps/JetVetoMaps_' + args.era + '.root'
    
    root_file = rt.TFile(filename, 'READ')
    
    for key in root_file.GetListOfKeys():
        obj_name = key.GetName()

        if not any(x in obj_name for x in ['hot', 'cold', 'eep', 'bpix', 'fpix']):
            continue
        
        if 'hotandcold' in obj_name:
            continue    
            
        print('Obj. = ' + obj_name)    
        hist = root_file.Get(obj_name)    
        
        for i in range(1, hist.GetNbinsX() + 1):
            for j in range(1, hist.GetNbinsY() + 1):
                cont = hist.GetBinContent(i, j)
                if(cont < 0):
                    hist.SetBinContent(i, j, -1.*cont)

        hist.SetDirectory(0)
        hist.SetStats(0)
        hist.SetTitle('')
        hist.SetFillStyle(1001)
        hist.SetLineWidth(2)
        hist.SetLineColor(rt.kBlack)
        
        color = rt.kBlack
        legentry = ''
        
        if 'hot' in obj_name:
            color = rt.kRed
            legentry = 'Hot towers'
        elif 'cold' in obj_name:
            color = rt.kBlue
            legentry = 'Dead channels'
        elif 'eep' in obj_name:
            color = rt.kOrange+1
            legentry = 'EE+ region'
        elif 'bpix' in obj_name:
            color = rt.kOrange+1  
            legentry = 'BPix region'          
        elif 'fpix' in obj_name:
            color = rt.kOrange-2
            legentry = 'FPix region'
            
        hist.SetFillColor(color)
        
        hist.Draw('BOX SAME')   
        
        legend.AddEntry(hist, legentry, 'F')


    legend.Draw()
    
    output_png = '../Histos_JetVetoMaps/JetVetoMaps_' + args.era + '.png'
    output_pdf = output_png.replace(".png", ".pdf")

    c.SaveAs(output_png)
    c.SaveAs(output_pdf)


if __name__ == '__main__':
    main()
