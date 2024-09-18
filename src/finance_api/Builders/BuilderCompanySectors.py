import time

from src.finance_api.Builders.BuilderMuliplactures import BuilderMultiplactures
from src.finance_api.Services.FinanceService import FinanceService


class BuilderCompanySectors:
    average_PE: {}
    average_PB: {}
    average_ROE: {}
    average_EPS: {}
    average_Quick_Ratio: {}
    average_Dept_eq: {}

    def __init__(self, companies: [str]):
        self.companies = companies
        self.builder_multiplactures = BuilderMultiplactures()
        self.finance_service = FinanceService()
        self.sectors_with_companies = self.__init_sectors_with_companies()
        self.sectors = self.sectors_with_companies.keys()

        self.average_PE = self.__create_average_PE()
        self.average_PB = self.__create_average_PB()
        self.average_ROE = self.__create_average_ROE()
        self.average_EPS = self.__create_average_EPS()
        self.average_Quick_Ratio = self.__create_average_quick_ratio()
        self.average_Dept_eq = self.__create_average_dept_eq()
        print('средние значения созданы')

    def __init_sectors_with_companies(self):
        sectors_comp = {}
        for comp in self.companies:
            sector = self.finance_service.yahoo_api.get_info(comp)['sector']
            if sector in sectors_comp.keys():
                sectors_comp[sector] += ' ' + comp
            else:
                sectors_comp[sector] = comp
        return sectors_comp

    def __create_average_PE(self):
        average_pe = self.builder_multiplactures.get_average_multi(self.sectors, self.sectors_with_companies, 'PE')
        return average_pe

    def __create_average_PB(self):
        average_pb = self.builder_multiplactures.get_average_multi(self.sectors, self.sectors_with_companies, 'PB')
        return average_pb

    def __create_average_ROE(self):
        average_roe = self.builder_multiplactures.get_average_multi(self.sectors, self.sectors_with_companies, 'ROE')
        return average_roe

    def __create_average_EPS(self):
        average_eps = self.builder_multiplactures.get_average_multi(self.sectors, self.sectors_with_companies, 'EPS')
        return average_eps

    def __create_average_quick_ratio(self):
        average_quick_ratio = self.builder_multiplactures.get_average_multi(self.sectors, self.sectors_with_companies,
                                                                            'Quick_Ratio')
        return average_quick_ratio

    def __create_average_dept_eq(self):
        average_dept_eq = self.builder_multiplactures.get_average_multi(self.sectors, self.sectors_with_companies,
                                                                        'Dept_Eq')
        return average_dept_eq

    def get_company_in_sector(self, company: str) -> [str]:
        company_sector = self.finance_service.get_company_sector(company)
        companies_in_sector = self.sectors_with_companies[company_sector].split(' ')
        companies_in_sector.remove(company)
        return companies_in_sector


if __name__ == "__main__":
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
    builder = BuilderCompanySectors(companies)
    print(builder.average_EPS)
    print(builder.get_company_in_sector('GOOG'))
    print(builder.average_PE)
    print(time.strftime('%X'))
