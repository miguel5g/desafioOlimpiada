from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Customer, CustomerCategory

router = APIRouter(prefix="/customer", tags=["Customer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(data: dict, db: Session = Depends(get_db)):
    data_mapped = {
        'name': data["name"].strip(),
        'categories': data["categories"]
    }
    
    if data_mapped["name"] is None or data_mapped["name"] is "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty")
    
    customer = Customer(name=data_mapped["name"])
    db.add(customer)
    db.commit()
    db.refresh(customer)

    for cat in data_mapped.get("categories", []):
        category = CustomerCategory(customer_id=customer.id, category_name=cat)
        db.add(category)
    db.commit()

    return {"customer_id": customer.id}

@router.put("/{customer_id}")
def update_customer(customer_id: int, data: dict, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    customer.name = data["name"]
    db.query(CustomerCategory).filter(CustomerCategory.customer_id == customer_id).delete()

    # for cat in data.get("categories", []):
    #     category = CustomerCategory(customer_id=customer.id, category_name=cat)
    #     db.add(category)
    # db.commit()

    return {"message": "Customer updated."}

@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    categories = db.query(CustomerCategory).filter(CustomerCategory.customer_id == customer_id).all()
    return {
        "id": customer.id,
        "name": customer.name,
        "categories": [c.category_name for c in categories]
    }
