def qq_plot(series_1,series_2,quantiles=10):
    quant_1 = series_1.quantile(np.arange(0,1.0001,1/quantiles))
    quant_2 = series_2.quantile(np.arange(0,1.0001,1/quantiles))
    maximum = max([quant_1.max(), quant_2.max()])
    plt.scatter(quant_1,quant_2)
    plt.plot([0,maximum],[0,maximum])
    plt.show()
