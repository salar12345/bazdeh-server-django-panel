class HomePageInstrument():
    def __init__(self, category, name, current_price, date_time, logo_url, prev_price):
        super().__init__()
        self.category = category
        self.name = name
        self.current_price = current_price
        self.date_time = date_time
        self.logo_url = logo_url
        self.prev_price = prev_price