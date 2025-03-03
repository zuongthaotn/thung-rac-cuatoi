import warnings
warnings.filterwarnings('ignore')

import AI.VN30ps.neat.sources.trainer as trainer

if __name__ == '__main__':
    ticker = "VN30F1M"
    trainer.run(ticker)