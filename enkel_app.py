"""
Enkel Energy Intelligence — Deep Tech Demo
Built by Umair Ali · Price Optimization · Clean Data · V2G Revenue

Deploy: streamlit run enkel_app.py
Host:   Streamlit Community Cloud (connect GitHub repo)
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import math

# ═══════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="Enkel Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    .stApp { background-color: #06090f; color: #e8edf3; }
    .header-container {
        display: flex; align-items: center; gap: 14px; padding: 8px 0 16px; flex-wrap: wrap;
    }
    .header-logo {
        width: 38px; height: 38px; border-radius: 10px;
        background: linear-gradient(135deg, #06d6a0, #118ab2);
        display: flex; align-items: center; justify-content: center;
        font-size: 19px; font-weight: 900; color: #06090f; flex-shrink: 0;
    }
    .header-title { font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 700; color: #e8edf3; }
    .header-sub { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4a5568; letter-spacing: 0.12em; }
    .badge {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 3px 10px; border-radius: 5px; font-size: 10px;
        font-weight: 700; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.04em;
    }
    .badge-cyan { color: #06d6a0; background: rgba(6,214,160,0.12); }
    .badge-purple { color: #8338ec; background: rgba(131,56,236,0.12); }
    .badge-amber { color: #ffd166; background: rgba(255,209,102,0.12); }
    .dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
    .dot-healthy { background: #06d6a0; box-shadow: 0 0 6px rgba(6,214,160,0.5); }
    .dot-degraded { background: #ffd166; box-shadow: 0 0 6px rgba(255,209,102,0.5); }
    .metric-card {
        background: #111820; border: 1px solid #1a2332; border-radius: 10px; padding: 16px 18px;
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4a5568;
        text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px;
    }
    .metric-value { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 700; }
    .metric-unit { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #4a5568; }
    .metric-sub { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4a5568; margin-top: 2px; }
    .pipeline-stage { text-align: center; border-radius: 8px; padding: 14px 8px; }
    .pipeline-icon { font-size: 22px; margin-bottom: 4px; }
    .pipeline-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; }
    .pipeline-sub { font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #4a5568; margin-top: 2px; }
    .pipeline-count { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #8899aa; margin-top: 6px; font-weight: 600; }
    .source-row {
        display: flex; align-items: center; gap: 14px; padding: 10px 0;
        border-bottom: 1px solid rgba(30,45,61,0.15); font-family: 'JetBrains Mono', monospace; font-size: 11px;
    }
    .source-row:last-child { border-bottom: none; }
    .q-bar-outer { width: 60px; height: 4px; border-radius: 2px; background: #1e2d3d; display: inline-block; overflow: hidden; vertical-align: middle; margin-right: 6px; }
    .q-bar-inner { height: 100%; border-radius: 2px; }
    .rule-row {
        display: flex; align-items: center; gap: 12px; padding: 9px 0;
        border-bottom: 1px solid rgba(30,45,61,0.15); font-family: 'JetBrains Mono', monospace; font-size: 11px;
    }
    .rule-row:last-child { border-bottom: none; }
    .thesis-card {
        background: linear-gradient(135deg, #111820 0%, #15101f 100%);
        border-radius: 10px; padding: 22px; border: 1px solid rgba(131,56,236,0.18); margin-top: 16px;
    }
    .thesis-title { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #8338ec; font-weight: 700; letter-spacing: 0.06em; margin-bottom: 12px; }
    .thesis-text { font-size: 13.5px; line-height: 1.75; color: #e8edf3; max-width: 720px; }
    .tag-row { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
    .card-box { background: #111820; border: 1px solid #1a2332; border-radius: 10px; padding: 20px; margin-bottom: 16px; }
    .card-title { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #4a5568; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 14px; }

    /* Streamlit overrides */
    .stTabs [data-baseweb="tab-list"] { gap: 0; background: #0c1117; border-bottom: 1px solid #1e2d3d; }
    .stTabs [data-baseweb="tab"] { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600; color: #4a5568; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { color: #06d6a0 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #06d6a0 !important; }
    .stTabs [data-baseweb="tab-border"] { display: none; }
    div[data-testid="stMetric"] { background: #111820; border: 1px solid #1a2332; border-radius: 10px; padding: 14px; }
    .stSlider > div > div > div { background: #1e2d3d; }
    section[data-testid="stSidebar"] { background: #0c1117; }
    .stMarkdown hr { border-color: #1e2d3d; }
    #MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# DATA GENERATION
# ═══════════════════════════════════════════
@st.cache_data
def generate_prices():
    rng = np.random.RandomState(42 + datetime.now().day)
    base = [0.38,0.32,0.28,0.25,0.24,0.30,0.55,0.82,
            1.02,0.91,0.75,0.68,0.62,0.58,0.55,0.60,
            0.78,1.22,1.58,1.35,1.02,0.78,0.58,0.45]
    hours = []
    for h in range(24):
        noise = (rng.random() - 0.5) * 0.3
        actual = max(0.05, base[h] + noise)
        f_err = (rng.random() - 0.5) * 0.12
        forecast = max(0.05, actual + f_err)
        ci = 0.08 + rng.random() * 0.15
        wind = max(10, min(92, 52 - actual*25 + (rng.random()-0.5)*15))
        solar = max(0, 18*math.sin((h-6)/14*math.pi) + (rng.random()-0.5)*8) if 6 <= h <= 20 else 0
        co2 = round(35 + actual*95 + (rng.random()-0.5)*25)
        hours.append({
            'hour': h, 'label': f'{h:02d}:00',
            'actual': round(actual, 2), 'forecast': round(forecast, 2),
            'upper': round(forecast + ci, 2), 'lower': round(max(0.02, forecast - ci), 2),
            'error': round(actual - forecast, 2),
            'wind_pct': round(wind), 'solar_pct': round(solar, 1), 'co2': co2,
        })
    return hours

prices = generate_prices()
now_hour = min(datetime.now().hour, 23)
current_price = prices[now_hour]['actual']
price_min = min(p['actual'] for p in prices)
price_max = max(p['actual'] for p in prices)
price_avg = sum(p['actual'] for p in prices) / 24
forecast_mae = sum(abs(p['actual'] - p['forecast']) for p in prices) / 24

# ═══════════════════════════════════════════
# PLOTLY HELPER
# ═══════════════════════════════════════════
CYAN = '#06d6a0'
BLUE = '#118ab2'
AMBER = '#ffd166'
RED = '#ef476f'
PURPLE = '#8338ec'
T3 = '#4a5568'
GRID_COLOR = 'rgba(30,45,61,0.12)'

def apply_layout(fig, height=300, show_legend=False):
    """Apply consistent dark theme layout to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor='#111820',
        plot_bgcolor='#111820',
        font_family='JetBrains Mono, monospace',
        font_color='#4a5568',
        font_size=10,
        margin=dict(l=40, r=20, t=30, b=40),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#161e2a', bordercolor='#2a3a4a',
            font=dict(family='JetBrains Mono', size=11, color='#e8edf3')
        ),
        height=height,
        showlegend=show_legend,
    )
    if show_legend:
        fig.update_layout(
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center',
                        font=dict(size=10, color='#8899aa'))
        )
    fig.update_xaxes(gridcolor=GRID_COLOR, zeroline=False)
    fig.update_yaxes(gridcolor=GRID_COLOR, zeroline=False)
    return fig

# ═══════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════
header_html = (
    '<div class="header-container">'
    '<div class="header-logo">E</div>'
    '<div>'
    '<div class="header-title">Enkel Energy Intelligence</div>'
    '<div class="header-sub">DEEP TECH · PRICE OPTIMIZATION · CLEAN DATA</div>'
    '</div>'
    '<div style="margin-left:auto;display:flex;align-items:center;gap:10px;">'
    '<span class="badge badge-cyan"><span class="dot dot-healthy"></span> PIPELINE HEALTHY</span>'
    f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#4a5568;">{datetime.now().strftime("%H:%M:%S")}</span>'
    '</div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "⟐  Data Pipeline", "◈  Price Forecast", "⬡  Optimizer", "⚡  V2G Revenue"
])

# Helper for metric cards
def metric_card(label, value, unit="", color="#e8edf3", sub=""):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ''
    unit_html = f'<span class="metric-unit">{unit}</span>' if unit else ''
    # NOTE: built as a single line with no leading whitespace — indented
    # multi-line HTML inside st.markdown gets misread as a Markdown code
    # block (4+ leading spaces triggers it), which is what caused the
    # stray "</div>" boxes to render as literal text.
    return (
        '<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div><span class="metric-value" style="color:{color}">{value}</span> {unit_html}</div>'
        f'{sub_html}'
        '</div>'
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: DATA PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Records Ingested", "14.8M", color=BLUE), unsafe_allow_html=True)
    c2.markdown(metric_card("Validated", "14.8M", color=CYAN, sub="0.33% drop rate"), unsafe_allow_html=True)
    c3.markdown(metric_card("Avg Latency", "23.4", "ms", AMBER, "p99: 87.2ms"), unsafe_allow_html=True)
    c4.markdown(metric_card("Uptime", "99.97", "%", CYAN), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pipeline architecture
    stages = [
        ("◉", "INGEST", "Kafka / REST", "14.8M", BLUE),
        ("◈", "VALIDATE", "Schema + Rules", "14.8M", AMBER),
        ("⬡", "ENRICH", "Join + Transform", "14.8M", PURPLE),
        ("⬢", "STORE", "TimescaleDB", "14.8M", CYAN),
        ("◎", "SERVE", "API / Stream", "14.8M", CYAN),
    ]
    cols = st.columns(len(stages) * 2 - 1)
    for i, (icon, label, sub, count, color) in enumerate(stages):
        with cols[i * 2]:
            rgb = f"{int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)}"
            stage_html = (
                f'<div class="pipeline-stage" style="background:rgba({rgb},0.06);border:1px solid rgba({rgb},0.25);">'
                f'<div class="pipeline-icon">{icon}</div>'
                f'<div class="pipeline-label" style="color:{color}">{label}</div>'
                f'<div class="pipeline-sub">{sub}</div>'
                f'<div class="pipeline-count">{count}</div>'
                '</div>'
            )
            st.markdown(stage_html, unsafe_allow_html=True)
        if i < len(stages) - 1:
            with cols[i * 2 + 1]:
                st.markdown('<div style="text-align:center;padding-top:30px;color:#4a5568;font-family:monospace;font-size:16px;">→</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Data sources
    sources = [
        ("healthy", "Energinet (DayAhead)", "4.2M", "1.2s", 99.8),
        ("healthy", "Nord Pool (Spot)", "3.8M", "0.8s", 99.9),
        ("healthy", "Charger Telemetry", "5.1M", "2.1s", 98.2),
        ("degraded", "DMI (Weather/Wind)", "1.2M", "5.4s", 97.5),
        ("healthy", "Energinet (Balancing)", "0.5M", "3.8s", 99.1),
    ]

    source_html = '<div class="card-box"><div class="card-title">Live Data Sources</div>'
    for status, name, records, freshness, quality in sources:
        dot_cls = f"dot-{status}"
        fresh_val = float(freshness.replace('s',''))
        fc = CYAN if fresh_val < 3 else AMBER
        qc = CYAN if quality > 99 else AMBER if quality > 98 else RED
        source_html += (
            '<div class="source-row">'
            f'<span class="dot {dot_cls}"></span>'
            f'<span style="color:#e8edf3;font-weight:500;flex:1;min-width:160px">{name}</span>'
            f'<span style="color:#8899aa;width:60px">{records}</span>'
            f'<span style="color:{fc};width:50px">{freshness}</span>'
            '<span style="width:100px">'
            f'<span class="q-bar-outer"><span class="q-bar-inner" style="width:{quality}%;background:{qc}"></span></span>'
            f'<span style="color:{qc};font-size:10px">{quality}%</span>'
            '</span>'
            '</div>'
        )
    source_html += '</div>'
    st.markdown(source_html, unsafe_allow_html=True)

    # Validation rules
    rules = [
        ("Price range [0, 15] DKK/kWh", "3,372", 99.98),
        ("Timestamp monotonicity", "191", 99.99),
        ("Null field rejection", "14,835", 99.90),
        ("Cross-source consistency", "26,287", 99.82),
        ("Outlier detection (3σ)", "8,175", 99.94),
    ]
    rules_html = '<div class="card-box"><div class="card-title">Data Quality — Validation Rules</div>'
    for rule, failed, rate in rules:
        bc = "badge-cyan" if rate > 99.9 else "badge-amber"
        rules_html += (
            '<div class="rule-row">'
            f'<span style="color:{CYAN};font-size:10px">✓</span>'
            f'<span style="flex:1;color:#8899aa">{rule}</span>'
            f'<span style="color:#4a5568;font-size:10px">{failed} rejected</span>'
            f'<span class="badge {bc}">{rate}%</span>'
            '</div>'
        )
    rules_html += '</div>'
    st.markdown(rules_html, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: PRICE FORECAST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Forecast MAE", f"{forecast_mae:.3f}", "DKK", CYAN, "Mean Absolute Error"), unsafe_allow_html=True)
    c2.markdown(metric_card("Current Spot", f"{current_price:.2f}", "kr/kWh", AMBER), unsafe_allow_html=True)
    c3.markdown(metric_card("Day Low", f"{price_min:.2f}", "kr/kWh", CYAN), unsafe_allow_html=True)
    c4.markdown(metric_card("Day High", f"{price_max:.2f}", "kr/kWh", RED), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    labels = [p['label'] for p in prices]

    # Forecast chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=labels, y=[p['upper'] for p in prices],
        mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=labels, y=[p['lower'] for p in prices],
        mode='lines', line=dict(width=0), fill='tonexty',
        fillcolor='rgba(17,138,178,0.12)', name='95% CI', hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=labels, y=[p['forecast'] for p in prices],
        mode='lines', line=dict(color=BLUE, width=2, dash='dash'), name='ML Forecast'))
    fig.add_trace(go.Scatter(x=labels, y=[p['actual'] for p in prices],
        mode='lines', line=dict(color=CYAN, width=2.5), name='Actual'))
    fig.add_hline(y=price_avg, line_dash="dot", line_color=T3, line_width=0.5)
    apply_layout(fig, height=320, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Error chart
    errors = [p['error'] for p in prices]
    colors = ['rgba(239,71,111,0.65)' if e > 0 else 'rgba(6,214,160,0.65)' for e in errors]
    fig2 = go.Figure(go.Bar(x=labels, y=errors, marker_color=colors,
        name='Error (DKK)', hovertemplate='%{x}: %{y:.3f} DKK<extra></extra>'))
    fig2.add_hline(y=0, line_color=T3, line_width=0.5)
    apply_layout(fig2, height=200)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: OPTIMIZER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.markdown('<div class="card-title">Optimization Parameters</div>', unsafe_allow_html=True)
    cc1, cc2, cc3, cc4, cc5, cc6 = st.columns(6)
    with cc1: battery_kwh = st.slider("Battery kWh", 20, 120, 75, 5)
    with cc2: current_soc = st.slider("Current SoC %", 5, 90, 20, 5)
    with cc3: target_soc = st.slider("Target SoC %", 50, 100, 80, 5)
    with cc4: charger_kw = st.slider("Charger kW", 3, 22, 11, 1)
    with cc5: departure_hour = st.slider("Departure Hour", 0, 23, 7, 1)
    with cc6: v2g_enabled = st.toggle("V2G Enabled", True)

    # Optimizer logic
    kwh_needed = battery_kwh * ((target_soc - current_soc) / 100)
    hours_needed = max(1, math.ceil(kwh_needed / charger_kw))
    sorted_cheap = sorted(prices, key=lambda p: p['actual'])
    sorted_exp = sorted(prices, key=lambda p: p['actual'], reverse=True)
    cheap_hours = [p['hour'] for p in sorted_cheap[:hours_needed]]
    v2g_hours = [p['hour'] for p in sorted_exp[:2] if p['hour'] not in cheap_hours] if v2g_enabled else []

    schedule = []
    for p in prices:
        is_charge = p['hour'] in cheap_hours
        is_v2g = p['hour'] in v2g_hours
        action = 'charge' if is_charge else 'v2g' if is_v2g else 'idle'
        power = charger_kw if is_charge else -charger_kw*0.6 if is_v2g else 0
        cost = p['actual']*charger_kw if is_charge else -(p['actual']*charger_kw*0.6) if is_v2g else 0
        schedule.append({**p, 'action': action, 'power': power, 'cost': cost})

    smart_cost = sum(s['cost'] for s in schedule if s['action'] == 'charge')
    v2g_revenue = abs(sum(s['cost'] for s in schedule if s['action'] == 'v2g'))
    avg_cost = price_avg * charger_kw * hours_needed
    saving = avg_cost - smart_cost
    saving_pct = (saving / avg_cost * 100) if avg_cost > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.markdown(metric_card("Smart Cost", f"{smart_cost:.1f}", "kr", CYAN, f"{hours_needed}h · {kwh_needed:.0f} kWh"), unsafe_allow_html=True)
    mc2.markdown(metric_card("Naive Cost", f"{avg_cost:.1f}", "kr", RED), unsafe_allow_html=True)
    mc3.markdown(metric_card("Savings", f"{saving:.1f}", "kr", CYAN, f"{saving_pct:.0f}% reduction"), unsafe_allow_html=True)
    if v2g_enabled:
        mc4.markdown(metric_card("V2G Revenue", f"{v2g_revenue:.1f}", "kr", PURPLE, "grid sell-back"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Schedule chart
    bar_colors = ['rgba(6,214,160,0.8)' if s['action']=='charge' else 'rgba(131,56,236,0.8)' if s['action']=='v2g' else 'rgba(74,85,104,0.12)' for s in schedule]
    fig3 = go.Figure(go.Bar(
        x=[s['label'] for s in schedule], y=[s['actual'] for s in schedule],
        marker_color=bar_colors, hovertemplate='%{x}: %{y:.2f} kr/kWh<extra></extra>'))
    fig3.add_hline(y=price_avg, line_dash="dot", line_color=T3, line_width=0.5)
    apply_layout(fig3, height=260)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    # Convergence
    rng = np.random.RandomState(99)
    conv_costs = [smart_cost + (avg_cost-smart_cost)*math.exp(-i*0.5) + rng.uniform(-1,1) for i in range(12)]
    fig4 = go.Figure(go.Scatter(
        x=[f'Iter {i+1}' for i in range(12)], y=conv_costs,
        mode='lines+markers', line=dict(color=CYAN, width=2),
        marker=dict(size=6, color=CYAN), hovertemplate='%{x}: %{y:.1f} kr<extra></extra>'))
    apply_layout(fig4, height=180)
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: V2G REVENUE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    monthly = v2g_revenue * 26
    annual = monthly * 12
    grid_contrib = charger_kw * 0.6 * 2

    vc1, vc2, vc3, vc4 = st.columns(4)
    vc1.markdown(metric_card("Daily V2G Revenue", f"{v2g_revenue:.1f}", "kr", PURPLE), unsafe_allow_html=True)
    vc2.markdown(metric_card("Monthly Projection", f"{monthly:.0f}", "kr", PURPLE, "~26 active days"), unsafe_allow_html=True)
    vc3.markdown(metric_card("Annual Earning", f"{annual/1000:.1f}", "k kr", CYAN), unsafe_allow_html=True)
    vc4.markdown(metric_card("Grid Contribution", f"{grid_contrib:.1f}", "kWh/day", BLUE, "flexibility provided"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    v2g_colors = ['rgba(6,214,160,0.75)' if s['action']=='charge' else 'rgba(131,56,236,0.75)' if s['action']=='v2g' else 'rgba(74,85,104,0.06)' for s in schedule]
    fig5 = go.Figure(go.Bar(
        x=[s['label'] for s in schedule], y=[s['power'] for s in schedule],
        marker_color=v2g_colors, hovertemplate='%{x}: %{y:+.1f} kW<extra></extra>'))
    fig5.add_hline(y=0, line_color=T3, line_width=0.8)
    apply_layout(fig5, height=260)
    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

    # Thesis
    tags = ''.join(f'<span class="badge badge-purple">{t}</span>' for t in [
        "Price Forecasting", "Rolling-Horizon Optimization",
        "V2G Arbitrage", "Data Quality Pipeline", "Sub-second Latency"])
    thesis_text = (
        "Every idle EV battery is untapped grid-scale flexibility. By forecasting spot prices "
        "with sub-minute ML inference, scheduling charge during wind-surplus lows, and selling "
        "back during demand peaks, each connected vehicle becomes a revenue-generating grid asset. "
        "Clean data is the foundation — millisecond-fresh, schema-validated, cross-source-consistent "
        "price feeds that the optimizer can trust unconditionally. The result: customers charge for "
        "less, earn from V2G, and the grid stays balanced without building new peaker plants."
    )
    thesis_html = (
        '<div class="thesis-card">'
        '<div class="thesis-title">⚡ THE ENKEL THESIS</div>'
        f'<div class="thesis-text">{thesis_text}</div>'
        f'<div class="tag-row">{tags}</div>'
        '</div>'
    )
    st.markdown(thesis_html, unsafe_allow_html=True)

# Footer
footer_html = (
    '<hr style="margin-top:40px;">'
    '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;'
    'font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#4a5568;padding-bottom:20px;">'
    '<span>Built by Umair Ali · Deep Tech Demo for Enkel</span>'
    '<span>Streamlit · Plotly · Rolling-Horizon Optimization · Real-time Data Pipeline</span>'
    '</div>'
)
st.markdown(footer_html, unsafe_allow_html=True)
