import pickle
import os
import neat

import sys
from pathlib import Path

ALGO_PATH = os.path.abspath(Path(__file__).parent.parent.parent.parent)
if ALGO_PATH not in sys.path:
    sys.path.insert(1, ALGO_PATH)
import AI.VN30ps.neat.sources.constants as constants

ticker = ''
net = None
is_debug_mode = False

def set_ticker(new_value):
    global ticker
    ticker = new_value

def reset_network():
    global net
    net = None

def set_is_debug_mode(new_value):
    global is_debug_mode
    is_debug_mode = new_value

def get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today):
    if not ticker:
        print("No ticker selected.")
        exit()
    global net
    if not net:
        config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
        # creating configuration basing on our configuration file
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME,
                                        ticker + constants.GENOME_BRAIN_POSTFIX)

        if config.genome_config.activation_default != constants.ACTIVATION_FUNCS:
            print("Check the activation functions again, they are unsync.")
            exit()

        # load best genome
        try:
            with open(best_genome_path, 'rb') as fp:
                best_genome = pickle.load(fp)
        except FileNotFoundError:
            print('You need to train a network first')
            return
        if is_debug_mode:
            print("Getting best genome/brain from file: \n {}".format(best_genome_path))
        net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    return net.activate((emaR_2, emaR_yesterday, emaR_today, rsi_today))

def is_trained():
    if not ticker:
        print("No ticker selected.")
        exit()
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME,
                                    ticker + constants.GENOME_BRAIN_POSTFIX)
    return os.path.isfile(best_genome_path)