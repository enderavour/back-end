from sqlalchemy import select
from app.models.company import Company
from .base import BaseRepository

class CompanyRepository(BaseRepository):
    model = Company
