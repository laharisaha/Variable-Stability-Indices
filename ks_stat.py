from time import sleep
from scipy.stats import ks_2samp
def plot_ks(old: pd.DataFrame, new: pd.DataFrame, grid: str= True, label: list=["old","new"]):
    if len(old.shape)==1:
        plt.figure(figsize=(10,8))
        old_dist = old.value_counts(normalize=True).sort_index().cumsum()
        new_dist = new.value_counts(normalize=True).sort_index().cumsum()
        ax1 = old_dist.plot(color='blue', grid=True, label='old')
        ax2 = new_dist.plot(color='red', grid=True, secondary_y=True, label='new')

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()


        plt.legend(h1+h2, l1+l2, loc=2)
        plt.show()
    else:
        if not set(old.columns)==set(new.columns):
            raise Exception('columns of old and new should match')
        old = old.select_dtypes('number')
        new = new.select_dtypes('number')
        ks_stat = {}
        ks_alt = {}
        for col_name in old.columns:
            old_col = old[col_name].value_counts(normalize=True).sort_index().cumsum()
            new_col = new[col_name].value_counts(normalize=True).sort_index().cumsum()
            old_new_df = pd.DataFrame(old_col).join(
                new_col,lsuffix='_old',rsuffix='_new',how='outer')
            old_new_df.plot(figsize=(10,8), drawstyle='steps')
            old_col_stat = old[col_name].dropna()
            new_col_stat = new[col_name].dropna()
            indx = pd.Series(old_col_stat.append(new_col_stat).unique()).sort_values()
            old_cumsum = indx.apply(lambda x: (old_col_stat<=x).sum()/old_col_stat.shape[0])
            new_cumsum = indx.apply(lambda x: (new_col_stat<=x).sum()/new_col_stat.shape[0])
            final = pd.DataFrame({'old':old_cumsum, 'new':new_cumsum}).set_index(indx)
            final['abs_dist'] = (final.old - final.new).abs()
            ks_stat[col_name] = final.abs_dist.max()
            ks_alt[col_name] = ks_2samp(old_col_stat, new_col_stat)
        return ks_stat, ks_alt
