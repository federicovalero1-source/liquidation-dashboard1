import streamlit as st
import requests

st.set_page_config(page_title="Liquidity Dashboard", layout="wide")

st.title("📊 Liquidity Dashboard (Clean Version)")

# ─────────────────────────────
# BINANCE DATA SAFE
# ─────────────────────────────

def get_data():
    url = "https://fapi.binance.com/futures/data/globalLongShortAccountRatio"

    params = {
        "symbol": "BTCUSDT",
        "period": "1h",
        "limit": 10
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()

        if not isinstance(data, list):
            return 50, 50

        long_total = 0
        short_total = 0

        for x in data:
            long_total += float(x.get("longAccount", 0))
            short_total += float(x.get("shortAccount", 0))

        return long_total, short_total

    except:
        return 50, 50


# ─────────────────────────────
# DATA
# ─────────────────────────────

long, short = get_data()
net = long - short

# ─────────────────────────────
# BIAS LOGIC
# ─────────────────────────────

if long > short:
    bias = "🟢 Alcista"
    up = 65
    down = 35
else:
    bias = "🔴 Bajista"
    up = 35
    down = 65

# ─────────────────────────────
# UI
# ─────────────────────────────

col1, col2, col3 = st.columns(3)

col1.metric("LONG", f"{long:.2f}")
col2.metric("SHORT", f"{short:.2f}")
col3.metric("NET", f"{net:.2f}")

st.subheader("BIAS DEL MERCADO")
st.write(bias)

st.progress(up / 100)
st.write(f"⬆️ Prob subida: {up}%")
st.write(f"⬇️ Prob bajada: {down}%")
