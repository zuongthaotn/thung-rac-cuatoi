from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
ALGO_DIR = Path(__file__).parent.parent.parent.parent

PATH_NEAT_BEST_GENOME = 'genomes'
PATH_NEAT_CONF = 'resources/config-feedforward'
GENOME_BRAIN_POSTFIX = '_ema_brain'

ACTIVATION_FUNCS = 'hat'
BUY_SIGNAL_LINE = 0.9
SELL_SIGNAL_LINE = 0.1

STARTING_CAPITAL = 1000
CSV_OPEN_COLUMN = 'Open'
CSV_CLOSE_COLUMN = 'Open'
CSV_DATE_COLUMN = 'Date'
NUMBER_OF_GENERATIONS = 100

TEST_FROM_DATE = "01/01/2022"
TEST_TO_DATE = "31/12/2023"