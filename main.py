from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib

telco_app = FastAPI()

model = joblib.load('telco_model.joblib')
scaler = joblib.load('scaler_telco.joblib')


class TelcoSchema(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: str
    InternetService: str
    OnlineSecurity: str
    TechSupport: str


contract_list = ['One year', 'Two year']
internet_service_list = ['Fiber optic', 'No']
online_security_list = ['No internet service', 'Yes']
tech_support_list = ['No internet service', 'Yes']


@telco_app.post('/predict')
async def predict_telco(telco: TelcoSchema):
    telco_data = telco.dict()

    contract = telco_data.pop('Contract')
    contract_0_1 = [
        1 if contract == i else 0 for i in contract_list
    ]

    internet_service = telco_data.pop('InternetService')
    internet_service_0_1 = [
        1 if internet_service == i else 0 for i in internet_service_list
    ]

    online_security = telco_data.pop('OnlineSecurity')
    online_security_0_1 = [
        1 if online_security == i else 0 for i in online_security_list
    ]

    tech_support = telco_data.pop('TechSupport')
    tech_support_0_1 = [
        1 if tech_support == i else 0 for i in tech_support_list
    ]

    data = (
        list(telco_data.values())
        + contract_0_1
        + internet_service_0_1
        + online_security_0_1
        + tech_support_0_1
    )
    scaled_data = scaler.transform([data])
    predict = int(model.predict(scaled_data)[0])
    pred_data = 'churn' if predict == 1 else 'no churn'
    return {'message': pred_data}


if __name__ == '__main__':
    uvicorn.run(telco_app, host='127.0.0.1', port=8002)