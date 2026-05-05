import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TRX Smart Predictor Pro", layout="wide")

# ၁။ Data Logic
def load_data():
    if os.path.exists("data.csv"):
        return pd.read_csv("data.csv")
    return pd.DataFrame(columns=["bs"])

def save_new_data(new_val):
    df = load_data()
    new_row = pd.DataFrame({"bs": [new_val]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("data.csv", index=False)
    st.cache_data.clear()

@st.cache_data
def get_prediction(selected_pat):
    df = load_data()
    if df.empty: return None
    data = df['bs'].tolist()
    m_b, m_s = 0, 0
    for i in range(len(data) - 4):
        pat = "".join(str(x) for x in data[i : i + 4])
        if pat == selected_pat:
            nxt = data[i + 4]
            if nxt == 'B': m_b += 1
            else: m_s += 1
    if m_b == 0 and m_s == 0: return None
    return "B" if m_b >= m_s else "S"

# ၂။ Session State
if 'recent_results' not in st.session_state:
    st.session_state.recent_results = []
if 'active_pattern' not in st.session_state:
    st.session_state.active_pattern = None
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None

# --- UI ---
st.title("🎯 TRX AI Smart Predictor")

# ၃။ Win/Loss Status Bar (HTML Error ပြင်ဆင်ပြီး)
st.subheader("🔥 Last 10 Sessions Status")
status_cols = st.columns(10)
results = st.session_state.recent_results

for i in range(10):
    with status_cols[i]:
        if i < len(results):
            res = results[i]
            color = "#28a745" if res == "W" else "#dc3545"
            st.markdown(f"""
                <div style="background-color:{color}; color:white; text-align:center; 
                padding:10px; border-radius:5px; font-weight:bold; border: 1px solid white;">
                {res}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color:#333; color:#555; text-align:center; 
                padding:10px; border-radius:5px; border: 1px solid #555;">
                -
                </div>
                """, unsafe_allow_html=True)

# ၄။ Pattern Buttons
st.divider()
all_pats = ["BBBB", "BBBS", "BBSS", "BSSS", "SSSS", "SSSB", "SSBB", "SBBB", 
            "BSBS", "SBSB", "BSSB", "SBBS", "BBSB", "SSBS", "BSBB", "SBSS"]

st.subheader("၁။ ဂိမ်းထဲက Pattern ကို နှိပ်ပါ")
cols = st.columns(4)
for idx, p in enumerate(all_pats):
    with cols[idx % 4]:
        if st.button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state.active_pattern = p
            st.session_state.current_prediction = get_prediction(p)

# ၅။ Prediction & Result Entry
if st.session_state.active_pattern:
    st.divider()
    pred = st.session_state.current_prediction
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.info(f"Selected: **{st.session_state.active_pattern}**")
        if pred:
            p_text = "BIG (B)" if pred == "B" else "SMALL (S)"
            p_color = "blue" if pred == "B" else "red"
            st.markdown(f"### AI Prediction: :{p_color}[{p_text}]")
        else:
            st.warning("Data မလုံလောက်သေးပါ။")

    with col_b:
        st.subheader("၂။ တကယ်ထွက်လာသည့် ရလဒ်ကို နှိပ်ပါ")
        rc1, rc2 = st.columns(2)
        
        def record_result(actual):
            if st.session_state.current_prediction:
                status = "W" if actual == st.session_state.current_prediction else "L"
                st.session_state.recent_results.append(status)
                if len(st.session_state.recent_results) > 10:
                    st.session_state.recent_results = st.session_state.recent_results[-10:]
            
            save_new_data(actual)
            st.session_state.active_pattern = None 
            st.session_state.current_prediction = None
            st.rerun()

        if rc1.button("Actually BIG (B)", key="real_b", use_container_width=True):
            record_result("B")
        if rc2.button("Actually SMALL (S)", key="real_s", use_container_width=True):
            record_result("S")

# Footer
with st.sidebar:
    st.write("### ⚙️ Session Info")
    if st.session_state.recent_results:
        w = st.session_state.recent_results.count("W")
        l = st.session_state.recent_results.count("L")
        st.write(f"Round Wins: **{w}**")
        st.write(f"Round Losses: **{l}**")
        if st.button("Reset Status Bar"):
            st.session_state.recent_results = []
            st.rerun()
