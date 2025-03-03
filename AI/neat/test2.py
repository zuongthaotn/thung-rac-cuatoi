import os
import pickle
import neat
# import visualize

# 2-input XOR inputs and expected outputs.
# xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
# xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]


import numpy as np
import random

X_1 = []
y_1 = []
for x in range(100):
    t1 = random.randint(1, 999)
    t2 = random.randint(1, 999)
    X_1.append((t1, t2))
    if (t1 + t2) % 3 == 0:
        y_1.append((1,))
    else:
        y_1.append((0,))
X_train = X_1
y_train = y_1

X_2 = []
y_2 = []
for x in range(10):
    t1 = random.randint(111, 333)
    t2 = random.randint(111, 222)
    X_2.append((t1, t2))
    if (t1 + t2) % 3 == 0:
        y_2.append((1,))
    else:
        y_2.append((0,))
X_test = X_2
y_test = y_2



def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(X_train, y_train):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0]) ** 2




def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    if os.path.isfile(trainner):
        # load the winner
        with open(trainner, 'rb') as f:
            winner = pickle.load(f)
    else:
        # Run for up to 300 generations.
        winner = p.run(eval_genomes, 300)
        with open(trainner, 'wb') as f:
            pickle.dump(winner, f)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(X_test, y_test):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-299')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'test1_config')
    trainner = os.path.join(local_dir, 'test2.pkl')
    run(config_path)
