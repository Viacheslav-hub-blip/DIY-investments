from concurrent.futures import ProcessPoolExecutor

import yfinance as yf
from datetime import datetime


def get_history(company: str, period: str, interval: str):
    history = yf.Ticker(company).history(period=period, interval=interval)
    return history


def get_recommendations_summary(company: str):
    recom = yf.Ticker(company).get_recommendations_summary()
    return recom


def get_info(company: str):
    info = yf.Ticker(company).info
    return info


def get_balance_sheet(company: str):
    return yf.Ticker(company).balance_sheet


def get_income_stmt(company: str):
    return yf.Ticker(company).income_stmt

if __name__ == "__main__":
    companies = [
        'GOOG',
        'AAPL',
        'MSFT',
        'NVDA',
        'META',
        'TSLA',
        'AMZN'
    ]

    t1 = datetime.now()
    for company in companies:
        print(get_info(company))
        print(get_recommendations_summary(company))
        print(get_balance_sheet(company))
        print(get_income_stmt(company))

    t2 = datetime.now()
    print(t2 - t1)
    print('-----------------------------------------')

    t1 = datetime.now()
    executor = ProcessPoolExecutor(max_workers=4)
    for company in executor.map(get_info, companies):
        print(company)
    for company in executor.map(get_balance_sheet, companies):
        print(company)
    for company in executor.map(get_income_stmt, companies):
        print(company)
    for company in executor.map(get_recommendations_summary, companies):
        print(company)

    t2  = datetime.now()
    print(t2-t1)

    print('-----------------------------------------')

    t1 = datetime.now()
    executor = ProcessPoolExecutor()
    for company in companies:
        p1 = executor.submit(get_info, company)
        p2 = executor.submit(get_history, company, '10y', '1d')
        p3 = executor.submit(get_recommendations_summary, company)
        p4 = executor.submit(get_income_stmt, company)
        p5 = executor.submit(get_balance_sheet, company)

        r1  = p1.result()
        r2  = p2.result()
        r3  = p3.result()
        r4  = p4.result()
        r5  = p5.result()

        print(r1, r2, r3, r4, r5)

    t2 = datetime.now()
    print(t2 - t1)

