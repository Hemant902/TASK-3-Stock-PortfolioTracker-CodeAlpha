import requests

API_KEY = 'YOUR_API_KEY'

def fetch_stock_quote(ticker):
    api_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(api_url)
    stock_info = response.json()
    return stock_info.get("Global Quote", None)

class InvestmentPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_investment(self, ticker, shares):
        if ticker in self.portfolio:
            self.portfolio[ticker] += shares
        else:
            self.portfolio[ticker] = shares

    def remove_investment(self, ticker, shares):
        if ticker in self.portfolio:
            self.portfolio[ticker] -= shares
            if self.portfolio[ticker] <= 0:
                del self.portfolio[ticker]

    def calculate_total_value(self):
        total = 0
        for ticker, shares in self.portfolio.items():
            stock_info = fetch_stock_quote(ticker)
            if stock_info:
                stock_price = float(stock_info['05. price'])
                total += stock_price * shares
        return total

def calculate_profit_or_loss(initial_value, current_value):
    return current_value - initial_value

def evaluate_diversification(portfolio):
    distribution = {}
    total_value = portfolio.calculate_total_value()
    for ticker, shares in portfolio.portfolio.items():
        stock_info = fetch_stock_quote(ticker)
        if stock_info:
            sector = stock_info.get('08. currency', ticker)
            if sector in distribution:
                distribution[sector] += shares * float(stock_info['05. price'])
            else:
                distribution[sector] = shares * float(stock_info['05. price'])
    return {sector: (value / total_value) * 100 for sector, value in distribution.items()}

def portfolio_manager():
    portfolio = InvestmentPortfolio()
    initial_investment = None

    while True:
        print("1. Add a stock to your portfolio")
        print("2. Remove a stock from your portfolio")
        print("3. View the total portfolio value")
        print("4. Exit the portfolio manager")

        selection = input("Choose an option: ")

        if selection == '1':
            ticker = input("Enter the stock ticker symbol: ")
            shares = int(input("Enter the number of shares: "))
            portfolio.add_investment(ticker, shares)
        elif selection == '2':
            ticker = input("Enter the stock ticker symbol: ")
            shares = int(input("Enter the number of shares to remove: "))
            portfolio.remove_investment(ticker, shares)
        elif selection == '3':
            current_value = portfolio.calculate_total_value()
            if initial_investment is None:
                initial_investment = current_value
            print(f"Current Portfolio Value: ${current_value:.2f}")
            print(f"Total Profit/Loss: ${calculate_profit_or_loss(initial_investment, current_value):.2f}")
            print("Portfolio Diversification Breakdown:")
            for sector, percentage in evaluate_diversification(portfolio).items():
                print(f"{sector}: {percentage:.2f}%")
        elif selection == '4':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    portfolio_manager()
