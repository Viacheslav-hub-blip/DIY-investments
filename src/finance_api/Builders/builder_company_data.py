import json
import time
from datetime import datetime, timedelta
from typing import NamedTuple
from src.finance_api.Services.finance_service import FinanceService
from src.finance_api.Builders.builder_muliplactures import BuilderMultiplactures
from src.finance_api.Builders.builder_company_sectors import BuilderCompanySectors
from src.finance_api.config import companies as available_companies
from functools import lru_cache, wraps
from src.finance_api.logg import logging


class CompanyGeneralData(NamedTuple):
    name: str
    logo_url: str
    description: str
    sector: str
    market_cap: int
    one_month_change: float


class CompanyFinancialData(NamedTuple):
    PE: dict
    PB: dict
    ROE: dict
    EPS: dict
    Quick_Ratio: dict
    DEPT_EQ: dict


class CompanyAverageFinancialDataInSector(NamedTuple):
    average_multi_in_sector: dict


class CompanyPriceData(NamedTuple):
    target_price_inform: dict
    price_month_history: dict
    price_5years_history: dict


class CompanyRecommendations(NamedTuple):
    buy_recommendations: str
    recommendations_summary: dict


class CompanyDataAll(NamedTuple):
    general_data: CompanyGeneralData
    financial_data: CompanyFinancialData
    average_data: CompanyAverageFinancialDataInSector
    price_data: CompanyPriceData
    recommendations_data: CompanyRecommendations


class CompanyGeneralFinance(NamedTuple):
    general_data: CompanyGeneralData
    financial_data: CompanyFinancialData


def convert_rows_to_dict(func):
    '''преобразует все поля CompanyDataAll из NamedTuple в dict'''

    def wrapper(*args, **kwargs):
        result: CompanyDataAll = func(*args, **kwargs)
        result_dict = {}
        for row, value in result._asdict().items():
            try:
                result_dict[row] = value._asdict()
            except:
                result_dict[row] = value
        return result_dict
    return wrapper


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper_cache


class BuilderCompany:
    def __init__(self):
        self.finance_service = FinanceService()
        self.builder_multiplactures = BuilderMultiplactures()
        self.builder_company_sectors = BuilderCompanySectors(available_companies)

    @timed_lru_cache(20)
    @convert_rows_to_dict
    def get_data_preview(self, company: str) -> CompanyGeneralData:
        """
        :param company: тикер компании
        :return: данные компании для предварительного просмотра
        """
        data: CompanyGeneralData = self._get_base_data(company)
        return data

    @timed_lru_cache(20)
    @convert_rows_to_dict
    def get_all_data(self, company: str) -> CompanyDataAll:
        """
        Полные данные
        :param company: тикер компании
        :return: обьект со всеми возможными полями
        """
        general_data: CompanyGeneralData = self._get_base_data(company)

        financial_data: CompanyFinancialData = CompanyFinancialData(
            *self.builder_multiplactures.get_all_available_multi(company))

        average_financial_multi_in_sector: CompanyAverageFinancialDataInSector = CompanyAverageFinancialDataInSector(
            self.builder_multiplactures.get_average_multi(
                self.builder_company_sectors.another_company_in_company_sector(company)
            )._asdict()
        )

        price_data: CompanyPriceData = CompanyPriceData(
            self.finance_service.get_target_price_information(company)._asdict(),
            self.finance_service.get_history_share_price_per_period(company, '1mo', '1d'),
            self.finance_service.get_history_share_price_per_period(company, '5y', '1wk'))

        buy_recommendations: CompanyRecommendations = CompanyRecommendations(
            self.finance_service.get_buy_recommendation(company),
            self.finance_service.get_recommendations_summary_current_month(company)._asdict())

        return CompanyDataAll(general_data, financial_data, average_financial_multi_in_sector, price_data,
                              buy_recommendations)

    @timed_lru_cache(20)
    def get_base_and_finance_data(self, company: str) -> CompanyGeneralFinance:
        """
        капитализация, сектор компании, мультипликаторы, логотип
        :param company: тикер компании
        :return:
        """
        general_data: CompanyGeneralData = self._get_base_data(company)
        financial: CompanyFinancialData = CompanyFinancialData(
            *self.builder_multiplactures.get_all_available_multi(company, last_year=True))
        return CompanyGeneralFinance(general_data, financial)

    def get_another_companies_in_sector(self, base_company: str) -> list[dict]:
        another_companies = self.builder_company_sectors.another_company_in_company_sector(base_company)
        another_companies_general_data = [self._get_base_data(company)._asdict() for company in another_companies]
        return another_companies_general_data

    def _get_base_data(self, company: str) -> CompanyGeneralData:
        """
        данные для превью
        :param company:
        :return:
        """
        market_cap: int = self.finance_service.get_marketcap(company)
        month_change: float = self.finance_service.get_one_month_change(company)
        sector: str = self.finance_service.get_company_sector(company)
        description: str = self.finance_service.get_company_description(company)
        logo_url: str = f'https://companiesmarketcap.com/img/company-logos/64/{company}.webp'
        return CompanyGeneralData(company, logo_url, description, sector, market_cap, month_change)


if __name__ == "__main__":
    builder = BuilderCompany()
    res = builder.get_another_companies_in_sector("AAPL")
    print(json.dumps(res))
