import pytest
from src.finance_api.Builders.BuilderCompanyData import BuilderCompany


@pytest.mark.parametrize('company', 'GOOG')
def test_get_general_data(company):
    builder = BuilderCompany()
    general_data = builder.get_data_preview(company)
    assert general_data is not None

@pytest.mark.parametrize('company', 'GOOG')
def test_get_all_company_data(company):
    builder = BuilderCompany()
    all_data  = builder.get_all_data(company)
    assert all_data is not None

def test_speed_general_data(company):
    builder = BuilderCompany()
    general_data = builder.get_data_preview(company)

def test_get_table_companies_data():
    pass
