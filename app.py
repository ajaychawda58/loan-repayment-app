import streamlit as st
import pandas as pd
import altair as alt


def calculate_loan_repayment(loan_amount, interest_rate, monthly_payment, additional_payment=0):
    month = 0
    remaining_balance = loan_amount
    total_payment = monthly_payment + additional_payment
    monthly_interest_rate = interest_rate / 100 / 12
    balance_history = []

    while remaining_balance > 0:
        interest = remaining_balance * monthly_interest_rate
        principal = total_payment - interest
        remaining_balance -= principal
        remaining_balance = max(0, remaining_balance)  
        month += 1
        balance_history.append({
            "Month": month,
            "Remaining Balance": remaining_balance,
            "Principal Paid": principal,
            "Interest Paid": interest
        })
        if remaining_balance == 0:
            break
    
    return balance_history


st.title("Loan Repayment Calculator with Principal and Interest Breakdown")


loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0, value=100000.0)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.1, value=5.0)
monthly_payment = st.number_input("Monthly Payment", min_value=0.0, step=100.0, value=1500.0)
additional_payment = st.number_input("Additional Monthly Payment", min_value=0.0, step=100.0, value=0.0)


no_additional_payment = calculate_loan_repayment(loan_amount, interest_rate, monthly_payment)


with_additional_payment = calculate_loan_repayment(loan_amount, interest_rate, monthly_payment, additional_payment)


df_no_additional = pd.DataFrame(no_additional_payment)
df_additional = pd.DataFrame(with_additional_payment)


months_without_additional = df_no_additional["Month"].max()
months_with_additional = df_additional["Month"].max()
time_saved = months_without_additional - months_with_additional

interest_without_additional = df_no_additional["Interest Paid"].sum()
interest_with_additional = df_additional["Interest Paid"].sum()
money_saved = interest_without_additional - interest_with_additional
st.markdown(f"### By making additional payments, you can repay the loan **{time_saved} months earlier!**")
st.markdown(f"### You will also save **{money_saved:,.2f}** in interest payments!")



col1, col2 = st.columns(2)

with col1:
    st.subheader("No Additional Payment")
    st.write(df_no_additional[["Month", "Remaining Balance", "Principal Paid", "Interest Paid"]])

with col2:
    st.subheader("Additional Payment")
    st.write(df_additional[["Month", "Remaining Balance", "Principal Paid", "Interest Paid"]])

st.subheader("Remaining Loan Balance Over Time")

balance_chart = alt.Chart(pd.concat([df_no_additional.assign(Payment_Type="Without Additional Payment"), 
                                     df_additional.assign(Payment_Type="With Additional Payment")])).mark_line().encode(
    x=alt.X("Month:Q", title="Month"),
    y=alt.Y("Remaining Balance:Q", title="Remaining Balance"),
    color="Payment_Type:N"
).properties(
    width=700,
    height=400
)

st.altair_chart(balance_chart)

st.subheader("Principal and Interest Payments Over Time")

principal_interest_chart = alt.Chart(pd.concat([df_no_additional.assign(Payment_Type="Without Additional Payment"), 
                                                df_additional.assign(Payment_Type="With Additional Payment")])).transform_fold(
    fold=["Principal Paid", "Interest Paid"],
    as_=["Payment Component", "Amount"]
).mark_line().encode(
    x=alt.X("Month:Q", title="Month"),
    y=alt.Y("Amount:Q", title="Amount Paid"),
    color="Payment Component:N",
    strokeDash="Payment_Type:N"
).properties(
    width=700,
    height=400
)

st.altair_chart(principal_interest_chart)
