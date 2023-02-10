import matplotlib.pyplot as plt 
import pandas as pd 
import os 

from utility import pickle_object
from genetic_algorithm.population import Population
from root_logger import RootLogger

INTERATION_HEADER = 'iteration'
FITNESS_HEADER = 'fitness'
TIME_HEADER = 'time'

RIDERSHIP_HEADER = 'ridership_val'
NUM_ROUTES_HEADER = 'routes_val'
COVERAGE_HEADER = 'coverage_val'
RIDERSHIP_DENSITY_HEADER = 'ridership_density_val'

ALPHA_VALUE = 0.5
DOT_SIZE = 1
SINGLE_DOT_SIZE = 5

def graph_all_metrics(Population: Population, results_csv: str, output_folder: str= None):
    RootLogger.log_debug(f'Graphing all metrics for results file {results_csv} and exporting to {output_folder}...')
    if output_folder is None:
        output_folder = f'{Population.iteration_number-1}i{Population.population_size}p/'
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plot_per_round_metrics(results_csv, os.path.join(output_folder, 'fitness_trend.png'))
    plot_all_fitness_metrics(results_csv, os.path.join(output_folder, 'fitness_breakdown.png'))
    plot_time(results_csv, os.path.join(output_folder, 'time.png'))
    plot_stddev(results_csv, os.path.join(output_folder, 'stddev.png'))
    RootLogger.log_debug(f'Done graphing all metrics.')

    pickle_object(Population, os.path.join(output_folder, 'population.pkl'))


def get_header(base: str, add_on: str):
    return add_on + '_' + base

def plot_per_round_avg(filename, output_file='plot1.png'):
    RootLogger.log_debug(f'Graphing per round average for {filename}, exporting to {output_file}...')
    df = pd.read_csv(filename)
    plt.scatter(df[INTERATION_HEADER], df[get_header(FITNESS_HEADER, 'avg')], s= DOT_SIZE, alpha=ALPHA_VALUE)
    plt.xlabel("Iteration #")
    plt.ylabel("Fitness")
    plt.title("Avg. Fitness per Round")
    plt.savefig(output_file)
    plt.clf()
    RootLogger.log_debug(f'Done graphing per round averages.')

def plot_all_fitness_metrics(filename, output_file='fitness_plot.png'):
    RootLogger.log_debug(f'Graphing detailed fitness metrics for {filename}, exporting to {output_file}...')
    df = pd.read_csv(filename)
    x = df[INTERATION_HEADER]
    avg_overall = df[get_header(FITNESS_HEADER, 'avg')]
    ridership = df[get_header(RIDERSHIP_HEADER, 'avg')]
    num_routes = df[get_header(NUM_ROUTES_HEADER, 'avg')].apply(lambda x: abs(x))
    coverage = df[get_header(COVERAGE_HEADER, 'avg')]
    ridership_density = df[get_header(RIDERSHIP_DENSITY_HEADER, 'avg')]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(x, avg_overall, c='black', marker="o", s= DOT_SIZE, alpha=ALPHA_VALUE, label='overall')
    ax1.scatter(x, ridership, c='blue', marker="o", s=DOT_SIZE, alpha=ALPHA_VALUE, label='ridership')
    ax1.scatter(x, num_routes, c='green', marker="o", s=DOT_SIZE, alpha=ALPHA_VALUE, label='num_routes(-1)')
    ax1.scatter(x, coverage, c='red', marker="o", s=DOT_SIZE, alpha=ALPHA_VALUE, label='coverage')
    ax1.scatter(x, ridership_density, c='orange', s=DOT_SIZE, alpha=ALPHA_VALUE, marker="o", label='ridership_density')

    plt.legend(loc='upper left')
    plt.xlabel("Iteration #")
    plt.ylabel("Fitness")
    plt.title("Fitness Breakdown per Round")
    plt.savefig(output_file)
    plt.clf()
    RootLogger.log_debug(f'Done graphing detailed fitness metrics.')
    

def plot_per_round_metrics(filename, output_file='plot_comb.png'):
    RootLogger.log_debug(f'Graphing per round metrics for {filename}, exporting to {output_file}...')
    df = pd.read_csv(filename)
    x = df[INTERATION_HEADER]
    avg = df[get_header(FITNESS_HEADER, 'avg')]
    best = df[get_header(FITNESS_HEADER, 'best')]
    med = df[get_header(FITNESS_HEADER, 'med')]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.xlabel("Iteration #")
    plt.ylabel("Fitness")
    plt.title("Fitness Statistics per Round")
    ax1.scatter(x, best, c='b', marker="o", s= DOT_SIZE, alpha=ALPHA_VALUE, label='best')
    ax1.scatter(x, avg, c='r', marker="o", s= DOT_SIZE, alpha=ALPHA_VALUE, label='average')
    ax1.scatter(x, med, c='g', marker="o", s= DOT_SIZE, alpha=ALPHA_VALUE, label='med')
    plt.legend(loc='upper left')
    plt.savefig(output_file)
    plt.clf()
    RootLogger.log_debug(f'Done graphing per round metrics.')

def plot_stddev(filename, output_file='genetic_diversity.png'):
    RootLogger.log_debug(f'Graphing stddev plots for {filename}, exporting to {output_file}...')
    df = pd.read_csv(filename)
    x = df[INTERATION_HEADER]
    std_overall = df[get_header(FITNESS_HEADER, 'stddev')]
    plt.scatter(x, std_overall, s= SINGLE_DOT_SIZE, alpha=ALPHA_VALUE)
    plt.xlabel("Iteration #")
    plt.ylabel("Stdev")
    plt.title("Fitness Deviation per Round")
    plt.savefig(output_file)
    plt.clf()
    RootLogger.log_debug(f'Done graphing the stddev plots.')

def plot_time(filename, output_file='time.png'):
    RootLogger.log_debug(f'Graphing runtime per round metrics for {filename}, exporting to {output_file}...')
    plt.xlabel("Iteration #")
    plt.ylabel("Time to compute (s)")
    plt.title("Computation Time per Round")
    df = pd.read_csv(filename)
    plt.scatter(df[INTERATION_HEADER], df[TIME_HEADER], marker="o", s= SINGLE_DOT_SIZE, alpha=ALPHA_VALUE)
    plt.savefig(output_file)
    plt.clf()
    RootLogger.log_debug(f'Done graphing runtime per round metrics.')