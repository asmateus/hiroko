from collections import namedtuple
import numpy as np
import random
import argparse
import csv
import sys
import os


DATA_PTH = os.path.dirname(os.path.abspath(__file__)).split('hiroko')[0] + 'hiroko/data/'
Node = namedtuple('Node', ['neighborhood', 'gis', 'clients', 'day'])


def csvRead(file='', delimiter=';'):
    with open(DATA_PTH + file, newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=delimiter)
        return list(csv_data)[1:]


def loadLittleInfo(csv_reader_out):
    clients = [int(data_point[2]) for data_point in csv_reader_out]
    little_info = np.array(clients)
    return little_info


def loadBigInfo(csv_reader_out):
    neighborhoods_data = list()
    for data_point in csv_reader_out:
        neighborhoods_data.append(Node(
            neighborhood=data_point[0],
            gis=data_point[1],
            clients=data_point[2],
            day=data_point[3]
        ))

    return neighborhoods_data


def generateRandomGenomePopulation(genome_alloc, clients):
    clients_cnt = list(range(len(clients)))
    for i in range(100):
        random.shuffle(clients_cnt)

    genome = [0] * len(genome_alloc)
    acum = 0
    for i in range(len(genome_alloc)):
        acum += genome_alloc[i]
        genome[i] = clients_cnt[acum - genome_alloc[i]:acum]
    return genome


def calculateStandardDeviation(population, cli_little_info):
    total_revisions = [sum(cli_little_info[i] for i in j) for j in population]
    print(total_revisions)
    return np.std(total_revisions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help='Days to distribute the revisions.')

    # Validate day number
    days = parser.parse_args().d
    try:
        days = int(days)
        if days < 10 or days > 20:
            raise Exception
    except Exception:
        print('Day number must be an integer between 10 and 20, inclusive.')
        sys.exit(1)

    # Read neighborhood data (only clients)
    cc = csvRead('neighborhood_description.csv')
    clients = loadLittleInfo(cc)

    # Read full neighborhood data
    neighborhoods_data = loadBigInfo(cc)

    # Days distribution
    d_distribution = len(clients) // days
    d_overhead = len(clients) - d_distribution * days

    # Genoma allocator
    genoma_alloc = [d_distribution] * days
    for i in range(d_overhead):
        genoma_alloc[i] += 1

    # Produce random genome
    for i in range(100):
        population = generateRandomGenomePopulation(genoma_alloc, clients)
        print(calculateStandardDeviation(population, clients))
