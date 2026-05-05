import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TRX Smart Predictor", layout="wide")

# ၁။ Data Loading & Writing Logic
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

# ၂။ Pattern Analysis (Prediction Logic)
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

# --- Session State ---
if 'bet_history' not in st.session_state:
    st.session_state.bet_history = []
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None
if 'active_pattern' not in st.session_state:
    st.session_state.active_pattern = None

# --- UI ---
st.title("🎯 TRX AI Smart Predictor (Win/Lose Tracker)")

# Pattern Boxes (4x4 Grid)
all_pats = ["BBBB", "BBBS", "BBSS", "BSSS", "SSSS", "SSSB", "SSBB", "SBBB", 
            "BSBS", "SBSB", "BSSB", "SBBS", "BBSB", "SSBS", "BSBB", "SBSS"]

st.subheader("၁။ ဂိမ်းထဲက Pattern ကို နှိပ်ပါ")
cols = st.columns(4)
for idx, p in enumerate(all_pats):
    with cols[idx % 4]:
        if st.button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state.active_pattern = p
            st.session_state.current_prediction = get_prediction(p)

# Display Prediction
if st.session_state.active_pattern:
    st.divider()
    pred = st.session_state.current_prediction
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.info(f"Selected: **{st.session_state.active_pattern}**")
        if pred:
            color = "blue" if pred == "B" else "red"
            st.markdown(f"### AI Prediction: :{color}[{ 'BIG (B)' if pred == 'B' else 'SMALL (S)' }]")
        else:
            st.warning("Data မလုံလောက်သေးပါ။")

    with col_b:
        st.subheader("၂။ တကယ်ထွက်လာသည့် ရလဒ်ကို နှိပ်ပါ")
        rc1, rc2 = st.columns(2)
        
        # ရလဒ်ထည့်သွင်းခြင်းနှင့် Win/Lose စစ်ခြင်း
        def record_result(actual):
            if st.session_state.current_prediction:
                status = "WIN" if actual == st.session_state.current_prediction else "LOSE"
                st.session_state.bet_history.append({
                    "Pattern": st.session_state.active_pattern,
                    "Prediction": st.session_state.current_prediction,
                    "Actual": actual,
                    "Result": status
                })
            save_new_data(actual)
            st.session_state.active_pattern = None # Reset for next round
            st.session_state.current_prediction = None
            st.rerun()

        if rc1.button("Actually BIG (B)", use_container_width=True):
            record_result("B")
        if rc2.button("Actually SMALL (S)", use_container_width=True):
            record_result("S")

# Summary Table
if st.session_state.bet_history:
    st.divider()
    st.subheader("📊 Summary & History")
    df_history = pd.DataFrame(st.session_state.bet_history)
    
    # Win/Lose အရေအတွက်တွက်မယ်
    wins = len(df_history[df_history['Result'] == 'WIN'])
    loses = len(df_history[df_history['Result'] == 'LOSE'])
    
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Total Bets", len(df_history))
    sc2.metric("Wins", wins, delta=f"{wins} ✅")
    sc3.metric("Loses", loses, delta=f"-{loses}", delta_color="inverse")
    
    st.dataframe(df_history.tail(10), use_container_width=True)
