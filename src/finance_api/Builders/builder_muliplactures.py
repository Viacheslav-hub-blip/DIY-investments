import enum
import time
from typing import Optional, NamedTuple
import re
from src.finance_api.Services.finance_service import FinanceService
import math


class MultiEnum(enum.Enum):
    pe: str = 'PE'
    pb: str = 'PB'
    roe: str = 'ROE'
    eps: str = 'EPS'
    quick_ratio: str = 'QR'
    dept_equity: str = 'DQ'


class AllMulti(NamedTuple):
    pe: dict[str, Optional[float]]
    pb: dict[str, Optional[float]]
    roe: dict[str, Optional[float]]
    eps: dict[str, Optional[float]]
    quick_ratio: dict[str, Optional[float]]
    dept_equity: dict[str, Optional[float]]


class BuilderMultiplactures:
    yahoo_service = FinanceService()

    @classmethod
    def get_company_PE(cls, company: str) -> dict[str, Optional[float]]:
        '''
        net_income: чистая прибыль компании за все доступные годы
        share_number: количество акций компании за все доступные годы
        share_price_in_year: цена акций компании в определенный год
        company_PE: вычисленный мультипликатор за все возможные годы

        P/E - соотношение капитализации компании и ее прибыли
        '''
        company_PE: dict[str, Optional[float]] = {}
        net_income: dict[str, Optional[float]] = cls.yahoo_service.get_net_income(company)
        shares_number: dict[str, Optional[float]] = cls.yahoo_service.get_shares_number(company)

        for year, net_income_, shares_number_ in zip(net_income.keys(), net_income.values(), shares_number.values()):
            share_price_in_year = \
                list((cls.yahoo_service.get_price_per_start_end_period(company, year, year)).values())[0]
            pe_value: float = (shares_number_ * share_price_in_year) / net_income_
            year = re.findall('(\d{4})', year)[0]
            if not math.isnan(pe_value): company_PE[year] = round(pe_value, 3)
        return company_PE

    @classmethod
    def get_company_PB(cls, company: str) -> dict[str, Optional[float]]:
        '''
        P/B - отношение капитализации компанию к балансовой стоимости ее активов
        возвращает словарь с мультипликатором P/B за достпные годы.Возможно значение nan
        '''
        pb: dict[str, Optional[float]] = {}
        shares_number: dict[str, Optional[float]] = cls.yahoo_service.get_shares_number(company)
        stockholders_equity: dict[str, Optional[float]] = cls.yahoo_service.get_stockholders_equity(company)

        for year, shares_number_, stockholders_equity_ in zip(shares_number.keys(), shares_number.values(),
                                                              stockholders_equity.values()):
            share_price_in_year = \
                list((cls.yahoo_service.get_price_per_start_end_period(company, year, year)).values())[0]
            market_cap: float = shares_number_ * share_price_in_year
            year = re.findall('(\d{4})', year)[0]
            if not math.isnan(market_cap): pb[year] = round(market_cap / stockholders_equity_, 3)
        return pb

    @classmethod
    def get_company_ROE(cls, company: str) -> dict[str, Optional[float]]:
        '''
        ROE  - показатель рнетабельности капитала
        возвращает словарь с мультипликатором ROE за достпные годы.Возможно значение nan

        '''
        roe: dict[str, Optional[float]] = {}
        net_income: dict[str, Optional[float]] = cls.yahoo_service.get_net_income(company)
        stockholders_equity: dict[str, Optional[float]] = cls.yahoo_service.get_stockholders_equity(company)

        for year, net_income_, stockholders_Equity_ in zip(net_income.keys(), net_income.values(),
                                                           stockholders_equity.values()):
            res = round(net_income_ / stockholders_Equity_, 3)
            year = re.findall('(\d{4})', year)[0]
            if not math.isnan(res): roe[year] = res
        return roe

    @classmethod
    def get_company_dept_eq(cls, company: str) -> dict[str, Optional[float]]:
        '''D/E отражает соотношение долга к собственному капиталу в активах компании.
        возвращает словарь с мультипликатором D/E за достпные годы.Возможно значение nan
        '''
        dept_eq: dict[str, Optional[float]] = {}
        stockholders_equity: dict[str, Optional[float]] = cls.yahoo_service.get_stockholders_equity(company)
        dept: dict[str, Optional[float]] = cls.yahoo_service.get_company_dept(company)

        for year, dept_, stockholders_Equity in zip(dept.keys(), dept.values(), stockholders_equity.values()):
            res = round(dept_ / stockholders_Equity, 3)
            year = re.findall('(\d{4})', year)[0]
            if not math.isnan(res): dept_eq[year] = res
        return dept_eq

    @classmethod
    def get_company_EPS(cls, company: str) -> dict[str, Optional[float]]:
        '''
        EPS - позывает, сколько чистой прибыли приходится на одну акцию
        возвращает словарь с мультипликатором EPS за достпные годы.Возможно значение nan
        '''
        eps: dict[str, Optional[float]] = {}
        net_income: dict[str, Optional[float]] = cls.yahoo_service.get_net_income(company)
        shares_number: dict[str, Optional[float]] = cls.yahoo_service.get_shares_number(company)

        for year, net_income_, shares_number_ in zip(net_income.keys(), net_income.values(), shares_number.values()):
            res = round(net_income_ / shares_number_, 3)
            year = re.findall('(\d{4})', year)[0]
            if not math.isnan(res): eps[year] = res
        return eps

    @classmethod
    def get_quick_ratio(cls, company: str) -> dict[str, Optional[float]]:
        '''
        Quick Ratio — это коэффициент быстрой ликвидности, который показывает
        способность компании выполнять свои
        краткосрочные обязательства с помощью наиболее ликвидных активов
        возвращает словарь с мультипликатором quick_ratio за достпные годы.Возможно значение nan
        '''
        quick_ratio: dict[str, Optional[float]] = {}
        equivalents_and_short_term_investment: dict[
            str, Optional[float]] = cls.yahoo_service.get_equivalents_and_short_term_investment(company)
        accounts_receivable: dict[str, Optional[float]] = cls.yahoo_service.get_accounts_receivable(company)
        current_liabilities: dict[str, Optional[float]] = cls.yahoo_service.get_current_liabilities(company)

        for year, EASTI, accounts_Receivable_, current_Liabilities_ in zip(equivalents_and_short_term_investment.keys(),
                                                                           equivalents_and_short_term_investment.values(),
                                                                           accounts_receivable.values(),
                                                                           current_liabilities.values()):
            res = round((EASTI + accounts_Receivable_) / current_Liabilities_, 3)
            year = re.findall('(\d{4})', year)[0]
            if not math.isnan(res): quick_ratio[year] = res
        return quick_ratio

    @classmethod
    def get_average_multi(cls, all_companies: [str]) -> AllMulti:
        '''
        Возвращает среднее значение мультипликатора среди компаний за доступные годы
        '''
        values: list = []
        for multi in MultiEnum:
            average_muiltiplactures = {}

            for company in all_companies:
                average_muiltiplactures = cls._calculate_average_value(average_muiltiplactures,
                                                                       cls._choose_multiplacture(company,
                                                                                                 multi))
            values.append(average_muiltiplactures)
        return AllMulti(*values)

    @classmethod
    def get_all_available_multi(cls, company, last_year=False) -> AllMulti:
        '''возворащает все определенные мультипликаторы
        при last_year=True возвращает значения мультипликаторов только за последний год
        '''
        multi_values: list = []
        for m in MultiEnum:
            multi_values.append(cls._choose_multiplacture(company, m))

        if not last_year:
            return AllMulti(*multi_values)
        else:
            last_multi_values = []
            for multi in multi_values:
                last_multi_values.append(multi[list(multi.keys())[-1]])
            return AllMulti(*last_multi_values)

    @classmethod
    def _choose_multiplacture(cls, company: str, multi: MultiEnum) -> dict[str, Optional[float]]:
        '''
        Возвращает мультипликатор компании
        '''
        if multi == MultiEnum.pe:
            return cls.get_company_PE(company)
        elif multi == MultiEnum.pb:
            return cls.get_company_PB(company)
        elif multi == MultiEnum.roe:
            return cls.get_company_ROE(company)
        elif multi == MultiEnum.eps:
            return cls.get_company_EPS(company)
        elif multi == MultiEnum.quick_ratio:
            return cls.get_quick_ratio(company)
        elif multi == MultiEnum.dept_equity:
            return cls.get_company_dept_eq(company)

    @classmethod
    def _calculate_average_value(cls, old_average_muiltiplactures, new_average_muiltiplactures) -> dict[
        str, Optional[float]]:
        '''
        Вычисляет среднее значение показателей компаний за каждый год
        '''
        calculated_average_muiltiplactures: dict[str, Optional[float]] = {}
        if len(old_average_muiltiplactures) != 0:
            for idx, (year, old_value, new_value) in enumerate(
                    zip(old_average_muiltiplactures.keys(), old_average_muiltiplactures.values(),
                        new_average_muiltiplactures.values())):
                calculated_average_muiltiplactures[year] = round((old_value + new_value) / (idx + 2), 2)
            return calculated_average_muiltiplactures
        else:
            return new_average_muiltiplactures


if __name__ == "__main__":
    builder_multi = BuilderMultiplactures()
    print(builder_multi.get_average_multi(['AAPL', 'GOOG']))
