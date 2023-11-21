import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.markdown("# 가정")
st.markdown(
"* 간단한 계산기에서 출발, 단계를 높일수록 가정을 풀면서 복잡한 계산기를 완성하겠습니다.\n\
    - 가정1 : 취업 당시 순자산은 0이다\n\
    - 가정2 : 결혼 및 출산은 하지 않는다. \n\
    - 가정3 : 상속분은 0이다. (부모로부터, 자식으로에게로 모두)\n\
    - 가정4 : 대형지출 (주택 / 차)는 모두 월세무이자 할부로 구매한다는 가정 \n\
    - 가정5 : 0~100 살까지 산다. \n\
    - 가정11 : 25세에 취업, 65세에 은퇴\n\
    - 가정6 : 예적금 저축 외 자본소득이 발생하지 않음을 가정\n\
    - 가정12 : 예적금 이자율곡선은 평평하고 무위험수익률을 얻을 수 있는 재투자기회는 무궁무진함을 가정\n\
    - 가정7 : 모든 것은 세후개념으로 논의\n\
    - 가정8 : 전쟁발발, 암 발병 등의 불확실성 없음\n\
    - 가정9 : 지출과 수입은 모두 선형적이고 증가하지 않음을 가정\n\
    - 가정10 : 은퇴 이후 수입은 없음을 가정")

st.header("조건입력")

# 인풋 정의
age_employed = st.number_input("age_employed", 0, 100, 25)
age_ret = st.number_input("age_ret", 0, 100, 65)
age_die = st.number_input("age_die", 0, 100, 100)
rf = st.number_input("rf", 0., 1., 0.04)
wealth_now = st.number_input("wealth_now", 0, 100, 0)
income_month = st.number_input("income_month", 0, value=3000000)
expenditure_month = st.number_input("expenditure_month", 0, value= 1500000)

# 연환산
income_year = 12 * income_month
expenditure_year = 12 * expenditure_month
saving_month = income_year - expenditure_year


# 나잇대별 현금흐름
## 나이
ages = [i for i in range(1,age_die+1)]
##수입
incomes_year_bf = [0 for _ in range(age_employed)]
incomes_year_at = [income_year for _ in range(age_employed,age_ret)]
incomes_year_af = [0 for _ in range(age_ret, age_die)]
incomes_year = incomes_year_bf + incomes_year_at + incomes_year_af
##지출
expenditures_year_bf = [expenditure_year for _ in range(age_employed)]
expenditures_year_at = [expenditure_year for _ in range(age_employed,age_ret)]
expenditures_year_af = [expenditure_year for _ in range(age_ret, age_die)]
expenditures_year = expenditures_year_bf + expenditures_year_at + expenditures_year_af
##저축
savings_year = [incomes_year[i]-expenditures_year[i] for i in range(len(incomes_year))]


st.header("나이별 현금흐름")

#결괏값 표시
##데이터프레임 생성
df = pd.DataFrame({
    "incomes" : incomes_year,
    "expenditures" : expenditures_year,
    "savings_year" : savings_year
})
## 인덱스 설정
df.index = ages
## 누적저축액 연산
df["cum_savings_year"] = df["savings_year"].cumsum()

st.write(df)

st.header("나이별 현금흐름 시각화")
# 시각화
from matplotlib.ticker import FuncFormatter
##데이터표시
fig = plt.figure(figsize=(10,5))
plt.step(df.index, df["incomes"], label='incomes')
plt.step(df.index, df["expenditures"], label = 'expenditure')
plt.step(df.index, df["savings_year"], label='saving')
plt.plot(df.index, df["cum_savings_year"], label='cummulated saving')
plt.axhline(0, c='black')
## 제목설정
plt.title("Individual's Life Cycle Curve")
plt.ylabel("Saving, Expenditure, Income")
plt.xlabel("Age")
## Y 축 화폐단위표시
def currency_formatter(value, _):
    return f'₩{value/1000:,.0f}'
plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_formatter))
## 범례표시
plt.legend()

st.write(fig)
