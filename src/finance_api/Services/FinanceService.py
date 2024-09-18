from src.finance_api.Finance_api import YahooApi
from typing import NamedTuple


class RecomendationsOnMonth(NamedTuple):
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


class FinanceService:
    def __init__(self):
        self.yahoo_api = YahooApi()

    def get_history_close(self, company: str, period: str, interval: str):
        close_history = self.yahoo_api.get_history(company, period, interval)['Close']
        return close_history

    def get_info(self, company: str) -> dict:
        return self.yahoo_api.get_info(company)

    def get_history_in_year(self, company, start, end, interval):
        return self.yahoo_api.get_price_in_year(company, start, end, interval)['Close']

    def get_history_close_with_date(self, company: str, period: str, interval: str) -> {}:
        close_history = self.yahoo_api.get_history(company, period, interval)
        data_2 = close_history[['Close']].reset_index()
        data_price_history = {}
        for index, row in data_2.iterrows():
            date_ = row['Date']
            date_format = date_.to_pydatetime().date()
            str_date = date_format.strftime('%d.%m.%Y')
            data_price_history[str_date] = round(row['Close'], 3)
        return data_price_history

    def get_company_description(self, company: str) -> str:
        return self.yahoo_api.get_info(company)['longBusinessSummary']

    def get_company_sector(self, company: str) -> str:
        return self.yahoo_api.get_info(company)['sector']

    def get_price_information(self, company: str) -> PriceInform:
        currentPrice = self.yahoo_api.get_info(company)['currentPrice']
        targetHighPrice = self.yahoo_api.get_info(company)['targetHighPrice']
        targetLowPrice = self.yahoo_api.get_info(company)['targetLowPrice']
        targetMeanPrice = self.yahoo_api.get_info(company)['targetMeanPrice']
        return PriceInform(currentPrice, targetHighPrice, targetLowPrice, targetMeanPrice)

    def get_recommendations_summary_current_month(self, company: str) -> dict:
        recom_dict = self.yahoo_api.get_recommendations_summary(company).head().iloc[0]
        recom = {"strongBuy": int(recom_dict['strongBuy']), "buy": int(recom_dict['buy']),
                 "hold": int(recom_dict["hold"]),
                 "sell": int(recom_dict["sell"]), "strongSell": int(recom_dict["strongSell"])}
        return recom

    def get_marketcap(self, company: str) -> int:
        marketcap = self.yahoo_api.get_info(company)['marketCap']
        return marketcap

    def get_one_month_change(self, company) -> float:
        close_history = self.yahoo_api.get_history(company, '1mo', '1d')['Close']
        first = close_history.head().iloc[0]
        last = close_history.head().iloc[-1]
        change = round(((last - first) / first) * 100, 2)
        # print('first', first, 'last', last, 'change', change)
        return change

    def get_buy_recommendation(self, company: str) -> str:
        recom = self.yahoo_api.get_info(company)['recommendationKey']
        return recom

    def get_net_income(self, company: str):
        # чистая прибыль
        # Получаем таблицу, выбираем нужные строку, преобразуем в словарь
        return self.yahoo_api.get_income_stmt(company).loc[['Net Income']].to_dict(orient='records')[0]

    def get_shares_number(self, company: str):
        # количество акций
        # получаем строку с количеством акций, преобразуем в словарь
        return self.yahoo_api.get_balance_sheet(company).loc[['Ordinary Shares Number']].to_dict(orient='records')[0]

    def get_share_current_price(self, company):
        # текущая цена акций
        return self.yahoo_api.get_info(company)['currentPrice']

    def get_Stockholders_Equity(self, company: str):
        # собственный капитал
        return self.yahoo_api.get_balance_sheet(company).loc[['Stockholders Equity']].to_dict(orient='records')[0]

    def get_company_Dept(self, company: str):
        # общие долги
        return self.yahoo_api.get_balance_sheet(company).loc[['Total Debt']].to_dict(orient='records')[0]

    def get_Equivalents_And_Short_Term_Investment(self, company: str):
        #  Денежные Средства, Их Эквиваленты и Краткосрочные Инвестиции
        return \
            self.yahoo_api.get_balance_sheet(company).loc[['Cash Cash Equivalents And Short Term Investments']].to_dict(
                orient='records')[0]

    def get_Accounts_Receivable(self, company):
        #  дебиторская задолженность
        return self.yahoo_api.get_balance_sheet(company).loc[['Accounts Receivable']].to_dict(orient='records')[0]

    def get_Current_Liabilities(self, company: str):
        #  Текущие обязательства
        return self.yahoo_api.get_balance_sheet(company).loc[['Current Liabilities']].to_dict(orient='records')[0]




if __name__ == "__main__":
    service = FinanceService()

    company = 'goog'
    print(service.get_one_month_change(company))
    print(service.get_marketcap(company))
    print()
    print(service.get_history_close(company, '1mo', '1d'))

    print()
    print(service.get_recommendations_summary_current_month(company))
    print(service.get_net_income('goog'))
