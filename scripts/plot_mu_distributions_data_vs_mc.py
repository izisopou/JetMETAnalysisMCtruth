import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser
import glob


def main():
    usage = 'Example: python3 plot_mu_distributions_data_vs_mc.py --data 2024CDEFGHI --mc RunIII2024Summer24' 

    parser = ArgumentParser(description='Script that plots the mu distribution of the MC before and after PU reweighting, along with the distribution in data.',epilog=usage)

    parser.add_argument("-data", "--data", dest="data", type=str, required=True,
                    help="Specify era in data", metavar="DATA")
    
    parser.add_argument("-mc", "--mc", dest="mc", type=str, required=True,
                    help="Specify era in MC", metavar="MC")
                    
    args = parser.parse_args()                
        
    c = rt.TCanvas('c','',800,700)
    c.SetTickx(1)
    c.SetTicky(1)
    c.SetLogy(1)
    c.SetLogx(0)
    c.SetRightMargin(0.03)
    c.SetLeftMargin(0.12)
    c.SetBottomMargin(0.12)

    frame = c.DrawFrame(0,5e-04,100,1)
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
                
    minbiasxsec = '75300' if args.data == '2024CDEFGHI' else '69200'
    file_name_data = '../Histos_PU/MyDataPUHisto_' + args.data + '_120Bins_' + minbiasxsec + '.root'
    root_file_data = rt.TFile(file_name_data, 'READ')
    
    file_name_mc_before = '../Histos_PU/MyMCPUHisto_' + args.mc + '_PremixedPU.root'
    root_file_mc_before = rt.TFile(file_name_mc_before, 'READ')
    
    file_name_mc_after = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/' + args.mc +  '/V0_withBPixFPixVetoMaps/Step4_AK4PUPPI_NoCorrectionsApplied/Merged.root'
    root_file_mc_after = rt.TFile(file_name_mc_after, 'READ')
    
    hist_data = root_file_data.Get('pileup')
    hist_mc_before = root_file_mc_before.Get('pileup')
    hist_mc_after = root_file_mc_after.Get('ak4puppi/mu_weighted')
    
    hist_data.SetDirectory(0)
    hist_data.SetLineColor(rt.kBlack)
    hist_data.SetLineWidth(2)
    hist_data.SetMarkerColor(rt.kBlack)
    hist_data.SetMarkerStyle(rt.kFullDotLarge)
    hist_data.SetMarkerSize(0.8)
    hist_data.SetStats(0)
    hist_data.SetTitle('')
    hist_data.Scale(1./hist_data.Integral())         
    
    hist_mc_before.SetDirectory(0)
    hist_mc_before.SetFillColorAlpha(rt.kRed-4, 0.5)
    hist_mc_before.SetFillStyle(1001)
    hist_mc_before.SetLineColor(rt.kRed-4)
    hist_mc_before.SetLineWidth(2)
    hist_mc_before.SetStats(0)
    hist_mc_before.SetTitle('')
    hist_mc_before.Scale(1./hist_mc_before.Integral())
    
    hist_mc_after.SetDirectory(0)
    hist_mc_after.SetFillColorAlpha(rt.kGreen-2, 0.5)
    hist_mc_after.SetFillStyle(1001)
    hist_mc_after.SetLineColor(rt.kGreen-2)
    hist_mc_after.SetLineWidth(2)
    hist_mc_after.SetStats(0)
    hist_mc_after.SetTitle('')
    hist_mc_after.Scale(1./hist_mc_after.Integral())
    
    hist_mc_before.Draw('HIST SAME')
    hist_mc_after.Draw('HIST SAME')
    hist_data.Draw('PE SAME')
    
    hist_data_cloned = hist_data.Clone()
    hist_data_cloned.SetMarkerSize(1.2)
    
    legend = rt.TLegend(0.25,0.65,0.45,0.86, '')
    legend.SetTextSize(0.03)
    legend.SetBorderSize(0)     
    minbiasxsec_leg = '75.3' if args.data == '2024CDEFGHI' else '69.2'
    legend.AddEntry(hist_data_cloned, args.data + ' data, #sigma_{MB} = ' + minbiasxsec_leg + ' mb', 'PE')
    legend.AddEntry(hist_mc_before, args.mc + ' MC -- before PU reweighting', 'F')
    legend.AddEntry(hist_mc_after, args.mc + ' MC -- after PU reweighting', 'F')    
    legend.Draw()
    
    output_png = '../Histos_PU/PUProfiles_' + args.data + '_vs_' + args.mc + '_BeforeAndAfter.png'
    output_pdf = output_png.replace(".png", ".pdf")

    c.SaveAs(output_png)
    c.SaveAs(output_pdf)


if __name__ == '__main__':
    main()
