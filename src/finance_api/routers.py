from src.finance_api.BuilderCompanyData import BuilderCompany
from src.finance_api.BuilderCompanySectors import BuilderCompanySectors
from src.finance_api.FinanceService import FinanceService
from fastapi import APIRouter

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
    for company in companies:
        data = builder.createDataPreview(company)
        companies_data.append(data._asdict())
    return companies_data


@router.get("/company")
async def get_company_all_data(company: str):
    data = builder.createAllData(company)
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
    for company in companies:
        data = builder.createDataTable(company)
        companies_data.append(data._asdict())
    return companies_data
