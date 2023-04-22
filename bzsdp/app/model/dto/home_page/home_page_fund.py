class HomePageFund():
    def __init__(self, category, name, date_time, logo_url, profit_percent, issuance_price):
        super().__init__()
        self.category = category
        self.name = name
        self.date_time = date_time
        self.logo_url = logo_url
        self.profit_percent = profit_percent
        self.issuance_price = issuance_price