import streamlit as st
import pandas as pd
import os

# CSV 파일 경로
DATA_FILE = "etf_data.csv"

# ETF 데이터 로드
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["ETF 이름", "기초지수", "유형", "펀드보수", "자산운용사", "NAV", "괴리율", "추적 오차율", "PDF 링크"])

# ETF 데이터 저장
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Streamlit UI
st.title("📊 ETF 정보 관리 프로그램")

# ETF 데이터 불러오기
df = load_data()

# --- ETF 추가 기능 ---
st.header("📌 ETF 추가하기")
with st.form("add_etf"):
    etf_name = st.text_input("ETF 이름")
    index = st.text_input("기초지수")
    etf_type = st.text_input("유형")
    fund_fee = st.number_input("펀드보수 (%)", min_value=0.0, step=0.01)
    asset_mgmt = st.text_input("자산운용사")
    nav = st.number_input("NAV", min_value=0.0, step=0.01)
    deviation = st.number_input("괴리율 (%)", min_value=-100.0, max_value=100.0, step=0.01)
    tracking_error = st.number_input("추적 오차율 (%)", min_value=0.0, step=0.01)
    pdf_link = st.text_input("PDF 링크")

    submit = st.form_submit_button("ETF 추가")

    if submit:
        new_data = pd.DataFrame([[etf_name, index, etf_type, fund_fee, asset_mgmt, nav, deviation, tracking_error, pdf_link]],
                                columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success(f"✅ {etf_name} 추가 완료!")

# --- ETF 조회 기능 ---
st.header("🔍 ETF 조회")
if not df.empty:
    etf_selected = st.selectbox("ETF 선택", df["ETF 이름"].unique())

    etf_info = df[df["ETF 이름"] == etf_selected]
    st.write(etf_info)

    # PDF 다운로드 링크 제공
    pdf_url = etf_info["PDF 링크"].values[0]
    if pdf_url:
        st.markdown(f"[📄 PDF 다운로드]({pdf_url})")
else:
    st.write("현재 등록된 ETF가 없습니다.")
