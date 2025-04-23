import glob, os
import ROOT as rt
rt.gROOT.SetBatch(rt.kTRUE)
from array import array
import numpy as np
import ctypes
from argparse import ArgumentParser


def main():
    usage = 'Example: python3 plot_inverse_median_response_vs_ptrec_bpix_fpix.py --jetCone 4 --jetAlgo puppi --era RunIII2024Summer24 --version V2 --issue BPix'

    parser = ArgumentParser(description='Script that plots the inverse of median response (correction) vs rec pt for nominal vs dedicated for bpix or fpix area',epilog=usage)

    parser.add_argument("-c", "--jetCone", dest="jet_cone", type=int, required=True,
                    help="Specify jet cone", metavar="JETCONE")
    
    parser.add_argument("-a", "--jetAlgo", dest="jet_algo", type=str, required=True,
                    help="Specify jet algorithm", metavar="JETALGO")
    
    parser.add_argument("-e", "--era", dest="era", type=str, required=True,
                    help="Specify era", metavar="ERA")
                    
    parser.add_argument("-v", "--version", dest="version", type=str, required=True,
                    help="Specify version", metavar="VERSION") 
                    
    parser.add_argument("-i", "--issue", dest="issue", type=str, required=True,
                    help="Specify issue: BPix or FPix", metavar="ISSUE")                                

    args = parser.parse_args()

    root_filename_nominal = '../condor_AK'+str(args.jet_cone)+args.jet_algo.upper()+'/Files/'+args.era+'_'+args.version+'_PhiIndependent/'+('L1' if args.jet_algo.lower() == 'chs' else '')+'L2L3_output/l2.root'    
    root_filename_dedicated = '../condor_AK'+str(args.jet_cone)+args.jet_algo.upper()+'/Files/'+args.era+'_'+args.version+'_PhiDependent/'+('L1' if args.jet_algo.lower() == 'chs' else '')+'L2L3_output_DedicatedFor'+args.issue+'Area/l2.root'
    
    print('Processing root file: ' + root_filename_nominal)
    print('Processing root file: ' + root_filename_dedicated)

    root_file_nominal = rt.TFile.Open(root_filename_nominal, "READ")    
    root_file_dedicated = rt.TFile.Open(root_filename_dedicated, "READ")
    
    jet_dir_name = 'ak' + str(args.jet_cone) + ('pf' if args.jet_algo.lower() == 'chs' else '') + args.jet_algo.lower() + ('l1' if args.jet_algo.lower() == 'chs' else '')
    
    if args.issue == 'BPix':
        eta_bins = ['-1.479', '-1.392', '-1.305', '-1.218', '-1.131', '-1.044', '-0.957', '-0.879', '-0.783', '-0.696', '-0.609', '-0.522', '-0.435', '-0.348', '-0.261', '-0.174', '-0.087', '0', '0.087']
    elif args.issue == 'FPix':
        eta_bins = ['-2.043', '-1.93', '-1.83', '-1.74', '-1.653', '-1.566']
    else:
        raise ValueError(f"Unknown issue type: {args.issue}")
        

    eta_ranges = [f'{start}to{end}' for start, end in zip(eta_bins[:-1], eta_bins[1:])]
    
    
    for eta_range in eta_ranges:
        eta_min_str, eta_max_str = eta_range.split('to')
        eta_min = float(eta_min_str)
        eta_max = float(eta_max_str)
        print('Processing eta bin: ' + eta_range)
        print('Processing graph: ' + jet_dir_name + '/AbsCorVsJetPt_JetEta' + eta_range)
                
        graph_nominal = root_file_nominal.Get(jet_dir_name + '/AbsCorVsJetPt_JetEta' + eta_range)
        graph_dedicated = root_file_dedicated.Get(jet_dir_name + '/AbsCorVsJetPt_JetEta' + eta_range)
        
        fit_nominal = graph_nominal.GetFunction('fit')
        fit_dedicated = graph_dedicated.GetFunction('fit')
                
        fit_nominal.SetLineColor(rt.kViolet)
        fit_nominal.SetLineWidth(2)
        fit_dedicated.SetLineColor(rt.kOrange+1 if args.issue == 'BPix' else rt.kOrange-2)
        fit_dedicated.SetLineWidth(2)
                                       
        c1 = rt.TCanvas("c1", "c1", 800, 700)
        c1.SetLogx(1)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.SetRightMargin(0.04)
        c1.SetLeftMargin(0.12)
        c1.SetTopMargin(0.10)
        c1.SetBottomMargin(0.13)

        ymin = 0.8
        ymax = 1.5 

        lastx_nominal, lasty_nominal = ctypes.c_double(0), ctypes.c_double(0)
        graph_nominal.GetPoint(graph_nominal.GetN() - 1, lastx_nominal, lasty_nominal)
        
        lastx_dedicated, lasty_dedicated = ctypes.c_double(0), ctypes.c_double(0)
        graph_dedicated.GetPoint(graph_dedicated.GetN() - 1, lastx_dedicated, lasty_dedicated)
                
        frame = c1.DrawFrame(6., ymin, lastx_nominal.value*1.1 if lastx_nominal.value>lastx_dedicated.value else lastx_dedicated.value*1.1, ymax)
        frame.GetXaxis().SetTitle("p_{T}^{rec} [GeV]")
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.05)
        frame.GetYaxis().SetTitle("Correction = [median(Response)]^{-1}")
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetLabelSize(0.04)
        frame.GetYaxis().SetLabelSize(0.035)
        
        chi2_legend = rt.TLegend(0.42, 0.16, 0.72, 0.32, "")
        chi2_legend.SetTextSize(0.035)
        chi2_legend.SetFillColor(0)
        chi2_legend.SetBorderSize(0)
        chi_text_nominal = f"#chi^{{2}} / ndf = {fit_nominal.GetChisquare():.1f} / {fit_nominal.GetNDF()}, Prob. = {fit_nominal.GetProb():.2f}"
        chi_text_dedicated = f"#chi^{{2}} / ndf = {fit_dedicated.GetChisquare():.1f} / {fit_dedicated.GetNDF()}, Prob. = {fit_dedicated.GetProb():.2f}"
        chi2_legend.SetHeader("Fit with standard+Gaussian function:")
        chi2_legend.AddEntry(fit_nominal, chi_text_nominal, "L")
        chi2_legend.AddEntry(fit_dedicated, chi_text_dedicated, "L")
        chi2_legend.Draw()

        graph_nominal.SetMarkerColor(rt.kViolet)
        graph_nominal.SetLineColor(rt.kViolet)
        graph_dedicated.SetMarkerColor(rt.kOrange+1 if args.issue == 'BPix' else rt.kOrange-2)
        graph_dedicated.SetLineColor(rt.kOrange+1 if args.issue == 'BPix' else rt.kOrange-2)
               
        graph_nominal.Draw("P SAME")
        graph_dedicated.Draw("P SAME")
        
        fit_nominal.SetRange(6., lastx_nominal)
        fit_dedicated.SetRange(6., lastx_dedicated)

        cms = rt.TPaveText(0.206, 0.91, 0.406, 0.95, "NDC")
        cms.AddText("#bf{CMS} #scale[0.7]{#it{Simulation Preliminary}}")
        cms.SetTextFont(42)
        cms.SetTextSize(0.05)
        cms.SetBorderSize(0)
        cms.SetFillColor(0)
        cms.Draw()

        sample = rt.TPaveText(0.865, 0.91, 0.965, 0.92, "NDC")
        sample.AddText((args.era[10:] if args.era == 'RunIII2024Summer24' else args.era) + ' (13.6 TeV)')
        sample.SetTextFont(42)
        sample.SetTextSize(0.05)
        sample.SetBorderSize(0)
        sample.SetFillColor(0)
        sample.SetTextAlign(31)
        sample.Draw()
        
        if args.issue == 'BPix':
            phi_range_dedicated_leg = 'BPix: -1.22 < #phi < -0.79'
            phi_range_nominal_leg = 'Not BPix: -#pi < #phi < -1.22 #vee -0.79 < #phi < #pi'
        elif (args.issue == 'FPix' and (eta_min>=-2.043 and eta_max<=-1.83)):
            phi_range_dedicated_leg = 'FPix: 2.44 < #phi < 3.05'
            phi_range_nominal_leg = 'Not FPix: -#pi < #phi < 2.44 #vee 3.05 < #phi < #pi'
        elif (args.issue == 'FPix' and (eta_min>=-1.83 and eta_max<=-1.566)):
            phi_range_dedicated_leg = 'FPix: 2.44 < #phi < 2.79' 
            phi_range_nominal_leg = 'Not FPix: -#pi < #phi < 2.44 #vee 2.79 < #phi < #pi'     
        else:
            phi_range_dedicated_leg = ''
            phi_range_nominal_leg = ''     
        
        legend = rt.TLegend(0.40, 0.68, 0.60, 0.88)
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.AddEntry(0, 'AK'+str(args.jet_cone)+' '+args.jet_algo.upper(), '')
        legend.AddEntry(0, f"{eta_min:.3f} < #eta < {eta_max:.3f}", '')
        legend.AddEntry(graph_dedicated, phi_range_dedicated_leg, 'PE')
        legend.AddEntry(graph_nominal, phi_range_nominal_leg, 'PE')
        legend.Draw()

        output_png = f'../OverviewPlotsBPixFPix/InverseOfResponseVsRecPt_AK{args.jet_cone}{args.jet_algo.upper()}_{args.era}_{args.version}_StandardJECs_vs_DedicatedFor{args.issue}Area_RecEta{eta_min:.3f}to{eta_max:.3f}.png'
        output_pdf = output_png.replace(".png", ".pdf")

        c1.SaveAs(output_png)
        c1.SaveAs(output_pdf)

        del c1

    root_file_nominal.Close()
    root_file_dedicated.Close()

    print("Processing complete. All plots saved.")

if __name__ == '__main__':
    main()
