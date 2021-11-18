def grangercausalitytests(x, maxlag, addconst=True, verbose=True):
    """
    Four tests for granger non causality of 2 time series.

    All four tests give similar results. `params_ftest` and `ssr_ftest` are
    equivalent based on F test which is identical to lmtest:grangertest in R.

    Parameters
    ----------
    x : array_like
        The data for test whether the time series in the second column Granger
        causes the time series in the first column. Missing values are not
        supported.
    maxlag : {int, Iterable[int]}
        If an integer, computes the test for all lags up to maxlag. If an
        iterable, computes the tests only for the lags in maxlag.
    addconst : bool
        Include a constant in the model.
    verbose : bool
        Print results.

    Returns
    -------
    dict
        All test results, dictionary keys are the number of lags. For each
        lag the values are a tuple, with the first element a dictionary with
        test statistic, pvalues, degrees of freedom, the second element are
        the OLS estimation results for the restricted model, the unrestricted
        model and the restriction (contrast) matrix for the parameter f_test.

    Notes
    -----
    TODO: convert to class and attach results properly

    The Null hypothesis for grangercausalitytests is that the time series in
    the second column, x2, does NOT Granger cause the time series in the first
    column, x1. Grange causality means that past values of x2 have a
    statistically significant effect on the current value of x1, taking past
    values of x1 into account as regressors. We reject the null hypothesis
    that x2 does not Granger cause x1 if the pvalues are below a desired size
    of the test.

    The null hypothesis for all four test is that the coefficients
    corresponding to past values of the second time series are zero.

    `params_ftest`, `ssr_ftest` are based on F distribution

    `ssr_chi2test`, `lrtest` are based on chi-square distribution

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Granger_causality

    .. [2] Greene: Econometric Analysis

    Examples
    --------
    """
    x = array_like(x, "x", ndim=2)
    if not np.isfinite(x).all():
        raise ValueError("x contains NaN or inf values.")
    addconst = bool_like(addconst, "addconst")
    verbose = bool_like(verbose, "verbose")
    try:
        maxlag = int_like(maxlag, "maxlag")
        if maxlag <= 0:
            raise ValueError("maxlag must a a positive integer")
        lags = np.arange(1, maxlag + 1)
    except TypeError:
        lags = np.array([int(lag) for lag in maxlag])
        maxlag = lags.max()
        if lags.min() <= 0 or lags.size == 0:
            raise ValueError(
                "maxlag must be a non-empty list containing only "
                "positive integers"
            )

    if x.shape[0] <= 3 * maxlag + int(addconst):
        raise ValueError(
            "Insufficient observations. Maximum allowable "
            "lag is {0}".format(int((x.shape[0] - int(addconst)) / 3) - 1)
        )

    resli = {}

    for mlg in lags:
        result = {}
        if verbose:
            print("\nGranger Causality")
            print("number of lags (no zero)", mlg)
        mxlg = mlg

        # create lagmat of both time series
        dta = lagmat2ds(x, mxlg, trim="both", dropex=1)

        # add constant
        if addconst:
            dtaown = add_constant(dta[:, 1 : (mxlg + 1)], prepend=False)
            dtajoint = add_constant(dta[:, 1:], prepend=False)
            if (
                dtajoint.shape[1] == (dta.shape[1] - 1)
                or (dtajoint.max(0) == dtajoint.min(0)).sum() != 1
            ):
                raise InfeasibleTestError(
                    "The x values include a column with constant values and so"
                    " the test statistic cannot be computed."
                )
        else:
            raise NotImplementedError("Not Implemented")
            # dtaown = dta[:, 1:mxlg]
            # dtajoint = dta[:, 1:]

        # Run ols on both models without and with lags of second variable
        res2down = OLS(dta[:, 0], dtaown).fit()
        res2djoint = OLS(dta[:, 0], dtajoint).fit()

        # print results
        # for ssr based tests see:
        # http://support.sas.com/rnd/app/examples/ets/granger/index.htm
        # the other tests are made-up

        # Granger Causality test using ssr (F statistic)
        if res2djoint.model.k_constant:
            tss = res2djoint.centered_tss
        else:
            tss = res2djoint.centered_tss
        if (
            tss == 0
            or res2djoint.ssr == 0
            or np.isnan(res2djoint.rsquared)
            or (res2djoint.ssr / tss) < np.finfo(float).eps
            or res2djoint.params.shape[0] != dtajoint.shape[1]
        ):
            raise InfeasibleTestError(
                "The Granger causality test statistic cannot be compute "
                "because the VAR has a perfect fit of the data."
            )
        fgc1 = (
            (res2down.ssr - res2djoint.ssr)
            / res2djoint.ssr
            / mxlg
            * res2djoint.df_resid
        )
        if verbose:
            print(
                "ssr based F test:         F=%-8.4f, p=%-8.4f, df_denom=%d,"
                " df_num=%d"
                % (
                    fgc1,
                    stats.f.sf(fgc1, mxlg, res2djoint.df_resid),
                    res2djoint.df_resid,
                    mxlg,
                )
            )
        result["ssr_ftest"] = (
            fgc1,
            stats.f.sf(fgc1, mxlg, res2djoint.df_resid),
            res2djoint.df_resid,
            mxlg,
        )

        # Granger Causality test using ssr (ch2 statistic)
        fgc2 = res2down.nobs * (res2down.ssr - res2djoint.ssr) / res2djoint.ssr
        if verbose:
            print(
                "ssr based chi2 test:   chi2=%-8.4f, p=%-8.4f, "
                "df=%d" % (fgc2, stats.chi2.sf(fgc2, mxlg), mxlg)
            )
        result["ssr_chi2test"] = (fgc2, stats.chi2.sf(fgc2, mxlg), mxlg)

        # likelihood ratio test pvalue:
        lr = -2 * (res2down.llf - res2djoint.llf)
        if verbose:
            print(
                "likelihood ratio test: chi2=%-8.4f, p=%-8.4f, df=%d"
                % (lr, stats.chi2.sf(lr, mxlg), mxlg)
            )
        result["lrtest"] = (lr, stats.chi2.sf(lr, mxlg), mxlg)

        # F test that all lag coefficients of exog are zero
        rconstr = np.column_stack(
            (np.zeros((mxlg, mxlg)), np.eye(mxlg, mxlg), np.zeros((mxlg, 1)))
        )
        ftres = res2djoint.f_test(rconstr)
        if verbose:
            print(
                "parameter F test:         F=%-8.4f, p=%-8.4f, df_denom=%d,"
                " df_num=%d"
                % (ftres.fvalue, ftres.pvalue, ftres.df_denom, ftres.df_num)
            )
        result["params_ftest"] = (
            np.squeeze(ftres.fvalue)[()],
            np.squeeze(ftres.pvalue)[()],
            ftres.df_denom,
            ftres.df_num,
        )

        resli[mxlg] = (result, [res2down, res2djoint, rconstr])

    return resli