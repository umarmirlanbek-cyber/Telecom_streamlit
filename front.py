import streamlit as st
import requests

api_url = 'http://127.0.0.1:8002/predict'

st.title('Telco Churn Project')

tenure = st.number_input('Стаж клиента (месяцев)', min_value=0, max_value=100, value=12, step=1)
MonthlyCharges = st.number_input('Ежемесячный платеж', min_value=0.0, value=70.0, step=5.0)
TotalCharges = st.number_input('Всего оплачено', min_value=0.0, value=1000.0, step=50.0)
Contract = st.selectbox('Тип контракта', ['Month-to-month', 'One year', 'Two year'])
InternetService = st.selectbox('Интернет услуга', ['DSL', 'Fiber optic', 'No'])
OnlineSecurity = st.selectbox('Онлайн безопасность', ['No', 'No internet service', 'Yes'])
TechSupport = st.selectbox('Техподдержка', ['No', 'No internet service', 'Yes'])

telco_data = {
    "tenure": tenure,
    "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges,
    "Contract": Contract,
    "InternetService": InternetService,
    "OnlineSecurity": OnlineSecurity,
    "TechSupport": TechSupport,
}

if st.button("Предсказать"):
    try:
        answer = requests.post(api_url, json=telco_data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.json(result)
        else:
            st.error(f"Ошибка: {answer.status_code}")
    except requests.exceptions.RequestException:
        st.error(f"Не удалось соединиться к API")