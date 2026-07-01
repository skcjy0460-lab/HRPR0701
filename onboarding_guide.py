"""
직원 온보딩(Onboarding) 가이드 모듈
단계별 체크리스트 + 직종별 온보딩 로드맵 + 실무 팁
"""
import streamlit as st
from datetime import datetime, date, timedelta

# ── 온보딩 체크리스트 마스터 데이터 ─────────────────────────────────────────────
ONBOARDING_CHECKLIST = {
    "입사 전 (Pre-boarding)": {
        "icon": "📬",
        "color": "#8E44AD",
        "담당": "인사팀",
        "items": [
            {"task": "환영 메시지 발송 (합격 축하 + 입사일/시간/장소/복장 안내)", "required": True, "law": ""},
            {"task": "지참 서류 목록 사전 안내 (면허증, 통장사본, 보건증 등)", "required": True, "law": ""},
            {"task": "PC·사원증·유니폼·명찰·비품 사전 준비", "required": True, "law": ""},
            {"task": "EMR·그룹웨어 계정 사전 생성", "required": True, "law": ""},
            {"task": "멘토(Buddy) 지정 및 사전 미팅 요청", "required": False, "law": ""},
            {"task": "주차 공간·식당·탈의실 위치 안내 문자 발송", "required": False, "law": ""},
        ],
    },
    "입사 1일차 (Day 1)": {
        "icon": "🌟",
        "color": "#E74C3C",
        "담당": "인사팀 + 부서장",
        "items": [
            {"task": "근로계약서 작성 및 교부 (당일 의무)", "required": True, "law": "근로기준법 제17조"},
            {"task": "필수 입사 서류 수합 (신분증, 면허증, 통장사본, 주민등록등본 등)", "required": True, "law": ""},
            {"task": "4대보험 취득신고 준비 (14일 이내 신고 의무)", "required": True, "law": "국민건강보험법 제9조"},
            {"task": "병원 투어 (원무과, 식당, 휴게실, 비상구, 소화기 위치)", "required": True, "law": ""},
            {"task": "병원장/부서장 환영 인사 및 부서원 소개", "required": True, "law": ""},
            {"task": "취업규칙 교부 및 주요 내용 설명 (근태, 연차, 복장, 식대 등)", "required": True, "law": "근로기준법 제93조"},
            {"task": "개인정보 수집·이용 동의서 및 비밀유지 서약서 징구", "required": True, "law": "개인정보보호법 제15조"},
            {"task": "PC 로그인·EMR 초기 설정 및 기본 사용법 안내", "required": True, "law": ""},
            {"task": "멘토(Buddy)와 환영 점심 식사", "required": False, "law": ""},
        ],
    },
    "입사 1주차 (Week 1)": {
        "icon": "📚",
        "color": "#E67E22",
        "담당": "부서장 + 멘토",
        "items": [
            {"task": "직무기술서(JD) 기반 업무 범위 및 기대 역할 설명", "required": True, "law": ""},
            {"task": "결핵·잠복결핵 검진 예약 (1개월 이내 실시 의무)", "required": True, "law": "결핵예방법 제11조"},
            {"task": "채용 신체검사 실시 또는 예약 (해당 시)", "required": True, "law": ""},
            {"task": "성희롱 예방교육 이수 (신규 입사자 우선 실시)", "required": True, "law": "남녀고용평등법 제13조"},
            {"task": "개인정보보호 교육 이수", "required": True, "law": "개인정보보호법 제28조"},
            {"task": "직장 내 괴롭힘 예방교육 이수", "required": True, "law": "근로기준법 제76조의3"},
            {"task": "감염관리 기본 교육 (손위생, 격리 지침, 표준주의 등)", "required": True, "law": "의료법 제47조"},
            {"task": "소방·안전 기본 교육 (소화기 사용법, 대피 경로)", "required": True, "law": "소방기본법"},
            {"task": "급여 지급일·방법·명세서 확인 방법 안내", "required": True, "law": "근로기준법 제48조"},
            {"task": "연차 발생 기준 및 사용 방법 안내", "required": True, "law": "근로기준법 제60조"},
        ],
    },
    "입사 1개월차 (Month 1)": {
        "icon": "🔍",
        "color": "#27AE60",
        "담당": "인사팀 + 부서장",
        "items": [
            {"task": "4대보험 취득신고 완료 확인", "required": True, "law": ""},
            {"task": "결핵·잠복결핵 검진 결과 수령 및 기록 보관 (3년)", "required": True, "law": "결핵예방법"},
            {"task": "1개월 적응 면담 실시 (부서장 또는 인사팀)", "required": True, "law": ""},
            {"task": "직무 교육 이수 현황 점검 (법정의무교육 포함)", "required": True, "law": ""},
            {"task": "수습 기간 목표 설정 (3개월 후 평가 기준 공유)", "required": True, "law": ""},
            {"task": "의료인 면허 신고 여부 확인 (3년 주기)", "required": False, "law": "의료법"},
            {"task": "보수교육 이수 계획 확인 (해당 직종)", "required": False, "law": ""},
        ],
    },
    "수습 종료 (3개월차)": {
        "icon": "🏆",
        "color": "#1B6CA8",
        "담당": "부서장 + 인사팀",
        "items": [
            {"task": "수습 평가 실시 (직무 수행 능력, 근태, 태도 등 종합 평가)", "required": True, "law": ""},
            {"task": "정규직 전환 확정 및 서면 통보", "required": True, "law": ""},
            {"task": "평가 결과 피드백 면담 (강점·개선점 공유)", "required": True, "law": ""},
            {"task": "온보딩 프로세스 만족도 설문 실시 (개선점 도출)", "required": False, "law": ""},
            {"task": "장기 직무 목표 및 경력 개발 계획 논의", "required": False, "law": ""},
        ],
    },
}

# ── 직종별 온보딩 특이사항 ─────────────────────────────────────────────────────
POSITION_SPECIFIC = {
    "간호사 (RN)": [
        "간호사 면허증 원본 확인 및 사본 보관",
        "BLS(기본심폐소생술) 이수 여부 확인 (미이수 시 조기 이수 독려)",
        "3교대 근무 일정 및 교대 인수인계 방법 교육",
        "투약 오류 예방 교육 (5 Rights: 정확한 환자, 약물, 용량, 경로, 시간)",
        "낙상 예방 프로토콜 교육",
        "EMR 간호 기록 작성 방법 집중 교육",
    ],
    "원무과 직원": [
        "건강보험 청구 기초 교육 (EDI 청구 방법)",
        "수납 오류 방지 교육 (현금 수납 절차, 영수증 발급)",
        "환자 민원 응대 매뉴얼 숙지",
        "의무기록 발급 절차 및 개인정보보호 강조",
        "의료급여 수급자 처리 방법 교육",
    ],
    "방사선사": [
        "방사선 안전 교육 (개인 피폭 선량계 착용 의무)",
        "방사선 발생 장치 사용 허가 확인",
        "조영제 부작용 대응 프로토콜 숙지",
        "PACS 시스템 사용 방법 교육",
        "방사선 관계 종사자 건강진단 일정 안내",
    ],
    "의무기록사": [
        "KCD 코딩 체계 및 병원 내 코딩 기준 교육",
        "의무기록 보존 기간 및 폐기 절차 교육",
        "의무기록 열람·사본 발급 절차 및 개인정보보호 강조",
        "암 등록 사업 관련 업무 인수인계",
    ],
    "간호조무사": [
        "간호조무사 자격증 원본 확인 및 사본 보관",
        "간호사 지도 하 업무 범위 명확히 교육 (무면허 의료행위 예방)",
        "환자 이동 보조 시 안전 수칙 (낙상 예방, 리프트 사용법)",
        "기본 감염 예방 수칙 (손위생, 개인보호구 착용)",
    ],
}


def render_onboarding_guide_page():
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">🚀</div>
      <div>
        <h1>직원 온보딩(Onboarding) 가이드</h1>
        <p>신규 입사자의 빠른 적응과 조직 몰입을 위한 단계별 체크리스트 & 직종별 특이사항</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      💡 <b>온보딩의 핵심 목적:</b> 단순한 서류 제출을 넘어, 신규 직원이 병원의 비전·문화·규정을 이해하고 자신의 역할에 빠르게 적응하도록 돕는 것입니다.
      체계적인 온보딩은 <b>조기 퇴사율을 낮추고</b>, 직원 만족도와 환자 안전을 동시에 높입니다.
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 단계별 온보딩 체크리스트", "👩‍⚕️ 직종별 특이사항", "📅 온보딩 일정 계산기"])

    with tab1:
        st.subheader("단계별 온보딩 체크리스트")
        st.markdown("각 단계를 클릭하여 세부 항목을 확인하세요. 필수 항목은 반드시 완료해야 합니다.")

        for stage, info in ONBOARDING_CHECKLIST.items():
            required_count = sum(1 for item in info["items"] if item["required"])
            total_count = len(info["items"])
            with st.expander(f"{info['icon']} {stage}  |  담당: {info['담당']}  |  필수 {required_count}/{total_count}개", expanded=False):
                for item in info["items"]:
                    badge = '<span class="badge badge-red">필수</span>' if item["required"] else '<span class="badge badge-gray">권장</span>'
                    law_html = f'<br><span style="font-size:0.78rem; color:#2980B9;">📜 근거: {item["law"]}</span>' if item["law"] else ""
                    icon = "✅" if item["required"] else "🔲"
                    st.markdown(f"""
                    <div class="checklist-item {'required' if item['required'] else 'optional'}">
                      <div style="flex-shrink:0; margin-top:2px; font-size:1.1rem;">{icon}</div>
                      <div>
                        <span style="font-size:0.92rem;">{item['task']}</span> {badge}{law_html}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.subheader("직종별 온보딩 특이사항")
        st.markdown("직종에 따라 추가로 확인해야 할 온보딩 항목입니다.")

        position = st.selectbox("직종 선택", list(POSITION_SPECIFIC.keys()))
        items = POSITION_SPECIFIC[position]

        st.markdown(f"""
        <div class="section-card">
          <h3>👩‍⚕️ {position} 추가 온보딩 체크사항</h3>
          <ul style="margin:0; padding-left:18px; font-size:0.92rem; color:#2C3E50; line-height:2;">
            {''.join(f"<li>{item}</li>" for item in items)}
          </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warn-box">
          ⚠️ <b>공통 주의사항:</b> 모든 직종에 관계없이 <b>근로계약서 당일 교부</b>, <b>4대보험 14일 이내 취득신고</b>,
          <b>결핵·잠복결핵 검진 1개월 이내 실시</b>는 반드시 이행해야 합니다. 미이행 시 과태료 대상입니다.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.subheader("온보딩 일정 자동 계산기")
        st.markdown("입사일을 입력하면 주요 온보딩 마감일을 자동으로 계산해 드립니다.")

        join_date = st.date_input("입사일", value=date.today())

        if join_date:
            d14 = join_date + timedelta(days=14)
            d30 = join_date + timedelta(days=30)
            d90 = join_date + timedelta(days=90)
            d365 = join_date + timedelta(days=365)

            st.markdown(f"""
            <table class="styled-table">
              <tr><th>처리 기한</th><th>업무 내용</th><th>근거 법령</th><th>비고</th></tr>
              <tr>
                <td><b style="color:#E74C3C;">입사 당일</b><br>{join_date.strftime('%Y.%m.%d')}</td>
                <td>근로계약서 작성 및 교부</td>
                <td>근로기준법 제17조</td>
                <td>⚠️ 미교부 시 500만원 이하 과태료</td>
              </tr>
              <tr>
                <td><b style="color:#E74C3C;">14일 이내</b><br>{d14.strftime('%Y.%m.%d')}까지</td>
                <td>4대보험 취득신고</td>
                <td>국민건강보험법 제9조</td>
                <td>⚠️ 지연 신고 시 소급 보험료 + 과태료</td>
              </tr>
              <tr>
                <td><b style="color:#E67E22;">1개월 이내</b><br>{d30.strftime('%Y.%m.%d')}까지</td>
                <td>결핵·잠복결핵 검진 실시</td>
                <td>결핵예방법 제11조</td>
                <td>⚠️ 미실시 시 200만원 이하 과태료</td>
              </tr>
              <tr>
                <td><b style="color:#27AE60;">1개월 이내</b><br>{d30.strftime('%Y.%m.%d')}까지</td>
                <td>법정의무교육 이수 (성희롱, 개인정보, 괴롭힘 예방)</td>
                <td>남녀고용평등법 등</td>
                <td>연간 1회 이수 의무</td>
              </tr>
              <tr>
                <td><b style="color:#1B6CA8;">3개월차</b><br>{d90.strftime('%Y.%m.%d')}까지</td>
                <td>수습 평가 및 정규직 전환 결정</td>
                <td>취업규칙 기준</td>
                <td>평가 기준 사전 공유 필수</td>
              </tr>
              <tr>
                <td><b style="color:#566573;">1년 후</b><br>{d365.strftime('%Y.%m.%d')}부터</td>
                <td>연차유급휴가 15일 발생 (출근율 80% 이상 시)</td>
                <td>근로기준법 제60조</td>
                <td>1년 미만 기간 중 발생 연차와 별도</td>
              </tr>
            </table>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="success-box" style="margin-top:16px;">
              ✅ <b>실무 팁:</b> 입사일 기준으로 위 일정을 캘린더에 미리 등록해 두면 누락 없이 처리할 수 있습니다.
              특히 <b>4대보험 취득신고(14일)</b>와 <b>결핵검진(1개월)</b>은 실무에서 가장 많이 놓치는 항목입니다.
            </div>
            """, unsafe_allow_html=True)
