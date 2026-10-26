import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Business Dashboard | Data Analytics",
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

    /* Completely remove Streamlit's default top header bar and toolbar (Deploy button, menu) */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    #MainMenu,
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
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
        display:flex; align-items:center; gap:11px;
        padding:10px 12px; margin:7px 0; border-radius:11px;
        color:#737985 !important; text-decoration:none !important;
        font-size:13px; font-weight:600;
        transition:all .15s ease;
    }
    .nav-link:hover { background:#F0F5FF; color:#283E68 !important; }
    .nav-link.active { background:#111318; color:#FFFFFF !important; }
    .nav-icon { width:20px; text-align:center; font-size:15px; }
    .nav-hint { color:#A0A5AD; font-size:10px; line-height:1.45; margin:5px 6px 15px; }

    div[data-testid="stFileUploader"] section { background:#FFFFFF !important; border:1px dashed #B9C7D4 !important; border-radius:12px !important; }
    div[data-testid="stFileUploader"] button { border-radius:9px !important; }

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
    /* Keep the date-picker calendar readable and clickable in either theme. */
    div[data-baseweb="calendar"],
    div[data-baseweb="datepicker"],
    div[data-baseweb="popover"] [role="dialog"] {
        background: #FFFFFF !important;
        color: #292B2D !important;
    }
    div[data-baseweb="calendar"] button {
        color: #292B2D !important;
        background: transparent;
        border-radius: 6px;
    }
    div[data-baseweb="calendar"] button:hover {
        background: #EAF4FB !important;
    }
    li[role="option"] {
        color: #292B2D !important;
        background: #FFFFFF !important;
    }
    li[role="option"]:hover {
        background: #EAF4FB !important;
    }

 
/* Minimal header controls — soft grey, circular icons, perfectly aligned */
.st-key-header_search_popover,
.st-key-header_bell_btn,
.st-key-header_theme_btn {
    display: inline-flex !important;
    align-items: center !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* All 3 Header Buttons: Search, Notification, Theme (Minimal Soft Grey Circular Buttons) */
.st-key-header_search_popover button,
.st-key-header_search_popover button[data-testid="stPopoverButton"],
.st-key-header_search_popover div[data-testid="stPopover"] > button,
.st-key-header_bell_btn button,
.st-key-header_bell_btn div[data-testid="stButton"] > button,
.st-key-header_theme_btn button,
.st-key-header_theme_btn div[data-testid="stButton"] > button {
    width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    border: 1px solid #D5D8DC !important;
    background: #E8EAED !important;
    color: #292B2D !important;
    box-shadow: none !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    transition: all 0.15s ease !important;
}

.st-key-header_search_popover button:hover,
.st-key-header_bell_btn button:hover,
.st-key-header_theme_btn button:hover {
    background: #DDE0E5 !important;
    border-color: #BFC3C8 !important;
    color: #111318 !important;
}

/* Material symbol styling inside circular buttons */
.st-key-header_search_popover span[data-testid="stIconMaterial"],
.st-key-header_bell_btn span[data-testid="stIconMaterial"],
.st-key-header_theme_btn span[data-testid="stIconMaterial"],
.st-key-header_search_popover .material-symbols-rounded,
.st-key-header_bell_btn .material-symbols-rounded,
.st-key-header_theme_btn .material-symbols-rounded {
    font-size: 19px !important;
    line-height: 1 !important;
    color: #292B2D !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
}

/* Hide chevron & label text in header buttons */
.st-key-header_search_popover button svg,
.st-key-header_search_popover button [data-testid="stIconMaterial"] ~ *,
.st-key-header_search_popover button p,
.st-key-header_bell_btn button p,
.st-key-header_theme_btn button p {
    display: none !important;
    margin: 0 !important;
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
# DATA UPLOAD + ADAPTIVE COLUMN DETECTION
# ============================================================
@st.cache_data(show_spinner=False)
def read_uploaded_file(file_name, file_bytes):
    """Read supported CSV/Excel files from uploaded bytes."""
    import io
    buffer = io.BytesIO(file_bytes)
    suffix = file_name.lower().rsplit(".", 1)[-1]
    if suffix == "csv":
        try:
            return pd.read_csv(buffer)
        except UnicodeDecodeError:
            buffer.seek(0)
            return pd.read_csv(buffer, encoding="latin-1")
    if suffix in ("xlsx", "xls"):
        return pd.read_excel(buffer)
    raise ValueError("Unsupported file type. Upload a CSV or Excel file.")


@st.cache_data(show_spinner=False)
def read_demo_file():
    data = pd.read_excel("data/raw/sample_-_superstore.xls")
    # Keep the original project's existing duplicate-removal logic when its
    # expected columns are available.
    duplicate_columns = [
        "Order ID", "Order Date", "Ship Date", "Customer ID", "Product ID",
        "Quantity", "Sales", "Discount", "Profit"
    ]
    if all(column in data.columns for column in duplicate_columns):
        data = data.drop_duplicates(subset=duplicate_columns).copy()
    return data


def clean_column_names(data):
    data = data.copy()
    data.columns = [str(column).strip() for column in data.columns]
    # Parse date-like columns only when the name or values strongly suggest dates.
    for column in data.columns:
        name = str(column).lower()
        if any(token in name for token in ("date", "time", "timestamp")):
            parsed = pd.to_datetime(data[column], errors="coerce")
            if parsed.notna().mean() >= 0.5:
                data[column] = parsed
    return data


def find_column(columns, aliases):
    """Return the first column matching a known name or alias."""
    lookup = {str(column).strip().lower(): column for column in columns}
    for alias in aliases:
        if alias in lookup:
            return lookup[alias]
    # Partial matching is useful for labels such as "Total Revenue", but
    # short/generic aliases (especially "date" and "time") cause false
    # positives such as matching "date" to "DailyRate". Keep it conservative.
    for alias in aliases:
        if len(alias) < 5 or alias in {"timestamp", "datetime"}:
            continue
        for lowered, original in lookup.items():
            if alias in lowered:
                return original
    return None


def detect_columns(data):
    cols = list(data.columns)
    mapping = {
        "sales": find_column(cols, [
            "sales", "revenue", "total revenue", "net sales", "amount",
            "total amount", "order value", "gross sales", "turnover"
        ]),
        "profit": find_column(cols, [
            "profit", "net profit", "gross profit", "earnings", "margin amount"
        ]),
        "date": find_column(cols, [
            "order date", "date", "transaction date", "sales date", "created at",
            "timestamp", "purchase date", "invoice date", "datetime"
        ]),
        "category": find_column(cols, [
            "category", "product category", "type", "department", "segment",
            "group", "product type"
        ]),
        "region": find_column(cols, [
            "region", "area", "territory", "market", "state", "country", "city"
        ]),
        "order": find_column(cols, [
            "order id", "order number", "transaction id", "invoice id",
            "purchase id", "order"
        ]),
        "customer": find_column(cols, [
            "customer id", "customer name", "client id", "client name", "customer"
        ]),
        "product": find_column(cols, [
            "product name", "product", "item name", "item", "product id", "sku"
        ]),
        "quantity": find_column(cols, [
            "quantity", "qty", "units sold", "units", "items sold"
        ]),
        "discount": find_column(cols, ["discount", "discount rate", "discount %"]),
    }

    # Infer a date column if its name was not recognized but its values are dates.
    if mapping["date"] is None:
        for column in cols:
            series = data[column]
            if pd.api.types.is_datetime64_any_dtype(series):
                mapping["date"] = column
                break

    numeric = [
        column for column in cols
        if pd.api.types.is_numeric_dtype(data[column])
        and not pd.api.types.is_bool_dtype(data[column])
    ]
    mapping["numeric"] = numeric
    # Avoid treating IDs as meaningful measures for charts and summary totals.
    mapping["measures"] = [
        column for column in numeric
        if not any(token in str(column).lower() for token in (
            " id", "_id", "postal", "zip", "phone", "year"
        ))
    ]
    mapping["sales"] = mapping["sales"] if mapping["sales"] in numeric else None
    mapping["profit"] = mapping["profit"] if mapping["profit"] in numeric else None
    mapping["quantity"] = mapping["quantity"] if mapping["quantity"] in numeric else None
    mapping["discount"] = mapping["discount"] if mapping["discount"] in numeric else None

    # Do not guess that an arbitrary numeric field (e.g. Age or DailyRate)
    # represents sales. Generic datasets get neutral descriptive statistics.
    return mapping


def format_value(value, column_name):
    name = str(column_name).lower()
    if any(token in name for token in ("sales", "revenue", "profit", "amount", "price", "cost", "income", "earnings")):
        return money(value)
    return f"{value:,.2f}" if isinstance(value, (int, float)) and not float(value).is_integer() else f"{value:,.0f}"


# ============================================================
# MINIMAL LANDING PAGE + DATASET SESSION
# No dashboard metrics or charts are shown until the user uploads a file.
# ============================================================
if "active_dataset_bytes" not in st.session_state:
    st.session_state.active_dataset_bytes = None
    st.session_state.active_dataset_name = None


def render_brand():
    st.markdown(
        """
        <div class="brand-lockup">
          <div class="brand-mark">✦</div>
          <div><div class="brand-name">Business Dashboard</div>
          <div class="brand-caption">DATA & ANALYTICS</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Show a clean upload-first experience until a valid dataset is selected.
if st.session_state.active_dataset_bytes is None:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display:none !important; }
        .block-container {
            max-width: 1320px !important;
            padding-top: 1.6rem !important;
            padding-bottom: 2rem !important;
        }
        .landing-nav {
            display:flex; align-items:center; gap:11px;
            padding: 2px 0 0; margin-bottom: 0;
        }
        .landing-mark {
            width:39px; height:39px; display:flex; align-items:center;
            justify-content:center; border-radius:12px; background:#111318;
            color:#fff; font-size:21px; flex-shrink:0;
        }
        .landing-brand { color:#202329; font-size:18px; font-weight:800; letter-spacing:-.04em; }
        .landing-tag { color:#8A9098; font-size:10px; letter-spacing:.12em; font-weight:700; margin-top:2px; }
        .landing-stage {
            position:relative; min-height:390px; display:flex; align-items:center;
            justify-content:center; padding:24px 0 8px; overflow:hidden;
        }
        .landing-hero { position:relative; z-index:2; width:min(100%, 720px); text-align:center; }
        .landing-eyebrow {
            color:#6B91B4; font-size:11px; font-weight:800; letter-spacing:.18em;
            text-transform:uppercase; margin-bottom:18px;
        }
        .landing-title {
            color:#15171A; font-size:clamp(2.6rem, 5vw, 4.7rem); line-height:1.04;
            letter-spacing:-.065em; font-weight:780; margin:0 0 18px;
        }
        .landing-title span { color:#9A9DA1; font-weight:500; }
        .landing-subtitle {
            color:#777D84; font-size:16px; line-height:1.6;
            max-width:540px; margin:0 auto 10px;
        }
        .upload-instruction { display:none; }
        .landing-upload-area { max-width:300px; margin:-54px auto 0; position:relative; z-index:3; }
        .landing-upload-label { display:none; }
        .landing-upload-card { background:transparent; border:0; border-radius:0; padding:0; box-shadow:none; }
        .landing-footnote { display:none; }
        .float-card {
            position:absolute; z-index:1; background:rgba(255,255,255,.88);
            border:1px solid #E7EAED; border-radius:17px;
            box-shadow:0 16px 40px rgba(31,43,55,.055); padding:16px;
            color:#6F7780; font-size:11px;
        }
        .float-card .card-title { font-weight:700; color:#41474E; font-size:12px; margin-bottom:12px; }
        .mini-bars { display:flex; align-items:end; gap:7px; height:62px; }
        .mini-bars i { display:block; width:13px; border-radius:4px 4px 2px 2px; background:#A9D2F0; }
        .mini-bars i:nth-child(2n) { background:#B9DCC9; }
        .mini-line { height:52px; display:flex; align-items:center; }
        .mini-line svg { width:100%; height:48px; }
        .float-left { left:3%; top:23%; width:190px; transform:rotate(-5deg); }
        .float-right { right:3%; bottom:19%; width:205px; transform:rotate(4deg); }
        .float-chip { display:inline-flex; padding:5px 8px; border-radius:7px; background:#F0F6FA; color:#5687AD; font-weight:700; margin-top:9px; }
        div[data-testid="stFileUploader"] section {
            background:transparent !important; border:0 !important;
            border-radius:0 !important; padding:0 !important; min-height:0 !important;
            display:flex !important; flex-direction:column !important; align-items:center !important;
        }
        div[data-testid="stFileUploader"] section > div:first-child { display:none !important; }
        div[data-testid="stFileUploader"] button {
            border-radius:10px !important; background:#111318 !important;
            color:#fff !important; border:1px solid #111318 !important;
            min-height:44px !important; padding:0 34px !important;
            font-weight:650 !important; box-shadow:none !important;
        }
        div[data-testid="stFileUploader"] button span { display:none !important; }
        div[data-testid="stFileUploader"] button::after {
            content:"Upload"; color:#fff; font-size:14px; font-weight:650;
        }
        div[data-testid="stFileUploader"] small { display:none !important; }
        div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] { display:none !important; }
        @media (max-width: 900px) {
            .landing-stage { min-height:350px; }
            .landing-upload-area { margin-top:-40px; }
            .float-left { left:-3%; top:8%; transform:scale(.82) rotate(-5deg); }
            .float-right { right:-4%; bottom:7%; transform:scale(.82) rotate(4deg); }
        }
        @media (max-width: 620px) {
            .landing-stage { min-height:330px; padding-top:28px; }
            .landing-upload-area { margin-top:-32px; }
            .float-card { opacity:.25; transform:scale(.72); }
            .float-left { left:-65px; top:0; }
            .float-right { right:-70px; bottom:0; }
            .landing-subtitle { font-size:14px; padding:0 10px; }
        }
        </style>
        <div class="landing-nav">
          <div class="landing-mark">✦</div>
          <div><div class="landing-brand">Business Dashboard</div><div class="landing-tag">DATA & ANALYTICS</div></div>
        </div>
        <div class="landing-stage">
          <div class="float-card float-left">
            <div class="card-title">Performance overview</div>
            <div class="mini-bars"><i style="height:34%"></i><i style="height:56%"></i><i style="height:45%"></i><i style="height:78%"></i><i style="height:64%"></i><i style="height:95%"></i><i style="height:72%"></i></div>
            <div style="margin-top:9px;color:#9AA1A8">A clearer view of your data</div>
          </div>
          <div class="float-card float-right">
            <div class="card-title">Trends at a glance</div>
            <div class="mini-line"><svg viewBox="0 0 180 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2 39 L29 30 L54 34 L80 15 L105 23 L132 9 L158 15 L178 3" stroke="#76B7E5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 39 L29 30 L54 34 L80 15 L105 23 L132 9 L158 15 L178 3 L178 48 L2 48 Z" fill="#EAF4FB"/></svg></div>
            <div class="float-chip">Insights, made simple</div>
          </div>
          <div class="landing-hero">
            <div class="landing-eyebrow">Your data. One clear view.</div>
            <div class="landing-title">Make your data<br><span>make sense.</span></div>
            <div class="landing-subtitle">Upload your dataset to uncover patterns, explore interactive charts, and find the insights that matter.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, landing_upload_col, _ = st.columns([1, 1.15, 1])
    with landing_upload_col:
        st.markdown('<div class="landing-upload-area"><div class="landing-upload-card">', unsafe_allow_html=True)
        landing_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            help="Supported formats: CSV, XLSX, and XLS.",
            key="landing_dataset_uploader",
            label_visibility="collapsed",
        )
        st.markdown('</div></div>', unsafe_allow_html=True)
    if landing_file is not None:
        try:
            preview_df = read_uploaded_file(landing_file.name, landing_file.getvalue())
            if preview_df.empty:
                st.error("This file appears to be empty. Please choose a dataset with rows and columns.")
            else:
                st.session_state.active_dataset_bytes = landing_file.getvalue()
                st.session_state.active_dataset_name = landing_file.name
                st.session_state.pop("dataset_uploader", None)
                st.rerun()
        except Exception as exc:
            st.error(f"We couldn't read this file: {exc}")
    st.stop()

# Once a dataset is active, show the dashboard sidebar and allow replacing it.
with st.sidebar:
    render_brand()
    if st.button("← Home / Upload new dataset", key="return_to_landing", use_container_width=True):
        st.session_state.active_dataset_bytes = None
        st.session_state.active_dataset_name = None
        # Clear uploader widget state so the same file can be selected again.
        st.session_state.pop("dataset_uploader", None)
        st.session_state.pop("landing_dataset_uploader", None)
        st.rerun()
    st.markdown(
        """
        <div class="nav-caption">Workspace</div>
        <a class="nav-link active" href="#dashboard-home"><span class="nav-icon">⌂</span>Overview</a>
        <a class="nav-link" href="#analytics"><span class="nav-icon">▥</span>Analytics</a>
        <a class="nav-link" href="#business-insights"><span class="nav-icon">◎</span>Insights</a>
        <a class="nav-link" href="#transaction-explorer"><span class="nav-icon">▤</span>Data Explorer</a>
        <div class="nav-hint">Upload another dataset at any time to refresh the dashboard.</div>
        <div class="nav-caption">Dataset</div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Replace dataset",
        type=["csv", "xlsx", "xls"],
        help="Upload another CSV or Excel file to replace the current dataset.",
        key="dataset_uploader",
    )
    if uploaded_file is not None:
        st.session_state.active_dataset_bytes = uploaded_file.getvalue()
        st.session_state.active_dataset_name = uploaded_file.name
    try:
        df = read_uploaded_file(
            st.session_state.active_dataset_name,
            st.session_state.active_dataset_bytes,
        )
        data_source_label = st.session_state.active_dataset_name
    except Exception as exc:
        st.error(f"Couldn't read this file: {exc}")
        st.stop()

    st.caption(f"Source: {data_source_label}")
    st.divider()
    st.header("Dashboard Filters")
    st.caption("Filters apply to the current dataset.")

if df.empty:
    st.error("The selected dataset is empty.")
    st.stop()

df = clean_column_names(df)
# Drop completely empty rows/columns without assuming a fixed schema.
df = df.dropna(axis=0, how="all").dropna(axis=1, how="all").copy()
if df.empty:
    st.error("The selected dataset contains no usable records.")
    st.stop()

mapping = detect_columns(df)

# Build only the filters that the current data supports.
selected_category = "All"
selected_region = "All"
selected_start_date = None
selected_end_date = None

with st.sidebar:
    category_col = mapping["category"]
    region_col = mapping["region"]
    date_col = mapping["date"]

    if category_col is not None and df[category_col].nunique(dropna=True) <= 300:
        categories = ["All"] + sorted(df[category_col].dropna().astype(str).unique().tolist())
        selected_category = st.selectbox(f"{category_col}", categories, key="filter_category")
    if region_col is not None and region_col != category_col and df[region_col].nunique(dropna=True) <= 300:
        regions = ["All"] + sorted(df[region_col].dropna().astype(str).unique().tolist())
        selected_region = st.selectbox(f"{region_col}", regions, key="filter_region")

    if date_col is not None:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        valid_dates = df[date_col].dropna()
        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            selected_start_date = st.date_input(
                "Start date", value=min_date, min_value=min_date, max_value=max_date,
                format="YYYY/MM/DD", key="filter_start_date"
            )
            selected_end_date = st.date_input(
                "End date", value=max_date, min_value=min_date, max_value=max_date,
                format="YYYY/MM/DD", key="filter_end_date"
            )

    st.divider()
    st.markdown("**Current selection**")
    st.caption(f"Category: {selected_category}" if category_col is not None else "Category filter: not available")
    st.caption(f"Region: {selected_region}" if region_col is not None else "Region filter: not available")
    if selected_start_date is not None and selected_end_date is not None:
        st.caption(f"Date range: {selected_start_date:%Y/%m/%d} – {selected_end_date:%Y/%m/%d}")
    else:
        st.caption("Date filter: not available")

filtered_df = df.copy()
if category_col is not None and selected_category != "All":
    filtered_df = filtered_df[filtered_df[category_col].astype(str) == selected_category]
if region_col is not None and selected_region != "All":
    filtered_df = filtered_df[filtered_df[region_col].astype(str) == selected_region]
if date_col is not None and selected_start_date is not None and selected_end_date is not None:
    if selected_start_date <= selected_end_date:
        filtered_df = filtered_df[
            filtered_df[date_col].dt.date.between(selected_start_date, selected_end_date)
        ]
    else:
        st.sidebar.warning("Start date must be on or before the end date.")
        filtered_df = filtered_df.iloc[0:0]

# Header controls — retain the existing visual style.
header_left, header_search, header_bell, header_theme = st.columns(
    [3.65, 0.45, 0.45, 0.45], vertical_alignment="center", gap="small"
)
with header_left:
    st.markdown('<div id="dashboard-home"></div><div class="eyebrow">YOUR DATA AT A GLANCE</div>', unsafe_allow_html=True)
    st.title("Welcome back!")
    st.caption(f"Explore insights from {data_source_label}.")
with header_search:
    with st.popover("", icon=":material/search:", help="Search the current dataset", key="header_search_popover"):
        search_query = st.text_input("Search", placeholder="Search records…", label_visibility="collapsed", key="header_search_query")
with header_bell:
    if st.button("", icon=":material/notifications:", help="View dashboard notifications", key="header_bell_btn"):
        st.toast("You're all caught up — no new dashboard notifications.", icon="🔔")
with header_theme:
    if "is_dark_mode" not in st.session_state:
        st.session_state.is_dark_mode = False
    current_theme_icon = ":material/dark_mode:" if st.session_state.is_dark_mode else ":material/light_mode:"
    current_help = "Switch to light theme" if st.session_state.is_dark_mode else "Switch to dark theme"
    if st.button("", icon=current_theme_icon, key="header_theme_btn", help=current_help):
        st.session_state.is_dark_mode = not st.session_state.is_dark_mode
        st.rerun()
    theme_choice = "🌙 Dark" if st.session_state.is_dark_mode else "☼ Light"

if search_query.strip():
    query = search_query.strip().lower()
    searchable_columns = [
        column for column in filtered_df.columns
        if not pd.api.types.is_datetime64_any_dtype(filtered_df[column])
    ]
    matches = pd.Series(False, index=filtered_df.index)
    for column in searchable_columns:
        matches |= filtered_df[column].astype(str).str.lower().str.contains(query, na=False, regex=False)
    filtered_df = filtered_df[matches]

if "Dark" in theme_choice:
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
      .st-key-header_search_popover button, .st-key-header_bell_btn button, .st-key-header_theme_btn button { background:#282C34 !important; border-color:#3E4450 !important; color:#F2F4F7 !important; }
      .st-key-header_search_popover span[data-testid="stIconMaterial"], .st-key-header_bell_btn span[data-testid="stIconMaterial"], .st-key-header_theme_btn span[data-testid="stIconMaterial"] { color:#F2F4F7 !important; }
    </style>
    """, unsafe_allow_html=True)
st.divider()

# ============================================================
# ADAPTIVE KPI SUMMARY
# ============================================================
st.markdown('<div class="eyebrow">Executive summary</div>', unsafe_allow_html=True)
st.subheader("Dataset Overview")

sales_col = mapping["sales"]
profit_col = mapping["profit"]
order_col = mapping["order"]
customer_col = mapping["customer"]
quantity_col = mapping["quantity"]
numeric_measures = mapping["measures"]

kpis = []
if sales_col is not None:
    kpis.append((f"Total {sales_col}", format_value(pd.to_numeric(filtered_df[sales_col], errors="coerce").sum(), sales_col), "Sum in current selection", "kpi-blue"))
if profit_col is not None:
    kpis.append((f"Total {profit_col}", format_value(pd.to_numeric(filtered_df[profit_col], errors="coerce").sum(), profit_col), "Sum in current selection", "kpi-green"))
if order_col is not None:
    kpis.append(("Unique Orders", f"{filtered_df[order_col].nunique(dropna=True):,}", f"Distinct {order_col}", "kpi-lavender"))
if customer_col is not None:
    kpis.append(("Unique Customers", f"{filtered_df[customer_col].nunique(dropna=True):,}", f"Distinct {customer_col}", "kpi-peach"))
if quantity_col is not None:
    kpis.append((f"Total {quantity_col}", format_value(pd.to_numeric(filtered_df[quantity_col], errors="coerce").sum(), quantity_col), "Sum in current selection", "kpi-yellow"))
if not kpis:
    # Generic datasets: show record count and descriptive statistics rather
    # than pretending the first numeric column is sales.
    kpis.append(("Records", f"{len(filtered_df):,}", "Rows in current selection", "kpi-blue"))
    for index, measure in enumerate(numeric_measures[:4]):
        values = pd.to_numeric(filtered_df[measure], errors="coerce").dropna()
        if not values.empty:
            kpis.append((f"Average {measure}", format_value(values.mean(), measure), "Mean in current selection", ["kpi-green", "kpi-lavender", "kpi-peach", "kpi-yellow"][index]))

kpi_cols = st.columns(min(len(kpis), 5), gap="small")
for col, (label, value, help_text, color_class) in zip(kpi_cols, kpis[:5]):
    with col:
        st.markdown(
            f'<div class="kpi-card {color_class}"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-foot">{help_text}</div></div>',
            unsafe_allow_html=True,
        )

if sales_col is not None and profit_col is not None:
    total_sales = pd.to_numeric(filtered_df[sales_col], errors="coerce").sum()
    total_profit = pd.to_numeric(filtered_df[profit_col], errors="coerce").sum()
    profit_margin = total_profit / total_sales * 100 if total_sales else 0
    st.metric("Profit Margin", f"{profit_margin:.2f}%", help=f"{profit_col} divided by {sales_col}.")
st.caption(f"{len(filtered_df):,} rows · {len(filtered_df.columns):,} columns · Source: {data_source_label}")
st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

# ============================================================
# ADAPTIVE ANALYTICS
# ============================================================
st.markdown('<div id="analytics"></div><div class="eyebrow">Explore your data</div>', unsafe_allow_html=True)
st.subheader("Analytics")

if filtered_df.empty:
    st.info("No records match the current filters.")
else:
    chart_count = 0
    # A time trend is shown when a date and numeric measure are available.
    if date_col is not None and sales_col is not None:
        time_data = filtered_df[[date_col, sales_col]].copy()
        time_data[sales_col] = pd.to_numeric(time_data[sales_col], errors="coerce")
        time_data = time_data.dropna(subset=[date_col, sales_col])
        if not time_data.empty:
            time_data["__period"] = time_data[date_col].dt.to_period("M").dt.to_timestamp()
            time_data = time_data.groupby("__period", as_index=False)[sales_col].sum()
            fig = px.line(time_data, x="__period", y=sales_col, markers=True, title=f"{sales_col} over time")
            fig.update_traces(line=dict(color=BLUE, width=3), marker=dict(color=BLUE, size=6))
            fig.update_layout(xaxis_title="", yaxis_title=sales_col, hovermode="x unified")
            st.plotly_chart(apply_chart_theme(fig, 330), use_container_width=True)
            chart_count += 1

    # Grouped measure chart: category first, then region/location-like dimension.
    dimension_col = category_col or region_col
    if dimension_col is not None and sales_col is not None and filtered_df[dimension_col].nunique(dropna=True) <= 100:
        grouped = filtered_df.groupby(dimension_col, dropna=True, as_index=False)[sales_col].sum()
        grouped = grouped.sort_values(sales_col, ascending=True).tail(20)
        if not grouped.empty:
            left, right = st.columns([1.1, 1], gap="medium")
            with left:
                fig = px.bar(grouped, x=sales_col, y=dimension_col, orientation="h",
                             color_discrete_sequence=[BLUE], title=f"{sales_col} by {dimension_col}")
                fig.update_layout(xaxis_title=sales_col, yaxis_title="")
                st.plotly_chart(apply_chart_theme(fig, 320), use_container_width=True)
            chart_count += 1
            if profit_col is not None and profit_col != sales_col:
                grouped_profit = filtered_df.groupby(dimension_col, dropna=True, as_index=False)[profit_col].sum()
                grouped_profit = grouped_profit.sort_values(profit_col, ascending=True).tail(20)
                with right:
                    fig = px.bar(grouped_profit, x=profit_col, y=dimension_col, orientation="h",
                                 color=profit_col, color_continuous_scale=["#D96B61", "#E6E7E8", "#62A9DF"],
                                 title=f"{profit_col} by {dimension_col}")
                    fig.update_layout(coloraxis_showscale=False, xaxis_title=profit_col, yaxis_title="")
                    st.plotly_chart(apply_chart_theme(fig, 320), use_container_width=True)
                chart_count += 1
            else:
                with right:
                    st.markdown("**Available numeric fields**")
                    st.write(", ".join(map(str, numeric_measures)) if numeric_measures else "No numeric measure columns detected.")

    # Generic dataset fallback: chart useful distributions and category counts,
    # even when the file has no sales, profit, or date fields.
    if sales_col is None:
        categorical_cols = [
            c for c in filtered_df.columns
            if not pd.api.types.is_numeric_dtype(filtered_df[c])
            and not pd.api.types.is_datetime64_any_dtype(filtered_df[c])
            and 1 < filtered_df[c].nunique(dropna=True) <= 30
        ]
        numeric_candidates = [c for c in numeric_measures if filtered_df[c].nunique(dropna=True) > 1]
        left, right = st.columns(2, gap="medium")
        if numeric_candidates:
            measure = numeric_candidates[0]
            values = pd.to_numeric(filtered_df[measure], errors="coerce").dropna()
            if not values.empty:
                with left:
                    fig = px.histogram(values.to_frame(name=measure), x=measure, nbins=25,
                                       title=f"Distribution of {measure}", color_discrete_sequence=[BLUE])
                    st.plotly_chart(apply_chart_theme(fig, 320), use_container_width=True)
                chart_count += 1
        if categorical_cols:
            dimension = next((c for c in categorical_cols if c != category_col), categorical_cols[0])
            counts = filtered_df[dimension].astype(str).value_counts().head(12).sort_values().reset_index()
            counts.columns = [dimension, "Record count"]
            with right:
                fig = px.bar(counts, x="Record count", y=dimension, orientation="h",
                             title=f"Records by {dimension}", color_discrete_sequence=[BLUE])
                fig.update_layout(xaxis_title="Number of records", yaxis_title="")
                st.plotly_chart(apply_chart_theme(fig, 320), use_container_width=True)
            chart_count += 1
        if len(numeric_candidates) >= 2:
            measure = numeric_candidates[1]
            values = pd.to_numeric(filtered_df[measure], errors="coerce").dropna()
            if not values.empty:
                fig = px.histogram(values.to_frame(name=measure), x=measure, nbins=25,
                                   title=f"Distribution of {measure}", color_discrete_sequence=["#62A9DF"])
                st.plotly_chart(apply_chart_theme(fig, 300), use_container_width=True)
                chart_count += 1

    if chart_count == 0:
        st.info("No suitable chart could be generated automatically from the detected columns. The data table below is still available.")
    with st.expander("Detected columns and data types"):
        profile = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data type": [str(df[column].dtype) for column in df.columns],
            "Non-empty values": [int(df[column].notna().sum()) for column in df.columns],
            "Unique values": [int(df[column].nunique(dropna=True)) for column in df.columns],
        })
        st.dataframe(profile, use_container_width=True, hide_index=True)

# ============================================================
# BUSINESS INSIGHTS — only generate claims supported by columns
# ============================================================
st.divider()
st.markdown('<div id="business-insights"></div><div class="eyebrow">Decision support</div>', unsafe_allow_html=True)
st.subheader("Business Insights")
if filtered_df.empty:
    st.info("Select filters that contain data to view insights.")
else:
    insights = []
    if category_col is not None and profit_col is not None:
        summary = filtered_df.groupby(category_col, dropna=True)[profit_col].sum()
        if not summary.empty:
            insights.append(("Highest total profit", str(summary.idxmax()), format_value(summary.max(), profit_col)))
            insights.append(("Lowest total profit", str(summary.idxmin()), format_value(summary.min(), profit_col)))
    elif category_col is not None and sales_col is not None:
        summary = filtered_df.groupby(category_col, dropna=True)[sales_col].sum()
        if not summary.empty:
            insights.append(("Highest total " + str(sales_col), str(summary.idxmax()), format_value(summary.max(), sales_col)))
    if region_col is not None and region_col != category_col and sales_col is not None:
        summary = filtered_df.groupby(region_col, dropna=True)[sales_col].sum()
        if not summary.empty:
            insights.append(("Top " + str(region_col) + " by " + str(sales_col), str(summary.idxmax()), format_value(summary.max(), sales_col)))
    if date_col is not None and sales_col is not None:
        dated = filtered_df.dropna(subset=[date_col]).copy()
        if not dated.empty:
            dated["__year"] = dated[date_col].dt.year
            yearly = dated.groupby("__year")[sales_col].sum()
            if not yearly.empty:
                insights.append(("Best year by " + str(sales_col), str(yearly.idxmax()), format_value(yearly.max(), sales_col)))
    if not insights and numeric_measures:
        for measure in numeric_measures[:3]:
            values = pd.to_numeric(filtered_df[measure], errors="coerce").dropna()
            if not values.empty:
                insights.append((f"Average {measure}", format_value(values.mean(), measure),
                                 f"Min {format_value(values.min(), measure)} · Max {format_value(values.max(), measure)}"))
    if not insights:
        for dimension in [c for c in filtered_df.columns if not pd.api.types.is_numeric_dtype(filtered_df[c]) and not pd.api.types.is_datetime64_any_dtype(filtered_df[c]) and 1 < filtered_df[c].nunique(dropna=True) <= 100][:2]:
            counts = filtered_df[dimension].dropna().astype(str).value_counts()
            if not counts.empty:
                insights.append((f"Most common {dimension}", str(counts.index[0]), f"{int(counts.iloc[0]):,} records"))
    if insights:
        insight_cols = st.columns(min(3, len(insights)), gap="small")
        for index, item in enumerate(insights):
            with insight_cols[index % len(insight_cols)]:
                st.metric(item[0], item[1], item[2])
    else:
        st.info("There aren't enough recognized category, region, date, or profit fields to create meaningful business insights for this dataset.")

# ============================================================
# DATA EXPLORER + EXPORT
# ============================================================
st.divider()
st.markdown('<div id="transaction-explorer"></div><div class="eyebrow">Data explorer</div>', unsafe_allow_html=True)
st.subheader("Explore Dataset")
st.caption("Review the filtered records or export them for further analysis.")
if filtered_df.empty:
    st.info("No records are available for the current selection.")
else:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    safe_name = "".join(char if char.isalnum() or char in "-_" else "_" for char in data_source_label.rsplit(".", 1)[0])
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_data,
        file_name=f"{safe_name or 'filtered_dataset'}.csv",
        mime="text/csv",
    )

st.caption("Business Dashboard · Built with Python, Pandas, Streamlit, and Plotly")
