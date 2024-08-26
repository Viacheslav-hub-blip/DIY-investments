import copy

from src.finance_api.FinanceService import FinanceService
from datetime import datetime, timedelta


class BuilderMultiplactures:
    def __init__(self):
        self.yahoo_service = FinanceService()

    def get_company_PE(self, company: str) -> dict:
        net_income = self.yahoo_service.get_net_income(company)
        shares_number = self.yahoo_service.get_shares_number(company)

        net_income = self.convertTimestamp(net_income)
        shares_number = self.convertTimestamp(shares_number)
        prices, company_PE = {}, {}

        prices = self.convertPrice(net_income, company)

        for net_income_, shares_number_, price_ in zip(net_income.items(), shares_number.items(), prices.items()):
            pe = int(price_[1]) / (net_income_[1] / shares_number_[1])
            company_PE[net_income_[0]] = round(pe, 2)

        return company_PE

    def get_company_PB(self, company: str) -> dict:
        shares_number = self.yahoo_service.get_shares_number(company)
        shares_number = self.convertTimestamp(shares_number)

        stockholders_Equity = self.yahoo_service.get_Stockholders_Equity(company)
        stockholders_Equity = self.convertTimestamp(stockholders_Equity)

        prices = self.convertPrice(shares_number, company)
        marketcap, pb = {}, {}

        for shares, prices in zip(shares_number.items(), prices.items()):
            marketcap[shares[0]] = shares[1] * prices[1]

        for marketcap_, stockholders_Equity_ in zip(marketcap.items(), stockholders_Equity.items()):
            pb[stockholders_Equity_[0]] = round(marketcap_[1] / stockholders_Equity_[1], 3)

        return pb

    def get_company_ROE(self, company: str) -> dict:
        net_income = self.yahoo_service.get_net_income(company)
        net_income = self.convertTimestamp(net_income)

        stockholders_Equity = self.yahoo_service.get_Stockholders_Equity(company)
        stockholders_Equity = self.convertTimestamp(stockholders_Equity)

        roe = {}

        for net_income_, stockholders_Equity_ in zip(net_income.items(), stockholders_Equity.items()):
            roe[net_income_[0]] = round(net_income_[1] / stockholders_Equity_[1], 3)

        return roe

    def get_company_Dept_Eq(self, company: str) -> dict:
        stockholders_Equity = self.yahoo_service.get_Stockholders_Equity(company)
        stockholders_Equity = self.convertTimestamp(stockholders_Equity)

        dept = self.yahoo_service.get_company_Dept(company)
        dept = self.convertTimestamp(dept)

        dept_eq = {}

        for dept_, stockholders_Equity in zip(dept.items(), stockholders_Equity.items()):
            dept_eq[dept_[0]] = round(dept_[1] / stockholders_Equity[1], 3)

        return dept_eq

    def get_company_EPS(self, company: str) -> dict:
        net_income = self.yahoo_service.get_net_income(company)
        net_income = self.convertTimestamp(net_income)

        shares_number = self.yahoo_service.get_shares_number(company)
        shares_number = self.convertTimestamp(shares_number)

        eps = {}

        for net_income_, shares_number_ in zip(net_income.items(), shares_number.items()):
            eps[net_income_[0]] = round(net_income_[1] / shares_number_[1], 3)
        return eps

    def get_Quick_Ratio(self, company: str) -> dict:
        equivalents_And_Short_Term_Investment = self.yahoo_service.get_Equivalents_And_Short_Term_Investment(company)
        equivalents_And_Short_Term_Investment = self.convertTimestamp(equivalents_And_Short_Term_Investment)

        accounts_Receivable = self.yahoo_service.get_Accounts_Receivable(company)
        accounts_Receivable = self.convertTimestamp(accounts_Receivable)

        current_Liabilities = self.yahoo_service.get_Current_Liabilities(company)
        current_Liabilities = self.convertTimestamp(current_Liabilities)

        quick_ratio = {}

        for EASTI, accounts_Receivable_, current_Liabilities_ in zip(equivalents_And_Short_Term_Investment.items(),
                                                                     accounts_Receivable.items(),
                                                                     current_Liabilities.items()):
            quick_ratio[EASTI[0]] = round((EASTI[1] + accounts_Receivable_[1]) / current_Liabilities_[1], 3)

        return quick_ratio

    def convertPrice(self, data: dict, company) -> dict:
        prices = {}
        for key, _ in data.items():
            try:
                price = \
                    self.yahoo_service.get_history_in_year(company, (datetime.strptime(key, '%Y-%m-%d')) - timedelta(2),
                                                           (datetime.strptime(key, '%Y-%m-%d')) - timedelta(1),
                                                           '1d').head().iloc[0]
                prices[((datetime.strptime(key, '%Y-%m-%d')) - timedelta(2)).strftime('%Y-%m-%d')] = price
            except:
                price = \
                    self.yahoo_service.get_history_in_year(company, (datetime.strptime(key, '%Y-%m-%d')) - timedelta(5),
                                                           (datetime.strptime(key, '%Y-%m-%d')) - timedelta(1),
                                                           '1d').head().iloc[0]
                prices[((datetime.strptime(key, '%Y-%m-%d')) - timedelta(2)).strftime('%Y-%m-%d')] = price

        return prices

    def convertTimestamp(self, data: dict) -> dict:
        keys, values, dates = [], [], []
        result_dict = {}

        for key, _ in data.items():
            keys.append(key)
            try:
                int(data[key])
                values.append(data[key])
            except:
                pass

        for date_ in keys:
            date_format = date_.to_pydatetime().date()
            str_date = date_format.strftime('%Y-%m-%d')
            if str_date != '2019-12-31':
                dates.append(str_date)

        dates = dates[::-1]
        values = values[::-1]
        for date, value in zip(dates, values):
            result_dict[date] = value

        return result_dict

    def get_average_multi(self, sectors: [str], all_companies: [str], multi: str):
        sectors_average = {}

        for sec in sectors:
            companies = all_companies[sec].split(' ')
            sectors_average[sec] = {}

            for comp in companies:
                multiplicator = {}

                if multi == 'PE':
                    multiplicator = self.get_company_PE(comp)
                elif multi == 'PB':
                    multiplicator = self.get_company_PB(comp)
                elif multi == 'ROE':
                    multiplicator = self.get_company_ROE(comp)
                elif multi == 'EPS':
                    multiplicator = self.get_company_EPS(comp)
                elif multi == 'Quick_Ratio':
                    multiplicator = self.get_Quick_Ratio(comp)
                elif multi == 'Dept_Eq':
                    multiplicator = self.get_company_Dept_Eq(comp)

                for key, value in multiplicator.items():
                    date = datetime.strptime(key, '%Y-%m-%d')
                    new_date = datetime.strftime(date, '%Y')

                    if new_date in sectors_average[sec].keys():
                        sectors_average[sec][new_date] += value
                    else:
                        sectors_average[sec][new_date] = value

            for key, value in sectors_average[sec].items():
                sectors_average[sec][key] = round(value / len(companies), 2)

        return sectors_average

    def convert_multiplacture_date_to_years(self, multiplac: [{}]) -> []:
        new_multi = []
        for placture in multiplac:
            new_placture = {}
            for key, value in placture.items():
                date = datetime.strptime(key, '%Y-%m-%d')
                new_date = datetime.strftime(date, '%Y')
                new_placture[new_date] = value
            new_multi.append(new_placture)
        return new_multi

    def comparison_average_multiplactures_years(self, multiplac: [{}], average_multiplac: [{}]) -> [{}]:
        new_average = copy.deepcopy(average_multiplac)
        for i, current_average_multi in enumerate(average_multiplac):
            for key in current_average_multi.keys():
                if key not in multiplac[i].keys():
                    del new_average[i][key]

        return new_average


if __name__ == "__main__":
    b = BuilderMultiplactures()
    print(b.get_company_PE('goog'))
    print(b.get_company_PB('goog'))
    print(b.get_company_ROE('goog'))
    print(b.get_company_Dept_Eq('goog'))
    print(b.get_company_EPS('goog'))
    print(b.get_Quick_Ratio('goog'))

    pe = b.get_company_PE('goog')
    pb = b.get_company_PB('goog')
    print('new', b.convert_multiplacture_date_to_years([pe, pb]))

    sectors = ['Communication Services', 'Technology', 'Consumer Cyclical']
    sectors_comp = {'Communication Services': 'GOOG META', 'Technology': 'AAPL MSFT NVDA',
                    'Consumer Cyclical': 'TSLA AMZN'}

    print(b.get_average_multi(sectors, sectors_comp, 'PB'))

    # sectors_average_PE = {}
    #
    # for sec in sectors:
    #     companies = sectors_comp[sec].split(' ')
    #     sectors_average_PE[sec] = {}
    #
    #     for comp in companies:
    #         pe = b.get_company_PE(comp)
    #         for key, value in pe.items():
    #             date = datetime.strptime(key, '%Y-%m-%d')
    #             new_date = datetime.strftime(date, '%Y')
    #
    #             if new_date in sectors_average_PE[sec].keys():
    #                 sectors_average_PE[sec][new_date] += value
    #             else:
    #                 sectors_average_PE[sec][new_date] = value
    #
    #     for key, value in sectors_average_PE[sec].items():
    #         sectors_average_PE[sec][key] = round(value / len(companies), 2)
    #
    # print(sectors_average_PE)
