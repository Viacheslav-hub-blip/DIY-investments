from fastapi import APIRouter
from src.finance_api.Builders.BuilderCompanyData import BuilderCompany
from src.finance_api.config import companies

router = APIRouter(
    prefix="/yahoo",
    tags=["Yahoo"]
)

company_builder = BuilderCompany()


@router.get("/companies")
async def get_companies_data_preview():
    companies_data = []
    for company in companies:
        companies_data.append(company_builder.get_data_preview(company))
    return companies_data


@router.get("/company")
async def get_company_all_data(company: str):
    data  = company_builder.get_all_data(company)
    print(data)
    return data


@router.get("/liked_companies")
async def get_liked_companies_preview(companies: str):
    companies = [comp for comp in companies.split(' ') if len(comp) > 1]
    companies_data = []
    for company in companies:
        print(company)
        companies_data.append(company_builder.get_data_preview(company))
    return companies_data


# @router.get("/company_table")
# async def get_company_data_for_table():
#     companies_data = []
#     with ThreadPoolExecutor() as executor:
#         futures = [executor.submit(builder.createDataTable, my_data) for my_data in companies]
#     for future in as_completed(futures):
#         companies_data.append((future.result())._asdict())
#     return companies_data
