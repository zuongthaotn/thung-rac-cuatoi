from multiprocessing import Pool

import vn_realtime_stock_data.stockRealtimes as stockRealtime
import AI.EMA.sources.trainer as trainer

if __name__ == '__main__':
    vn100 = stockRealtime.get_vn100_tickers()
    with Pool(10) as pool:
        # perform calculations by multi CPU
        results = pool.map(trainer.run, vn100)
