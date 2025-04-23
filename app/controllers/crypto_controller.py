from fastapi import APIRouter, status, HTTPException
import httpx
from datetime import datetime, timedelta

router = APIRouter(prefix="/crypto", tags=["Crypto"])

@router.post("/{crypto}")
async def psgft(crypto: str, data: dict):
    quantidade = data["quantidade"]

    if type(quantidade) is not float:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Quantity must be an float")
    
    data_compra = datetime.fromisoformat(data["dataCompra"])
    data_venda = datetime.fromisoformat(data["dataVenda"])
    dias = (data_venda - data_compra).days
    previsao = False

    if data_compra > datetime.now():
        data_compra = datetime.now() - timedelta(days=1)
        previsao = True
    if data_venda > datetime.now():
        data_venda = datetime.now() - timedelta(days=1)
        previsao = True


    if dias < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Dates cannot be negative")

    async with httpx.AsyncClient() as client:
        compra = await client.get(f"https://www.mercadobitcoin.net/api/{crypto}/day-summary/{data_compra.year}/{data_compra.month}/{data_compra.day}/")
        venda = await client.get(f"https://www.mercadobitcoin.net/api/{crypto}/day-summary/{data_venda.year}/{data_venda.month}/{data_venda.day}/")

    # if previsao:
    #     async with httpx.AsyncClient() as client:
    #         historico = await client.get(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4447/dados?formato=json")
    #         # infracao = historico[:-1]
    #         print(historico)
        
    avg_compra = compra.json()["avg_price"]
    avg_venda = venda.json()["avg_price"]
    valor_compra = avg_compra * quantidade
    valor_venda = avg_venda * quantidade
    lucro = valor_venda - valor_compra
    lucro_pct = (lucro / valor_compra) * 100

    return {
        "previsao": previsao,
        "valor_da_compra": round(valor_compra, 2),
        "valor_da_venda": round(valor_venda, 2),
        "lucro": round(lucro, 2),
        "lucro_percentual": round(lucro_pct, 2),
        "intervalo_em_dias": dias
    }