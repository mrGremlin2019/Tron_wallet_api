from pydantic import BaseModel
from datetime import datetime

class WalletData(BaseModel):
    address: str
    bandwidth: int
    energy: int
    trx_balance: int

class QueryResponse(BaseModel):
    wallet_address: str
    bandwidth: int
    energy: int
    trx_balance: int
    query_time: datetime

class PaginatedResponse(BaseModel):
    results: list[QueryResponse]
    total: int
    page: int
    limit: int