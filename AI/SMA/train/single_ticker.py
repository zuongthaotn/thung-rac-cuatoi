import neat
import os
import pickle

import time
import datetime

import AI.SMA.sources.constants as constants
from AI.SMA.sources.broker import Broker
import vn_realtime_stock_data.stockHistory as stockHistory
import method.SMA.v3 as v3

def training(genomes, config):
    # We have x number of genomes. X is specified in the configuration file
    # for ever genome we will create one object of Broker class, this object will simulate behaviour of the person
    # which buys and sells stocks
    # Also for each genome we create a neural network
    brokers = []
    nets = []
    ge = []
    # Creating individual data for every object in this generation
    for _, genome in genomes:
        broker = Broker(constants.STARTING_CAPITAL)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        brokers.append(broker)
        nets.append(net)
        ge.append(genome)

    # starting simulation, from 20 because we need to omit all the zeroes that appears during calculating MACD
    alive_brokers = brokers
    alive_ge = ge
    alive_nets = nets
    for i in range(23, rows_number):
        today_price = prepared_data['Close'][i]
        yesterday_price = prepared_data['Close'][i-1]
        brokers = alive_brokers
        alive_brokers = []
        ge = alive_ge
        alive_ge = []
        nets = alive_nets
        alive_nets = []
        for j in range(0, len(brokers)):
            # Give 1 point reward for each broker still alive
            ge[j].fitness += 1

            if brokers[j].number_of_stocks:
                # Increase fitness when broker sold stock with profit
                # Decrease fitness when broker sold stock with loss
                difference = brokers[j].number_of_stocks * (today_price - yesterday_price)
                ge[j].fitness = ge[j].fitness + difference

            # decision can be a real number form 0 to 1
            decision = nets[j].activate((smaR[i-2], smaR[i-1], smaR[i]))

            brokers[j].do_action(decision, today_price, prepared_data.index[i])
            if not brokers[j].is_alive:
                ge[j].fitness -= 100000
            else:
                alive_brokers.append(brokers[j])
                alive_ge.append(ge[j])
                alive_nets.append(nets[j])


    # if len(alive_brokers) > 0:
    #     the_best_broker = 0
    #     equity_peak = 0
    #     for k in range(0, len(alive_brokers)):
    #         if alive_brokers[k].capital > equity_peak:
    #             equity_peak = alive_brokers[k].capital
    #             the_best_broker = k
    #
    #     the_best_gen = 0
    #     fitness_peak = 0
    #     for f in range(0, len(alive_ge)):
    #         if alive_ge[f].fitness > fitness_peak:
    #             fitness_peak = alive_ge[f].fitness
    #             the_best_gen = f
    #
    #     print("The best broker ID: {}" . format(the_best_broker))
    #     print("The best fitness: {}" . format(fitness_peak))
    #     print("The best genome ID: {}" . format(the_best_gen))
    #
    #     print(alive_brokers[the_best_broker].capital)
    #     print(alive_brokers[the_best_broker].history)


def run(config_path):
    # creating configuration basing on our configuration file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # creating population basing on our configuration
    population = neat.Population(config)

    # creating reporter that will print crucial data in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # saving the best genome after completing the training
    # winner = population.run(training, constants.NUMBER_OF_GENERATIONS)
    winner = population.run(training, 10)


    # statistics of the best genome
    print('\nBest genome:\n{!s}'.format(winner))

    # save the best genome to a file
    save_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME, "best_" + ticker)
    with open(save_path, 'wb') as fp:
        pickle.dump(winner, fp)


def main():
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    run(config_path)


if __name__ == '__main__':
    ticker = "MBB"
    # getting data for this generation
    date_to = "31/12/2022"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    prepared_data = v3.prepareData(htd)
    smaR = prepared_data['SMA_R']
    rows_number = len(prepared_data.index)
    main()