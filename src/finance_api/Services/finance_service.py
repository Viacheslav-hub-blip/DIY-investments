from pandas import Series
from src.finance_api.finance_api import YahooApi
from typing import NamedTuple, Any, Optional


class RecommendationsOnMonth(NamedTuple):
    strongBuy: int
    buy: int
    hold: int
    sell: int
    strongSell: int


class PriceInform(NamedTuple):
    currentPrice: float
    targetHighPrice: float
    targetLowPrice: float
    targetMeanPrice: float


def convert_time_stamp(func):
    """
    Преобразует значение ключа из timestamp в str datetime.Значение
    ключа не изменяется    """

    def wrapper(*args, **kwargs) -> dict[str, Any]:
        converted_dict: dict[str, float] = {}
        result_func = func(*args, **kwargs)

        for date, value in result_func.items():
            date_str = date.to_pydatetime().date().strftime("%Y-%m-%d")
            converted_dict[date_str] = round(value,3)

        return converted_dict

    return wrapper


class FinanceService:
    yahoo_api: YahooApi = YahooApi

    @classmethod
    def get_info(cls, company: str) -> dict:
        '''Общие сведения о компании(описание ....)'''
        return cls.yahoo_api.get_info(company)

    @classmethod
    @convert_time_stamp
    def get_price_per_start_end_period(cls, company:str, start:str, end:str, interval:str='1d') -> dict[str, float]:
        '''цену акций в периоде от начального значения до конечного с заданным интервалом'''
        return cls.yahoo_api.get_price_per_start_end_period(company, start, end, interval)['Close']

    @classmethod
    @convert_time_stamp
    def get_history_share_price_per_period(cls, company: str, period: str, interval: str='1d') -> dict[str, float]:
        '''Цена акций за заданный период'''
        return cls.yahoo_api.get_history_share_price_per_period(company, period, interval)['Close']

    @classmethod
    def get_company_description(cls, company: str) -> str:
        """Вовзращает строку с описанием компании"""
        return cls.yahoo_api.get_info(company)['longBusinessSummary']

    @classmethod
    def get_company_sector(cls, company: str) -> str:
        """Вовзращает сектор в котором работает компания"""
        return cls.yahoo_api.get_info(company)['sector']

    @classmethod
    def get_target_price_information(cls, company: str) -> PriceInform:
        current_price = cls.yahoo_api.get_info(company)['currentPrice']
        target_high_price = cls.yahoo_api.get_info(company)['targetHighPrice']
        target_low_price = cls.yahoo_api.get_info(company)['targetLowPrice']
        target_mean_price = cls.yahoo_api.get_info(company)['targetMeanPrice']
        return PriceInform(current_price, target_high_price, target_low_price, target_mean_price)

    @classmethod
    def get_recommendations_summary_current_month(cls, company: str) -> RecommendationsOnMonth:
        """Вовзвращает мнение аналитиков и их количество в виде RecommendationsOnMonth"""
        recom_dict = cls.yahoo_api.get_recommendations_summary(company).head().iloc[0]
        recommendations = RecommendationsOnMonth(
            int(recom_dict['strongBuy']),
            int(recom_dict['buy']),
            int(recom_dict["hold"]),
            int(recom_dict["sell"]),
            int(recom_dict["strongSell"]))
        return recommendations

    @classmethod
    def get_marketcap(cls, company: str) -> int:
        """Вовзращает рыночную капитализацию"""
        marketcap = cls.yahoo_api.get_info(company)['marketCap']
        return marketcap

    @classmethod
    def get_one_month_change(cls, company) -> float:
        """Возвращает изменение цены акциий за месяц в %"""
        close_history = cls.yahoo_api.get_history_share_price_per_period(company, '1mo', '1d')['Close']
        first = close_history.head().iloc[0]
        last = close_history.head().iloc[-1]
        change = float(round(((last - first) / first) * 100, 2))
        return change

    @classmethod
    def get_buy_recommendation(cls, company: str) -> str:
        """Возвращает рекомендацию аналитиков (buy, hold...)"""
        recom = cls.yahoo_api.get_info(company)['recommendationKey']
        return recom

    @classmethod
    @convert_time_stamp
    def get_net_income(cls, company: str) -> dict[str, Optional[float]]:
        # чистая прибыль
        # Получаем таблицу, выбираем нужные строку, преобразуем в словарь
        return cls.yahoo_api.get_income_stmt(company).loc[['Net Income']].to_dict(orient='records')[0]

    @classmethod
    @convert_time_stamp
    def get_shares_number(cls, company: str) -> dict[str, Optional[float]]:
        # количество акций
        # получаем строку с количеством акций, преобразуем в словарь
        return cls.yahoo_api.get_balance_sheet(company).loc[['Ordinary Shares Number']].to_dict(orient='records')[0]

    @classmethod
    def get_share_current_price(cls, company) -> float:
        # текущая цена акций
        return cls.yahoo_api.get_info(company)['currentPrice']

    @classmethod
    @convert_time_stamp
    def get_stockholders_equity(cls, company: str) -> dict[str, Optional[float]]:
        # собственный капитал
        return cls.yahoo_api.get_balance_sheet(company).loc[['Stockholders Equity']].to_dict(orient='records')[0]

    @classmethod
    @convert_time_stamp
    def get_company_dept(cls, company: str) -> dict[str, Optional[float]]:
        # общие долги
        return cls.yahoo_api.get_balance_sheet(company).loc[['Total Debt']].to_dict(orient='records')[0]

    @classmethod
    @convert_time_stamp
    def get_equivalents_and_short_term_investment(cls, company: str) -> dict[str, Optional[float]]:
        #  Денежные Средства, Их Эквиваленты и Краткосрочные Инвестиции
        return \
            cls.yahoo_api.get_balance_sheet(company).loc[['Cash Cash Equivalents And Short Term Investments']].to_dict(
                orient='records')[0]

    @classmethod
    @convert_time_stamp
    def get_accounts_receivable(cls, company) -> dict[str, Optional[float]]:
        #  дебиторская задолженность
        return cls.yahoo_api.get_balance_sheet(company).loc[['Accounts Receivable']].to_dict(orient='records')[0]

    @classmethod
    @convert_time_stamp
    def get_current_liabilities(cls, company: str) -> dict[str, Optional[float]]:
        #  Текущие обязательства
        return cls.yahoo_api.get_balance_sheet(company).loc[['Current Liabilities']].to_dict(orient='records')[0]


if __name__ == "__main__":
    service  = FinanceService()
    print(service.get_stockholders_equity("AAPL"))