import cloudscraper
import datetime


class BaseHistoricData:
    def __init__(self, datasource_id, referer, start_date=None, end_date=None):
        self.datasource_id = datasource_id
        self.referer = referer
        self.start_date = start_date or "2020-24-03"
        self.end_date = end_date or datetime.date.today().strftime("%Y-%m-%d")
        self.historical_data = self.scrape_data()

    def scrape_data(self) -> dict[int, dict]:
        url = f"https://www.lme.com/api/trading-data/chart-data?datasourceId={self.datasource_id}&startDate={self.start_date}&endDate={self.end_date}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Referer": self.referer,
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.lme.com",
            "X-Requested-With": "XMLHttpRequest",
        }

        scraper = cloudscraper.create_scraper()

        try:
            response = scraper.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                historic_dates = data["Labels"]

                cash_bid = data["Datasets"][0]['Data']
                cash_offer = data["Datasets"][1]['Data']
                month_bid = data["Datasets"][2]['Data']
                month_offer = data["Datasets"][3]['Data']

                # разбил данные и даты попарно в словари
                data_cash_bid = {label: value for label, value in zip(historic_dates, cash_bid)}
                data_cash_offer = {label: value for label, value in zip(historic_dates, cash_offer)}
                data_month_bid = {label: value for label, value in zip(historic_dates, month_bid)}
                data_month_offer = {label: value for label, value in zip(historic_dates, month_offer)}

                historical_data = {
                    0: data_cash_bid,
                    1: data_cash_offer,
                    2: data_month_bid,
                    3: data_month_offer
                }

                return historical_data
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return {}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}


class AluminiumHistoricData(BaseHistoricData):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(
            datasource_id="dddbc815-1a81-4f35-beed-6a193f4c946a",
            referer="https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium#Price+graphs",
            start_date=start_date,
            end_date=end_date
        )


class CopperHistoricData(BaseHistoricData):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(
            datasource_id="39fabad0-95ca-491b-a733-bcef31818b16",
            referer="https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Price+graphs",
            start_date=start_date,
            end_date=end_date
        )


class NickelHistoricData(BaseHistoricData):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(
            datasource_id="0ab0e715-84cd-41d1-8318-a96070917a43",
            referer="https://www.lme.com/en/Metals/Non-ferrous/LME-Nickel#Price+graphs",
            start_date=start_date,
            end_date=end_date
        )


class ZincHistoricData(BaseHistoricData):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(
            datasource_id="1a1aca59-3032-4ea6-b22b-18b151514b84",
            referer="https://www.lme.com/en/Metals/Non-ferrous/LME-Zinc#Price+graphs",
            start_date=start_date,
            end_date=end_date
        )


class TinHistoricData(BaseHistoricData):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(
            datasource_id="707be4f9-a4f5-4fe3-8f5b-7bd2886f58e7",
            referer="https://www.lme.com/en/Metals/Non-ferrous/LME-Tin#Price+graphs",
            start_date=start_date,
            end_date=end_date
        )


class LeadHistoricData(BaseHistoricData):
    def __init__(self, start_date=None, end_date=None):
        super().__init__(
            datasource_id="9f2cf5c9-855d-4f68-939a-387babebe11f",
            referer="https://www.lme.com/en/Metals/Non-ferrous/LME-Lead#Price+graphs",
            start_date=start_date,
            end_date=end_date
        )

# begin_date = "2024-10-22"
# finish_date = "2024-12-22"

# Пример использования
# aluminium_data = AluminiumHistoricData(start_date=start_date, end_date=end_date)
# copper_data = CopperHistoricData(start_date=start_date, end_date=end_date)
# nickel_data = NickelHistoricData(start_date=begin_date, end_date=finish_date)
# zinc_data = ZincHistoricData(start_date=start_date, end_date=end_date)
# tin_data = TinHistoricData(start_date=start_date, end_date=end_date)
# lead_data = LeadHistoricData(start_date=start_date, end_date=end_date)

# print(next(reversed(aluminium_data.historical_data.get(0).items())))
# print(aluminium_data.historical_data.get(0).items())
#
# print(next(reversed(copper_data.historical_data.get(0).items())))
# print(copper_data.historical_data.get(0).items())
#
# print(next(reversed(nickel_data.historical_data.get(0).items())))
# print(nickel_data.historical_data.get(0).items())
#
# print(next(reversed(zinc_data.historical_data.get(0).items())))
# print(zinc_data.historical_data.get(0).items())
#
# print(next(reversed(tin_data.historical_data.get(0).items())))
# print(tin_data.historical_data.get(0).items())
#
# print(next(reversed(lead_data.historical_data.get(0).items())))
# print(lead_data.historical_data.get(0).items())
