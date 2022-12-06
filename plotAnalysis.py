def get_reg_fit(data, yvar, xvar, alpha=0.05):
    import statsmodels.formula.api as smf

    xaxis = xvar.split(" + ")[0]
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xaxis]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = (
        alt.Chart(predictions)
        .mark_line(opacity=treatment)
        .encode(
            x=xaxis,
            y=alt.Y(yvar, axis=alt.Axis(title="Price"))
        )
        .properties(title="Pricing Regression")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband()
        .encode(
            x=xaxis,
            y=alt.Y("ci_low", title="Price"),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart