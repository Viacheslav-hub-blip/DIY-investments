import time
from datetime import datetime, timedelta
from typing import NamedTuple
from src.finance_api.Services.FinanceService import FinanceService
from src.finance_api.Builders.BuilderMuliplactures import BuilderMultiplactures
from src.finance_api.Builders.BuilderCompanySectors import BuilderCompanySectors
from src.finance_api.config import companies as available_companies
from functools import lru_cache, wraps
from src.finance_api.logg import logging


class CompanyGeneralData(NamedTuple):
    name: str
    logo_url: str
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


class CompanyAverageFinancialData(NamedTuple):
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
    average_data: CompanyAverageFinancialData
    price_data: CompanyPriceData
    recommendations_data: CompanyRecommendations


class CompanyTable(NamedTuple):
    name: str
    logo: str
    sector: str
    market_cap: float
    financial_data: CompanyFinancialData


def convert_rows_to_dict(func):
    '''преобразует все поля CompanyDataAll из NamedTuple в dict'''

    def wrapper(*args, **kwargs):
        result: CompanyDataAll = func(*args, **kwargs)
        result_dict = {}
        for row, value in result._asdict().items():
            result_dict[row] = value._asdict()
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
    def get_data_preview(self, company: str):
        """
        :param company: тикер компании
        :return: данные компании для предварительного просмотра
        """
        data: CompanyGeneralData = self._get_base_data(company)
        return data

    # @lru_cache(maxsize=None)
    # @logging
    @timed_lru_cache(20)
    @convert_rows_to_dict
    def get_all_data(self, company: str) -> CompanyDataAll:
        """
        Полные данные
        :param company: тикер компании
        :return: обьект со всееми возможными полями
        """
        general_data: CompanyGeneralData = self._get_base_data(company)
        financial_data: CompanyFinancialData = CompanyFinancialData(
            *self.builder_multiplactures.get_all_available_multi(company))
        average_financial_data: CompanyAverageFinancialData = CompanyAverageFinancialData(
            self.builder_multiplactures.get_average_multi(company)._asdict())
        price_data: CompanyPriceData = CompanyPriceData(
            self.finance_service.get_target_price_information(company)._asdict(),
            self.finance_service.get_history_share_price_per_period(company, '1mo', '1d'),
            self.finance_service.get_history_share_price_per_period(company, '5y', '1wk'))
        buy_recommendations: CompanyRecommendations = CompanyRecommendations(
            self.finance_service.get_buy_recommendation(company),
            self.finance_service.get_recommendations_summary_current_month(company)._asdict())
        return CompanyDataAll(general_data, financial_data, average_financial_data, price_data, buy_recommendations)

    @timed_lru_cache(20)
    def create_data_table(self, company: str) -> CompanyTable:
        """
        капитализация, сектор компании, мультипликаторы, логотип
        :param company: тикер компании
        :return:
        """
        logo_url: str = f'https://companiesmarketcap.com/img/company-logos/64/{company}.webp'
        sector: str = self.finance_service.get_company_sector(company)
        market_cap: float = self.finance_service.get_marketcap(company)
        financial: CompanyFinancialData = CompanyFinancialData(
            *self.builder_multiplactures.get_all_available_multi(company, last_year=True))
        return CompanyTable(company, logo_url, sector, market_cap, financial)

    def _get_base_data(self, company: str) -> CompanyGeneralData:
        """
        данные для превью
        :param company:
        :return:
        """
        market_cap: int = self.finance_service.get_marketcap(company)
        month_change: float = self.finance_service.get_one_month_change(company)
        sector: str = self.finance_service.get_company_sector(company)
        logo_url: str = f'https://companiesmarketcap.com/img/company-logos/64/{company}.webp'
        return CompanyGeneralData(company, logo_url, sector, market_cap, month_change)


# def get_preview_in_sector(self, companies_in_sector: [str]) -> []:
#     """
#     :param companies_in_sector: список тикеров компаний в одном секторе с целевой компанией
#     :return: превью компаний, которые входят в один сектор с целевой компанией
#     """
#     companies_data = []
#     with ThreadPoolExecutor() as executor:
#         futures = [executor.submit(self.create_data_preview, company) for company in companies_in_sector]
#
#     for future in futures:
#         companies_data.append((future.result())._asdict())
#     return companies_data


if __name__ == '__main__':
    companies = [
        'GOOG',
        'AAPL',
        'MSFT',
        'NVDA',
        'META',
        'TSLA',
        'AMZN'
    ]
    builder = BuilderCompany()
    for i in range(3):
        print()
        print(time.strftime('%X'))
        t1 = datetime.now()
        print(builder.get_all_data(companies[0]))
        t2 = datetime.now()
        print(t2 - t1)
        time.sleep(10)
