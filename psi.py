def psi(actual: pd.DataFrame, exp: pd.DataFrame, binning_method: str='quantile', n_bins: int=10, cat_col: list=None)-> dict:
    if cat_col is None:
        cat_col = actual.columns[actual.dtypes == object]
    num_col = list(set(actual.columns).difference(cat_col)) 
    psi_dict = {}
    for col_name in num_col:
        try:
            if binning_method == 'quantile':
                probs = np.arange(1/n_bins,1,1/n_bins)
                breaks = actual[col_name].quantile(probs)
                breaks = np.insert(np.append(breaks, np.inf), 0, -np.inf)
                actual_rel_freq = np.repeat(1/n_bins, n_bins) * 100
                exp_rel_freq = pd.cut(exp[col_name],breaks, retbins=False).value_counts(normalize=True) * 100
                psi_dict[col_name] = round(((actual_rel_freq - exp_rel_freq) * np.log(actual_rel_freq / exp_rel_freq)).sum(), 3)
            else:
                range = actual[col_name].max() - actual[col_name].min()
                step = range/n_bins
                breaks = np.arange(actual[col_name].min() + step, actual[col_name].max(), step)
                actual_rel_freq = pd.cut(actual[col_name],breaks, retbins=False).value_counts(normalize=True) * 100
                exp_rel_freq = pd.cut(exp[col_name],breaks, retbins=False).value_counts(normalize=True) * 100
                psi_dict[col_name] = round(((actual_rel_freq - exp_rel_freq) * np.log(actual_rel_freq / exp_rel_freq)).sum(), 3)
        except:
            print('error in col:', col_name)
    for col_name in cat_col:
        actual_rel_freq = actual[col_name].value_counts(normalize=True) * 100
        exp_rel_freq = exp[col_name].value_counts(normalize=True) * 100
        psi_dict[col_name] = round(((actual_rel_freq - exp_rel_freq) * np.log(actual_rel_freq / exp_rel_freq)).sum(), 3)

    return psi_dict
