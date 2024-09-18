from src.finance_api.Builders.BuilderCompanyData import BuilderCompany
from src.finance_api.Services.FinanceService import FinanceService

def builder_company():
    return BuilderCompany(FinanceService())