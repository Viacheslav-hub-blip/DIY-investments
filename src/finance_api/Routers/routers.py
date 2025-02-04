import json

from fastapi import APIRouter
from src.finance_api.Builders.builder_company_data import BuilderCompany
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
    return data

@router.get("/another_companies")
async def get_another_companies_data(base_company: str):
    return company_builder.get_another_companies_in_sector(base_company)


@router.get("/liked_companies")
async def get_liked_companies_preview(companies: str):
    companies = [comp for comp in companies.split(' ') if len(comp) > 1]
    companies_data = []
    for company in companies:
        print(company)
        companies_data.append(company_builder.get_data_preview(company))
    return companies_data
