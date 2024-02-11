from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
import uvicorn
import pickle


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"predicted_price": False})


@app.post("/predict", response_class=HTMLResponse)
def predict(
        request: Request,
        ram: int = Form(),
        weight: float = Form(),
        cpu: str = Form(),
        os: str = Form(),
        gpu: str = Form(),
        manufacturer: str = Form(),
        type: str = Form(),
        touch: bool = Form(False),
        ips: bool = Form(False)
):

    companies = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
    types = ['2 in 1 convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
    os_list = ["linux", "mac", "other", "windows"]
    gpu_list = ['amd', 'intel', 'nvidia', 'nvidia gtx']
    cpu_list = ['amd', 'intel core i3', 'intel core i5', 'intel core i7', 'other']

    data = [ram, weight, int(touch), int(ips)]

    for company in companies:
        data.append(int(company == manufacturer.lower()))

    for t in types:
        data.append(int(t == type.lower()))

    for i in os_list:
        data.append(int(i == os.lower()))

    for g in gpu_list:
        data.append(int(g == gpu.lower()))

    for c in cpu_list:
        data.append(int(c == cpu.lower()))

    price = predict_price(data)
    return templates.TemplateResponse(request=request, name="index.html", context={"predicted_price": price})


def predict_price(data):
    filename = 'model.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)

    predicted_price = model.predict([data])
    return round(euro_to_usd(predicted_price[0]), 2)


def euro_to_usd(euro_price):
    return euro_price * 1.08


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
