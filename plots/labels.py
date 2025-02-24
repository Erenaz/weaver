label_dict = {
    "qcd_old": {"legend": "QCD", "label": "fj_isQCD"},
    "qcd": {"legend": "QCD", "label": "fj_bkg_label"},
    "qcdnolep": {"legend": "QCD", "label": "fj_bkg_label"},
    "qcd1lep": {"legend": "QCD", "label": "fj_bkg_label"},
    "qcd_astw": {"legend": "QCD", "label": "fj_bkg_label"},
    "qcd_asttbar": {"legend": "QCD", "label": "fj_bkg_label"},
    "w_asttbar": {"legend": "WJets", "label": "fj_bkg_label"},
    "w_asqcd": {"legend": "WJets", "label": "fj_bkg_label"},
    "top_asqcd": {"legend": "Top", "label": "fj_bkg_label"},
    "wtop_asqcd": {"legend": "WJets+Top", "label": "fj_bkg_label"},
    "w_asQCD": {"legend": "WJets", "label": "fj_bkg_label"},
    "top_asQCD": {"legend": "Top", "label": "fj_bkg_label"},
    "wtop_asQCD": {"legend": "WJets+Top", "label": "fj_bkg_label"},

    "top": {"legend": "Top", "label": "fj_isTop_label"},
    "top_lep": {"legend": "Top lep", "label": "fj_isToplep"},
    "top_merged": {"legend": "Top merged", "label": "fj_isTop_merged"},
    "top_semimerged": {"legend": "Top semi-merged", "label": "fj_isTop_semimerged"},
    "top_lepmerged": {"legend": "Top merged lepton", "label": "fj_isToplep_merged"},   
    "top_bsplit": {"legend": "Top unmerged b", "label": "fj_ttbar_bsplit"},
    "top_bmerged": {"legend": "Top merged b", "label": "fj_ttbar_bmerged"},
    
    "top_lm": {"legend": "ttbar merged lep", "label": "fj_ttbar_lepmerged"},
    "top_ls": {"legend": "ttbar split lep", "label": "fj_ttbar_lepsplit"},
    "wjets_lm": {"legend": "W+Jets merged lep", "label": "fj_wjets_lepmerged"},
    "wjets_ls": {"legend": "W+Jets split lep", "label": "fj_wjets_lepsplit"},
    
    "hww_ele_lm": {"legend": "H(VV) ele merged lep", "label": "fj_isHVV_elenuqq_lepmerged"},
    "hww_mu_lm": {"legend": "H(VV) mu merged lep", "label": "fj_isHVV_munuqq_lepmerged"},
    "hww_tau_lm": {"legend": "H(VV) tau merged lep", "label": "fj_isHVV_taunuqq_lepmerged"},
    "hww_ele_ls": {"legend": "H(VV) ele split lep", "label": "fj_isHVV_elenuqq_lepsplit"},
    "hww_mu_ls": {"legend": "H(VV) mu split lep", "label": "fj_isHVV_munuqq_lepsplit"},
    "hww_tau_ls": {"legend": "H(VV) tau split lep", "label": "fj_isHVV_taunuqq_lepsplit"},
    
    "ttbar": {"legend": "ttbar", "label": "fj_bkg_label"},
    "ttbar_l": {"legend": "ttbar", "label": "fj_bkg_label"},
    "wjets": {"legend": "W+Jets", "label": "fj_wjets_label"},
    "wjets_l": {"legend": "W+Jets", "label": "fj_bkg_label"},
    
    "ttbarwjets": {"legend": "W+Jets and ttbar", "label": "fj_bkg_label"},
    "ttbarwjetsqcd": {"legend": "W+Jets and ttbar and QCD", "label": "fj_bkg_label"},

    "hww_4q": {"legend": "H(VV) all-had", "label": "fj_H_VV_4q"},
    "hww_4q_merged": {"legend": "H(VV) 4q", "label": "fj_H_VV_4q_4q"},
    "hww_3q_merged": {"legend": "H(VV) 3q", "label": "fj_H_VV_4q_3q"},
    
    "hbb": {"legend": "H(bb)", "label": "fj_H_bb"},
    
    "hww_ele": {"legend": "H(VV) ele", "label": "fj_isHVV_elenuqq"},
    "hww_mu": {"legend": "H(VV) mu", "label": "fj_isHVV_munuqq"},
    "hww_tau": {"legend": "H(VV) tau", "label": "fj_isHVV_taunuqq"},
    "hww_tau_el": {"legend": "H(VV) tau (el)", "label": "fj_H_VV_leptauelvqq"},
    "hww_tau_mu": {"legend": "H(VV) leptau (mu)", "label": "fj_H_VV_leptaumuvqq"},
    "hww_tau_had": {"legend": "H(VV) hadtau ", "label": "fj_H_VV_hadtauvqq"},
    
    "hww_elenuqq": {"legend": "H(VV) ele", "label": "fj_H_VV_elenuqq"},
    "hww_munuqq": {"legend": "H(VV) mu", "label": "fj_H_VV_munuqq"},
    "hww_taunuqq": {"legend": "H(VV) tau merged", "label": "fj_isHVV_taunuqq_merged"},
    "hww_munuqq_merged": {"legend": "H(VV) mu merged", "label": "fj_isHVV_munuqq_merged"},
    "hww_munuqq_semimerged": {
        "legend": "H(VV) mu semi-merged",
        "label": "fj_isHVV_munuqq_semimerged",
    },
    "hww_elenuqq_merged": {"legend": "H(VV) ele merged", "label": "fj_isHVV_elenuqq_merged"},
    "hww_elenuqq_semimerged": {
        "legend": "H(VV) ele semi-merged",
        "label": "fj_isHVV_elenuqq_semimerged",
    },
    "hww_taunuqq_merged": {"legend": "H(VV) tau merged", "label": "fj_isHVV_taunuqq_merged"},
    "hww_taunuqq_semimerged": {
        "legend": "H(VV) tau semi-merged",
        "label": "fj_isHVV_taunuqq_semimerged",
    },

    "qcd_dnn": {"legend": "QCD", "label": "fj_QCD_label"},
    "hww_4q_dnn": {"legend": "H(VV) 4q", "label": "label_H_ww4q"},
    "hww_3q_dnn": {"legend": "H(VV) 3q", "label": "label_H_ww3q"},
    "hww_lvqq_dnn": {"legend": "H(VV) lvqq", "label": "label_H_wwlvqq"},
    "hww_ltvqq_dnn": {"legend": "H(VV) ltvqq", "label": "label_H_wwleptauvqq"},
    "hww_htvqq_dnn": {"legend": "H(VV) htvqq", "label": "label_H_wwhadtauvqq"},
    "hww_evqq_dnn": {"legend": "H(VV) evqq", "label": "label_H_wwevqq"},
    "hww_mvqq_dnn": {"legend": "H(VV) mvqq", "label": "label_H_wwmvqq"},
    "hww_etvqq_dnn": {"legend": "H(VV) etvqq", "label": "label_H_wwleptauevqq"},
    "hww_mtvqq_dnn": {"legend": "H(VV) mtvqq", "label": "label_H_wwleptaumvqq"},
}
