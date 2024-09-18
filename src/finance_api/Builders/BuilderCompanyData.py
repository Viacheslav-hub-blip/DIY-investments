import time
from datetime import datetime
from typing import NamedTuple
from src.finance_api.Services.FinanceService import FinanceService, RecomendationsOnMonth, PriceInform
from src.finance_api.Builders.BuilderMuliplactures import BuilderMultiplactures
from src.finance_api.Builders.BuilderCompanySectors import BuilderCompanySectors
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


class CompanyDataPreview(NamedTuple):
    name: str
    logo_url: str
    marketcap: int
    one_month_change: float
    buy_recommendations: str


class CompanyDataAll(NamedTuple):
    name: str
    logo_url: str
    marketcap: int
    one_month_change: float
    buy_recommendations: str

    recommendationsOnMonth: dict
    priceInform: dict
    priceHistory: dict
    price5YearsHistory: dict
    description: str
    sector: str
    another_companies_in_sector: list

    PE: dict
    PB: dict
    ROE: dict
    DEPT_EQ: dict
    EPS: dict
    Quick_Ratio: dict

    average_multi: dict


class CompanyTable(NamedTuple):
    name: str
    logo: str
    sector: str
    marketcap: int

    PE: dict
    PB: dict
    ROE: dict
    DEPT_EQ: dict
    EPS: dict
    Quick_Ratio: dict


class BuilderCompany:
    def __init__(self, finance_service: FinanceService, builder_company_sectors: BuilderCompanySectors):
        self.finance_service = finance_service
        self.builder_multiplactures = BuilderMultiplactures()
        self.builder_company_sectors = builder_company_sectors

    def createDataPreview(self, company: str):
        '''
        :param company: тикер компании
        :return: данные компании для предварительного просмотра
        '''
        marketcap, month_change, buy_recommendation, logo_url = self.baseData(company)
        data = CompanyDataPreview(company, logo_url, marketcap, month_change, buy_recommendation)
        return data

    def createAllData(self, company: str) -> CompanyDataAll:
        '''
        Полные данные
        :param company: тикер компании
        :return: обьект со всееми возможными полями
        '''
        with ThreadPoolExecutor() as executor:
            feature_baseData = executor.submit(self.baseData, company)
            feature_price = executor.submit(self.finance_service.get_price_information, company)
            feature_description = executor.submit(self.finance_service.get_company_description, company)
            feature_industry = executor.submit(self.finance_service.get_company_sector, company)
            feature_multi = executor.submit(self.multiplactures, company)
            feature_av = executor.submit(self.get_average_multiplactures, company)
            feature_recom = executor.submit(self.finance_service.get_recommendations_summary_current_month, company)
        # рекомендации аналитиков

        history_close_with_dat = self.finance_service.get_history_close_with_date(company, '1mo', '1d')
        history_price_5Years = self.finance_service.get_history_close_with_date(company, '5y', '5d')
        another_companies_in_sector = self.create_companies_preview_in_sector(
            self.builder_company_sectors.get_company_in_sector(company))

        marketcap, month_change, buy_recommendation, logo_url = feature_baseData.result()
        description = feature_description.result()
        industry = feature_industry.result()
        priceInform = feature_price.result()
        recommendationsOnMonth = feature_recom.result()

        # мультипликаторы
        PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio = feature_multi.result()

        average_PE, average_PB, average_ROE, average_DEPT_EQ, average_EPS, average_Quick_Ratio = feature_av.result()

        average_PE, average_PB, average_ROE, average_DEPT_EQ, average_EPS, average_Quick_Ratio = self.builder_multiplactures.comparison_average_multiplactures_years(
            [PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio],
            [average_PE, average_PB, average_ROE,
             average_DEPT_EQ, average_EPS,
             average_Quick_Ratio])

        average_multi = {'average_PE': average_PE, 'average_PB': average_PB, 'average_ROE': average_ROE,
                         'average_DEPT_EQ': average_DEPT_EQ, 'average_EPS': average_EPS,
                         'average_Quick_Ratio': average_Quick_Ratio}

        return CompanyDataAll(company,
                              logo_url,
                              marketcap,
                              month_change,
                              buy_recommendation,
                              recommendationsOnMonth,
                              priceInform._asdict(),
                              history_close_with_dat,
                              history_price_5Years,
                              description,
                              industry,
                              another_companies_in_sector,
                              PE,
                              PB,
                              ROE,
                              Dept_Eq,
                              EPS,
                              Quick_Ratio,
                              average_multi)

    def createDataTable(self, company: str) -> CompanyTable:
        '''
        капитализация, сектор компании, мультипликаторы, логотип
        :param company: тикер компании
        :return:
        '''
        marketcap = self.finance_service.get_marketcap(company)
        industry = self.finance_service.get_company_sector(company)
        PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio = self.get_last_year_from_multiplactures(company)
        logo_url = f'https://companiesmarketcap.com/img/company-logos/64/{company}.webp'

        return CompanyTable(company, logo_url, industry, marketcap, PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio)

    def baseData(self, company: str) -> ():
        '''
        данные для превью
        :param company:
        :return:
        '''
        marketcap = self.finance_service.get_marketcap(company)
        month_change = self.finance_service.get_one_month_change(company)
        buy_recommendation = self.finance_service.get_buy_recommendation(company)
        logo_url = f'https://companiesmarketcap.com/img/company-logos/64/{company}.webp'
        return (marketcap, month_change, buy_recommendation, logo_url)

    def create_companies_preview_in_sector(self, companies_in_sector: [str]) -> []:
        '''

        :param companies_in_sector: список тикеров компаний в одном секторе с целевой компанией
        :return: превью компаний, которые входят в один сектор с целевой компанией
        '''
        companies_data = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.createDataPreview, company) for company in companies_in_sector]

        for future in futures:
            companies_data.append((future.result())._asdict())
        return companies_data

    def multiplactures(self, company: str) -> ():
        '''
        мультипликаторы. Все мультипликаторы за все доступные года
        :param company:
        :return:
        '''
        with ThreadPoolExecutor() as executor:
            featurePE = executor.submit(self.builder_multiplactures.get_company_PE, company)
            featurePB = executor.submit(self.builder_multiplactures.get_company_PB, company)
            featureROE = executor.submit(self.builder_multiplactures.get_company_ROE, company)
            featureDept_Eq = executor.submit(self.builder_multiplactures.get_company_Dept_Eq, company)
            featureEPS = executor.submit(self.builder_multiplactures.get_company_EPS, company)
            featureQuick_Ratio = executor.submit(self.builder_multiplactures.get_Quick_Ratio, company)

        PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio = featurePE.result(), featurePB.result(), featureROE.result(), featureDept_Eq.result(), featureEPS.result(), featureQuick_Ratio.result()

        PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio = self.builder_multiplactures.convert_multiplacture_date_to_years(
            [PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio])

        return (PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio)

    def get_last_year_from_multiplactures(self, company):
        '''
        Мультипликаторы за последний доступный год
        :param company:
        :return:
        '''
        PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio = self.multiplactures(company)

        PE = PE[list(PE.keys())[-1]]
        PB = PB[list(PB.keys())[-1]]
        ROE = ROE[list(ROE.keys())[-1]]
        Dept_Eq = Dept_Eq[list(Dept_Eq.keys())[-1]]
        EPS = EPS[list(EPS.keys())[-1]]
        Quick_Ratio = Quick_Ratio[list(Quick_Ratio.keys())[-1]]

        return (PE, PB, ROE, Dept_Eq, EPS, Quick_Ratio)

    def get_average_multiplactures(self, company: str) -> ():
        '''
        Средние значеняи мультипликаторов
        :param company:
        :return:
        '''

        sector = self.finance_service.get_info(company)['sector']
        average_PE = self.builder_company_sectors.average_PE[sector]
        average_PB = self.builder_company_sectors.average_PB[sector]
        average_ROE = self.builder_company_sectors.average_ROE[sector]
        average_DEPT_EQ = self.builder_company_sectors.average_Dept_eq[sector]
        average_EPS = self.builder_company_sectors.average_EPS[sector]
        average_Quick_Ratio = self.builder_company_sectors.average_Quick_Ratio[sector]

        return (average_PE, average_PB, average_ROE, average_DEPT_EQ, average_EPS, average_Quick_Ratio)


if __name__ == '__main__':
    print(time.strftime('%X'))
    companies = [
        'GOOG',
        'AAPL',
        'MSFT',
        'NVDA',
        'META',
        'TSLA',
        'AMZN'
    ]
    builder_sectors = BuilderCompanySectors(companies)
    companies_data = []
    builder_company = BuilderCompany(FinanceService(), builder_sectors)

    t1 = datetime.now()
    executor = ThreadPoolExecutor()

    futures = [executor.submit(builder_company.createDataPreview, my_data) for my_data in companies]

    for future in as_completed(futures):
        result = future.result()
        print(result)

    t2 = datetime.now()
    print(t2 - t1)
