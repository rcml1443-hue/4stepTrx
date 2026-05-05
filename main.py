import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pattern Pro Tracker", layout="wide")

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

# ၂။ Session State (Pattern တစ်ခုချင်းစီအတွက် History သိမ်းဆည်းရန်)
if 'pattern_histories' not in st.session_state:
    st.session_state.pattern_histories = {} # {'BBBB': ['W', 'L'], 'SSSS': ['W']}
if 'active_pattern' not in st.session_state:
    st.session_state.active_pattern = None
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None

# --- UI ---
st.title("🎯 TRX Pattern-Specific Tracker")
st.write("Pattern တစ်ခုချင်းစီရဲ့ အပေါ်မှာ အရင်က နိုင်/ရှုံး မှတ်တမ်းကို ကြည့်နိုင်ပါတယ်")

# ၃။ Pattern Grid (Pattern တစ်ခုချင်းစီအတွက် Box နဲ့ History)
all_pats = ["BBBB", "BBBS", "BBSS", "BSSS", "SSSS", "SSSB", "SSBB", "SBBB", 
            "BSBS", "SBSB", "BSSB", "SBBS", "BBSB", "SSBS", "BSBB", "SBSS"]

cols = st.columns(4)
for idx, p in enumerate(all_pats):
    with cols[idx % 4]:
        # အပေါ်က History အစိမ်း/အနီ အစက်လေးများ ပြရန်
        history = st.session_state.pattern_histories.get(p, [])
        # နောက်ဆုံး ၅ ခုပဲ အစက်ပြမယ်
        history_display = ""
        for h in history[-5:]:
            color = "🟢" if h == "W" else "🔴"
            history_display += color
        
        st.write(f"Record: {history_display if history_display else '➖'}")
        
        if st.button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state.active_pattern = p
            st.session_state.current_prediction = get_prediction(p)

# ၄။ Prediction & Entry
if st.session_state.active_pattern:
    st.divider()
    p = st.session_state.active_pattern
    pred = st.session_state.current_prediction
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.info(f"Selected: **{p}**")
        if pred:
            p_color = "blue" if pred == "B" else "red"
            st.markdown(f"### AI Prediction: :{p_color}[{ 'BIG (B)' if pred == 'B' else 'SMALL (S)' }]")
        else:
            st.warning("Data မရှိသေးပါ။")

    with col_b:
        st.subheader("တကယ်ထွက်လာသည့် ရလဒ်ကို နှိပ်ပါ")
        rc1, rc2 = st.columns(2)
        
        def record_result(actual):
            if st.session_state.current_prediction:
                status = "W" if actual == st.session_state.current_prediction else "L"
                
                # အဲဒီ Pattern အတွက်ပဲ History ထဲထည့်မယ်
                if p not in st.session_state.pattern_histories:
                    st.session_state.pattern_histories[p] = []
                st.session_state.pattern_histories[p].append(status)
            
            save_new_data(actual)
            st.session_state.active_pattern = None 
            st.session_state.current_prediction = None
            st.rerun()

        if rc1.button("Actually BIG (B)", key="b_entry", use_container_width=True):
            record_result("B")
        if rc2.button("Actually SMALL (S)", key="s_entry", use_container_width=True):
            record_result("S")

# Sidebar - Summary
with st.sidebar:
    if st.button("Clear All Pattern Records"):
        st.session_state.pattern_histories = {}
        st.rerun()
