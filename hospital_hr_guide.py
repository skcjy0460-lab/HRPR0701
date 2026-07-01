"""
병원 인사노무 실무 가이드
신규 입사자 / 재직자 관리 시스템
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
from job_description import render_job_description_page
from onboarding_guide import render_onboarding_guide_page
from ai_consulting import render_ai_consulting_page
from hr_calculator import render_calculator_page

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="병원 인사노무 실무 가이드",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 전역 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─ 기본 폰트 & 배경 ─ */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* ─ 사이드바 ─ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D3B6E 0%, #1A5276 60%, #1B6CA8 100%);
}
[data-testid="stSidebar"] * { color: #ECF0F1 !important; }
[data-testid="stSidebar"] .stRadio label { color: #BDC3C7 !important; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    background-color: #2980B9 !important;
}

/* ─ 헤더 배너 ─ */
.page-header {
    background: linear-gradient(135deg, #0D3B6E 0%, #1B6CA8 100%);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.page-header h1 {
    color: #FFFFFF;
    font-size: 1.85rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.3;
}
.page-header p {
    color: #AED6F1;
    font-size: 0.92rem;
    margin: 4px 0 0;
}
.header-icon { font-size: 3rem; }

/* ─ 섹션 카드 ─ */
.section-card {
    background: #FFFFFF;
    border: 1px solid #D5E8F5;
    border-left: 5px solid #1B6CA8;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.section-card h3 {
    color: #0D3B6E;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0 0 10px;
}

/* ─ 뱃지 ─ */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 6px;
}
.badge-red    { background:#FDEDEC; color:#C0392B; border:1px solid #E74C3C; }
.badge-orange { background:#FEF9E7; color:#D35400; border:1px solid #F39C12; }
.badge-green  { background:#EAFAF1; color:#1E8449; border:1px solid #27AE60; }
.badge-blue   { background:#EAF4FD; color:#1A5276; border:1px solid #2980B9; }
.badge-gray   { background:#F2F3F4; color:#566573; border:1px solid #AAB7B8; }

/* ─ 정보 박스 ─ */
.info-box {
    background: #EAF4FD;
    border: 1px solid #AED6F1;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.9rem;
    color: #1A5276;
}
.warn-box {
    background: #FEF9E7;
    border: 1px solid #F9E79F;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.9rem;
    color: #7D6608;
}
.danger-box {
    background: #FDEDEC;
    border: 1px solid #F1948A;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.9rem;
    color: #922B21;
}
.success-box {
    background: #EAFAF1;
    border: 1px solid #A9DFBF;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.9rem;
    color: #1D6A39;
}

/* ─ 테이블 ─ */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin: 10px 0;
}
.styled-table th {
    background: #0D3B6E;
    color: #FFFFFF;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}
.styled-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #D5E8F5;
    vertical-align: top;
    line-height: 1.5;
}
.styled-table tr:nth-child(even) td { background: #F4F9FD; }
.styled-table tr:hover td { background: #EAF4FD; }

/* ─ 체크리스트 ─ */
.checklist-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 6px;
    background: #F8FBFF;
    border: 1px solid #D5E8F5;
    font-size: 0.9rem;
}
.checklist-item.required { border-left: 4px solid #E74C3C; }
.checklist-item.optional { border-left: 4px solid #F39C12; }

/* ─ 탭 ─ */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #F0F4F8;
    padding: 8px;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 500;
    color: #566573;
    background: transparent;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #1B6CA8 !important;
    color: #FFFFFF !important;
}

/* ─ 진행률 라벨 ─ */
.progress-label {
    font-size: 0.85rem;
    color: #566573;
    margin-bottom: 4px;
}
.penalty-chip {
    display:inline-block;
    background:#FDEDEC;
    color:#C0392B;
    border:1px solid #E74C3C;
    border-radius:4px;
    padding:2px 8px;
    font-size:0.8rem;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 데이터 정의
# ═══════════════════════════════════════════════════════════════════════════════

# ── 법정의무교육 마스터 데이터 ─────────────────────────────────────────────────
MANDATORY_EDUCATION = [
    {
        "no": 1,
        "name": "직장 내 성희롱 예방교육",
        "law": "남녀고용평등과 일·가정 양립 지원에 관한 법률 제13조",
        "target": "전 직원 (1인 이상 모든 사업장)",
        "cycle": "연 1회 이상",
        "hours": "1시간 이상",
        "method": "집합·영상·온라인",
        "note": "사업주도 의무 이수 대상. 강사 자격 요건 있음(전문강사 또는 관련 교육 이수자). 교육자료·결과 3년 보존",
        "penalty": "최대 500만원",
        "penalty_detail": "1차 300만원, 2차 400만원, 3차 500만원",
        "submit": "별도 제출처 없음(자체보관)",
        "category": "전체공통",
        "color": "red",
    },
    {
        "no": 2,
        "name": "개인정보보호 교육",
        "law": "개인정보 보호법 제28조",
        "target": "개인정보 취급 직원 전원",
        "cycle": "연 1회 이상",
        "hours": "법정 최소시간 미지정(통상 1~2시간)",
        "method": "집합·영상·온라인",
        "note": "개인정보처리방침 공개·안전조치 의무 포함. 교육일지·수료증 보존 권장",
        "penalty": "최대 5천만원 (과징금별도)",
        "penalty_detail": "미교육 시 과태료 최대 1천만원, 안전조치 위반 시 최대 3천만원",
        "submit": "별도 제출처 없음(자체보관)",
        "category": "전체공통",
        "color": "red",
    },
    {
        "no": 3,
        "name": "직장 내 장애인 인식개선 교육",
        "law": "장애인고용촉진 및 직업재활법 제5조의2",
        "target": "전 직원 (1인 이상 모든 사업장)",
        "cycle": "연 1회 이상",
        "hours": "1시간 이상",
        "method": "집합·영상·온라인(한국장애인고용공단 승인 콘텐츠)",
        "note": "50인 이상: 전문 강사 파견 or 승인 콘텐츠 이수. 50인 미만: 고용공단 교육자료로 자체교육 가능. 교육자료 3년 보존",
        "penalty": "최대 300만원",
        "penalty_detail": "1차 100만원, 2차 200만원, 3차 300만원",
        "submit": "한국장애인고용공단(실적 보고 의무 없으나 확인 시 증빙 필요)",
        "category": "전체공통",
        "color": "orange",
    },
    {
        "no": 4,
        "name": "직장 내 괴롭힘 예방교육",
        "law": "근로기준법 제76조의3 제7항",
        "target": "전 직원",
        "cycle": "연 1회 이상 (취업규칙 기재 필수)",
        "hours": "법정 최소시간 미지정",
        "method": "집합·영상·온라인",
        "note": "취업규칙에 직장 내 괴롭힘 예방·조치 사항 기재 의무. 10인 미만 사업장 적용 일부 제외",
        "penalty": "500만원 이하 과태료",
        "penalty_detail": "조치의무 위반 시 500만원 이하 과태료",
        "submit": "별도 제출처 없음(자체보관)",
        "category": "전체공통",
        "color": "orange",
    },
    {
        "no": 5,
        "name": "산업안전보건교육 (정기교육)",
        "law": "산업안전보건법 제29조",
        "target": "5인 이상 사업장 근로자 (보건업 포함 병원급)",
        "cycle": "분기 1회 (매 분기)",
        "hours": "사무직: 분기 3시간 이상 / 비사무직(간호사·의료기사 등): 분기 6시간 이상",
        "method": "집합·온라인(고용노동부 인정기관)",
        "note": "의원급(의사·치과의사·한의사 단독 5인 미만): 적용 제외. 병원급 5인 이상 보건업은 의무. 관리감독자 별도 16시간/년 의무",
        "penalty": "500만원 이하 과태료",
        "penalty_detail": "미실시 근로자 1인당 과태료. 1차 50만원, 2차 100만원, 3차 150만원",
        "submit": "별도 제출처 없음(자체보관, 고용노동부 점검 시 제출)",
        "category": "병원급이상",
        "color": "orange",
    },
    {
        "no": 6,
        "name": "아동학대 신고의무자 교육",
        "law": "아동복지법 제26조 제6항, 동법 시행령 제26조",
        "target": "의료기관 종사자 전원 (의료인·의료기사·간호조무사 등 신고의무자)",
        "cycle": "연 1회 이상",
        "hours": "1시간 이상",
        "method": "아동권리보장원 배포자료로 교육 (중앙아동보호전문기관 승인 자료만 인정)",
        "note": "반드시 아동권리보장원 배포 공식 교육자료 사용. 자체 제작자료 불인정. 교육결과 12월 말까지 관할 보건소 제출",
        "penalty": "최대 300만원",
        "penalty_detail": "1차 100만원, 2차 200만원, 3차 300만원",
        "submit": "관할 보건소 (매년 12월 말까지)",
        "category": "전체공통",
        "color": "red",
    },
    {
        "no": 7,
        "name": "노인학대 신고의무자 교육",
        "law": "노인복지법 제39조의6 제6항",
        "target": "노인 관련 진료·돌봄 의료기관 종사자",
        "cycle": "연 1회 이상",
        "hours": "1시간 이상",
        "method": "보건복지부 배포자료 or 온라인(중앙노인보호전문기관)",
        "note": "반드시 보건복지부 배포 공식 자료 사용. 교육결과 12월 말까지 관할 보건소 제출",
        "penalty": "최대 300만원",
        "penalty_detail": "1차 100만원, 2차 200만원, 3차 300만원",
        "submit": "관할 보건소 (매년 12월 말까지)",
        "category": "노인관련기관",
        "color": "orange",
    },
    {
        "no": 8,
        "name": "퇴직연금 교육",
        "law": "근로자퇴직급여 보장법 제32조",
        "target": "퇴직연금(DB/DC) 가입 사업장 전 가입 근로자",
        "cycle": "연 1회 이상",
        "hours": "법정 최소시간 미지정",
        "method": "집합·온라인·영상",
        "note": "퇴직연금 미도입 사업장 해당 없음. DB형은 사업주, DC형·IRP는 근로자에게 운용지시 교육 포함",
        "penalty": "1천만원 이하 과태료",
        "penalty_detail": "교육 미실시 시 과태료",
        "submit": "별도 제출처 없음(자체보관)",
        "category": "퇴직연금가입",
        "color": "blue",
    },
    {
        "no": 9,
        "name": "감염병 예방관리 교육 (감염관리담당자)",
        "law": "의료법 제47조, 의료관련감염 예방관리 종합대책",
        "target": "감염관리담당자 (모든 의료기관 지정 의무)",
        "cycle": "연 24시간 이상",
        "hours": "24시간 이상/년",
        "method": "대한감염관리간호사회·질병관리청 지정기관 교육",
        "note": "병원급 이상: 감염관리실 설치·전담인력 의무. 의원급: 감염관리담당자만 지정 가능(의사 본인 담당 가능). 교육 미이수 시 행정처분",
        "penalty": "시정명령→업무정지",
        "penalty_detail": "1차 경고, 2차 시정명령, 3차 업무정지 15일",
        "submit": "질병관리청·보건소(요청 시 증빙 제출)",
        "category": "전체공통",
        "color": "red",
    },
    {
        "no": 10,
        "name": "성폭력 예방교육",
        "law": "성폭력방지 및 피해자보호 등에 관한 법률 제5조",
        "target": "국가·지방자치단체·공공기관 종사자 (공공의료기관)",
        "cycle": "연 1회 이상",
        "hours": "1시간 이상",
        "method": "집합·온라인",
        "note": "민간의료기관은 법적 의무 없으나 권고. 공공의료기관(국립·지방의료원 등)은 의무",
        "penalty": "300만원 이하 과태료 (공공기관)",
        "penalty_detail": "공공기관만 해당",
        "submit": "여성가족부(공공기관 이행실적 제출)",
        "category": "공공의료기관",
        "color": "gray",
    },
    {
        "no": 11,
        "name": "결핵 및 잠복결핵감염 검진 (연 1회)",
        "law": "결핵예방법 제11조, 동법 시행규칙 제4조",
        "target": "의료기관 전 종사자 (의료인·의료기사·간호조무사·행정직 포함)",
        "cycle": "연 1회 (신규입사자: 1개월 이내)",
        "hours": "해당없음(검진)",
        "method": "흉부 X선 + 잠복결핵감염검진(TST 또는 IGRA)",
        "note": "신규채용 1개월 이내 최초 실시. 이후 매년 정기검진. 결과 3년 보관 의무. 양성자 치료비 국가지원",
        "penalty": "200만원 이하 과태료",
        "penalty_detail": "검진 미실시·기록 미보존 시 과태료",
        "submit": "별도 제출처 없음(자체보관 3년)",
        "category": "전체공통",
        "color": "red",
    },
]

# ── 입사 서류 마스터 데이터 ────────────────────────────────────────────────────
ONBOARDING_DOCS = {
    "인사기본서류": [
        {"name": "입사지원서 / 이력서", "required": True, "note": "자사 양식 사용 권장. 사진 부착 여부는 내규에 따름", "law": ""},
        {"name": "주민등록등본", "required": True, "note": "발급일 3개월 이내. 온라인 발급 가능(정부24)", "law": ""},
        {"name": "가족관계증명서", "required": False, "note": "부양가족 공제 신청 시 필요. 갑근세 원천징수영수증 처리용", "law": "소득세법"},
        {"name": "학력증명서 (졸업증명서·졸업예정증명서)", "required": True, "note": "최종학력 기준. 재직 중 변경 시 추가 제출", "law": ""},
        {"name": "경력증명서", "required": False, "note": "해당자만. 전 직장 경력 확인용. 4대보험 가입이력으로 대체 가능", "law": ""},
        {"name": "면허증·자격증 사본", "required": True, "note": "의사·간호사·의료기사 등 의료인은 필수. 원본 대조 후 사본 보관", "law": "의료법"},
        {"name": "자동차운전면허증 사본", "required": False, "note": "방문진료·왕진 업무 해당자만", "law": ""},
    ],
    "세금·4대보험 서류": [
        {"name": "근로소득세 원천징수 신고서 (근로소득자 소득·세액 공제신고서)", "required": True, "note": "입사 후 최초 연말정산 또는 중도 입사 시 제출. 국세청 홈택스 출력", "law": "소득세법 제140조"},
        {"name": "4대보험 취득신고 (사업주 의무)", "required": True, "note": "입사일로부터 14일 이내 사업주가 신고. 건강보험·국민연금·고용보험·산재보험", "law": "국민건강보험법, 국민연금법"},
        {"name": "건강보험 피부양자 등록 신청서", "required": False, "note": "부양가족이 있는 경우. 건강보험공단 제출", "law": "국민건강보험법"},
    ],
    "건강검진·의무검사 서류": [
        {"name": "채용 건강진단서 (일반건강진단)", "required": True, "note": "입사 전후 1~3개월 이내. 산업안전보건법에 따른 배치 전 건강진단 포함. 1년 이상 보존", "law": "산업안전보건법 제129조"},
        {"name": "결핵검진 결과서 (흉부 X선)", "required": True, "note": "입사 1개월 이내. 채용 건강진단에 포함되므로 동시 실시 가능", "law": "결핵예방법 제11조"},
        {"name": "잠복결핵감염 검진 결과서 (TST 또는 IGRA)", "required": True, "note": "채용건강진단과 별도 실시. 입사 1개월 이내. 양성 시 치료 권고. 결과 3년 보존", "law": "결핵예방법 제11조, 시행규칙 제4조"},
        {"name": "B형간염 항원·항체 검사 결과서", "required": True, "note": "의료종사자 의무. 항체 없는 경우 예방접종 권고(3회). 채용 건강진단에 포함", "law": "의료법(감염관리지침)"},
        {"name": "특수건강진단 결과서", "required": False, "note": "방사선·화학물질 취급 근무자(방사선사·수술실 종사자 등)만 해당. 배치 전 실시", "law": "산업안전보건법 제130조"},
    ],
    "서약·동의 서류": [
        {"name": "근로계약서", "required": True, "note": "반드시 서면 작성·교부 의무(전자문서 가능). 임금·근무시간·휴일 등 명시. 1부씩 상호 보관", "law": "근로기준법 제17조"},
        {"name": "비밀유지·보안서약서", "required": True, "note": "환자정보·병원경영정보 보안. 개인정보보호법 연계", "law": "개인정보보호법"},
        {"name": "개인정보 수집·이용 동의서", "required": True, "note": "인사관리 목적 개인정보 처리 동의. 구체적 수집항목·보유기간 명시", "law": "개인정보보호법 제15조"},
        {"name": "직장 내 성희롱 예방 서약서", "required": False, "note": "권고. 입사 시 서약 징구 시 성희롱 예방교육 효과 제고", "law": "남녀고용평등법"},
        {"name": "복무서약서 (취업규칙 준수 서약)", "required": True, "note": "병원 취업규칙·복무규정 확인 및 준수 서약", "law": "근로기준법 제93조"},
    ],
    "자격·면허 관련 서류": [
        {"name": "면허(자격증) 원본 확인 및 사본 보관", "required": True, "note": "의료인 면허는 복지부 면허정보조회 시스템(www.mhw.go.kr)에서 실시간 확인 권장", "law": "의료법 제4조"},
        {"name": "보수교육 이수증 (해당자)", "required": False, "note": "의료인: 매년 8~12시간 보수교육 의무(의료법 제30조). 입사 시 최근 연도 이수증 확인 권장", "law": "의료법 제30조"},
        {"name": "전문의 자격증 사본 (해당자)", "required": False, "note": "전문의 수당·직책 부여 시 필요", "law": ""},
    ],
    "기타 서류": [
        {"name": "신원조회 동의서 및 결과", "required": False, "note": "아동·청소년 진료 기관: 아동청소년 성범죄 경력 조회 의무(아동복지법, 아청법). 성인만 진료하는 기관도 권고", "law": "아동·청소년의 성보호에 관한 법률 제56조"},
        {"name": "성범죄 경력 조회 동의서·결과서", "required": True, "note": "아동·청소년 관련 의료기관 전 종사자 의무. 취업제한 대상자 확인 필수. 채용 전 조회", "law": "아동·청소년의 성보호에 관한 법률 제56조"},
        {"name": "통장 사본 (급여 이체용)", "required": True, "note": "본인 명의 계좌. 압류 여부 확인 권장", "law": ""},
        {"name": "고용보험 피보험자 이력 확인", "required": False, "note": "전 직장 이직 확인서 연동. 실업급여 수급 이력 확인(사업주 참고용)", "law": "고용보험법"},
        {"name": "외국인 등록증 (해당자)", "required": False, "note": "외국인 근로자: 취업비자(E-6, E-7 등) 및 외국인 면허 확인. 보건복지부 면허 확인 필수", "law": "출입국관리법, 의료법"},
    ],
}

# ── 보수교육 데이터 ─────────────────────────────────────────────────────────────
CONTINUING_EDUCATION = [
    {
        "job": "의사 (전문의 포함)",
        "law": "의료법 제30조, 시행규칙 제20조",
        "hours": "연 8시간 이상",
        "org": "대한의사협회 (의사협회 보수교육센터)",
        "note": "온라인 가능. 미이수 시 면허 효력 정지 가능. 면허 신고(3년마다) 시 이수 확인",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "치과의사",
        "law": "의료법 제30조",
        "hours": "연 8시간 이상",
        "org": "대한치과의사협회",
        "note": "대한치과의사협회 보수교육 포털 이용",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "한의사",
        "law": "의료법 제30조",
        "hours": "연 8시간 이상",
        "org": "대한한의사협회",
        "note": "한의사협회 교육포털 이용",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "간호사",
        "law": "의료법 제30조",
        "hours": "연 8시간 이상",
        "org": "대한간호협회 (교육이수관리시스템)",
        "note": "온라인·집합 혼합. 전문간호사는 추가 요건 있음",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "간호조무사",
        "law": "의료법 제80조의2",
        "hours": "연 8시간 이상",
        "org": "대한간호조무사협회",
        "note": "자격 신고(3년마다) 시 이수 확인",
        "penalty": "자격신고 미이행 시 자격정지",
    },
    {
        "job": "방사선사",
        "law": "의료기사 등에 관한 법률 제20조",
        "hours": "연 12시간 이상",
        "org": "대한방사선사협회",
        "note": "면허 신고(3년마다). 매년 이수 권고",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "임상병리사",
        "law": "의료기사 등에 관한 법률 제20조",
        "hours": "연 12시간 이상",
        "org": "대한임상병리사협회",
        "note": "면허 신고(3년마다)",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "물리치료사",
        "law": "의료기사 등에 관한 법률 제20조",
        "hours": "연 12시간 이상",
        "org": "대한물리치료사협회",
        "note": "면허 신고(3년마다)",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "작업치료사",
        "law": "의료기사 등에 관한 법률 제20조",
        "hours": "연 12시간 이상",
        "org": "대한작업치료사협회",
        "note": "면허 신고(3년마다)",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
    {
        "job": "치과기공사 / 치과위생사",
        "law": "의료기사 등에 관한 법률 제20조",
        "hours": "연 12시간 이상",
        "org": "대한치과기공사협회 / 대한치과위생사협회",
        "note": "면허 신고(3년마다)",
        "penalty": "면허신고 미이행 시 면허 자격정지",
    },
]

# ── 연간 인사노무 일정 ─────────────────────────────────────────────────────────
ANNUAL_SCHEDULE = [
    {"month": "1월", "tasks": [
        "연말정산 서류 수집·처리 (전년도 귀속)",
        "4대보험 연말정산 (건강보험료 정산)",
        "최저임금 변경 확인 및 급여 반영",
        "연간 법정의무교육 계획 수립",
        "직원 정기건강진단 계획 수립",
    ]},
    {"month": "2월", "tasks": [
        "근로소득 지급명세서 제출 (2월 말까지)",
        "일용직 지급명세서 제출",
        "연말정산 환급·납부 처리",
    ]},
    {"month": "3월", "tasks": [
        "산업재해 현황 보고 (전년도)",
        "취업규칙 변경 신고 (해당 시)",
        "감염관리담당자 교육 계획 확인",
    ]},
    {"month": "4월", "tasks": [
        "건강보험료 정산 (4월 납부)",
        "장애인 의무고용 현황 신고",
        "1분기 산업안전보건교육 실시 확인",
    ]},
    {"month": "5월", "tasks": [
        "직장 내 성희롱 예방교육 상반기 실시",
        "개인정보보호 교육 실시",
        "근로자 건강진단 실시 (상반기)",
        "고용보험 피보험자 실태조사 제출",
    ]},
    {"month": "6월", "tasks": [
        "2분기 산업안전보건교육 실시",
        "직장 내 장애인 인식개선 교육 실시",
        "직장 내 괴롭힘 예방교육 실시",
        "상반기 결핵검진 미실시자 점검",
    ]},
    {"month": "7월", "tasks": [
        "최저임금 변경 시행 (매년 1월부터이나 하반기 재확인)",
        "3분기 산업안전보건교육 준비",
        "아동학대 신고의무자 교육 실시",
    ]},
    {"month": "8월", "tasks": [
        "의료인 보수교육 이수 현황 중간점검",
        "3분기 산업안전보건교육 실시",
        "근로계약서 갱신 대상자 확인 (계약직)",
    ]},
    {"month": "9월", "tasks": [
        "노인학대 신고의무자 교육 실시",
        "퇴직연금 교육 실시",
        "연간 교육이수 현황 중간점검",
    ]},
    {"month": "10월", "tasks": [
        "4분기 산업안전보건교육 준비",
        "연말정산 준비 안내 (직원 공지)",
        "내년도 최저임금 확인 및 급여체계 검토",
    ]},
    {"month": "11월", "tasks": [
        "4분기 산업안전보건교육 실시",
        "연간 법정의무교육 미이수자 보완 실시",
        "연간 결핵검진 미실시자 실시 독려",
        "아동학대·노인학대 교육결과 보건소 제출 준비",
    ]},
    {"month": "12월", "tasks": [
        "아동학대 신고의무자 교육결과 보건소 제출 (12월 말까지)",
        "노인학대 신고의무자 교육결과 보건소 제출 (12월 말까지)",
        "연간 법정의무교육 모든 항목 이수 최종 확인",
        "교육자료·수료증·교육일지 3년 보존 파일 정리",
        "다음 연도 4대보험 요율 확인",
        "다음 연도 근로계약서 갱신 준비",
    ]},
]

# ═══════════════════════════════════════════════════════════════════════════════
# 사이드바
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px;'>
      <div style='font-size:2.8rem;'>🏥</div>
      <div style='color:#FFFFFF; font-size:1.1rem; font-weight:700; margin-top:6px;'>병원 인사노무</div>
      <div style='color:#AED6F1; font-size:0.8rem; margin-top:2px;'>실무 가이드 시스템</div>
    </div>
    <hr style='border-color:#2980B9; margin:10px 0;'>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "메뉴 선택",
        [
            "🏠 홈 · 개요",
            "📋 신규입사자 체크리스트",
            "🚀 직원 온보딩 가이드",
            "📝 직무기술서(JD) 작성",
            "🧮 인사노무 스마트 계산기",
            "🤖 AI 인사노무 상담",
            "🎓 법정의무교육 가이드",
            "🩺 의료인 보수교육",
            "📅 연간 인사노무 일정",
            "⚠️ 과태료·처벌 기준",
            "❓ 자주 묻는 질문 (FAQ)",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#2980B9; margin:14px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.78rem; color:#7FB3D3; text-align:center; line-height:1.6;'>
      📅 최종 업데이트<br>
      <b style='color:#AED6F1;'>2026년 6월</b><br><br>
      ⚠️ 본 자료는 참고용이며<br>법령 변경 시 관계기관 확인 요망
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 페이지 라우팅
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🚀 직원 온보딩 가이드":
    render_onboarding_guide_page()
elif menu == "📝 직무기술서(JD) 작성":
    render_job_description_page()
elif menu == "🧮 인사노무 스마트 계산기":
    render_calculator_page()
elif menu == "🤖 AI 인사노무 상담":
    render_ai_consulting_page()

# ═══════════════════════════════════════════════════════════════════════════════
# 기존 페이지: 홈
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 홈 · 개요":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">🏥</div>
      <div>
        <h1>병원 인사노무 실무 가이드</h1>
        <p>신규 입사자 관리 · 법정의무교육 · 연간 일정 · 과태료 기준 — 실무 담당자를 위한 종합 가이드</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("📋", "입사 서류", "5개 분류", "32개 항목"),
        ("🎓", "법정의무교육", "11개 항목", "전체공통 7종"),
        ("⚠️", "최고 과태료", "5,000만원", "개인정보보호 위반"),
        ("📅", "연간 일정", "12개월", "월별 핵심 업무"),
    ]
    for col, (icon, title, val, sub) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="section-card" style="text-align:center; border-left-color:#1B6CA8;">
              <div style="font-size:2rem;">{icon}</div>
              <div style="font-size:0.85rem; color:#566573; font-weight:600;">{title}</div>
              <div style="font-size:1.4rem; font-weight:700; color:#0D3B6E;">{val}</div>
              <div style="font-size:0.8rem; color:#1B6CA8;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📌 이 가이드의 주요 기능")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="section-card">
          <h3>📋 신규 입사자 체크리스트</h3>
          <ul style="margin:0; padding-left:18px; font-size:0.9rem; color:#2C3E50; line-height:1.9;">
            <li>인사기본서류 완전 목록</li>
            <li>세금·4대보험 서류</li>
            <li>채용 건강진단 + 결핵검진 + 잠복결핵</li>
            <li>서약·동의 서류 (근로계약서 포함)</li>
            <li>성범죄 경력 조회 (아동·청소년 기관)</li>
            <li>근거 법령 링크 제공</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
          <h3>🎓 법정의무교육 가이드</h3>
          <ul style="margin:0; padding-left:18px; font-size:0.9rem; color:#2C3E50; line-height:1.9;">
            <li>11가지 교육 항목 상세 안내</li>
            <li>대상 / 주기 / 시간 / 방법</li>
            <li>교육 종료 후 제출처 명시</li>
            <li>위반 시 과태료 단계별 안내</li>
            <li>의원·병원·종합병원 적용 차이</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="section-card">
          <h3>🩺 의료인 보수교육</h3>
          <ul style="margin:0; padding-left:18px; font-size:0.9rem; color:#2C3E50; line-height:1.9;">
            <li>직종별 이수 시간·기관 안내</li>
            <li>면허 신고 주기 (3년마다)</li>
            <li>미이수 시 면허 자격정지 경고</li>
            <li>온라인 이수 방법 및 링크</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
          <h3>📅 연간 인사노무 일정</h3>
          <ul style="margin:0; padding-left:18px; font-size:0.9rem; color:#2C3E50; line-height:1.9;">
            <li>월별 핵심 업무 한눈에 확인</li>
            <li>연말정산·4대보험·교육 일정 통합</li>
            <li>누락 방지를 위한 체크 포인트</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="danger-box">
      ⚠️ <b>중요 안내:</b> 본 가이드는 2026년 6월 기준으로 작성되었습니다. 
      법령 및 행정지침은 수시로 변경되므로, 최신 법령은 
      <b>국가법령정보센터(law.go.kr)</b>, <b>고용노동부(moel.go.kr)</b>, 
      <b>보건복지부(mohw.go.kr)</b>에서 반드시 재확인하시기 바랍니다.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 페이지: 신규입사자 체크리스트
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "📋 신규입사자 체크리스트":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">📋</div>
      <div>
        <h1>신규 입사자 체크리스트</h1>
        <p>입사 시 징구해야 할 서류 목록 · 근거법령 · 실무 주의사항</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
      📌 <b>실무 포인트:</b> 입사일 기준으로 <b>근로계약서는 당일 교부</b>, 
      <b>4대보험 취득신고는 14일 이내</b>, 
      <b>결핵·잠복결핵 검진은 1개월 이내</b>에 완료해야 합니다.
    </div>
    """, unsafe_allow_html=True)

    # ── 기관 유형 선택
    st.subheader("🏥 기관 유형 선택")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        inst_type = st.selectbox("의료기관 종류", ["의원급 (의원·치과의원·한의원)", "병원급 (병원·치과병원·한방병원)", "종합병원·상급종합병원"])
    with col_b:
        child_care = st.checkbox("아동·청소년 진료 기관", value=False, help="소아청소년과, 아동병원 등 아동·청소년 대상 진료 시 체크")
    with col_c:
        elderly_care = st.checkbox("노인 관련 진료 기관", value=False, help="노인요양병원, 노인의원, 치매안심병원 등")

    st.markdown("---")

    for category, docs in ONBOARDING_DOCS.items():
        with st.expander(f"📁 {category}  ({len(docs)}개 항목)", expanded=True):
            for doc in docs:
                req = doc["required"]
                item_class = "required" if req else "optional"
                badge_html = '<span class="badge badge-red">필수</span>' if req else '<span class="badge badge-orange">해당시</span>'
                law_html = f'<span style="font-size:0.78rem; color:#2980B9;">📜 {doc["law"]}</span>' if doc["law"] else ""
                st.markdown(f"""
                <div class="checklist-item {item_class}">
                  <div style="flex-shrink:0; margin-top:2px;">
                    {"✅" if req else "🔲"}
                  </div>
                  <div>
                    <b>{doc["name"]}</b> {badge_html}<br>
                    <span style="font-size:0.85rem; color:#566573;">{doc["note"]}</span><br>
                    {law_html}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── 기관 유형별 추가 서류
    st.markdown("---")
    st.subheader("📌 기관 유형별 추가 확인 사항")

    if "병원급" in inst_type or "종합병원" in inst_type:
        st.markdown("""
        <div class="info-box">
          🏥 <b>병원급 이상 추가 의무:</b><br>
          • 산업안전보건교육 (분기별) — 5인 이상 보건업 의무<br>
          • 관리감독자: 안전보건교육 연 16시간 별도 이수<br>
          • 방사선 종사자: 배치 전 특수건강진단 실시 (방사선사, 수술실 종사자)<br>
          • 감염관리담당자 지정 및 연 24시간 교육 (의료법 제47조)
        </div>
        """, unsafe_allow_html=True)

    if child_care:
        st.markdown("""
        <div class="danger-box">
          👶 <b>아동·청소년 관련 기관 필수 추가 확인:</b><br>
          • <b>성범죄 경력 조회 필수</b> — 아동·청소년의 성보호에 관한 법률 제56조<br>
          &nbsp;&nbsp;&nbsp;→ 전 직원 대상. 취업 전 조회 의무. 확인서 보관 3년<br>
          • <b>아동학대 신고의무자 교육</b> — 아동복지법 제26조. 연 1회 이상<br>
          • 교육결과 보건소 제출 (매년 12월 말)<br>
          ⚠️ 미확인·미신고 시 과태료 + 취업 제한 해제 미조치 시 300만원 이하 과태료
        </div>
        """, unsafe_allow_html=True)

    if elderly_care:
        st.markdown("""
        <div class="warn-box">
          👴 <b>노인 관련 기관 추가 확인:</b><br>
          • <b>노인학대 신고의무자 교육</b> — 노인복지법 제39조의6. 연 1회 이상<br>
          • 교육결과 보건소 제출 (매년 12월 말)<br>
          • 보건복지부 배포 공식 자료 사용 필수 (자체 제작 불인정)
        </div>
        """, unsafe_allow_html=True)

    # ── 중요 기한 요약
    st.markdown("---")
    st.subheader("⏰ 입사 후 주요 처리 기한")
    st.markdown("""
    <table class="styled-table">
      <tr>
        <th>기한</th><th>업무</th><th>근거법령</th><th>비고</th>
      </tr>
      <tr>
        <td><b>당일</b></td>
        <td>근로계약서 작성·교부</td>
        <td>근로기준법 제17조</td>
        <td>전자문서 가능. 미교부 시 500만원 이하 과태료</td>
      </tr>
      <tr>
        <td><b>14일 이내</b></td>
        <td>4대보험 취득신고</td>
        <td>국민건강보험법, 국민연금법</td>
        <td>사업주 의무. 건강·연금·고용·산재 동시 신고</td>
      </tr>
      <tr>
        <td><b>1개월 이내</b></td>
        <td>결핵검진 (흉부 X선)</td>
        <td>결핵예방법 제11조</td>
        <td>채용 건강진단에 포함 실시 가능</td>
      </tr>
      <tr>
        <td><b>1개월 이내</b></td>
        <td>잠복결핵감염 검진 (TST 또는 IGRA)</td>
        <td>결핵예방법 시행규칙 제4조</td>
        <td>흉부 X선과 <b>별도</b> 실시. 결과 3년 보존</td>
      </tr>
      <tr>
        <td><b>배치 전</b></td>
        <td>특수건강진단 (해당자)</td>
        <td>산업안전보건법 제130조</td>
        <td>방사선·화학물질 취급 업무 배치 전</td>
      </tr>
      <tr>
        <td><b>채용 전</b></td>
        <td>성범죄 경력 조회 (아동기관)</td>
        <td>아청법 제56조</td>
        <td>아동·청소년 관련 기관 전 직원 의무</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 페이지: 법정의무교육 가이드
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🎓 법정의무교육 가이드":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">🎓</div>
      <div>
        <h1>법정의무교육 가이드</h1>
        <p>의료기관 종사자가 매년 이수해야 할 법정교육 — 항목별 대상·주기·방법·과태료 완전 정리</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
      ⚠️ <b>핵심 주의사항:</b> 
      아동학대·노인학대 신고의무자 교육 결과는 <b>매년 12월 말까지 관할 보건소에 제출</b>해야 합니다.
      단순 교육 실시만으로는 의무 완료가 아닙니다. 
      아동학대 교육은 <b>반드시 아동권리보장원 배포 자료</b>로 실시해야만 인정됩니다.
    </div>
    """, unsafe_allow_html=True)

    # ── 필터
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        cat_filter = st.selectbox(
            "카테고리 필터",
            ["전체", "전체공통", "병원급이상", "노인관련기관", "공공의료기관", "퇴직연금가입"]
        )
    with col_f2:
        search_kw = st.text_input("교육명 검색", placeholder="예: 성희롱, 결핵, 아동학대...")

    # ── 교육 항목 표시
    for edu in MANDATORY_EDUCATION:
        # 필터 적용
        if cat_filter != "전체" and edu["category"] != cat_filter:
            continue
        if search_kw and search_kw.lower() not in edu["name"].lower():
            continue

        color_map = {"red": "#E74C3C", "orange": "#F39C12", "blue": "#2980B9", "gray": "#95A5A6"}
        border_color = color_map.get(edu["color"], "#1B6CA8")

        category_labels = {
            "전체공통": "🔴 전체공통",
            "병원급이상": "🟠 병원급이상",
            "노인관련기관": "🟡 노인관련기관",
            "공공의료기관": "⚪ 공공기관",
            "퇴직연금가입": "🔵 퇴직연금가입",
        }

        with st.expander(
            f"{'⚡' if edu['color']=='red' else '📘'} {edu['no']:02d}. {edu['name']}  "
            f"[{category_labels.get(edu['category'], edu['category'])}]",
            expanded=False
        ):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"""
                <table class="styled-table">
                  <tr><th width="30%">항목</th><th>내용</th></tr>
                  <tr><td>📜 근거법령</td><td>{edu['law']}</td></tr>
                  <tr><td>👥 교육 대상</td><td>{edu['target']}</td></tr>
                  <tr><td>🔄 교육 주기</td><td><b>{edu['cycle']}</b></td></tr>
                  <tr><td>⏱️ 교육 시간</td><td>{edu['hours']}</td></tr>
                  <tr><td>📚 교육 방법</td><td>{edu['method']}</td></tr>
                  <tr><td>📨 결과 제출처</td><td><b>{edu['submit']}</b></td></tr>
                </table>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="danger-box">
                  <b>💰 위반 시 과태료</b><br><br>
                  <span class="penalty-chip">{edu['penalty']}</span><br><br>
                  {edu['penalty_detail']}
                </div>
                <div class="info-box" style="margin-top:10px;">
                  <b>📌 실무 주의사항</b><br>
                  {edu['note']}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 교육 종류별 요약 테이블
    st.subheader("📊 법정의무교육 전체 요약 테이블")

    rows = []
    for edu in MANDATORY_EDUCATION:
        rows.append({
            "No": edu["no"],
            "교육명": edu["name"],
            "대상": edu["target"][:30] + "..." if len(edu["target"]) > 30 else edu["target"],
            "주기": edu["cycle"],
            "시간": edu["hours"],
            "제출처": edu["submit"],
            "최대과태료": edu["penalty"],
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 페이지: 의료인 보수교육
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🩺 의료인 보수교육":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">🩺</div>
      <div>
        <h1>의료인 · 의료기사 보수교육</h1>
        <p>직종별 연간 이수 시간 · 소관 협회 · 면허신고 주기 · 미이수 시 제재</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="danger-box">
      🚨 <b>경고:</b> 의료인·의료기사 보수교육 미이수 시 <b>면허 효력 정지(자격정지)</b>가 발생할 수 있습니다.
      보수교육은 법정의무교육과 <b>별도</b>로 관리되며, 면허신고(3년마다)와 연동됩니다.
    </div>
    """, unsafe_allow_html=True)

    # ── 보수교육 상세 테이블
    st.subheader("📋 직종별 보수교육 상세")

    for edu in CONTINUING_EDUCATION:
        st.markdown(f"""
        <div class="section-card">
          <h3>👤 {edu['job']}</h3>
          <table class="styled-table">
            <tr>
              <td width="20%"><b>📜 근거법령</b></td>
              <td>{edu['law']}</td>
              <td width="20%"><b>⏱️ 이수 시간</b></td>
              <td><b style="color:#C0392B;">{edu['hours']}</b></td>
            </tr>
            <tr>
              <td><b>🏛️ 소관 협회</b></td>
              <td>{edu['org']}</td>
              <td><b>⚠️ 미이수 제재</b></td>
              <td><span class="penalty-chip">{edu['penalty']}</span></td>
            </tr>
            <tr>
              <td colspan="4"><b>📌 비고:</b> {edu['note']}</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔗 보수교육 온라인 이수 주요 링크")
    st.markdown("""
    <table class="styled-table">
      <tr>
        <th>직종</th><th>시스템명</th><th>URL</th>
      </tr>
      <tr>
        <td>의사</td>
        <td>대한의사협회 보수교육센터</td>
        <td><a href="https://edu.kma.org" target="_blank">edu.kma.org</a></td>
      </tr>
      <tr>
        <td>치과의사</td>
        <td>대한치과의사협회 교육포털</td>
        <td><a href="https://edu.kda.or.kr" target="_blank">edu.kda.or.kr</a></td>
      </tr>
      <tr>
        <td>한의사</td>
        <td>대한한의사협회</td>
        <td><a href="https://www.akom.org" target="_blank">akom.org</a></td>
      </tr>
      <tr>
        <td>간호사</td>
        <td>대한간호협회 교육이수관리시스템</td>
        <td><a href="https://edu.koreanurse.or.kr" target="_blank">edu.koreanurse.or.kr</a></td>
      </tr>
      <tr>
        <td>간호조무사</td>
        <td>대한간호조무사협회</td>
        <td><a href="https://www.kasna.or.kr" target="_blank">kasna.or.kr</a></td>
      </tr>
      <tr>
        <td>방사선사·임상병리사 등 의료기사</td>
        <td>의료기사국가시험원 / 각 협회</td>
        <td>각 협회 홈페이지 참조</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="margin-top:16px;">
      💡 <b>면허신고 안내:</b> 의료인은 <b>3년마다 보건복지부</b>에 면허신고 의무가 있습니다.
      신고 시 보수교육 이수 여부를 확인하며, 미신고 시 면허 효력 정지가 발생합니다.
      면허신고는 <a href="https://www.mhw.go.kr" target="_blank">보건복지부 의료인 면허신고 시스템</a>에서 가능합니다.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 페이지: 연간 인사노무 일정
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "📅 연간 인사노무 일정":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">📅</div>
      <div>
        <h1>연간 인사노무 업무 일정</h1>
        <p>월별 핵심 업무 · 법정교육 일정 · 신고·제출 마감일 한눈에 보기</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    current_month = datetime.now().month
    st.markdown(f"""
    <div class="info-box">
      📌 현재 월: <b>{current_month}월</b> — 해당 월의 업무를 우선 확인하세요.
    </div>
    """, unsafe_allow_html=True)

    # ── 월별 카드 레이아웃
    cols_per_row = 3
    for i in range(0, len(ANNUAL_SCHEDULE), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(ANNUAL_SCHEDULE):
                sched = ANNUAL_SCHEDULE[i + j]
                month_num = i + j + 1
                is_current = month_num == current_month
                border = "5px solid #E74C3C" if is_current else "5px solid #1B6CA8"
                bg = "#FFF5F5" if is_current else "#FFFFFF"
                header_style = "color:#C0392B; font-weight:800;" if is_current else "color:#0D3B6E; font-weight:700;"

                task_items = "".join([
                    f'<li style="margin-bottom:4px; font-size:0.85rem;">{t}</li>'
                    for t in sched["tasks"]
                ])
                current_badge = ' <span class="badge badge-red">이번 달</span>' if is_current else ""

                with col:
                    st.markdown(f"""
                    <div style="background:{bg}; border:1px solid #D5E8F5; border-left:{border};
                                border-radius:10px; padding:16px; margin-bottom:14px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.06); min-height:180px;">
                      <div style="{header_style} font-size:1.1rem; margin-bottom:10px;">
                        📅 {sched['month']}{current_badge}
                      </div>
                      <ul style="margin:0; padding-left:16px; color:#2C3E50; line-height:1.7;">
                        {task_items}
                      </ul>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📆 연도별 반복 주요 마감 일정")
    st.markdown("""
    <table class="styled-table">
      <tr><th>마감 시기</th><th>업무</th><th>제출처</th><th>비고</th></tr>
      <tr>
        <td>매년 2월 말</td>
        <td>근로소득 지급명세서 제출</td>
        <td>국세청 홈택스</td>
        <td>전년도 귀속</td>
      </tr>
      <tr>
        <td>매년 4월</td>
        <td>건강보험료 연말정산 납부</td>
        <td>국민건강보험공단</td>
        <td>전년도 보수총액 기준 정산</td>
      </tr>
      <tr>
        <td>매년 12월 말</td>
        <td>아동학대 신고의무자 교육결과 제출</td>
        <td>관할 보건소</td>
        <td>⚠️ 미제출 시 과태료</td>
      </tr>
      <tr>
        <td>매년 12월 말</td>
        <td>노인학대 신고의무자 교육결과 제출</td>
        <td>관할 보건소</td>
        <td>⚠️ 해당 기관만</td>
      </tr>
      <tr>
        <td>매년 12월 31일</td>
        <td>연간 법정의무교육 전 항목 이수 완료</td>
        <td>자체 보관</td>
        <td>교육자료·수료증 3년 보존</td>
      </tr>
      <tr>
        <td>3년마다</td>
        <td>의료인 면허 신고</td>
        <td>보건복지부</td>
        <td>보수교육 이수 확인 포함</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 페이지: 과태료·처벌 기준
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "⚠️ 과태료·처벌 기준":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">⚠️</div>
      <div>
        <h1>과태료 · 처벌 기준 가이드</h1>
        <p>의무 불이행 시 발생하는 과태료·행정처분 기준 정리 — 사전 예방이 최선입니다</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="danger-box">
      🚨 <b>경고:</b> 과태료는 위반 횟수에 따라 <b>가중부과</b>됩니다. 
      단순 미실시뿐 아니라 <b>교육자료 미보존(3년)</b>만으로도 과태료 대상이 될 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

    penalty_data = [
        {
            "category": "노동·고용",
            "items": [
                ["근로계약서 미교부", "근로기준법 제17조", "500만원 이하 과태료", "1회 위반 시 즉시 부과 가능. 근로자 1인당"],
                ["최저임금 미준수", "최저임금법 제6조", "2천만원 이하 벌금 또는 3년 이하 징역", "형사처벌 사안"],
                ["4대보험 취득신고 지연", "국민건강보험법 등", "과태료 + 소급 보험료 납부", "14일 이내 미신고"],
                ["직장 내 성희롱 예방교육 미실시", "남녀고용평등법 제39조", "1차 300만원 / 2차 400만원 / 3차 500만원", "교육자료 미보존도 동일 과태료"],
                ["직장 내 장애인 인식개선 미실시", "장애인고용법", "1차 100만원 / 2차 200만원 / 3차 300만원", ""],
                ["직장 내 괴롭힘 취업규칙 미기재", "근로기준법 제93조", "500만원 이하 과태료", "10인 이상 사업장"],
                ["산업안전보건교육 미실시", "산업안전보건법 제29조", "근로자 1인당 1차 50만원 / 2차 100만원 / 3차 150만원", "분기별 미실시 시 가중"],
                ["퇴직연금 교육 미실시", "근로자퇴직급여 보장법", "1천만원 이하 과태료", "퇴직연금 가입 사업장만"],
            ],
        },
        {
            "category": "의료·보건",
            "items": [
                ["결핵검진 미실시", "결핵예방법 제11조", "200만원 이하 과태료", "신규입사 1개월 이내 미실시"],
                ["잠복결핵검진 결과 미보존", "결핵예방법", "200만원 이하 과태료", "3년 보존 의무 위반"],
                ["아동학대 교육결과 미제출", "아동복지법 제26조", "1차 100만원 / 2차 200만원 / 3차 300만원", "12월 말 보건소 제출 미이행"],
                ["노인학대 교육결과 미제출", "노인복지법", "1차 100만원 / 2차 200만원 / 3차 300만원", "해당 기관만"],
                ["감염관리 교육 미이수 (감염관리담당자)", "의료법 제47조", "시정명령→15일 업무정지", "행정처분 사안"],
                ["성범죄 경력 미조회 (아동기관)", "아청법 제56조", "1천만원 이하 과태료", "아동·청소년 관련 기관 전 직원 의무"],
                ["의료인 면허 미신고 (3년)", "의료법", "면허 효력 정지", "보수교육 미이수 포함"],
            ],
        },
        {
            "category": "개인정보",
            "items": [
                ["개인정보 안전조치 위반", "개인정보보호법 제29조", "3천만원 이하 과태료", "암호화·접근권한 미설정 등"],
                ["개인정보 교육 미실시", "개인정보보호법 제28조", "1천만원 이하 과태료", "취급직원 전원 대상"],
                ["개인정보 유출 (고의·과실)", "개인정보보호법", "최대 5억원 과징금 + 형사처벌", "5년 이하 징역 또는 5천만원 이하 벌금"],
                ["개인정보처리방침 미공개", "개인정보보호법 제30조", "1천만원 이하 과태료", "홈페이지·원내 게시 의무"],
            ],
        },
    ]

    for section in penalty_data:
        st.subheader(f"📌 {section['category']} 관련 과태료")
        st.markdown("""
        <table class="styled-table">
          <tr><th>위반 사항</th><th>근거법령</th><th>과태료·처벌</th><th>비고</th></tr>
        """ + "".join([
            f"<tr><td>{r[0]}</td><td>{r[1]}</td>"
            f"<td><b style='color:#C0392B;'>{r[2]}</b></td><td>{r[3]}</td></tr>"
            for r in section["items"]
        ]) + "</table>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      💡 <b>과태료 경감 팁:</b> 「질서위반행위규제법」 제18조에 따라 의견 제출 기한 내 
      자진납부 시 <b>20% 범위 내 감경</b>이 가능합니다. 
      또한 고용노동부 자율개선 기간 중 자진 시정 시 과태료가 면제·감경될 수 있습니다.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 페이지: FAQ
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "❓ 자주 묻는 질문 (FAQ)":
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">❓</div>
      <div>
        <h1>자주 묻는 질문 (FAQ)</h1>
        <p>실무 현장에서 자주 헷갈리는 질문들을 모았습니다</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        {
            "q": "Q. 의원급은 산업안전보건교육을 받아야 하나요?",
            "a": """
            <b>의원급은 원칙적으로 적용 제외이나, 조건에 따라 다릅니다.</b><br><br>
            • 의원급이라도 <b>상시 근로자 5인 이상</b>이면 적용 (단, 의사·치과의사·한의사만으로 구성된 경우 일부 제외 해석 있음)<br>
            • <b>병원급 이상(병원·종합병원)</b>은 보건업 종사자로서 5인 이상이면 분기별 안전보건교육 의무<br>
            • 사무직(원무과·행정): 분기 3시간 이상 / 비사무직(간호사·의료기사): 분기 6시간 이상<br>
            • 관리감독자(팀장·부서장): 별도 연 16시간 이상<br><br>
            <b>실무 팁:</b> 의원급이라도 5인 이상이면 교육 실시를 권고합니다. 고용노동부 해석은 사안별로 다를 수 있으니 확인 요망.
            """,
        },
        {
            "q": "Q. 잠복결핵감염 검진을 기존 채용 건강진단에 포함해서 받아도 되나요?",
            "a": """
            <b>채용 건강진단에 포함하는 것이 가능하나, 잠복결핵 검진은 반드시 별도 항목으로 실시해야 합니다.</b><br><br>
            • 흉부 X선(결핵검진)과 잠복결핵감염검진(TST 또는 IGRA)은 <b>서로 다른 검사</b>입니다.<br>
            • 동일 날짜·동일 의료기관에서 함께 받는 것은 가능하나, 검사 항목은 반드시 구분 실시<br>
            • 결과 기록을 <b>3년간 보존</b>해야 하며, 미보존 시 과태료 대상<br>
            • 채용 건강진단 기관에 사전 요청하여 한 번에 진행하는 방법 권장
            """,
        },
        {
            "q": "Q. 아동학대 신고의무자 교육을 유튜브 영상이나 자체 제작 자료로 진행해도 되나요?",
            "a": """
            <b>안 됩니다. 반드시 아동권리보장원에서 배포한 공식 자료로만 교육해야 합니다.</b><br><br>
            • 유튜브, 자체 제작 PPT, 외부 교육기관 자료 등은 인정 <b>불가</b><br>
            • <b>아동권리보장원(www.ncrc.or.kr)</b> 홈페이지에서 최신 교육자료 다운로드<br>
            • 교육 후 교육일지, 출석명부, 수료증을 보관하고 <b>12월 말까지 관할 보건소에 결과 제출</b><br>
            • 노인학대 교육도 동일 원칙: 반드시 <b>보건복지부 배포 자료</b>로 실시
            """,
        },
        {
            "q": "Q. 직장 내 성희롱 예방교육을 온라인으로 실시해도 되나요?",
            "a": """
            <b>가능하나, 사업장 규모에 따라 조건이 다릅니다.</b><br><br>
            • <b>10인 미만 사업장:</b> 온라인 포함 어떤 방식도 가능 (홍보물 게시, 교육자료 배포 등도 인정)<br>
            • <b>10인 이상:</b> 영상·온라인 교육 가능하나 수료 여부 확인 필수. 단순 배포는 불인정<br>
            • <b>사업주 본인도</b> 교육 대상 (소규모 의원에서 놓치기 쉬운 부분)<br>
            • 교육일지, 출석명부, 수료증 등 증빙 서류 <b>3년 보존</b> 필수
            """,
        },
        {
            "q": "Q. 간호조무사도 보수교육을 받아야 하나요? 의무인가요?",
            "a": """
            <b>네, 의무입니다.</b> 간호조무사는 의료법이 아닌 의료법 제80조의2에 따라 보수교육 의무가 있습니다.<br><br>
            • 소관 기관: <b>대한간호조무사협회</b><br>
            • 이수 시간: 연 8시간 이상<br>
            • 자격 신고(3년마다)와 연동되며, 미이수 시 자격 효력 정지<br>
            • 온라인 이수 가능 (대한간호조무사협회 홈페이지: kasna.or.kr)
            """,
        },
        {
            "q": "Q. 근로계약서를 전자문서로 작성해도 법적으로 유효한가요?",
            "a": """
            <b>네, 유효합니다.</b> 전자문서 및 전자거래 기본법에 따라 전자서명이 있는 전자 근로계약서는 서면과 동일한 효력을 가집니다.<br><br>
            • 조건: 전자서명법에 따른 전자서명 필요 (카카오페이, 네이버 전자서명 등 공인된 서비스 활용)<br>
            • 단순 이메일 첨부나 카카오톡 전송은 전자 서명 없이는 효력 불명확<br>
            • 근로자가 원하는 경우 서면 교부도 가능하도록 해야 함<br>
            • <b>교부 의무:</b> 임금, 근로시간, 휴일, 연차유급휴가 등 필수 기재사항을 포함해야 함
            """,
        },
        {
            "q": "Q. 파트타임(단시간)·계약직 직원도 법정의무교육 대상인가요?",
            "a": """
            <b>네, 대부분의 법정의무교육은 고용형태에 관계없이 전 직원이 대상입니다.</b><br><br>
            • 성희롱 예방, 개인정보보호, 장애인 인식개선, 직장 내 괴롭힘 예방 교육은 <b>파트타임·계약직 포함 전 직원</b><br>
            • 산업안전보건교육은 근로 형태(단시간·기간제)에 관계없이 적용<br>
            • 결핵검진: 근무일 수에 관계없이 의료기관 종사자면 의무<br>
            • 실무 팁: 교육 참여 어려운 파트타임 직원은 온라인 교육 이수를 활용하고 수료증 보관 필수
            """,
        },
        {
            "q": "Q. B형간염 항체가 없는 신규 직원에게 예방접종을 강제할 수 있나요?",
            "a": """
            <b>법적 강제 접종은 불가하나, 사업주는 예방접종을 강력히 권고하고 비용을 지원해야 합니다.</b><br><br>
            • 의료관련감염 예방관리 지침상 의료기관 종사자 B형간염 예방접종 권고<br>
            • 항원 양성자(보균자)는 혈액·체액 노출 가능성이 높은 업무 배치 조정 검토 필요<br>
            • 항체 미보유자에 대한 <b>3회 접종 비용은 사업주 부담</b> 권고 (산업재해 예방 목적)<br>
            • 접종 거부 시 서면 동의서 받아 보관 (향후 감염 발생 시 책임 소재 명확화)
            """,
        },
        {
            "q": "Q. 교육자료나 수료증을 몇 년이나 보관해야 하나요?",
            "a": """
            <b>법정의무교육 관련 서류는 원칙적으로 3년 보존입니다.</b><br><br>
            <table class="styled-table">
              <tr><th>서류 종류</th><th>보존 기간</th><th>근거</th></tr>
              <tr><td>법정의무교육 자료·수료증·교육일지</td><td>3년</td><td>각 개별 법령</td></tr>
              <tr><td>근로계약서</td><td>퇴직 후 3년</td><td>근로기준법 제42조</td></tr>
              <tr><td>결핵·잠복결핵 검진 결과</td><td>3년</td><td>결핵예방법</td></tr>
              <tr><td>채용 건강진단 결과</td><td>5년 (특수건강진단 30년)</td><td>산업안전보건법</td></tr>
              <tr><td>4대보험 서류</td><td>3~5년</td><td>각 보험법</td></tr>
              <tr><td>임금대장</td><td>3년</td><td>근로기준법 제42조</td></tr>
            </table>
            """,
        },
        {
            "q": "Q. 신규입사자가 이전 직장에서 이미 잠복결핵 검진을 받았다면 다시 받아야 하나요?",
            "a": """
            <b>원칙적으로 새 의료기관 입사 시 1개월 이내에 다시 받아야 하지만, 예외가 있습니다.</b><br><br>
            • 법 취지: 의료기관 간 이동 시마다 중복 검진 방지 목적으로 <b>동일 시설군(의료기관·산후조리원·학교 등) 간 이동은 1회만 실시</b> 해석도 가능<br>
            • 실무 적용: 타 의료기관에서 발급받은 최근 잠복결핵 검진 결과서를 제출하면 수용하는 경우가 많음<br>
            • 단, <b>6개월 이상 의료 업무 공백 후 복귀자</b>는 반드시 재검진 필요<br>
            • 보건소·질병관리청에 확인하여 지역별 적용 기준을 명확히 파악 권고
            """,
        },
    ]

    for faq in faqs:
        with st.expander(faq["q"], expanded=False):
            st.markdown(f"""
            <div class="info-box">
              {faq["a"]}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="success-box">
      ✅ <b>추가 문의처</b><br><br>
      • <b>고용노동부 고객상담센터</b>: ☎ 1350 (노동관계법, 임금, 4대보험)<br>
      • <b>국민건강보험공단</b>: ☎ 1577-1000 (건강보험 취득·상실 신고)<br>
      • <b>국민연금공단</b>: ☎ 1355 (국민연금 취득·상실 신고)<br>
      • <b>근로복지공단</b>: ☎ 1588-0075 (산재보험, 고용보험)<br>
      • <b>보건복지부 상담센터</b>: ☎ 129 (의료법, 감염관리, 결핵예방)<br>
      • <b>질병관리청 콜센터</b>: ☎ 1339 (결핵·잠복결핵 검진 문의)<br>
      • <b>아동권리보장원</b>: ☎ 02-6383-9114 (아동학대 교육자료 문의)<br>
      • <b>개인정보보호위원회</b>: ☎ 국번없이 182 (개인정보 보호 법령 문의)
    </div>
    """, unsafe_allow_html=True)
