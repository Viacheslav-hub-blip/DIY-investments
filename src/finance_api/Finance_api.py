from datetime import datetime, timedelta
import yfinance as yf
from pandas import DataFrame


class YahooApi:
    @staticmethod
    def get_history_share_price_per_period(company: str, period: str, interval: str) -> DataFrame:
        """
         Возвращает дату и цену акции за определенный период в виде DataFrame
        """
        history = yf.Ticker(company).history(period=period, interval=interval)
        return history

    @staticmethod
    def get_price_per_start_end_period(company: str, start: str, end: str, interval: str) -> DataFrame:
        """
        Возвращает дату и цену акции за определенный период в пределах start, end в виде DataFrame. Если котировки
        на дату отсутствуют, то возвращает котировки ближайшей даты
        в последующие 4 дня
        """
        price: DataFrame = yf.Ticker(company).history(interval=interval, start=start, end=end)

        if len(price) != 0:
            return price
        else:
            return yf.Ticker(company).history(interval=interval, start=start,
                                              end=(datetime.strptime(start, '%Y-%m-%d') + timedelta(days=5)).strftime(
                                                  '%Y-%m-%d')).head(1)

    @staticmethod
    def get_recommendations_summary(company: str) -> DataFrame:
        recom = yf.Ticker(company).get_recommendations_summary()
        return recom

    @staticmethod
    def get_info(company: str) -> dict:
        """
        Возвращает словаь, содержащий всю информацию о компании
        """
        info = yf.Ticker(company).info
        return info

    @staticmethod
    def get_balance_sheet(company: str) -> DataFrame:
        """
        Возвращает баланс компании в виде DataFrame за доступные годы
        """
        return yf.Ticker(company).balance_sheet

    @staticmethod
    def get_income_stmt(company: str) -> DataFrame:
        """
        Вовзвращает показатели вырчуки в виде DataFrame за дсотупные годы
        """
        return yf.Ticker(company).income_stmt