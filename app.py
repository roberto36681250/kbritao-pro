
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/resultado", response_class=HTMLResponse)
def calcular(
    request: Request,
    tipo_carga: str = Form(...),
    tipo_caminhao: str = Form(...),
    origem: str = Form(...),
    destino: str = Form(...),
    distancia_km: float = Form(...),
    valor_carga: float = Form(...),
    preco_diesel: float = Form(...),
    preco_arla: float = Form(...),
    dias_viagem: int = Form(...),
    lucro_percentual: float = Form(...)
):
    fatores_pedagio = {
        "VUC": 0.10,
        "Toco": 0.12,
        "Truck": 0.16,
        "Cavalo 2 eixos": 0.18,
        "Cavalo 3 eixos": 0.22
    }

    consumo_km_por_litro = 3.5 if tipo_carga != "Carne Refrigerada" else 2.5
    diesel_total = distancia_km / consumo_km_por_litro * preco_diesel
    arla_total = diesel_total / 20 * preco_arla
    manutencao = distancia_km * 0.30
    diaria_motorista = dias_viagem * 100
    seguro = valor_carga * 0.005
    pedagio = distancia_km * fatores_pedagio.get(tipo_caminhao, 0.16)
    ipva = distancia_km * 0.12
    depre = distancia_km * 0.20
    rastreamento = (150 / 30) * dias_viagem
    pneus = distancia_km * 0.15
    imprevistos = distancia_km * 0.05

    custo_total = sum([
        diesel_total, arla_total, manutencao, diaria_motorista, seguro, pedagio,
        ipva, depre, rastreamento, pneus, imprevistos
    ])

    frete_final = custo_total * (1 + lucro_percentual / 100)

    whatsapp_msg = f"""🚛 *Cotação de Frete - KBRITÃO Pro* 🚛
📦 *Tipo de Carga:* {tipo_carga}
🚚 *Tipo de Caminhão:* {tipo_caminhao}
📍 *Origem:* {origem}
🏁 *Destino:* {destino}
📏 *Distância:* {distancia_km} km

🧮 *Resumo dos custos:*
⛽ Diesel: R$ {diesel_total:.2f}
🧪 ARLA: R$ {arla_total:.2f}
🔧 Manutenção: R$ {manutencao:.2f}
👨‍✈️ Motorista: R$ {diaria_motorista:.2f}
🔐 Seguro: R$ {seguro:.2f}
🛣️ Pedágio: R$ {pedagio:.2f}
💳 IPVA: R$ {ipva:.2f}
📉 Depreciação: R$ {depre:.2f}
📡 Rastreamento: R$ {rastreamento:.2f}
🛞 Pneus: R$ {pneus:.2f}
⚠️ Imprevistos: R$ {imprevistos:.2f}

💰 *Custo Total:* R$ {custo_total:.2f}
📈 *Lucro:* {lucro_percentual:.1f}%
✅ *Frete Sugerido:* R$ {frete_final:.2f}
"""

    whatsapp_url = "https://wa.me/?text=" + quote(whatsapp_msg)

    return templates.TemplateResponse("resultado.html", {
        "request": request,
        "tipo_carga": tipo_carga,
        "tipo_caminhao": tipo_caminhao,
        "origem": origem,
        "destino": destino,
        "distancia_km": distancia_km,
        "valor_carga": valor_carga,
        "diesel_total": round(diesel_total, 2),
        "arla_total": round(arla_total, 2),
        "manutencao": round(manutencao, 2),
        "diaria_motorista": round(diaria_motorista, 2),
        "seguro": round(seguro, 2),
        "pedagio": round(pedagio, 2),
        "ipva": round(ipva, 2),
        "depreciacao": round(depre, 2),
        "rastreamento": round(rastreamento, 2),
        "pneus": round(pneus, 2),
        "imprevistos": round(imprevistos, 2),
        "custo_total": round(custo_total, 2),
        "frete_final": round(frete_final, 2),
        "lucro_percentual": lucro_percentual,
        "whatsapp_url": whatsapp_url
    })
