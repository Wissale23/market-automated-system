import streamlit as st
import pandas as pd
import plotly.express as px
import json

from main import run_pipeline
from config.config import INITIAL_CAPITAL


# ---------------------------------
# Page configuration
# ---------------------------------

st.set_page_config(
    page_title="Market Automated System",
    page_icon="📈",
    layout="wide"
)


# ---------------------------------
# Title
# ---------------------------------

st.title("📈 Market Automated Trading System")

st.markdown(
    """
    Quantitative research dashboard:

    **Data → Features → Signals → Risk Management → Backtesting → Portfolio Optimisation**
    """
)


# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.header("Strategy Configuration")


tickers = st.sidebar.multiselect(
    "Select assets",
    [
        "AAPL",
        "MSFT",
        "GOOG",
        "META",
        "AMZN",
        "NVDA"
    ],
    default=[
        "AAPL",
        "MSFT",
        "GOOG",
        "META",
        "AMZN",
        "NVDA"
    ]
)


optimizer = st.sidebar.selectbox(
    "Portfolio Optimiser",
    [
        "maximum_sharpe",
        "minimum_variance",
        "volatility_weight",
        "equal_weight"
    ]
)


capital = st.sidebar.number_input(
    "Initial Capital (£)",
    value=float(INITIAL_CAPITAL),
    step=1000.0
)



# Strategy parameters

st.sidebar.subheader("Strategy Parameters")


ma_short = st.sidebar.slider(
    "Short Moving Average",
    min_value=3,
    max_value=30,
    value=5
)


ma_long = st.sidebar.slider(
    "Long Moving Average",
    min_value=10,
    max_value=100,
    value=20
)


stop_loss = st.sidebar.slider(
    "Stop Loss",
    min_value=0.01,
    max_value=0.20,
    value=0.05,
    step=0.01
)



run = st.sidebar.button(
    "Run Strategy"
)



# ---------------------------------
# Run pipeline
# ---------------------------------

if run:

    if len(tickers) == 0:

        st.warning(
            "Please select at least one asset."
        )

        st.stop()


    with st.spinner(
        "Running quantitative pipeline..."
    ):


        (
            results,
            weights,
            portfolio_curve,
            portfolio_metrics,
            final_value

        ) = run_pipeline(

            tickers=tickers,

            optimiser=optimizer,

            initial_capital=capital,

            ma_short=ma_short,

            ma_long=ma_long,

            stop_loss=stop_loss
        )



    st.success(
        "Pipeline completed successfully!"
    )


    # ---------------------------------
    # Portfolio summary
    # ---------------------------------

    st.header(
        "Portfolio Overview"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Initial Capital",
            f"£{capital:,.2f}"
        )


    with col2:

        st.metric(
            "Final Value",
            f"£{final_value:,.2f}"
        )


    with col3:

        portfolio_return = (
            final_value / capital - 1
        )

        st.metric(
            "Return",
            f"{portfolio_return:.2%}"
        )



    # ---------------------------------
    # Portfolio weights
    # ---------------------------------

    st.header(
        "Portfolio Allocation"
    )


    weights_df = pd.DataFrame(
        {
            "Asset": list(weights.keys()),
            "Weight": list(weights.values())
        }
    )


    st.dataframe(
        weights_df,
        use_container_width=True
    )


    fig = px.pie(
        weights_df,
        names="Asset",
        values="Weight",
        title="Portfolio Allocation"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # ---------------------------------
    # Equity curve
    # ---------------------------------

    st.header(
        "Portfolio Equity Curve"
    )


    equity_df = pd.DataFrame(
        {
            "Day": range(
                len(portfolio_curve)
            ),

            "Portfolio Value": portfolio_curve
        }
    )


    fig = px.line(
        equity_df,
        x="Day",
        y="Portfolio Value",
        title="Portfolio Growth"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # ---------------------------------
    # Portfolio metrics
    # ---------------------------------

    st.header(
        "Risk Metrics"
    )


    metrics_df = pd.DataFrame(
        portfolio_metrics.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


    st.dataframe(
        metrics_df,
        use_container_width=True
    )



    # ---------------------------------
    # Download report
    # ---------------------------------

    st.header(
        "Export Results"
    )


    report = {

        "weights": weights,

        "portfolio_metrics": portfolio_metrics,

        "initial_capital": capital,

        "final_value": float(final_value),

        "return": float(portfolio_return)

    }


    report_json = json.dumps(
        report,
        indent=4,
        default=float
    )


    st.download_button(

        label="Download Portfolio Report",

        data=report_json,

        file_name="portfolio_report.json",

        mime="application/json"
    )



    # ---------------------------------
    # Individual assets
    # ---------------------------------

    st.header(
        "Individual Asset Performance"
    )


    for symbol, result in results.items():

        st.subheader(symbol)


        df = result["data"]


        chart_df = df[
            [
                "portfolio_value",
                "buy_hold_value"
            ]
        ]


        fig = px.line(
            chart_df,
            title=f"{symbol} Strategy vs Buy & Hold"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.write(
            "Metrics"
        )


        st.json(
            result["metrics"]
        )