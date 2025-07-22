import json
import statistics
import streamlit as st
import random
import os
from langchain_community.chat_models import ChatOpenAI

# ✅ Streamlit 설정
st.set_page_config(page_title="🍱 Food Defense GPT")
st.title("🍱 역곡역 점심 추천 디펜스 GPT")

# ✅ API 키 하드코딩
try:
    api_key = "OPEANAPI KEY를 입력하세요"
    os.environ["OPENAI_API_KEY"] = api_key
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=api_key)
except Exception as e:
    st.error(f"❌ OpenAI 설정 오류: {e}")
    print(f"[OpenAI 설정 오류] {e}")

# ✅ GPT 설명 함수
def ask_gpt_about_random_place(llm, place: dict) -> str:
    prompt = f"""
        너는 지금부터 **역곡역 인근 점심 맛집을 추천해주는 디펜서** 역할이야! 
        사용자가 'top 20 맛집 중에 랜덤으로 한 곳'을 추천해달라고 했어!
        그럼 상냥하고 귀여운 말투로 추천해줘 

        이번에 추천할 곳은 바로 여기에요 ⬇️  
        - 음식 종류: {place['type']}  
        - 가게 이름: {place['name']}  
        - 위치: 강남 (자세한 주소는 생략)

        이 가게는 대표 메뉴나 인기 메뉴로 특히 유명한데, 어떤 메뉴가 좋은지 자연스럽고 생생하게 소개해줘 

        그리고 왜 이 가게가 랜덤 추천인데도 한 번쯤 꼭 가볼만한지,  
        1~2문장 정도로 **설득력 있게 이유를 곁들여줘** 

        👉 단답형은 ❌!  
        👉 한 문단 이상으로 **따뜻하고 다정한 말투**로 이야기해줘!  
        👉 문장 중간중간에 이모티콘도 많이 써줘! 총 추천 문장은 5문장 이내로 해. 
        """

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print(f"[GPT 함수 오류] {e}")
        return f"⚠️ GPT 응답 오류: {e}"

# ✅ 데이터 로드
DATA_PATH = r'C:\Users\lyjin\Desktop\vscode\Project\Kakao_map\catholic\food_data.json'

@st.cache_data
def load_data():
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)['음식점정보']
    except Exception as e:
        st.error(f"❌ JSON 로드 오류: {e}")
        print(f"[파일 로드 오류] {e}")
        return []

try:
    data = load_data()
except Exception as e:
    data = []
    st.error(f"❌ 데이터 로드 실패: {e}")
    print(f"[데이터 로드 실패] {e}")

# ✅ Bayesian 점수 계산
try:
    ratings = [item['rating'] for item in data if item['rating'] is not None]
    C = sum(ratings) / len(ratings)

    review_counts = [item['review_count'] for item in data if item['review_count'] is not None]
    m = int(statistics.quantiles(review_counts, n=10)[7])  # 상위 30%

    for item in data:
        r = item['rating']
        v = item['review_count']
        if r is not None and v is not None:
            bayesian_score = (v / (v + m)) * r + (m / (v + m)) * C
        else:
            bayesian_score = 0
        item['bayesian_score'] = round(bayesian_score, 4)
except Exception as e:
    st.error(f"❌ Bayesian 계산 오류: {e}")
    print(f"[Bayesian 오류] {e}")

# ✅ 상위 20개 추출
try:
    top_20 = sorted(data, key=lambda x: x['bayesian_score'], reverse=True)[:20]
    gpt_pick = top_20[0]
except Exception as e:
    top_20 = []
    gpt_pick = {}
    st.error(f"❌ Top 20 추출 오류: {e}")
    print(f"[Top20 오류] {e}")

# ✅ 출력 - GPT 추천
try:
    st.subheader("✨ GPT 추천 맛집")
    st.success(f"**{gpt_pick['name']}**\n\n> {gpt_pick['type']} | 평점 ⭐ {gpt_pick['rating']}점 | 리뷰수 💬 {gpt_pick['review_count']}개")
except Exception as e:
    st.error(f"❌ GPT 추천 출력 오류: {e}")
    print(f"[GPT 추천 출력 오류] {e}")

# ✅ 출력 - 리스트
st.divider()
st.subheader("🍽️ 상위 20개 맛집 리스트 (Bayesian 점수 기준)")
for idx, item in enumerate(top_20, start=1):
    try:
        st.markdown(f"""
        **{idx}. {item['name']}**  
        - 분류: {item['type']}  
        - 평점: ⭐ {item['rating']} / 리뷰: 💬 {item['review_count']}개  
        - Bayesian 점수: `{item['bayesian_score']}`
        """)
    except Exception as e:
        st.error(f"❌ 리스트 항목 {idx} 출력 오류: {e}")
        print(f"[리스트 출력 오류] {e}")

# ✅ GPT 랜덤 추천
st.divider()
st.subheader("🎲 GPT에게 랜덤 맛집 추천받기")

if st.button("추천 받기"):
    try:
        random_place = random.choice(top_20)
        with st.spinner("GPT가 맛집을 탐색 중입니다..."):
            gpt_random_explanation = ask_gpt_about_random_place(llm, random_place)

        st.markdown(f"#### 🍴 추천 가게: **{random_place['name']}** ({random_place['type']})")
        st.info(gpt_random_explanation)
    except Exception as e:
        st.error(f"❌ GPT 랜덤 추천 오류: {e}")
        print(f"[GPT 추천 버튼 오류] {e}")
