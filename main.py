import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pattern Interactive Tracker", layout="wide")

# ၁။ Data Loading & Analysis
@st.cache_data
def analyze_patterns(file_path):
    try:
        df = pd.read_csv(file_path)
        data = df['bs'].tolist()
        patterns = {}
        # 4-length patterns analysis
        for i in range(len(data) - 4):
            pat = "".join(data[i : i + 4])
            nxt = data[i + 4]
            if pat not in patterns:
                patterns[pat] = {'B': 0, 'S': 0, 'total': 0}
            patterns[pat][nxt] += 1
            patterns[pat]['total'] += 1
        return patterns
    except:
        return None

# ၂။ Session State များ သတ်မှတ်ခြင်း
if 'bet_history' not in st.session_state:
    st.session_state.bet_history = []
if 'selected_pattern' not in st.session_state:
    st.session_state.selected_pattern = None

# ၃။ UI Layout
st.title("📊 Pattern Interactive Analysis & Bet Tracker")

patterns_dict = analyze_patterns("data.csv")

if patterns_dict:
    all_pats = [
        "BBBB", "BBBS", "BBSS", "BSSS",
        "SSSS", "SSSB", "SSBB", "SBBB",
        "BSBS", "SBSB", "BSSB", "SBBS",
        "BBSB", "SSBS", "BSBB", "SBSS"
    ]

    st.subheader("၁။ Pattern တစ်ခုကို ရွေးချယ်ပါ")
    
    cols = st.columns(4)
    for idx, p in enumerate(all_pats):
        with cols[idx % 4]:
            if st.button(p, key=p, use_container_width=True):
                st.session_state.selected_pattern = p

    if st.session_state.selected_pattern:
        p = st.session_state.selected_pattern
        st.divider()
        st.subheader(f"🔍 Analysis for Pattern: {p}")
        
        stats = patterns_dict.get(p, {'B': 0, 'S': 0, 'total': 0})
        if stats['total'] > 0:
            b_per = (stats['B'] / stats['total']) * 100
            s_per = (stats['S'] / stats['total']) * 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Past Matches", f"{stats['total']} times")
            c2.metric("Next BIG %", f"{round(b_per, 1)}%")
            c3.metric("Next SMALL %", f"{round(s_per, 1)}%")
            
            st.write("---")
            st.subheader("၂။ Real Bet မှတ်တမ်းတင်ရန်")
            bc1, bc2 = st.columns(2)
            
            # Error တက်နေတဲ့ ခလုတ်နေရာကို ဒီမှာ ပြင်ပေးထားပါတယ်
            if bc1.button("🎯 BET WON", type="primary", use_container_width=True):
                st.session_state.bet_history.append({"Pattern": p, "Result": "WIN", "Confidence": f"{max(b_per, s_per):.1f}%"})
                st.rerun()
            if bc2.button("❌ BET LOST", type="secondary", use_container_width=True):
                st.session_state.bet_history.append({"Pattern": p, "Result": "LOSE", "Confidence": f"{max(b_per, s_per):.1f}%"})
                st.rerun()
        else:
            st.info("ဒီ Pattern က သမိုင်းကြောင်းမှာ မရှိဖူးသေးပါဘူး။")

    # ၆။ History Table
    if st.session_state.bet_history:
        st.divider()
        st.subheader("📋 Today's Betting History")
        history_df = pd.DataFrame(st.session_state.bet_history)
        st.table(history_df.tail(10))
        
        wins = sum(1 for x in st.session_state.bet_history if x['Result'] == 'WIN')
        total_bets = len(st.session_state.bet_history)
        st.write(f"**Total Summary:** {total_bets} ပွဲထိုးထားပြီး {wins} ပွဲနိုင်ထားပါတယ်။ (Win Rate: {(wins/total_bets)*100:.1f}%)")

else:
    st.error("'data.csv' ဖိုင်ကို ရှာမတွေ့ပါ။ GitHub မှာ upload ပြန်လုပ်ပေးပါဗျ။")
