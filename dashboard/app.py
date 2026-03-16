import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Dashboard Financeiro")

# -------------------------
# Funções de dados
# -------------------------

def fetch_bcb_series(series_id, start_date):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}/dados"
    params = {
        "formato": "json",
        "dataInicial": start_date.strftime("%d/%m/%Y")
    }

    r = requests.get(url, params=params)
    data = pd.DataFrame(r.json())

    data["data"] = pd.to_datetime(data["data"], dayfirst=True)
    data["valor"] = pd.to_numeric(data["valor"])

    return data.set_index("data")


def load_data():

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365*3)

    selic = fetch_bcb_series(11, start_date)
    usd = fetch_bcb_series(1, start_date)
    ipca = fetch_bcb_series(433, start_date)

    df = pd.DataFrame({
        "SELIC": selic["valor"],
        "USD": usd["valor"],
        "IPCA": ipca["valor"]
    })

    return df


df = load_data()

# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("Filtros")

period = st.sidebar.selectbox(
    "Período",
    ["6 meses", "1 ano", "2 anos", "Histórico completo"]
)

if period == "6 meses":
    df_filtered = df.last("180D")
elif period == "1 ano":
    df_filtered = df.last("365D")
elif period == "2 anos":
    df_filtered = df.last("730D")
else:
    df_filtered = df

page = st.sidebar.radio(
    "Página",
    ["Executivo", "Detalhamento"]
)

# -------------------------
# Cálculos
# -------------------------

usd_returns = df["USD"].pct_change()

usd_vol_30 = usd_returns.tail(30).std()

usd_now = df["USD"].iloc[-1]
usd_7 = df["USD"].iloc[-7]
usd_30 = df["USD"].iloc[-30]

usd_ret_7 = (usd_now/usd_7 - 1)*100
usd_ret_30 = (usd_now/usd_30 - 1)*100

selic_now = df["SELIC"].iloc[-1]
selic_30 = df["SELIC"].iloc[-30]

selic_var = selic_now - selic_30

ipca_12m = df["IPCA"].tail(12).sum()

# Percentil alerta
usd_percentil90 = df["USD"].quantile(0.9)

# Rolling correlation
rolling_corr = df["USD"].rolling(90).corr(df["SELIC"])

# -------------------------
# Página Executivo
# -------------------------

if page == "Executivo":

    st.title("📊 Dashboard Financeiro - Visão Executiva")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("SELIC Atual", f"{selic_now:.2f}", f"{selic_var:.2f}")

    col2.metric("USD/BRL", f"{usd_now:.2f}")

    col3.metric("Retorno USD 7D", f"{usd_ret_7:.2f}%")

    col4.metric("Retorno USD 30D", f"{usd_ret_30:.2f}%")

    st.metric("Volatilidade USD 30D", f"{usd_vol_30:.4f}")
    st.metric("IPCA acumulado 12M", f"{ipca_12m:.2f}%")

    if usd_now > usd_percentil90:
        st.warning("⚠️ Dólar acima do percentil 90 do histórico recente")

    corr_df = rolling_corr.dropna().reset_index()
    corr_df.columns = ["data", "correlation"]

    chart = alt.Chart(corr_df).mark_line().encode(
        x="data:T",
        y="correlation:Q"
    ).properties(title="Correlação móvel 90 dias: USD vs SELIC")

    st.altair_chart(chart, use_container_width=True)

# -------------------------
# Página Detalhamento
# -------------------------

if page == "Detalhamento":

    st.title("📈 Análises Detalhadas")

    df_plot = df_filtered.reset_index()

    chart_usd = alt.Chart(df_plot).mark_line().encode(
        x="data:T",
        y="USD:Q"
    ).properties(title="USD/BRL")

    chart_selic = alt.Chart(df_plot).mark_line().encode(
        x="data:T",
        y="SELIC:Q"
    ).properties(title="SELIC")

    chart_ipca = alt.Chart(df_plot).mark_line().encode(
        x="data:T",
        y="IPCA:Q"
    ).properties(title="IPCA")

    st.altair_chart(chart_usd, use_container_width=True)
    st.altair_chart(chart_selic, use_container_width=True)
    st.altair_chart(chart_ipca, use_container_width=True)

    # M/M e Y/Y
    usd_month = df["USD"].resample("M").last().pct_change()*100
    usd_year = df["USD"].resample("Y").last().pct_change()*100

    st.subheader("Variação USD")

    st.write("Mensal (%)")
    st.dataframe(usd_month.dropna())

    st.write("Anual (%)")
    st.dataframe(usd_year.dropna())

    st.subheader("Dados Brutos")
    st.dataframe(df_filtered)