"""
직무기술서(Job Description) 모듈
병원 직종별 사전 템플릿 + 커스텀 작성 + HTML 다운로드 기능
"""
import streamlit as st
import base64
from datetime import datetime

# ── 병원 직종별 JD 사전 템플릿 ─────────────────────────────────────────────────
JD_TEMPLATES = {
    "직접 선택하지 않음": None,
    "간호사 (병동)": {
        "직무명": "병동 간호사 (RN)",
        "소속부서": "간호부",
        "직급": "간호사",
        "직책": "스태프",
        "보고체계": "수간호사 → 간호부장",
        "직무목적": "병동 입원 환자에게 전문적인 간호 서비스를 제공하여 환자의 건강 회복 및 안전을 도모하고, 의료팀과의 협력을 통해 최상의 의료 서비스 실현에 기여한다.",
        "주요업무": [
            "입원 환자의 활력징후 측정, 투약, 처치 등 기본 간호 업무 수행",
            "의사 처방 확인 및 정확한 투약 관리 (5 Rights 준수)",
            "환자 및 보호자 교육 (퇴원 교육, 투약 교육, 질환 관리 등)",
            "간호기록 작성 및 EMR 입력 (입원 사정, 간호 계획, 경과 기록)",
            "응급 상황 발생 시 초기 대응 및 의료팀 보고",
            "감염 예방 및 관리 지침 준수 (손위생, 격리 지침 등)",
            "의료기기 및 물품 관리 (재고 확인, 이상 유무 점검)",
        ],
        "자격요건": {
            "학력": "간호학과 전문학사 이상",
            "경력": "신입 가능 (경력자 우대)",
            "필수면허": "간호사 면허증 (RN)",
            "우대사항": "BLS(기본심폐소생술) 이수자, 병동 근무 경력자",
        },
        "핵심역량": [
            "환자 중심의 공감 능력 및 커뮤니케이션",
            "정확하고 신속한 임상 판단력",
            "팀워크 및 다직종 협업 능력",
            "꼼꼼함과 책임감",
        ],
        "근무조건": {
            "근무형태": "정규직 (3교대: 낮번/저녁번/밤번)",
            "근무시간": "8시간 교대 근무 (낮 07:00~15:30, 저녁 15:00~23:30, 밤 23:00~07:30)",
            "급여수준": "병원 내규에 따름 (경력 반영)",
        },
        "주요KPI": ["환자 낙상 발생률", "투약 오류 발생률", "환자 만족도 점수", "간호 기록 완성도"],
    },
    "원무과 직원": {
        "직무명": "원무과 직원",
        "소속부서": "원무과",
        "직급": "사원/주임",
        "직책": "스태프",
        "보고체계": "원무과장",
        "직무목적": "환자의 접수, 수납, 보험 청구 업무를 정확하고 친절하게 처리하여 원활한 의료 서비스 제공을 지원하고 병원의 재정 건전성에 기여한다.",
        "주요업무": [
            "외래 환자 접수 및 예약 관리 (전화, 온라인, 방문 접수)",
            "진료비 수납 및 영수증 발급 (현금, 카드, 보험 처리)",
            "건강보험 및 의료급여 청구 업무 (EDI 청구, 심사 결과 관리)",
            "입·퇴원 수속 처리 및 병실 배정 지원",
            "환자 민원 접수 및 1차 응대 처리",
            "의무기록 발급 및 관리 (진단서, 소견서, 진료기록 사본)",
            "각종 증명서 발급 (재직증명서 제외, 의료 관련 증명서)",
        ],
        "자격요건": {
            "학력": "고졸 이상 (전문대졸 우대)",
            "경력": "신입 가능",
            "필수면허": "해당 없음",
            "우대사항": "의무행정사 자격증, 병원 원무 경력자, 의료정보시스템(EMR) 사용 경험자",
        },
        "핵심역량": [
            "친절하고 신속한 고객 서비스 마인드",
            "정확한 숫자 처리 능력 및 꼼꼼함",
            "건강보험 청구 관련 기초 지식",
            "컴퓨터 활용 능력 (MS Office, EMR)",
        ],
        "근무조건": {
            "근무형태": "정규직 (주간 근무)",
            "근무시간": "09:00~18:00 (주 5일, 점심 1시간)",
            "급여수준": "병원 내규에 따름",
        },
        "주요KPI": ["수납 오류율", "청구 반려율", "환자 대기 시간", "민원 처리 만족도"],
    },
    "의료기사 (방사선사)": {
        "직무명": "방사선사",
        "소속부서": "영상의학과",
        "직급": "방사선사",
        "직책": "스태프",
        "보고체계": "영상의학과 주임 → 과장",
        "직무목적": "환자에게 안전하고 정확한 방사선 검사를 시행하여 정확한 진단을 위한 고품질 영상 자료를 제공하고, 방사선 안전 관리를 통해 환자 및 직원을 보호한다.",
        "주요업무": [
            "일반 방사선 촬영 (X-ray), CT, MRI 검사 시행",
            "검사 전 환자 확인 및 검사 목적 설명",
            "방사선 장비 일일 점검 및 QC(품질관리) 수행",
            "방사선 피폭 관리 및 방사선 안전 수칙 준수",
            "영상 판독 보조 및 PACS 시스템 관리",
            "조영제 투여 보조 및 환자 모니터링",
            "방사선 관계 종사자 피폭 선량 관리",
        ],
        "자격요건": {
            "학력": "방사선학과 전문학사 이상",
            "경력": "신입 가능",
            "필수면허": "방사선사 면허증",
            "우대사항": "CT/MRI 경력자, 방사선 취급 면허 보유자",
        },
        "핵심역량": [
            "방사선 안전 의식 및 환자 보호 마인드",
            "정밀한 영상 촬영 기술",
            "응급 상황 대처 능력",
            "의료팀과의 원활한 소통",
        ],
        "근무조건": {
            "근무형태": "정규직 (교대 근무 가능)",
            "근무시간": "주간/야간 교대 (병원 규모에 따라 상이)",
            "급여수준": "병원 내규에 따름 (면허 수당 포함)",
        },
        "주요KPI": ["영상 재촬영률", "검사 대기 시간", "장비 가동률", "방사선 피폭 관리 준수율"],
    },
    "의무기록사": {
        "직무명": "의무기록사",
        "소속부서": "의무기록실",
        "직급": "의무기록사",
        "직책": "스태프",
        "보고체계": "의무기록실장 → 행정부장",
        "직무목적": "의료기관 내 모든 환자의 의무기록을 체계적으로 관리하고, 의료 정보의 정확성과 보안을 유지하여 진료의 연속성 및 법적 요건을 충족시킨다.",
        "주요업무": [
            "입·퇴원 환자 의무기록 수집, 분류, 코딩 (KCD 진단코드 부여)",
            "의무기록 완결도 점검 및 미완결 기록 독려",
            "의무기록 사본 발급 및 열람 요청 처리 (개인정보보호법 준수)",
            "건강보험 심사 청구를 위한 기록 검토 지원",
            "의무기록 보존 및 폐기 관리 (법정 보존 기간 준수)",
            "의료 통계 작성 및 보고 (입원율, 평균 재원일수 등)",
            "암 등록 사업 관련 자료 수집 및 보고",
        ],
        "자격요건": {
            "학력": "의무기록학과 전문학사 이상",
            "경력": "신입 가능",
            "필수면허": "의무기록사 면허증",
            "우대사항": "RHIA/RHIT 자격 보유자, KCD 코딩 경력자",
        },
        "핵심역량": [
            "의학 용어 및 KCD 코딩 지식",
            "개인정보보호에 대한 높은 윤리 의식",
            "꼼꼼한 기록 관리 능력",
            "의료정보시스템(EMR, HIS) 활용 능력",
        ],
        "근무조건": {
            "근무형태": "정규직 (주간 근무)",
            "근무시간": "09:00~18:00 (주 5일)",
            "급여수준": "병원 내규에 따름",
        },
        "주요KPI": ["의무기록 완결율", "코딩 정확도", "기록 발급 처리 시간", "개인정보 보안 사고 건수"],
    },
    "간호조무사": {
        "직무명": "간호조무사",
        "소속부서": "간호부 / 해당 진료과",
        "직급": "간호조무사",
        "직책": "스태프",
        "보고체계": "담당 간호사 → 수간호사",
        "직무목적": "간호사의 지도 하에 환자 간호 보조 업무를 수행하여 환자의 안위와 안전을 도모하고 원활한 진료 지원을 통해 의료 서비스의 질 향상에 기여한다.",
        "주요업무": [
            "간호사 지도 하 활력징후 측정 및 기록 보조",
            "환자 이동 보조 (이송, 체위 변경, 보행 보조)",
            "진료 준비 및 의료 소모품 정리·보충",
            "병실 환경 관리 (청결 유지, 물품 정리)",
            "환자 식사 보조 및 영양 섭취 관찰",
            "검체 운반 및 처방 전달 보조",
            "환자 및 보호자 안내 및 기본 응대",
        ],
        "자격요건": {
            "학력": "고졸 이상",
            "경력": "신입 가능",
            "필수면허": "간호조무사 자격증",
            "우대사항": "병원 근무 경력자, 요양보호사 자격 보유자",
        },
        "핵심역량": [
            "환자에 대한 따뜻한 배려와 친절",
            "체력 및 신체적 건강",
            "팀워크 및 지시 이행 능력",
            "기본적인 의학 지식 및 감염 예방 수칙 이해",
        ],
        "근무조건": {
            "근무형태": "정규직 / 계약직 (교대 근무 가능)",
            "근무시간": "8시간 교대 또는 주간 근무",
            "급여수준": "병원 내규에 따름",
        },
        "주요KPI": ["환자 낙상 보조 예방 기여도", "물품 관리 정확도", "환자 만족도"],
    },
    "직접 작성 (커스텀)": {
        "직무명": "",
        "소속부서": "",
        "직급": "",
        "직책": "",
        "보고체계": "",
        "직무목적": "",
        "주요업무": ["", "", "", "", ""],
        "자격요건": {"학력": "", "경력": "", "필수면허": "", "우대사항": ""},
        "핵심역량": ["", "", ""],
        "근무조건": {"근무형태": "", "근무시간": "", "급여수준": ""},
        "주요KPI": ["", "", ""],
    },
}

def generate_html_content(data: dict, hospital_name: str) -> str:
    today = datetime.now().strftime("%Y년 %m월 %d일")
    tasks_html = "\n".join([f"<li>{t}</li>" for t in data.get("주요업무", []) if t.strip()])
    comps_html = "\n".join([f"<li>{c}</li>" for c in data.get("핵심역량", []) if c.strip()])
    kpi_html = "\n".join([f"<li>{k}</li>" for k in data.get("주요KPI", []) if k.strip()])
    req = data.get("자격요건", {})
    wc = data.get("근무조건", {})

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data.get('직무명', '직무기술서')}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Noto Sans KR', sans-serif; color: #2c3e50; background: #f8f9fa; }}
  .wrapper {{ max-width: 860px; margin: 30px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }}
  .header {{ background: linear-gradient(135deg, #0D3B6E 0%, #1B6CA8 100%); color: #fff; padding: 36px 40px; }}
  .header .hospital {{ font-size: 0.9rem; color: #AED6F1; margin-bottom: 6px; letter-spacing: 1px; text-transform: uppercase; }}
  .header h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; }}
  .header .meta {{ font-size: 0.85rem; color: #AED6F1; }}
  .body {{ padding: 36px 40px; }}
  .section {{ margin-bottom: 32px; }}
  .section-title {{ font-size: 1rem; font-weight: 700; color: #0D3B6E; border-left: 4px solid #1B6CA8; padding-left: 12px; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .info-item {{ background: #f4f9fd; border: 1px solid #d5e8f5; border-radius: 8px; padding: 12px 16px; }}
  .info-item .label {{ font-size: 0.75rem; color: #1B6CA8; font-weight: 600; margin-bottom: 4px; text-transform: uppercase; }}
  .info-item .value {{ font-size: 0.95rem; color: #2c3e50; font-weight: 500; }}
  .purpose-box {{ background: #eaf4fd; border: 1px solid #aed6f1; border-radius: 8px; padding: 16px 20px; font-size: 0.95rem; line-height: 1.7; color: #1a5276; }}
  ul.task-list {{ list-style: none; padding: 0; }}
  ul.task-list li {{ padding: 10px 14px; border-bottom: 1px solid #eef2f7; font-size: 0.92rem; line-height: 1.6; }}
  ul.task-list li:before {{ content: "▶ "; color: #1B6CA8; font-size: 0.75rem; }}
  ul.task-list li:last-child {{ border-bottom: none; }}
  .req-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  .req-table th {{ background: #0D3B6E; color: #fff; padding: 10px 14px; text-align: left; font-weight: 600; width: 25%; }}
  .req-table td {{ padding: 10px 14px; border-bottom: 1px solid #e8f0f8; }}
  .req-table tr:nth-child(even) td {{ background: #f4f9fd; }}
  .comp-list {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .comp-tag {{ background: #eaf4fd; color: #1a5276; border: 1px solid #aed6f1; border-radius: 20px; padding: 6px 16px; font-size: 0.88rem; font-weight: 500; }}
  .kpi-list {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .kpi-tag {{ background: #eafaf1; color: #1d6a39; border: 1px solid #a9dfbf; border-radius: 20px; padding: 6px 16px; font-size: 0.88rem; font-weight: 500; }}
  .footer {{ background: #f4f9fd; border-top: 1px solid #d5e8f5; padding: 16px 40px; font-size: 0.8rem; color: #7f8c8d; display: flex; justify-content: space-between; }}
  .stamp {{ text-align: right; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; }}
  .stamp-line {{ display: inline-block; width: 200px; border-bottom: 1px solid #333; margin-left: 20px; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <div class="hospital">🏥 {hospital_name}</div>
    <h1>{data.get('직무명', '직무기술서')}</h1>
    <div class="meta">직무기술서 (Job Description) &nbsp;|&nbsp; 작성일: {today}</div>
  </div>
  <div class="body">

    <div class="section">
      <div class="section-title">01. 기본 정보</div>
      <div class="info-grid">
        <div class="info-item"><div class="label">소속 부서</div><div class="value">{data.get('소속부서', '-')}</div></div>
        <div class="info-item"><div class="label">직급 / 직책</div><div class="value">{data.get('직급', '-')} / {data.get('직책', '-')}</div></div>
        <div class="info-item"><div class="label">보고 체계</div><div class="value">{data.get('보고체계', '-')}</div></div>
        <div class="info-item"><div class="label">근무 형태</div><div class="value">{wc.get('근무형태', '-')}</div></div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">02. 직무 목적</div>
      <div class="purpose-box">{data.get('직무목적', '-')}</div>
    </div>

    <div class="section">
      <div class="section-title">03. 주요 업무 (Key Responsibilities)</div>
      <ul class="task-list">{tasks_html}</ul>
    </div>

    <div class="section">
      <div class="section-title">04. 자격 요건 (Requirements)</div>
      <table class="req-table">
        <tr><th>학력</th><td>{req.get('학력', '-')}</td></tr>
        <tr><th>경력</th><td>{req.get('경력', '-')}</td></tr>
        <tr><th>필수 면허/자격</th><td>{req.get('필수면허', '-')}</td></tr>
        <tr><th>우대 사항</th><td>{req.get('우대사항', '-')}</td></tr>
      </table>
    </div>

    <div class="section">
      <div class="section-title">05. 핵심 역량 (Core Competencies)</div>
      <div class="comp-list">{" ".join([f'<span class="comp-tag">✓ {c}</span>' for c in data.get("핵심역량", []) if c.strip()])}</div>
    </div>

    <div class="section">
      <div class="section-title">06. 근무 조건</div>
      <table class="req-table">
        <tr><th>근무 형태</th><td>{wc.get('근무형태', '-')}</td></tr>
        <tr><th>근무 시간</th><td>{wc.get('근무시간', '-')}</td></tr>
        <tr><th>급여 수준</th><td>{wc.get('급여수준', '-')}</td></tr>
      </table>
    </div>

    <div class="section">
      <div class="section-title">07. 주요 성과 지표 (KPI)</div>
      <div class="kpi-list">{" ".join([f'<span class="kpi-tag">📊 {k}</span>' for k in data.get("주요KPI", []) if k.strip()])}</div>
    </div>

    <div class="stamp">
      <span>작성자: <span class="stamp-line"></span></span>
      &nbsp;&nbsp;
      <span>검토자: <span class="stamp-line"></span></span>
      &nbsp;&nbsp;
      <span>승인자: <span class="stamp-line"></span></span>
    </div>
  </div>
  <div class="footer">
    <span>📋 본 직무기술서는 채용, 성과 평가, 직무 교육의 기준으로 활용됩니다.</span>
    <span>작성일: {today}</span>
  </div>
</div>
</body>
</html>"""


def render_job_description_page():
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">📝</div>
      <div>
        <h1>직무기술서(JD) 작성 및 다운로드</h1>
        <p>병원 직종별 사전 템플릿 제공 · 커스텀 작성 · 전문 디자인 HTML 다운로드</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      💡 <b>직무기술서(Job Description)란?</b> 특정 직무에서 수행해야 할 업무 내용, 자격 요건, 핵심 역량, 성과 지표를 체계적으로 정리한 문서입니다.
      채용 공고, 수습 평가, 연간 성과 평가, 직무 교육 설계의 핵심 기준이 됩니다.
    </div>
    """, unsafe_allow_html=True)

    # ── 병원명 입력
    hospital_name = st.text_input("🏥 병원명 (문서 헤더에 표시됩니다)", placeholder="예: ○○병원, ○○의원")

    # ── 템플릿 선택
    st.subheader("직종 템플릿 선택")
    template_choice = st.selectbox(
        "직종을 선택하면 해당 직무기술서 양식이 자동으로 채워집니다.",
        list(JD_TEMPLATES.keys()),
    )

    tpl = JD_TEMPLATES.get(template_choice)
    if tpl is None:
        st.info("직종을 선택하거나 '직접 작성'을 선택하여 작성을 시작하세요.")
        return

    # ── 폼 작성
    with st.form("jd_form_v2"):
        st.subheader("1. 기본 정보")
        c1, c2 = st.columns(2)
        with c1:
            job_title = st.text_input("직무명 *", value=tpl["직무명"])
            dept = st.text_input("소속부서 *", value=tpl["소속부서"])
        with c2:
            grade = st.text_input("직급", value=tpl["직급"])
            position = st.text_input("직책", value=tpl["직책"])
        report_to = st.text_input("보고 체계 (직속 상급자)", value=tpl["보고체계"])

        st.subheader("2. 직무 목적")
        purpose = st.text_area("직무 목적 *", value=tpl["직무목적"], height=100,
                               help="이 직무가 병원 내에서 존재하는 이유와 핵심 목표를 2~3문장으로 요약하세요.")

        st.subheader("3. 주요 업무 (최대 7개)")
        tasks = []
        default_tasks = tpl.get("주요업무", [""] * 7)
        for i in range(7):
            val = default_tasks[i] if i < len(default_tasks) else ""
            t = st.text_input(f"주요 업무 {i+1}", value=val, key=f"task_v2_{i}")
            if t.strip():
                tasks.append(t)

        st.subheader("4. 자격 요건")
        req = tpl.get("자격요건", {})
        c3, c4 = st.columns(2)
        with c3:
            edu = st.text_input("학력 요건", value=req.get("학력", ""))
            license_req = st.text_input("필수 면허/자격증", value=req.get("필수면허", ""))
        with c4:
            career = st.text_input("경력 요건", value=req.get("경력", ""))
            preferred = st.text_input("우대 사항", value=req.get("우대사항", ""))

        st.subheader("5. 핵심 역량 (최대 5개)")
        comps = []
        default_comps = tpl.get("핵심역량", [""] * 5)
        for i in range(5):
            val = default_comps[i] if i < len(default_comps) else ""
            c = st.text_input(f"핵심 역량 {i+1}", value=val, key=f"comp_v2_{i}")
            if c.strip():
                comps.append(c)

        st.subheader("6. 근무 조건")
        wc = tpl.get("근무조건", {})
        c5, c6, c7 = st.columns(3)
        with c5:
            work_type = st.text_input("근무 형태", value=wc.get("근무형태", ""))
        with c6:
            work_time = st.text_input("근무 시간", value=wc.get("근무시간", ""))
        with c7:
            salary = st.text_input("급여 수준", value=wc.get("급여수준", "병원 내규에 따름"))

        st.subheader("7. 주요 성과 지표 (KPI, 최대 4개)")
        kpis = []
        default_kpis = tpl.get("주요KPI", [""] * 4)
        for i in range(4):
            val = default_kpis[i] if i < len(default_kpis) else ""
            k = st.text_input(f"KPI {i+1}", value=val, key=f"kpi_v2_{i}",
                              placeholder="예: 환자 만족도 점수, 오류 발생률")
            if k.strip():
                kpis.append(k)

        submitted = st.form_submit_button("✅ 직무기술서 생성", use_container_width=True)

    if submitted:
        if not job_title.strip():
            st.error("직무명을 입력해주세요.")
            return

        final_data = {
            "직무명": job_title,
            "소속부서": dept,
            "직급": grade,
            "직책": position,
            "보고체계": report_to,
            "직무목적": purpose,
            "주요업무": tasks,
            "자격요건": {"학력": edu, "경력": career, "필수면허": license_req, "우대사항": preferred},
            "핵심역량": comps,
            "근무조건": {"근무형태": work_type, "근무시간": work_time, "급여수준": salary},
            "주요KPI": kpis,
        }

        html_str = generate_html_content(final_data, hospital_name or "병원")
        b64 = base64.b64encode(html_str.encode("utf-8")).decode()
        safe_name = job_title.replace(" ", "_").replace("/", "_")
        filename = f"JD_{safe_name}_{datetime.now().strftime('%Y%m%d')}.html"

        st.success(f"✅ '{job_title}' 직무기술서가 생성되었습니다!")

        st.markdown(f"""
        <div style="text-align:center; margin: 20px 0;">
          <a href="data:text/html;base64,{b64}" download="{filename}"
             style="display:inline-block; padding:14px 36px; background:linear-gradient(135deg,#0D3B6E,#1B6CA8);
                    color:white; text-decoration:none; border-radius:8px; font-size:1rem; font-weight:700;
                    box-shadow:0 4px 12px rgba(27,108,168,0.4);">
            📥 HTML 파일로 다운로드
          </a>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📄 미리보기 (주요 내용 확인)"):
            st.markdown(f"**직무명:** {job_title} | **소속:** {dept} | **직급/직책:** {grade}/{position}")
            st.markdown(f"**보고체계:** {report_to}")
            st.markdown(f"**직무목적:** {purpose}")
            if tasks:
                st.markdown("**주요 업무:**")
                for t in tasks:
                    st.markdown(f"- {t}")
            if kpis:
                st.markdown(f"**KPI:** {', '.join(kpis)}")

        st.markdown("""
        <div class="info-box" style="margin-top:16px;">
          💡 <b>활용 팁:</b> 다운로드한 HTML 파일은 웹 브라우저에서 바로 열어볼 수 있으며, 인쇄 시 PDF로 저장할 수 있습니다.
          채용 공고 게시, 신규 직원 오리엔테이션, 연간 성과 평가 기준 자료로 활용하세요.
        </div>
        """, unsafe_allow_html=True)
