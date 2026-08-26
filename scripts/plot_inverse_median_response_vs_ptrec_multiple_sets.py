import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_inverse_median_response_vs_ptrec_multiple_sets.py --jetCone 4 --jetAlgo puppi'

    parser = ArgumentParser(description='Script that plots the inverse of median response (correction) vs rec pt for multiple MC campaigns',epilog=usage)

    parser.add_argument("-c", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-a", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
    
    args = parser.parse_args()
    
    jet_dir_name = 'ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + ('l1' if args.jet_algo.lower() == 'chs' else '')
    
    eta_bins = ['-5.191', '-4.889', '-4.716', '-4.538', '-4.363', '-4.191', '-4.013', '-3.839', '-3.664', '-3.489', '-3.314', '-3.139', '-2.964', '-2.853', '-2.65', '-2.5', '-2.322', '-2.172', '-2.043', '-1.93', '-1.83', '-1.74', '-1.653', '-1.566', '-1.479', '-1.392', '-1.305', '-1.218', '-1.131', '-1.044', '-0.957', '-0.879', '-0.783', '-0.696', '-0.609', '-0.522', '-0.435', '-0.348', '-0.261', '-0.174', '-0.087', '0', '0.087', '0.174', '0.261', '0.348', '0.435', '0.522', '0.609', '0.696', '0.783', '0.879', '0.957', '1.044', '1.131', '1.218', '1.305', '1.392', '1.479', '1.566', '1.653', '1.74', '1.83', '1.93', '2.043', '2.172', '2.322', '2.5', '2.65', '2.853', '2.964', '3.139', '3.314', '3.489', '3.664', '3.839', '4.013', '4.191', '4.363', '4.538', '4.716', '4.889', '5.191']
        

    eta_ranges = [f'{start}to{end}' for start, end in zip(eta_bins[:-1], eta_bins[1:])]
    
    
    for eta_range in eta_ranges:
        eta_min_str, eta_max_str = eta_range.split('to')
        eta_min = float(eta_min_str)
        eta_max = float(eta_max_str)
        print('Processing eta bin: ' + eta_range)
        print('Processing graph: ' + jet_dir_name + '/AbsCorVsJetPt_JetEta' + eta_range)
                
        c1 = rt.TCanvas("c1", "c1", 800, 700)
        c1.SetLogx(1)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.SetRightMargin(0.04)
        c1.SetLeftMargin(0.12)
        c1.SetTopMargin(0.10)
        c1.SetBottomMargin(0.13)
        
        if(eta_max > 0):
            if(abs(eta_max) <= 2.5):
                ymin = 0.75
                ymax = 1.45
            elif(abs(eta_max) <= 2.964):
                ymin = 0.10
                ymax = 2.75
            else:
                ymin = 0.55
                ymax = 1.65
        else:
            if(abs(eta_min) <= 2.5):
                ymin = 0.75
                ymax = 1.45
            elif(abs(eta_min) <= 2.964):
                ymin = 0.10
                ymax = 2.75
            else:
                ymin = 0.55
                ymax = 1.65          
        
        frame = c1.DrawFrame(8., ymin, 5500, ymax)
        frame.GetXaxis().SetTitle("p_{T}^{rec} [GeV]")
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.05)
        frame.GetYaxis().SetTitle("Correction = [median(Response)]^{-1}")
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetLabelSize(0.04)
        frame.GetYaxis().SetLabelSize(0.035)
        
        cms = rt.TPaveText(0.206, 0.91, 0.406, 0.95, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextSize(0.05)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        sample = rt.TPaveText(0.865, 0.91, 0.965, 0.92, "NDC")
        sample.AddText('(13.6 TeV)')
        sample.SetTextFont(42)
        sample.SetTextSize(0.05)
        sample.SetBorderSize(0)
        sample.SetFillColor(0)
        sample.SetTextAlign(31)
        sample.Draw()
        
        jet_info = rt.TPaveText(0.78, 0.72, 0.91, 0.84, "NDC")
        jet_info.AddText('AK'+str(args.jet_cone)+' '+args.jet_algo.upper())
        jet_info.AddText(f"{eta_min:.3f} < #eta < {eta_max:.3f}")
        jet_info.SetTextFont(42)
        jet_info.SetTextSize(0.05)
        jet_info.SetBorderSize(0)
        jet_info.SetFillColor(0)
        jet_info.SetTextAlign(31)
        jet_info.Draw()
        
        legend = rt.TLegend(0.34, 0.16, 0.64, 0.38, "")
        legend.SetTextSize(0.035)
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        #legend.SetHeader("Fits with standard+Gaussian function:")
                
        line_horiz = rt.TLine(8, 1.0, 5500, 1.0)
        line_horiz.SetLineWidth(2)
        line_horiz.SetLineStyle(rt.kDashed)
        line_horiz.Draw('same')
        
        eras = ['Summer22', 'Summer22EE', 'Summer23', 'Summer23BPix', 'Summer24']
        colors = [rt.kBlue-4, rt.kRed-4, rt.kGreen-2, rt.kViolet, rt.kOrange+1]
        
        for era, color in zip(eras, colors):
                        
            root_filename = '/eos/cms/store/group/phys_jetmet/ilias/JEC_NewMethods_Run3/Responses/l2_AK'+str(args.jet_cone)+args.jet_algo.upper()+'_'+era+'.root'    
            print('Processing root file: ' + root_filename)
            root_file = rt.TFile.Open(root_filename, "READ")                
            graph = root_file.Get(jet_dir_name + '/AbsCorVsJetPt_JetEta' + eta_range)
        
            fit = graph.GetFunction('fit')              
            fit.SetLineColor(color)
            fit.SetLineWidth(2)

            lastx_nominal, lasty_nominal = ctypes.c_double(0), ctypes.c_double(0)
            graph.GetPoint(graph.GetN() - 1, lastx_nominal, lasty_nominal)
        
            text = f"{era} #scale[0.8]{{(#chi^{{2}} / ndf = {fit.GetChisquare():.1f} / {fit.GetNDF()}, Prob. = {fit.GetProb():.2f})}}"
            legend.AddEntry(graph, text, "LPE")
        
            graph.SetMarkerColor(color)
            graph.SetMarkerSize(0.5)
            graph.SetLineColor(color)
               
            graph.Draw("P SAME")
        
            fit.SetRange(8., lastx_nominal)
               
            
        legend.Draw()
        

        output_png = (f"../Plots/Fits/InverseOfResponseVsRecPt_AK{args.jet_cone}{args.jet_algo.upper()}_"f"{'_'.join(eras)}_RecEta{eta_min:.3f}to{eta_max:.3f}.png")
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)

        del c1


if __name__ == '__main__':
    main()
