from src.finance_api.BuilderCompanyData import BuilderCompany
from src.finance_api.FinanceService import FinanceService

def builder_company():
    return BuilderCompany(FinanceService())