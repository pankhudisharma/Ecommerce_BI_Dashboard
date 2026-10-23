import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="E-Commerce BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM — soft grey canvas, white cards, charcoal text,
# and muted blue chart accents inspired by the reference image.
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --canvas: #E7E7E8;
        --card: #FFFFFF;
        --ink: #292B2D;
        --muted: #777B80;
        --line: #E5E6E7;
        --blue: #62A9DF;
        --blue-soft: #EAF4FB;
        --green: #2E9D63;
        --red: #D96B61;
    }

    /* App canvas and page spacing */
    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }
    [data-testid="stAppViewContainer"] {
        background: var(--canvas);
    }
    .block-container {
        max-width: 1600px;
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Hide Streamlit's default top chrome for a cleaner app-like page */
    header[data-testid="stHeader"] {
        background: rgba(231, 231, 232, 0.95);
    }
    div[data-testid="stToolbar"] {
        right: 1rem;
    }

    /* Typography */
    h1, h2, h3, h4 {
        color: var(--ink) !important;
        letter-spacing: -0.025em;
    }
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.15rem !important;
    }
    h2 {
        font-size: 1.15rem !important;
        font-weight: 650 !important;
    }
    h3 {
        font-size: 1rem !important;
        font-weight: 650 !important;
    }
    p, label, [data-testid="stCaptionContainer"] {
        color: #62666A;
    }

    /* Sidebar shell inspired by a modern commerce app */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E1E4E8;
        min-width: 245px;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1.15rem;
    }
    section[data-testid="stSidebar"] h2 {
        font-size: 1.02rem !important;
    }
    .brand-lockup {
        display:flex; align-items:center; gap:10px;
        padding: 8px 5px 18px 5px; margin-bottom:12px;
        border-bottom:1px solid #ECEEF0;
    }
    .brand-mark {
        width:38px; height:38px; display:flex; align-items:center;
        justify-content:center; border-radius:12px; background:#111318;
        color:#FFFFFF; font-size:19px; font-weight:800;
    }
    .brand-name { color:#202329; font-size:18px; font-weight:750; letter-spacing:-.04em; }
    .brand-caption { color:#8A9098; font-size:10px; margin-top:2px; }
    .nav-caption {
        color:#9298A1; font-size:10px; font-weight:800;
        letter-spacing:.12em; text-transform:uppercase;
        margin:16px 0 7px 5px;
    }
    .nav-link {
        display:flex; align-items:center; gap:13px;
        padding:11px 15px; margin:7px 0; border-radius:11px;
        color:#737985 !important; text-decoration:none !important;
        font-size:13px; font-weight:600;
        transition:all .15s ease;
    }
    .nav-link:hover { background:#F0F5FF; color:#283E68 !important; }
    .nav-link.active { background:#111318; color:#FFFFFF !important; }
    .nav-icon { width:22px; text-align:center; font-size:16px; }

    /* Minimal circular header controls inspired by the reference */
    .header-control-note {
        color:#777B80; font-size:11px; text-align:center;
    }
    .eyebrow {
        color: #626A74 !important;
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
        opacity: 1 !important;
    }
    .kpi-row-spacer { height: 22px; }
    div[data-testid="stTextInput"] input {
        min-height:42px;
        border-radius:24px !important;
        padding-left:15px !important;
    }
    div[data-testid="stButton"]:has(button[kind="secondary"]) button {
        width:42px; height:42px; min-height:42px;
        padding:0 !important;
        border-radius:50% !important;
        background:#FFFFFF !important;
        border:1px solid #E3E5E8 !important;
        color:#292B2D !important;
        box-shadow:0 1px 3px rgba(20,25,30,.04);
        font-size:17px !important;
    }
    div[data-testid="stButton"]:has(button[kind="secondary"]) button:hover {
        background:#EAF4FB !important;
        border-color:#BFDCEE !important;
    }
    /* All three header actions share the same circular button treatment. */
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
        width:42px !important; height:42px !important; min-height:42px !important;
        padding:0 !important; border-radius:50% !important;
        background:#FFFFFF !important; border:1px solid #E3E5E8 !important;
        color:#292B2D !important; box-shadow:0 1px 3px rgba(20,25,30,.05);
        font-size:17px !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
        background:#EAF4FB !important; border-color:#BFDCEE !important;
    }
    .top-header-row { margin-bottom: 0.25rem; }
    .nav-hint { color:#A0A5AD; font-size:10px; line-height:1.45; margin:5px 6px 15px; }

    /* Inputs: force a light appearance even if the browser/app theme is dark */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D9DADD !important;
        border-radius: 8px !important;
        color: #292B2D !important;
        min-height: 42px;
    }
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #292B2D;
    }
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background: #FFFFFF !important;
        color: #292B2D !important;
        border: 1px solid #D9DADD !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background: #FFFFFF !important;
        color: #292B2D !important;
    }
    li[role="option"] {
        color: #292B2D !important;
        background: #FFFFFF !important;
    }
    li[role="option"]:hover {
        background: #EAF4FB !important;
    }

    /* Metric cards */
    .kpi-card {
        min-height:112px; padding:15px 15px 13px;
        border:1px solid rgba(40,50,60,.045); border-radius:15px;
        box-shadow:0 3px 9px rgba(25,35,45,.025);
        overflow:hidden;
    }
    .kpi-label { color:#626A74; font-size:12px; font-weight:600; margin-bottom:12px; }
    .kpi-value { color:#202329; font-size:clamp(19px, 1.65vw, 27px); font-weight:760; letter-spacing:-.045em; line-height:1.12; white-space:nowrap; }
    .kpi-foot { color:#69717B; font-size:10px; margin-top:9px; }
    .kpi-blue { background:#E5F4F8; }
    .kpi-green { background:#EAF8ED; }
    .kpi-lavender { background:#EEF0FF; }
    .kpi-peach { background:#FFF0E6; }
    .kpi-yellow { background:#FFF7D9; }
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E3E4;
        border-radius: 12px;
        padding: 1rem 1.05rem;
        min-height: 112px;
        box-shadow: 0 2px 7px rgba(20, 25, 30, 0.025);
        gap: 0.25rem;
    }
    div[data-testid="stMetricLabel"] {
        color: #777B80 !important;
        font-size: 0.82rem !important;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        color: #292B2D !important;
        font-size: clamp(1.25rem, 1.7vw, 1.9rem) !important;
        font-weight: 700 !important;
        line-height: 1.2;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.75rem;
    }

    /* White panels around charts and tables */
    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #E2E3E4;
        border-radius: 12px;
        padding: 0.45rem;
        box-shadow: 0 2px 7px rgba(20, 25, 30, 0.025);
    }

    /* Streamlit alerts and expanders */
    div[data-testid="stAlert"] {
        border-radius: 9px;
    }
    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E2E3E4;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: #292B2D !important;
        border: 1px solid #D9DADD !important;
        border-radius: 8px !important;
        min-height: 40px;
        font-weight: 600;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #EAF4FB !important;
        border-color: #9CC9E8 !important;
        color: #285E83 !important;
    }

    hr {
        border-color: #D8D9DA;
    }

    /* Small labels used as section kickers */
    .eyebrow {
        color: #777B80;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .muted-note {
        color: #777B80;
        font-size: 0.82rem;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHART THEME HELPER
# ============================================================
BLUE = "#62A9DF"
DARK = "#3D4145"
GREY = "#B8BABC"
GREEN = "#42A879"
RED = "#D96B61"


def apply_chart_theme(fig, height=310):
    """Apply consistent colors, spacing, and gridlines to a Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color="#44484C", size=11),
        title=dict(font=dict(size=14, color="#292B2D"), x=0.02, xanchor="left"),
        margin=dict(l=18, r=18, t=48, b=22),
        hoverlabel=dict(
            bgcolor="#292B2D",
            bordercolor="#292B2D",
            font=dict(color="#FFFFFF", size=12),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=10),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#E2E3E4",
        tickfont=dict(color="#777B80", size=10),
        title_font=dict(color="#777B80", size=10),
        zerolinecolor="#E2E3E4",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#ECEDEE",
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(color="#777B80", size=10),
        title_font=dict(color="#777B80", size=10),
        zerolinecolor="#D9DADD",
    )
    return fig


def money(value):
    """Format money compactly for dashboard labels."""
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def chart_or_empty(data, message="No data available for the selected filters."):
    if data.empty:
        st.info(message)
        return True
    return False


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    data = pd.read_excel("data/raw/sample_-_superstore.xls")
    data = data.drop_duplicates(
        subset=[
            "Order ID",
            "Order Date",
            "Ship Date",
            "Customer ID",
            "Product ID",
            "Quantity",
            "Sales",
            "Discount",
            "Profit",
        ]
    ).copy()
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    data["Ship Date"] = pd.to_datetime(data["Ship Date"], errors="coerce")
    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "I couldn't find the Excel file. Make sure this file exists relative to "
        "dashboard.py: data/raw/sample_-_superstore.xls"
    )
    st.stop()
except Exception as exc:
    st.error(f"The dataset could not be loaded: {exc}")
    st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()


# ============================================================
# FILTERS — preserved and styled
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
          <div class="brand-mark">✦</div>
          <div><div class="brand-name">Business Dashboard</div>
          <div class="brand-caption">SALES & ANALYTICS</div></div>
        </div>
        <div class="nav-caption">Workspace</div>
        <a class="nav-link active" href="#dashboard-home"><span class="nav-icon">⌂</span>Overview</a>
        <a class="nav-link" href="#monthly-sales"><span class="nav-icon">▥</span>Analytics</a>
        <a class="nav-link" href="#product-performance"><span class="nav-icon">◇</span>Products</a>
        <a class="nav-link" href="#business-insights"><span class="nav-icon">◎</span>Insights</a>
        <a class="nav-link" href="#transaction-explorer"><span class="nav-icon">▤</span>Transactions</a>
        <div class="nav-hint">Choose a section to jump to it. Your filters below update the full dashboard.</div>
        <div class="nav-caption">Filters</div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Dashboard Filters")
    st.caption("All charts and KPIs update with your selections.")

    categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
    selected_category = st.selectbox("Product category", categories)

    regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
    selected_region = st.selectbox("Sales region", regions)

    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    selected_dates = st.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="YYYY/MM/DD",
    )

    st.divider()
    st.markdown("**Current selection**")
    st.caption(f"Category: {selected_category}")
    st.caption(f"Region: {selected_region}")
    st.caption("Date range: choose both a start and end date above.")

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.date.between(start_date, end_date)
    ]


# ============================================================
# HEADER — welcome, search, notifications, and theme preference
# ============================================================
header_left, header_search_icon, header_bell, header_theme = st.columns([7.2, 0.55, 0.55, 0.55], gap="medium")
with header_left:
    st.markdown('<div id="dashboard-home"></div><div class="eyebrow">YOUR STORE AT A GLANCE</div>', unsafe_allow_html=True)
    st.title("Welcome back!")
    st.caption("Here’s what’s happening with your business today.")

# Search is represented by the small circular icon in the header.
# Clicking it reveals the functional search field below the header.
if "show_dashboard_search" not in st.session_state:
    st.session_state.show_dashboard_search = False

with header_search_icon:
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    if st.button("⌕", key="search_toggle", help="Open dashboard search"):
        st.session_state.show_dashboard_search = not st.session_state.show_dashboard_search

with header_bell:
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    if st.button("♧", key="notification_bell", help="View dashboard notifications"):
        st.toast("You're all caught up — no new dashboard notifications.", icon="🔔")

with header_theme:
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    if "dashboard_dark_mode" not in st.session_state:
        st.session_state.dashboard_dark_mode = False
    current_theme_icon = "☀" if st.session_state.dashboard_dark_mode else "☼"
    if st.button(current_theme_icon, key="theme_toggle", help="Switch between light and dark theme"):
        st.session_state.dashboard_dark_mode = not st.session_state.dashboard_dark_mode
    theme_choice = "🌙 Dark" if st.session_state.dashboard_dark_mode else "☀️ Light"

search_query = ""
if st.session_state.show_dashboard_search:
    search_query = st.text_input(
        "Search dashboard",
        placeholder="Search products, customers, orders…",
        label_visibility="collapsed",
        key="dashboard_search_query",
    )

# Search narrows the same dataset used by the KPI cards and all charts.
if search_query.strip():
    query = search_query.strip().lower()
    searchable_columns = [c for c in ["Product Name", "Customer Name", "Customer ID", "Order ID", "Category", "Sub-Category", "Region", "State", "City"] if c in filtered_df.columns]
    matches = pd.Series(False, index=filtered_df.index)
    for column in searchable_columns:
        matches = matches | filtered_df[column].astype(str).str.lower().str.contains(query, na=False, regex=False)
    filtered_df = filtered_df[matches]

# Apply a coordinated dark palette when selected; Light remains the default.
if theme_choice == "🌙 Dark":
    st.markdown("""
    <style>
      :root { --canvas:#171A1F; --card:#22262D; --ink:#F2F4F7; --muted:#A7AFBA; --line:#373D46; }
      .stApp, [data-testid="stAppViewContainer"] { background:#171A1F !important; color:#F2F4F7 !important; }
      h1,h2,h3,h4,p,label,[data-testid="stCaptionContainer"] { color:#E7EAF0 !important; }
      section[data-testid="stSidebar"] { background:#20242B !important; border-right:1px solid #373D46 !important; }
      div[data-testid="stMetric"], div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"], div[data-testid="stExpander"] { background:#22262D !important; border-color:#373D46 !important; }
      div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"] { color:#F2F4F7 !important; }
      div[data-baseweb="select"] > div, div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input { background:#292E36 !important; color:#F2F4F7 !important; border-color:#414956 !important; }
      .brand-name { color:#F2F4F7 !important; }
      .kpi-label,.kpi-value,.kpi-foot { color:#202329 !important; }
    </style>
    """, unsafe_allow_html=True)
st.divider()


# ============================================================
# KPI SUMMARY
# ============================================================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
average_order_value = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

st.markdown('<div class="eyebrow">Executive summary</div>', unsafe_allow_html=True)
st.subheader("Business Overview")

kpi_cols = st.columns(5, gap="medium")
kpis = [
    ("Total Sales", f"${total_sales:,.0f}", "Revenue in current selection", "kpi-blue"),
    ("Total Profit", f"${total_profit:,.0f}", "Profit after recorded costs", "kpi-green"),
    ("Total Orders", f"{total_orders:,}", "Distinct orders", "kpi-lavender"),
    ("Customers", f"{total_customers:,}", "Distinct customers", "kpi-peach"),
    ("Average Order Value", f"${average_order_value:,.2f}", "Sales per order", "kpi-yellow"),
]
for col, (label, value, help_text, color_class) in zip(kpi_cols, kpis):
    with col:
        st.markdown(
            f'<div class="kpi-card {color_class}"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-foot">{help_text}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="kpi-row-spacer"></div>', unsafe_allow_html=True)
margin_col, selection_col = st.columns([1, 2], gap="large")
with margin_col:
    st.metric("Profit Margin", f"{profit_margin:.2f}%", help="Total profit divided by total sales.")
with selection_col:
    st.markdown(
        f"""
        <div style="height:100%;min-height:92px;background:#FFFFFF;border:1px solid #E2E3E4;
        border-radius:12px;padding:16px 18px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.08em;color:#777B80;
          text-transform:uppercase;margin-bottom:8px;">Active selection</div>
          <div style="font-size:14px;color:#292B2D;font-weight:600;">
          {selected_category} <span style="color:#B8BABC;">/</span> {selected_region}
          </div>
          <div style="font-size:12px;color:#777B80;margin-top:5px;">
          {len(filtered_df):,} transaction rows included in the current analysis
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")


# ============================================================
# MAIN CHARTS — compact two-column composition
# ============================================================
left_col, right_col = st.columns([0.95, 1.8], gap="medium")

with left_col:
    st.markdown('<div class="eyebrow">Profitability</div>', unsafe_allow_html=True)
    st.subheader("Profit by Category")
    if not chart_or_empty(filtered_df):
        category_profit = (
            filtered_df.groupby("Category", as_index=False)["Profit"]
            .sum()
            .sort_values("Profit", ascending=True)
        )
        fig_category = px.bar(
            category_profit,
            x="Profit",
            y="Category",
            orientation="h",
            text=category_profit["Profit"].map(money),
            color="Profit",
            color_continuous_scale=["#D96B61", "#E6E7E8", "#62A9DF"],
            title=None,
        )
        fig_category.update_traces(textposition="outside", cliponaxis=False)
        fig_category.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Profit ($)",
            yaxis_title="",
        )
        st.plotly_chart(apply_chart_theme(fig_category, 280), use_container_width=True)

    st.markdown('<div class="eyebrow">Business highlights</div>', unsafe_allow_html=True)
    st.subheader("Quick Insights")
    if filtered_df.empty:
        st.info("Select filters that contain data to view insights.")
    else:
        category_summary = filtered_df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        subcategory_summary = filtered_df.groupby("Sub-Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        region_summary = filtered_df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        discount_summary = filtered_df.groupby("Discount").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))

        best_category = category_summary["Profit"].idxmax()
        worst_subcategory = subcategory_summary["Profit"].idxmin()
        best_region = region_summary["Profit"].idxmax()
        loss_discounts = discount_summary[discount_summary["Profit"] < 0]

        st.markdown(
            f"""
            <div style="background:#FFFFFF;border:1px solid #E2E3E4;border-radius:10px;
            padding:13px 14px;margin-bottom:9px;">
              <div style="color:#777B80;font-size:11px;font-weight:700;text-transform:uppercase;
              letter-spacing:.06em;">Top category by profit</div>
              <div style="color:#292B2D;font-size:16px;font-weight:700;margin-top:5px;">{best_category}</div>
              <div style="color:#55585B;font-size:12px;margin-top:3px;">{money(category_summary.loc[best_category, 'Profit'])} profit</div>
            </div>
            <div style="background:#FFFFFF;border:1px solid #E2E3E4;border-radius:10px;
            padding:13px 14px;margin-bottom:9px;">
              <div style="color:#777B80;font-size:11px;font-weight:700;text-transform:uppercase;
              letter-spacing:.06em;">Largest subcategory loss / lowest profit</div>
              <div style="color:#292B2D;font-size:16px;font-weight:700;margin-top:5px;">{worst_subcategory}</div>
              <div style="color:{RED if subcategory_summary.loc[worst_subcategory, 'Profit'] < 0 else '#55585B'};font-size:12px;margin-top:3px;">{money(subcategory_summary.loc[worst_subcategory, 'Profit'])} profit</div>
            </div>
            <div style="background:#FFFFFF;border:1px solid #E2E3E4;border-radius:10px;
            padding:13px 14px;margin-bottom:9px;">
              <div style="color:#777B80;font-size:11px;font-weight:700;text-transform:uppercase;
              letter-spacing:.06em;">Top region by profit</div>
              <div style="color:#292B2D;font-size:16px;font-weight:700;margin-top:5px;">{best_region}</div>
              <div style="color:#55585B;font-size:12px;margin-top:3px;">{money(region_summary.loc[best_region, 'Profit'])} profit</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not loss_discounts.empty:
            worst_discount = loss_discounts["Profit"].idxmin()
            st.warning(
                f"Largest aggregate loss among discount groups: "
                f"{worst_discount:.0%} discount ({money(loss_discounts.loc[worst_discount, 'Profit'])})."
            )

with right_col:
    st.markdown('<div id="monthly-sales"></div><div class="eyebrow">Revenue performance</div>', unsafe_allow_html=True)
    st.subheader("Monthly Sales Trend")
    if not chart_or_empty(filtered_df):
        monthly_sales = (
            filtered_df.assign(Month=filtered_df["Order Date"].dt.to_period("M").dt.to_timestamp())
            .groupby("Month", as_index=False)["Sales"]
            .sum()
        )
        fig_monthly = px.line(
            monthly_sales,
            x="Month",
            y="Sales",
            markers=True,
            labels={"Month": "", "Sales": "Revenue ($)"},
            title=None,
        )
        fig_monthly.update_traces(
            line=dict(color=BLUE, width=3),
            marker=dict(color=BLUE, size=6),
            fill="tozeroy",
            fillcolor="rgba(98,169,223,0.10)",
            hovertemplate="%{x|%b %Y}<br>Revenue: $%{y:,.0f}<extra></extra>",
        )
        fig_monthly.update_yaxes(tickprefix="$", tickformat="~s")
        fig_monthly.update_layout(hovermode="x unified", showlegend=False)
        st.plotly_chart(apply_chart_theme(fig_monthly, 340), use_container_width=True)

    sub_left, sub_right = st.columns(2, gap="small")
    with sub_left:
        st.subheader("Regional Performance")
        if not chart_or_empty(filtered_df):
            region_data = (
                filtered_df.groupby("Region", as_index=False)
                .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
                .sort_values("Sales", ascending=True)
            )
            fig_region = px.bar(
                region_data,
                x="Sales",
                y="Region",
                orientation="h",
                color_discrete_sequence=[BLUE],
                labels={"Sales": "Sales ($)", "Region": ""},
                title=None,
            )
            fig_region.update_traces(hovertemplate="%{y}<br>Sales: $%{x:,.0f}<extra></extra>")
            fig_region.update_xaxes(tickprefix="$", tickformat="~s")
            st.plotly_chart(apply_chart_theme(fig_region, 260), use_container_width=True)

    with sub_right:
        st.subheader("Discount vs Profit")
        if not chart_or_empty(filtered_df):
            discount_data = (
                filtered_df.groupby("Discount", as_index=False)
                .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
                .sort_values("Discount")
            )
            discount_data["Discount (%)"] = discount_data["Discount"] * 100
            discount_data["Profit status"] = discount_data["Profit"].apply(
                lambda value: "Profit" if value >= 0 else "Loss"
            )
            fig_discount = px.bar(
                discount_data,
                x="Discount (%)",
                y="Profit",
                color="Profit status",
                color_discrete_map={"Profit": BLUE, "Loss": RED},
                labels={"Discount (%)": "Discount", "Profit": "Profit ($)"},
                title=None,
                hover_data={"Sales": ":,.0f"},
            )
            fig_discount.add_hline(y=0, line_dash="dot", line_color="#92969A")
            fig_discount.update_layout(showlegend=False)
            fig_discount.update_xaxes(ticksuffix="%")
            fig_discount.update_yaxes(tickprefix="$", tickformat="~s")
            st.plotly_chart(apply_chart_theme(fig_discount, 260), use_container_width=True)


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================
st.divider()
st.markdown('<div id="product-performance"></div><div class="eyebrow">Product performance</div>', unsafe_allow_html=True)
st.subheader("Sales vs Profit by Subcategory")

if not chart_or_empty(filtered_df):
    subcategory_data = (
        filtered_df.groupby("Sub-Category", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values("Sales", ascending=False)
    )
    fig_subcategory = px.bar(
        subcategory_data,
        x="Sub-Category",
        y=["Sales", "Profit"],
        barmode="group",
        color_discrete_sequence=[BLUE, GREY],
        labels={"Sub-Category": "", "value": "Amount ($)", "variable": "Metric"},
        title=None,
    )
    fig_subcategory.update_layout(hovermode="x unified")
    fig_subcategory.update_xaxes(tickangle=-35)
    fig_subcategory.update_yaxes(tickprefix="$", tickformat="~s")
    st.plotly_chart(apply_chart_theme(fig_subcategory, 350), use_container_width=True)

product_left, product_right = st.columns(2, gap="medium")
with product_left:
    st.subheader("Top 10 Profitable Products")
    if not chart_or_empty(filtered_df):
        product_profit = (
            filtered_df.groupby("Product Name", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .sort_values("Profit", ascending=False)
            .head(10)
            .sort_values("Profit", ascending=True)
        )
        fig_products = px.bar(
            product_profit,
            x="Profit",
            y="Product Name",
            orientation="h",
            color_discrete_sequence=[BLUE],
            labels={"Profit": "Profit ($)", "Product Name": ""},
            title=None,
            hover_data={"Sales": ":,.2f"},
        )
        fig_products.update_xaxes(tickprefix="$", tickformat="~s")
        st.plotly_chart(apply_chart_theme(fig_products, 390), use_container_width=True)

with product_right:
    st.subheader("Top 10 Loss-Making Products")
    if not chart_or_empty(filtered_df):
        product_losses = (
            filtered_df.groupby("Product Name", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        )
        product_losses = (
            product_losses[product_losses["Profit"] < 0]
            .sort_values("Profit", ascending=True)
            .head(10)
            .sort_values("Profit", ascending=False)
        )
        if product_losses.empty:
            st.info("No loss-making products found for the selected filters.")
        else:
            fig_losses = px.bar(
                product_losses,
                x="Profit",
                y="Product Name",
                orientation="h",
                color_discrete_sequence=[RED],
                labels={"Profit": "Profit / loss ($)", "Product Name": ""},
                title=None,
                hover_data={"Sales": ":,.2f"},
            )
            fig_losses.add_vline(x=0, line_dash="dot", line_color="#92969A")
            fig_losses.update_xaxes(tickprefix="$", tickformat="~s")
            st.plotly_chart(apply_chart_theme(fig_losses, 390), use_container_width=True)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================
st.divider()
st.markdown('<div id="business-insights"></div><div class="eyebrow">Decision support</div>', unsafe_allow_html=True)
st.subheader("Business Insights")

if filtered_df.empty:
    st.info("Select filters that contain data to view insights.")
else:
    insight_cols = st.columns(3, gap="small")
    category_summary = filtered_df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    subcategory_summary = filtered_df.groupby("Sub-Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    region_summary = filtered_df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    discount_summary = filtered_df.groupby("Discount").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))

    best_category = category_summary["Profit"].idxmax()
    worst_subcategory = subcategory_summary["Profit"].idxmin()
    best_region = region_summary["Profit"].idxmax()
    loss_discounts = discount_summary[discount_summary["Profit"] < 0]

    with insight_cols[0]:
        st.metric("Most Profitable Category", best_category, f"{money(category_summary.loc[best_category, 'Profit'])} profit")
    with insight_cols[1]:
        st.metric("Lowest-Profit Subcategory", worst_subcategory, f"{money(subcategory_summary.loc[worst_subcategory, 'Profit'])} profit")
    with insight_cols[2]:
        st.metric("Most Profitable Region", best_region, f"{money(region_summary.loc[best_region, 'Profit'])} profit")

    if not loss_discounts.empty:
        worst_discount = loss_discounts["Profit"].idxmin()
        st.warning(
            f"The {worst_discount:.0%} discount group has the largest total loss among the discount groups in this selection "
            f"({money(loss_discounts.loc[worst_discount, 'Profit'])}). This is an association, not proof that the discount alone caused the loss."
        )


# ============================================================
# FILTERED TRANSACTION DATA AND CSV EXPORT
# ============================================================
st.divider()
st.markdown('<div id="transaction-explorer"></div><div class="eyebrow">Transaction explorer</div>', unsafe_allow_html=True)
st.subheader("Explore Transaction Data")
st.caption("Review the records matching the current filters or export them for further analysis.")

if filtered_df.empty:
    st.info("No transactions are available for the selected filters.")
else:
    display_columns = [
        "Order ID",
        "Order Date",
        "Customer Name",
        "Category",
        "Sub-Category",
        "Product Name",
        "Region",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
    ]
    available_columns = [column for column in display_columns if column in filtered_df.columns]
    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        hide_index=True,
    )
    csv_data = filtered_df[available_columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_data,
        file_name="filtered_ecommerce_data.csv",
        mime="text/csv",
    )

st.caption("E-Commerce BI Dashboard · Built with Python, Pandas, Streamlit, and Plotly")
