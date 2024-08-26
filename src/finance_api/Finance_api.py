import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

from pandas import Timestamp


class YahooApi():
    def get_history(self, company: str, period: str, interval: str):
        '''

        :param company:тикер компании
        :param period:период
        :param interval:
        :return:
        '''
        history = yf.Ticker(company).history(period=period, interval=interval)
        return history

    def get_price_in_year(self, company, start, end, interval):
        return yf.Ticker(company).history(interval=interval, start=start, end=end)

    def get_recommendations_summary(self, company: str):
        recom = yf.Ticker(company).get_recommendations_summary()
        return recom

    def get_info(self, company: str):
        info = yf.Ticker(company).info
        return info

    def get_balance_sheet(self, company: str):
        return yf.Ticker(company).balance_sheet

    def get_income_stmt(self, company: str):
        return yf.Ticker(company).income_stmt


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
    yahoo_api = YahooApi()
    sectors = {}

    for c in companies:
        sector = yahoo_api.get_info(c)['sector']
        if sector in sectors.keys():
            sectors[sector] += ' '+ c
        else:
            sectors[sector] = c

    print(sectors)

    # data = yahoo_api.get_history('goog', '1mo', '1d')
    # data_l = yahoo_api.get_history('goog', '5y', '5d')
    # print()
    # #print(data_l)
    # print()
    # data_2 = data[['Close']]
    # data_2 = data_2.reset_index()
    # # print(data[['Close']])
    # data_price_history = {}
    # for index, row in data_2.iterrows():
    #     #print(row['Date'], row['Close'])
    #     date_  = row['Date']
    #     date_format  = date_.to_pydatetime().date()
    #     str_date  = date_format.strftime('%d.%m.%Y')
    #     #print(str_date)
    #     data_price_history[str_date] = round(row['Close'], 3)
    # #print('data price', data_price_history)
    #
    # #print(data['Close'].iloc[0], data['Close'].iloc[-1])
    # recom = yahoo_api.get_recommendations_summary('goog')
    # #print(recom.head().iloc[0])
    #
    # google = yf.Ticker('goog')
    #
    # df  = google.balance_sheet
    # print(google.balance_sheet[['2023-12-31 00:00:00']].to_markdown())
    # df2 = df[df.columns[~df.columns.isin(['2023-12-31 00:00:00', '2022-12-31 00:00:00', '2021-12-31 00:00:00', '2020-12-31 00:00:00', '2019-12-31 00:00:00'])]]
    # print()
    # print(df2.to_markdown())
    #
    # print()
    # df  = google.income_stmt
    # df2 = df[df.columns[~df.columns.isin(
    #     ['2023-12-31 00:00:00', '2022-12-31 00:00:00', '2021-12-31 00:00:00', '2020-12-31 00:00:00',
    #      '2019-12-31 00:00:00'])]]
    # print(google.income_stmt[['2023-12-31 00:00:00']].to_markdown())
    # print()
    # print(df2.to_markdown())
    #
    #
    # history = google.info['longBusinessSummary']
    # industry = google.info['industry']
    # #print(history)
    # #print(industry)
    #
    # recom = google.info['recommendationKey']
    # marketcap = google.info['marketCap']

    google = yf.Ticker('MSFT')
    #print(google.info)
    # print(yahoo_api.get_price_in_year('NVDA', start='2022-01-28', end='2022-01-30', interval='1d'))

    print()
    table = google.balance_sheet
    table_2 = google.income_stmt
    table_2.index.name = 'new_name'

    # print(table_2.loc[table_2.index['Net Income']])

    print(table_2.loc[['Net Income']].to_dict(orient='records')[0])
    # print(table_2[table_2['new_name'] == 'Net Income'].index)
    # print(table_2.to_markdown())
    print()
    print(google.dividends)
    # google_net_income = table_2[23:24].to_dict(orient='records')[0]
    # print('income', google_net_income)
    #
    # print()
    #
    # google_shares_number = table[1:2].to_dict(orient='records')[0]
    # print('shares', google_shares_number)
    #
    # print()
    #
    # current_share_price = google.info['currentPrice']
    # print(current_share_price)
    #
    # # google_PE = current_share_price / (google_net_income[Timestamp('2023-12-31 00:00:00')] / google_shares_number[
    # #     Timestamp('2023-12-31 00:00:00')])
    # # print('PE', google_PE, google_net_income[Timestamp('2023-12-31 00:00:00')],
    # #       google_shares_number[Timestamp('2023-12-31 00:00:00')])
    #
    # print()
    #
    # google_marketcap = google.info['marketCap']
    # print('marketcap', google_marketcap)
    #
    # google_Stockholders_Equity = table[12:13].to_dict(orient='records')[0]
    # print('google_Stockholders_Equity', google_Stockholders_Equity)
    #
    # google_PB = google_marketcap / google_Stockholders_Equity[Timestamp('2023-12-31 00:00:00')]
    # print('PB', google_PB)
    #
    # google_ROE = google_net_income[Timestamp('2023-12-31 00:00:00')] / google_Stockholders_Equity[
    #     Timestamp('2023-12-31 00:00:00')]
    # print('roe', google_ROE)
    #
    # google_Dept = table[3:4].to_dict(orient='records')[0]
    # print('dept', google_Dept)
    # google_Dept_Eq = google_Dept[Timestamp('2023-12-31 00:00:00')] / google_Stockholders_Equity[
    #     Timestamp('2023-12-31 00:00:00')]
    # print('dept eq', google_Dept_Eq)
    #
    # google_EPS = google_net_income[Timestamp('2023-12-31 00:00:00')] / google_shares_number[
    #     Timestamp('2023-12-31 00:00:00')]
    # print('eps', google_EPS)
    #
    # google_Equivalents_And_Short_Term_Investment = table[71:72].to_dict(orient='records')[0]
    # print('cash', google_Equivalents_And_Short_Term_Investment)
    #
    # google_Accounts_Receivable = table[68:69].to_dict(orient='records')[0]
    # print('receivable', google_Accounts_Receivable)
    #
    # google_Current_Liabilities = table[29:30].to_dict(orient='records')[0]
    # print('lia', google_Current_Liabilities)
    #
    # google_quick_ratio = (google_Equivalents_And_Short_Term_Investment[Timestamp('2023-12-31 00:00:00')] +
    #                       google_Accounts_Receivable[Timestamp('2023-12-31 00:00:00')]) / google_Current_Liabilities[
    #                          Timestamp('2023-12-31 00:00:00')]
    # print('quick', google_quick_ratio)
    #
    # print()
    # print(table[3:4].to_dict(orient='records'))
    # print(table.to_markdown())
    # print(table_2.to_markdown())
