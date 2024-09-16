from concurrent.futures import ThreadPoolExecutor, as_completed

from src.finance_api.BuilderCompanyData import BuilderCompany
from src.finance_api.BuilderCompanySectors import BuilderCompanySectors
from src.finance_api.FinanceService import FinanceService
from fastapi import APIRouter
import time

companies = [
    'GOOG',
    'AAPL',
    'MSFT',
    'NVDA',
    'META',
    'TSLA',
    'AMZN'
]

fin_service = FinanceService()
builder_sectors = BuilderCompanySectors(companies)
builder = BuilderCompany(fin_service, builder_sectors)

router = APIRouter(
    prefix="/yahoo",
    tags=["Yahoo"]
)


@router.get("/companies")
async def get_companies_data_preview():
    companies_data = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(builder.createDataPreview, my_data) for my_data in companies]
    for future in as_completed(futures):
        companies_data.append((future.result())._asdict())
    return companies_data


@router.get("/company")
async def get_company_all_data(company: str):
    print('gte comp')
    print(time.strftime('%X'))
    data = builder.createAllData(company)
    print(time.strftime('%X'))
    return data._asdict()


@router.get("/liked_companies")
async def get_liked_companies_preview(companies: str):
    print('comp', companies)
    companies = [comp for comp in companies.split(' ') if len(comp) > 1]
    companies_data = []
    for company in companies:
        data = builder.createDataPreview(company)
        companies_data.append(data._asdict())
    return companies_data


@router.get("/company_table")
async def get_company_data_for_table():
    companies_data = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(builder.createDataTable, my_data) for my_data in companies]
    for future in as_completed(futures):
        companies_data.append((future.result())._asdict())
    return companies_data
