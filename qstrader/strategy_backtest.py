# @Author: Chen yunsheng(Leo YS CHen)
# @Location: Taiwan
# @E-mail:leoyenschen@gmail.com
# @Date:   2017-02-14 00:11:27
# @Last Modified by:   Chen yunsheng

import click

from qstrader import settings
from qstrader.compat import queue
from qstrader.price_parser import PriceParser
from qstrader.price_handler.sqlite_daily_bar import SqliteDBBarPriceHandler
from qstrader.strategy import Strategies, DisplayStrategy
from qstrader.risk_manager.example import ExampleRiskManager
from qstrader.portfolio_handler import PortfolioHandler
from qstrader.compliance.example import ExampleCompliance
from qstrader.execution_handler.ib_simulated import IBSimulatedExecutionHandler
#from qstrader.statistics.simple import SimpleStatistics
from qstrader.statistics.tearsheet import TearsheetStatistics
from qstrader.trading_session.backtest import Backtest
#====================================================
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,dir)
print("parentdir")
print(parentdir)
print("dir")
print(dir)
from custom_strategy import CustomStrategy
from custom_position import CustomPositionSizer

def run(config, testing, tickers, filename, start_date, end_date):

    # Set up variables needed for backtest
    events_queue = queue.Queue()
    csv_dir = config.CSV_DATA_DIR
    initial_equity = PriceParser.parse(500000.00)

    # Use Yahoo Daily Price Handler
    price_handler = SqliteDBBarPriceHandler(
        csv_dir, events_queue, tickers, start_date, end_date
    )

    # Use the Buy and Hold Strategy
    strategy = CustomStrategy(tickers, events_queue)
    strategy = Strategies(strategy, DisplayStrategy())

    # Use an example Position Sizer
    position_sizer = CustomPositionSizer()

    # Use an example Risk Manager
    risk_manager = ExampleRiskManager()

    # Use the default Portfolio Handler
    portfolio_handler = PortfolioHandler(
        initial_equity, events_queue, price_handler,
        position_sizer, risk_manager
    )

    # Use the ExampleCompliance component
    compliance = ExampleCompliance(config)

    # Use a simulated IB Execution Handler
    execution_handler = IBSimulatedExecutionHandler(
        events_queue, price_handler, compliance
    )

    # Use the default Statistics
    statistics = TearsheetStatistics(
        config, portfolio_handler, title=""
    )

    # Set up the backtest
    backtest = Backtest(
        price_handler, strategy,
        portfolio_handler, execution_handler,
        position_sizer, risk_manager,
        statistics, initial_equity
    )
    results = backtest.simulate_trading(testing=testing)
    statistics.save(filename)
    return results

"""
@click.command()
@click.option('--config', default=settings.DEFAULT_CONFIG_FILENAME, help='Config filename')
@click.option('--testing/--no-testing', default=False, help='Enable testing mode')
@click.option('--tickers', default='SP500TR', help='Tickers (use comma)')
@click.option('--filename', default='', help='Pickle (.pkl) statistics filename')
"""
def main(config, testing, tickers, filename, start_date=None, end_date=None):
    tickers = tickers.split(",")
    config = settings.from_file(config, testing)
    run(config, testing, tickers, filename, start_date, end_date)


if __name__ == "__main__":
    tickers = sys.argv[1]
    print("sys.argv[2]")
    print(sys.argv[2])
    print("sys.argv[3]")
    print(sys.argv[3])
    main(settings.DEFAULT_CONFIG_FILENAME,False,tickers,'',sys.argv[2],sys.argv[3])
