import robin_stocks.robinhood as r
import getpass
import importlib
import subprocess

from prettytable import PrettyTable


# comment this function call after first ever run of this script
def checkInstallPackages():
    # List of required packages
    packages = ['prettytable', 'getpass', 'robin_stocks']

    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"{package} is not installed. Installing...")
            subprocess.check_call(['pip', 'install', package])
            print(f"{package} has been successfully installed.")


def getUserPassword():
    try:
        return getpass.getpass(prompt='Enter your password: ')
    except Exception as e:
        print(f"Error: {e}")
        return None


def getStockDetails():
    checkInstallPackages()
    userName = input("Enter your username: ")
    password = getUserPassword()

    # Log in to Robinhood
    r.login(userName, password)

    # Get a list of your positions
    print('Querying Robinhood...')
    positions = r.account.build_holdings()

    # Create a PrettyTable instance and add columns
    table = PrettyTable()
    table.field_names = ['Name', 'Symbol', 'Average Buy Price', 'Price', 'Total Buy', 'Equity', 'Gain', 'Gain %']
    table.sortby = 'Gain'
    table.reversesort = True

    # Add data to the table
    netBuy = 0
    netEquity = 0
    netGain = 0
    totalGain = 0
    totalLoss = 0
    for symbol in positions.keys():
        buyPrice = round(float(positions[symbol]['average_buy_price']) * float(positions[symbol]['quantity']), 2)
        gain = round(float(positions[symbol]['equity_change']), 2)
        gainPercentage = round(((gain / buyPrice) * 100), 2)
        equity = round(float(positions[symbol]['equity']), 2)
        row_data = [positions[symbol]['name'],
                    symbol,
                    round(float(positions[symbol]['average_buy_price']), 2),
                    round(float(positions[symbol]['price']), 2),
                    buyPrice,
                    equity,
                    gain,
                    gainPercentage]
        table.add_row(row_data)
        netBuy += buyPrice
        netEquity += equity
        netGain += gain
        if gain < 0:
            totalLoss += gain
        else:
            totalGain += gain

    print('\nPositions Summary')
    print(str(table))

    table = PrettyTable()
    table.field_names = ['Net Buy', 'Net Equity', 'Total Gain', 'Total Loss', 'Net Gain', 'Net Gain %']
    netGainPercentage = round(((netGain / netBuy) * 100), 2)
    table.add_row([netBuy, netEquity, totalGain, totalLoss, round(netGain, 2), netGainPercentage])

    print('\nPortfolio Summary')
    print(str(table))


if __name__ == "__main__":
    getStockDetails()
