from fastapi import APIRouter

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.get("/calculate/{value}/{amount}")
def calculate(value: float, amount: int):
    installments = []
    installment_value = round(value / amount, 2)
    installment_rest = value - (installment_value * amount)

    for order_id in range(1, amount + 1):
        installments.append({"order": order_id, "value": installment_value + installment_rest})

        if order_id == 1:
            installment_rest = 0

    return {
        "value": value,
        "amount": amount,
        "installments": installments
    }