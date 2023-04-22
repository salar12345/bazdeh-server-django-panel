class HomePageHomePrice():
    def __init__(self, category, name, current_price, month, year, logo_url, prev_price):
        super().__init__()
        self.category = category
        self.name = name
        self.current_price = current_price
        self.month = month
        self.year = year
        self.logo_url = logo_url
        self.prev_price = prev_price
