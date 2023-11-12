import requests

class MutualFundProfitCalculator:
    @staticmethod
    def get_nav(scheme_code, date):
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: Request failed - {e}")
            return None

        nav = None

        for entry in data['data']:
            if entry['date'] >= date:
                try:
                    nav = float(entry['nav'])
                except ValueError:
                    print("Error: Invalid NAV value")
                    return None
                break

        return nav

    @staticmethod
    def calculate_profit(scheme_code, start_date, end_date, capital=1000000.0):
        start_nav = MutualFundProfitCalculator.get_nav(scheme_code, start_date)
        end_nav = MutualFundProfitCalculator.get_nav(scheme_code, end_date)

        if start_nav is None or end_nav is None:
            return None

        capital = float(capital)
        units_allotted = capital / start_nav
        value_on_redemption_date = units_allotted * end_nav
        net_profit = value_on_redemption_date - capital

        return net_profit

