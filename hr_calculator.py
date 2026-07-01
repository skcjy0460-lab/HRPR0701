"""
인사노무 스마트 계산기 모듈
퇴직금 / 연차 / 주휴수당 / 4대보험 / 연장·야간·휴일 가산수당
2025-2026년 최신 법령 기준 적용
"""
import streamlit as st
from datetime import date, datetime
import math

# ── 2026년 기준 상수 ──────────────────────────────────────────────────────────
MIN_HOURLY_2025 = 10030      # 2025년 최저시급
MIN_HOURLY_2026 = 10320      # 2026년 최저시급 (2026.1.1 시행)
MIN_MONTHLY_2026 = 2156880   # 2026년 최저월급 (주40시간 기준, 209시간)

# 2026년 4대보험 요율
INS_RATES = {
    "국민연금": {"근로자": 0.0475, "사업주": 0.0475, "합계": 0.095},
    "건강보험": {"근로자": 0.03595, "사업주": 0.03595, "합계": 0.0719},
    "장기요양": {"근로자": 0.004724, "사업주": 0.004724, "합계": 0.009448},  # 건보료의 13.14%
    "고용보험": {"근로자": 0.009, "사업주": 0.009, "합계": 0.018},
}

# 국민연금 상한/하한 (2025.7~2026.6)
NP_UPPER = 6370000
NP_LOWER = 400000
# 건강보험 상한/하한 (2026년)
HI_UPPER = 127725730
HI_LOWER = 280383


def calc_severance(avg_daily_wage: float, total_days: int) -> dict:
    """퇴직금 계산"""
    if total_days < 365:
        return {"eligible": False, "amount": 0}
    amount = avg_daily_wage * 30 * (total_days / 365)
    return {"eligible": True, "amount": amount}


def calc_avg_daily_wage(wage_3m: float, days_3m: int) -> float:
    """1일 평균임금 계산"""
    if days_3m == 0:
        return 0
    return wage_3m / days_3m


def calc_annual_leave(months_worked: int, attendance_rate: float = 100.0, over_1year: bool = False, years: int = 1) -> dict:
    """연차 계산"""
    if not over_1year:
        # 1년 미만: 1개월 개근 시 1일
        days = min(months_worked, 11)
        return {"days": days, "type": "1년미만", "note": f"1개월 개근 시 1일 발생 ({months_worked}개월 → {days}일)"}
    else:
        # 1년 이상
        if attendance_rate < 80:
            # 출근율 80% 미만: 비례 계산
            base = 15
            actual = math.floor(base * (attendance_rate / 100))
            return {"days": actual, "type": "1년이상(출근율80%미만)", "note": f"출근율 {attendance_rate}% → 비례 계산 {actual}일"}
        else:
            # 출근율 80% 이상
            base = 15
            # 2년마다 1일 추가 (최대 25일)
            extra = min((years - 1) // 2, 10)
            total = base + extra
            return {"days": total, "type": "1년이상", "note": f"기본 15일 + 가산 {extra}일 (근속 {years}년) = {total}일"}


def calc_weekly_holiday(hourly_wage: float, weekly_hours: float, weekly_days: int = 5) -> dict:
    """주휴수당 계산"""
    if weekly_hours < 15:
        return {"eligible": False, "amount": 0, "reason": "주 소정근로시간 15시간 미만 (초단시간 근로자)"}
    # 주휴수당 = 1일 소정근로시간 × 시급
    daily_hours = weekly_hours / weekly_days if weekly_days > 0 else 8
    daily_hours = min(daily_hours, 8)  # 1일 최대 8시간
    amount = hourly_wage * daily_hours
    return {
        "eligible": True,
        "amount": amount,
        "daily_hours": daily_hours,
        "reason": f"주 {weekly_hours}시간 / {weekly_days}일 = 1일 {daily_hours:.1f}시간 × 시급 {hourly_wage:,.0f}원"
    }


def calc_insurance(monthly_salary: float, company_size: str = "150인 미만") -> dict:
    """4대보험 계산"""
    # 국민연금: 상한/하한 적용
    np_base = max(min(monthly_salary, NP_UPPER), NP_LOWER)
    np_base = math.floor(np_base / 1000) * 1000  # 1,000원 미만 절사

    # 건강보험
    hi_base = max(min(monthly_salary, HI_UPPER), HI_LOWER)

    # 고용보험 사업주 추가 부담 (고용안정·직업능력개발)
    emp_extra = {
        "150인 미만": 0.0025,
        "150인 이상(우선지원대상)": 0.0045,
        "150~999인": 0.0065,
        "1000인 이상": 0.0085,
    }.get(company_size, 0.0025)

    result = {
        "국민연금": {
            "근로자": math.floor(np_base * INS_RATES["국민연금"]["근로자"]),
            "사업주": math.floor(np_base * INS_RATES["국민연금"]["사업주"]),
        },
        "건강보험": {
            "근로자": math.floor(hi_base * INS_RATES["건강보험"]["근로자"]),
            "사업주": math.floor(hi_base * INS_RATES["건강보험"]["사업주"]),
        },
        "장기요양": {
            "근로자": math.floor(math.floor(hi_base * INS_RATES["건강보험"]["근로자"]) * 0.1314),
            "사업주": math.floor(math.floor(hi_base * INS_RATES["건강보험"]["사업주"]) * 0.1314),
        },
        "고용보험": {
            "근로자": math.floor(monthly_salary * INS_RATES["고용보험"]["근로자"]),
            "사업주": math.floor(monthly_salary * (INS_RATES["고용보험"]["사업주"] + emp_extra)),
        },
    }
    result["근로자_합계"] = sum(v["근로자"] for v in result.values() if isinstance(v, dict))
    result["사업주_합계"] = sum(v["사업주"] for v in result.values() if isinstance(v, dict))
    result["총합계"] = result["근로자_합계"] + result["사업주_합계"]
    return result


def calc_extra_pay(base_hourly: float, overtime_h: float, night_h: float,
                   holiday_h_8: float, holiday_h_over8: float, is_5plus: bool = True) -> dict:
    """연장·야간·휴일 가산수당 계산"""
    if not is_5plus:
        return {
            "overtime": 0, "night": 0, "holiday_8": 0, "holiday_over8": 0,
            "total": 0, "note": "5인 미만 사업장은 연장·야간·휴일 가산수당 적용 제외"
        }

    overtime_pay = overtime_h * base_hourly * 1.5       # 연장: 1.5배 (기본1.0 + 가산0.5)
    night_pay = night_h * base_hourly * 0.5             # 야간: 0.5배 추가 가산 (기본 별도)
    holiday_8_pay = holiday_h_8 * base_hourly * 1.5     # 휴일 8시간 이내: 1.5배
    holiday_over8_pay = holiday_h_over8 * base_hourly * 2.0  # 휴일 8시간 초과: 2.0배

    total = overtime_pay + night_pay + holiday_8_pay + holiday_over8_pay
    return {
        "overtime": overtime_pay,
        "night": night_pay,
        "holiday_8": holiday_8_pay,
        "holiday_over8": holiday_over8_pay,
        "total": total,
    }


def render_calculator_page():
    st.markdown("""
    <div class="page-header">
      <div class="header-icon">🧮</div>
      <div>
        <h1>인사노무 스마트 계산기</h1>
        <p>2025-2026년 최신 법령 기준 · 퇴직금 · 연차 · 주휴수당 · 4대보험 · 가산수당</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      📌 <b>2026년 최저임금:</b> 시간급 <b>10,320원</b> (2026.1.1 시행) | 월 환산 <b>2,156,880원</b> (주 40시간, 209시간 기준)
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 퇴직금", "🌴 연차 계산", "🏖️ 주휴수당", "🛡️ 4대보험", "⏱️ 가산수당"])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1: 퇴직금
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        st.subheader("퇴직금 계산기")
        st.markdown("""
        <div class="info-box">
          📜 <b>근거:</b> 근로자퇴직급여 보장법 제8조<br>
          <b>지급 요건:</b> 계속근로기간 1년 이상 + 4주 평균 주 소정근로시간 15시간 이상<br>
          <b>공식:</b> 1일 평균임금 × 30일 × (재직일수 / 365)
        </div>
        """, unsafe_allow_html=True)

        calc_method = st.radio("계산 방법 선택", ["직접 입력 (1일 평균임금 + 재직일수)", "상세 계산 (3개월 임금 + 입퇴사일)"], horizontal=True)

        if calc_method == "직접 입력 (1일 평균임금 + 재직일수)":
            c1, c2 = st.columns(2)
            with c1:
                avg_daily = st.number_input("1일 평균임금 (원, 세전)", min_value=0, value=100000, step=1000,
                                            help="퇴직 전 3개월간 임금총액 ÷ 퇴직 전 3개월간 총 일수")
            with c2:
                total_days = st.number_input("총 재직일수 (일)", min_value=0, value=730, step=1)

            if st.button("퇴직금 계산", key="sev_simple"):
                result = calc_severance(avg_daily, total_days)
                if not result["eligible"]:
                    st.warning("⚠️ 계속근로기간이 1년(365일) 미만입니다. 법정 퇴직금 지급 대상이 아닙니다.")
                else:
                    years = total_days / 365
                    st.markdown(f"""
                    <div class="success-box">
                      <b>📊 퇴직금 계산 결과</b><br><br>
                      • 1일 평균임금: <b>{avg_daily:,.0f}원</b><br>
                      • 재직일수: <b>{total_days}일</b> (약 {years:.1f}년)<br>
                      • 계산식: {avg_daily:,.0f} × 30 × ({total_days}/365)<br>
                      <hr style="border-color:#A9DFBF; margin:10px 0;">
                      💰 <b>예상 법정 퇴직금: {result['amount']:,.0f}원 (세전)</b>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("※ 퇴직소득세 공제 후 실수령액은 국세청 홈택스(hometax.go.kr)에서 확인하세요.")

        else:  # 상세 계산
            c1, c2 = st.columns(2)
            with c1:
                join_date = st.date_input("입사일", value=date(2023, 1, 1))
                wage_m1 = st.number_input("퇴직 전 3개월 중 1개월 임금 (원)", min_value=0, value=3000000, step=100000)
                wage_m2 = st.number_input("퇴직 전 3개월 중 2개월 임금 (원)", min_value=0, value=3000000, step=100000)
            with c2:
                retire_date = st.date_input("퇴직일", value=date.today())
                wage_m3 = st.number_input("퇴직 전 3개월 중 3개월 임금 (원)", min_value=0, value=3000000, step=100000)
                bonus_3m = st.number_input("3개월분 상여금 해당액 (원, 없으면 0)", min_value=0, value=0, step=100000)

            if st.button("퇴직금 상세 계산", key="sev_detail"):
                total_days = (retire_date - join_date).days
                wage_total = wage_m1 + wage_m2 + wage_m3 + bonus_3m
                days_3m = 91  # 3개월 평균 일수 (실무상 91일 또는 실제 일수 사용)
                avg_daily_calc = wage_total / days_3m
                result = calc_severance(avg_daily_calc, total_days)

                if total_days < 365:
                    st.warning(f"⚠️ 재직기간이 {total_days}일로 1년 미만입니다. 법정 퇴직금 지급 대상이 아닙니다.")
                else:
                    st.markdown(f"""
                    <div class="success-box">
                      <b>📊 퇴직금 상세 계산 결과</b><br><br>
                      • 재직기간: {join_date} ~ {retire_date} (<b>{total_days}일</b>)<br>
                      • 3개월 임금총액: {wage_total:,.0f}원<br>
                      • 1일 평균임금: {wage_total:,.0f} ÷ {days_3m}일 = <b>{avg_daily_calc:,.0f}원</b><br>
                      • 계산식: {avg_daily_calc:,.0f} × 30 × ({total_days}/365)<br>
                      <hr style="border-color:#A9DFBF; margin:10px 0;">
                      💰 <b>예상 법정 퇴직금: {result['amount']:,.0f}원 (세전)</b>
                    </div>
                    """, unsafe_allow_html=True)

        with st.expander("💡 퇴직금 실무 Q&A"):
            st.markdown("""
            **Q. 퇴직금 지급 기한은?**
            퇴직일로부터 **14일 이내** 지급해야 합니다. 당사자 합의 시 연장 가능하나, 미지급 시 연 20% 지연이자 발생.

            **Q. 상여금도 평균임금에 포함되나요?**
            네. 퇴직 전 12개월 동안 지급된 상여금 총액의 3/12을 3개월 임금에 합산합니다.

            **Q. 연차수당도 포함되나요?**
            퇴직 전 1년간 발생한 미사용 연차수당(전년도분)을 3/12로 환산하여 포함합니다.

            **Q. 중간정산 후 퇴직금은?**
            중간정산 이후 기간에 대해서만 퇴직금을 산정합니다. 단, 중간정산은 법정 사유(주택 구입 등)에 해당해야 합니다.
            """)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2: 연차 계산
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.subheader("연차유급휴가 계산기")
        st.markdown("""
        <div class="info-box">
          📜 <b>근거:</b> 근로기준법 제60조<br>
          • <b>1년 미만:</b> 1개월 개근 시 1일 (최대 11일)<br>
          • <b>1년 이상:</b> 출근율 80% 이상 시 15일 + 2년마다 1일 가산 (최대 25일)
        </div>
        """, unsafe_allow_html=True)

        leave_type = st.radio("근속 기간 선택", ["1년 미만 (입사 후 1년 미경과)", "1년 이상"], horizontal=True)

        if leave_type == "1년 미만 (입사 후 1년 미경과)":
            c1, c2 = st.columns(2)
            with c1:
                months = st.number_input("개근한 개월 수 (1~11)", min_value=0, max_value=11, value=6)
            with c2:
                st.markdown("""
                <div class="info-box" style="margin-top:28px;">
                  1개월 개근 = 소정근로일 전부 출근<br>
                  결근 1일이라도 있으면 해당 월 연차 미발생
                </div>
                """, unsafe_allow_html=True)

            if st.button("연차 계산", key="leave_under1"):
                result = calc_annual_leave(months)
                st.markdown(f"""
                <div class="success-box">
                  🌴 <b>발생 연차: {result['days']}일</b><br>
                  {result['note']}
                </div>
                """, unsafe_allow_html=True)

                # 월별 발생 현황 표
                st.markdown("**월별 연차 발생 현황:**")
                table_rows = ""
                for m in range(1, 12):
                    status = "✅ 발생" if m <= months else "⬜ 미발생"
                    table_rows += f"<tr><td>{m}개월차</td><td>{status}</td><td>{min(m, 11)}일 (누계)</td></tr>"
                st.markdown(f"""
                <table class="styled-table">
                  <tr><th>개월차</th><th>상태</th><th>누계 연차</th></tr>
                  {table_rows}
                </table>
                """, unsafe_allow_html=True)

        else:  # 1년 이상
            c1, c2, c3 = st.columns(3)
            with c1:
                years_worked = st.number_input("근속 연수 (년)", min_value=1, max_value=30, value=3)
            with c2:
                att_rate = st.number_input("연간 출근율 (%)", min_value=0.0, max_value=100.0, value=95.0, step=1.0)
            with c3:
                st.markdown("""
                <div class="info-box" style="margin-top:28px; font-size:0.82rem;">
                  출근율 = 출근일수 / 소정근로일수 × 100
                </div>
                """, unsafe_allow_html=True)

            if st.button("연차 계산", key="leave_over1"):
                result = calc_annual_leave(0, att_rate, True, years_worked)
                st.markdown(f"""
                <div class="success-box">
                  🌴 <b>발생 연차: {result['days']}일</b><br>
                  {result['note']}
                </div>
                """, unsafe_allow_html=True)

                # 연도별 연차 발생 테이블
                st.markdown("**연도별 연차 발생 기준 (출근율 80% 이상 가정):**")
                table_rows = ""
                for y in range(1, 21):
                    extra = min((y - 1) // 2, 10)
                    total = 15 + extra
                    highlight = "background:#EAF4FD;" if y == years_worked else ""
                    table_rows += f"<tr style='{highlight}'><td>{y}년차</td><td>15일 + {extra}일</td><td><b>{total}일</b></td></tr>"
                st.markdown(f"""
                <table class="styled-table">
                  <tr><th>근속 연수</th><th>계산</th><th>연차 일수</th></tr>
                  {table_rows}
                </table>
                """, unsafe_allow_html=True)

        with st.expander("💡 연차 실무 Q&A"):
            st.markdown("""
            **Q. 연차수당은 언제 지급하나요?**
            연차 발생일로부터 1년 이내에 미사용한 연차에 대해 **통상임금**으로 수당 지급. 단, 연차 촉진 제도를 적법하게 시행한 경우 지급 의무 면제.

            **Q. 연차 촉진 제도란?**
            사용자가 연차 사용을 2회 서면 촉구했음에도 근로자가 미사용한 경우, 미사용 연차수당 지급 의무가 면제됩니다.
            (1차 촉구: 연차 만료 6개월 전, 2차 촉구: 만료 2개월 전)

            **Q. 병가·출산휴가·육아휴직 기간은 출근으로 인정되나요?**
            네. 출산전후휴가, 육아휴직, 업무상 재해로 인한 휴업 기간은 출근한 것으로 봅니다.
            """)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3: 주휴수당
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.subheader("주휴수당 계산기")
        st.markdown("""
        <div class="info-box">
          📜 <b>근거:</b> 근로기준법 제55조<br>
          <b>지급 조건:</b> ① 1주 소정근로시간 15시간 이상 ② 1주일 소정근로일 개근<br>
          <b>공식:</b> 1일 소정근로시간 × 시급 (단, 1일 최대 8시간 기준)
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            hourly = st.number_input("시급 (원)", min_value=10320, value=10320, step=100,
                                     help="2026년 최저시급: 10,320원")
        with c2:
            weekly_h = st.number_input("1주 소정근로시간 (시간)", min_value=0.0, max_value=52.0, value=40.0, step=1.0)
        with c3:
            weekly_d = st.number_input("1주 소정근로일수 (일)", min_value=1, max_value=6, value=5)

        if st.button("주휴수당 계산", key="weekly_holiday"):
            result = calc_weekly_holiday(hourly, weekly_h, weekly_d)
            if not result["eligible"]:
                st.warning(f"⚠️ {result['reason']}")
            else:
                monthly_holiday = result["amount"] * 4.345  # 월 평균 주수
                st.markdown(f"""
                <div class="success-box">
                  🏖️ <b>주휴수당 계산 결과</b><br><br>
                  • {result['reason']}<br>
                  <hr style="border-color:#A9DFBF; margin:10px 0;">
                  💰 <b>1주 주휴수당: {result['amount']:,.0f}원</b><br>
                  💰 <b>월 주휴수당 (4.345주 기준): {monthly_holiday:,.0f}원</b>
                </div>
                """, unsafe_allow_html=True)

        # 주휴수당 포함 월급 계산
        st.markdown("---")
        st.subheader("주휴수당 포함 월 환산 임금 계산")
        st.markdown("시급제 근로자의 주휴수당 포함 월 예상 임금을 계산합니다.")

        c4, c5 = st.columns(2)
        with c4:
            hourly2 = st.number_input("시급 (원)", min_value=10320, value=10320, step=100, key="hourly2")
        with c5:
            weekly_h2 = st.number_input("1주 소정근로시간 (시간)", min_value=0.0, max_value=52.0, value=40.0, step=1.0, key="wh2")

        if st.button("월 환산 임금 계산"):
            if weekly_h2 < 15:
                st.warning("주 15시간 미만은 주휴수당 미발생. 월 임금 = 시급 × 주 근로시간 × 4.345주")
                monthly = hourly2 * weekly_h2 * 4.345
            else:
                # 주휴수당 포함 월 환산: (주 근로시간 + 주휴시간) × 시급 × 4.345
                daily_h = min(weekly_h2 / 5, 8)
                monthly = hourly2 * (weekly_h2 + daily_h) * 4.345
            st.success(f"예상 월 환산 임금 (주휴 포함): **{monthly:,.0f}원**")

        with st.expander("💡 주휴수당 실무 Q&A"):
            st.markdown("""
            **Q. 파트타임(아르바이트)도 주휴수당을 받을 수 있나요?**
            네. 주 15시간 이상 근무하고 소정근로일을 개근하면 고용 형태에 관계없이 지급해야 합니다.

            **Q. 결근하면 주휴수당이 없어지나요?**
            소정근로일 중 1일이라도 결근하면 해당 주의 주휴수당은 발생하지 않습니다. 단, 연차를 사용한 날은 출근으로 봅니다.

            **Q. 월급제 직원도 주휴수당을 따로 받나요?**
            월급제의 경우 통상 월급에 주휴수당이 포함되어 있습니다. 주 40시간 기준 월 209시간(주 40시간 + 주휴 8시간) × 4.345주 = 209시간으로 계산합니다.
            """)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 4: 4대보험
    # ══════════════════════════════════════════════════════════════════════════
    with tab4:
        st.subheader("4대보험료 계산기 (2026년 기준)")
        st.markdown("""
        <div class="info-box">
          📌 <b>2026년 4대보험 요율 (근로자 부담분)</b><br>
          국민연금 4.75% | 건강보험 3.595% | 장기요양 건보료의 13.14% | 고용보험 0.9%
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            monthly_sal = st.number_input("월 보수액 (비과세 제외, 원)", min_value=0, value=3000000, step=100000,
                                          help="비과세 항목(식대 20만원, 차량유지비 등) 제외한 과세 급여")
        with c2:
            comp_size = st.selectbox("사업장 규모 (고용보험 사업주 부담 결정)", 
                                     ["150인 미만", "150인 이상(우선지원대상)", "150~999인", "1000인 이상"])

        if st.button("4대보험 계산", key="insurance"):
            result = calc_insurance(monthly_sal, comp_size)

            st.markdown(f"""
            <table class="styled-table">
              <tr><th>보험 종류</th><th>요율</th><th>근로자 부담</th><th>사업주 부담</th><th>합계</th></tr>
              <tr>
                <td>국민연금</td><td>9.5% (각 4.75%)</td>
                <td>{result['국민연금']['근로자']:,}원</td>
                <td>{result['국민연금']['사업주']:,}원</td>
                <td>{result['국민연금']['근로자']+result['국민연금']['사업주']:,}원</td>
              </tr>
              <tr>
                <td>건강보험</td><td>7.19% (각 3.595%)</td>
                <td>{result['건강보험']['근로자']:,}원</td>
                <td>{result['건강보험']['사업주']:,}원</td>
                <td>{result['건강보험']['근로자']+result['건강보험']['사업주']:,}원</td>
              </tr>
              <tr>
                <td>장기요양보험</td><td>건보료의 13.14%</td>
                <td>{result['장기요양']['근로자']:,}원</td>
                <td>{result['장기요양']['사업주']:,}원</td>
                <td>{result['장기요양']['근로자']+result['장기요양']['사업주']:,}원</td>
              </tr>
              <tr>
                <td>고용보험</td><td>근로자 0.9%</td>
                <td>{result['고용보험']['근로자']:,}원</td>
                <td>{result['고용보험']['사업주']:,}원</td>
                <td>{result['고용보험']['근로자']+result['고용보험']['사업주']:,}원</td>
              </tr>
              <tr style="background:#0D3B6E; color:white;">
                <td><b>합계</b></td><td>-</td>
                <td><b>{result['근로자_합계']:,}원</b></td>
                <td><b>{result['사업주_합계']:,}원</b></td>
                <td><b>{result['총합계']:,}원</b></td>
              </tr>
            </table>
            """, unsafe_allow_html=True)

            net_pay = monthly_sal - result["근로자_합계"]
            st.markdown(f"""
            <div class="success-box" style="margin-top:12px;">
              💰 <b>월 실수령액 추정 (4대보험 공제 후, 소득세 제외):</b> {net_pay:,.0f}원<br>
              <span style="font-size:0.85rem;">※ 근로소득세·지방소득세는 별도 공제됩니다. 정확한 세액은 국세청 홈택스 간이세액표를 참고하세요.</span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("💡 4대보험 실무 Q&A"):
            st.markdown("""
            **Q. 비과세 항목은 어떤 것이 있나요?**
            식대(월 20만원 이내), 차량유지비(월 20만원 이내), 보육수당(월 20만원 이내), 야간근로수당(생산직 근로자 월 240만원 이내) 등이 있습니다.

            **Q. 국민연금 상한액·하한액이란?**
            기준소득월액 상한액(2025.7~2026.6: 637만원)을 초과하는 급여는 637만원으로, 하한액(40만원) 미만은 40만원으로 계산합니다.

            **Q. 건강보험 연말정산이란?**
            매년 4월, 전년도 실제 보수총액을 기준으로 보험료를 재산정하여 추가 납부 또는 환급합니다.
            """)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 5: 가산수당
    # ══════════════════════════════════════════════════════════════════════════
    with tab5:
        st.subheader("연장·야간·휴일 가산수당 계산기")
        st.markdown("""
        <div class="info-box">
          📜 <b>근거:</b> 근로기준법 제56조 (상시 5인 이상 사업장 적용)<br>
          • <b>연장근로:</b> 통상시급 × 1.5배 (기본 1.0 + 가산 0.5)<br>
          • <b>야간근로</b> (22:00~06:00): 기본 근로수당 + 통상시급 × 0.5 추가<br>
          • <b>휴일근로:</b> 8시간 이내 × 1.5배 / 8시간 초과 × 2.0배
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            base_h = st.number_input("통상시급 (원)", min_value=10320, value=15000, step=500,
                                     help="통상시급 = 통상임금 ÷ 소정근로시간")
        with c2:
            is_5plus = st.checkbox("상시 5인 이상 사업장", value=True,
                                   help="5인 미만 사업장은 연장·야간·휴일 가산수당 적용 제외")

        st.markdown("**근로 시간 입력:**")
        c3, c4 = st.columns(2)
        with c3:
            ot_h = st.number_input("연장근로 시간 (1일 8h 또는 주 40h 초과)", min_value=0.0, value=0.0, step=0.5,
                                   help="1일 8시간, 주 40시간을 초과하는 근로시간")
            night_h = st.number_input("야간근로 시간 (22:00~06:00 사이 근로)", min_value=0.0, value=0.0, step=0.5)
        with c4:
            hol_8 = st.number_input("휴일근로 시간 (8시간 이내)", min_value=0.0, value=0.0, step=0.5)
            hol_over8 = st.number_input("휴일근로 시간 (8시간 초과분)", min_value=0.0, value=0.0, step=0.5)

        if st.button("가산수당 계산", key="extra_pay"):
            result = calc_extra_pay(base_h, ot_h, night_h, hol_8, hol_over8, is_5plus)

            if not is_5plus:
                st.warning(result["note"])
            else:
                total = result["total"]
                st.markdown(f"""
                <table class="styled-table">
                  <tr><th>수당 종류</th><th>계산 공식</th><th>금액</th></tr>
                  <tr>
                    <td>연장근로수당</td>
                    <td>{base_h:,}원 × 1.5 × {ot_h}시간</td>
                    <td><b>{result['overtime']:,.0f}원</b></td>
                  </tr>
                  <tr>
                    <td>야간근로 가산수당</td>
                    <td>{base_h:,}원 × 0.5 × {night_h}시간 (기본 별도)</td>
                    <td><b>{result['night']:,.0f}원</b></td>
                  </tr>
                  <tr>
                    <td>휴일근로수당 (8h 이내)</td>
                    <td>{base_h:,}원 × 1.5 × {hol_8}시간</td>
                    <td><b>{result['holiday_8']:,.0f}원</b></td>
                  </tr>
                  <tr>
                    <td>휴일근로수당 (8h 초과)</td>
                    <td>{base_h:,}원 × 2.0 × {hol_over8}시간</td>
                    <td><b>{result['holiday_over8']:,.0f}원</b></td>
                  </tr>
                  <tr style="background:#0D3B6E; color:white;">
                    <td colspan="2"><b>총 가산수당 합계</b></td>
                    <td><b>{total:,.0f}원</b></td>
                  </tr>
                </table>
                """, unsafe_allow_html=True)

                # 중복 가산 안내
                if ot_h > 0 and night_h > 0:
                    combined = base_h * ot_h * 1.5 + base_h * night_h * 0.5
                    st.markdown(f"""
                    <div class="warn-box">
                      ⚠️ <b>연장+야간 중복 발생 시:</b> 연장근로 중 야간시간대(22:00~06:00)가 포함된 경우,
                      연장수당(1.5배)과 야간가산(0.5배)이 <b>각각 합산</b>되어 통상시급의 <b>2.0배</b>가 됩니다.
                    </div>
                    """, unsafe_allow_html=True)

        with st.expander("💡 가산수당 실무 Q&A"):
            st.markdown("""
            **Q. 통상시급은 어떻게 계산하나요?**
            통상시급 = 통상임금 ÷ 소정근로시간
            월급제의 경우: 통상임금 ÷ 209시간 (주 40시간 기준)

            **Q. 3교대 간호사의 밤번 근무는 연장근로인가요?**
            교대 근무의 경우 소정근로시간(8시간)을 초과하지 않으면 연장근로가 아닙니다.
            단, 야간시간대(22:00~06:00)에 해당하는 시간에 대해서는 야간 가산수당을 지급해야 합니다.

            **Q. 5인 미만 의원에서는 야간수당을 안 줘도 되나요?**
            네. 상시 5인 미만 사업장은 근로기준법 제56조(가산수당) 적용이 제외됩니다.
            단, 최저임금 이상 지급 의무는 사업장 규모에 관계없이 적용됩니다.

            **Q. 포괄임금제로 연장수당을 미리 포함했는데 추가 지급해야 하나요?**
            포괄임금에 포함된 시간을 초과하는 연장근로가 발생하면 차액을 지급해야 합니다.
            """)
