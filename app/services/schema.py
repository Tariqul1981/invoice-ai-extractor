from pydantic import BaseModel
from typing import List, Optional

from pydantic import BaseModel
from typing import List, Optional


class FieldWithConfidence(BaseModel):
    value: Optional[str]
    confidence: Optional[float]


class LineItem(BaseModel):
    description: Optional[str]
    quantity: Optional[str]
    unit_price: Optional[str]
    total: Optional[str]


class InvoiceSchema(BaseModel):
    invoice_number: Optional[FieldWithConfidence]
    invoice_date: Optional[FieldWithConfidence]
    vendor_name: Optional[FieldWithConfidence]
    buyer_name: Optional[FieldWithConfidence]
    total_amount: Optional[FieldWithConfidence]
    vat_amount: Optional[FieldWithConfidence]
    currency: Optional[FieldWithConfidence]
    line_items: Optional[List[LineItem]]