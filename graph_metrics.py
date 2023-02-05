import matplotlib.pyplot as plt 
import pandas as pd 

INTERATION_HEADER = 'iteration'
FITNESS_HEADER = 'fitness'
TIME_HEADER = 'time'

RIDERSHIP_HEADER = 'ridership_val'
NUM_ROUTES_HEADER = 'routes_val'
COVERAGE_HEADER = 'coverage_val'
RIDERSHIP_DENSITY_HEADER = 'ridership_density_val'

def get_header(base: str, add_on: str):
    return add_on + '_' + base

def plot_per_round_metrics(filename, output_file='plot1.png'):
    df = pd.read_csv(filename)
    plt.plot(df[INTERATION_HEADER], df[get_header(FITNESS_HEADER, 'avg')])
    plt.savefig(output_file)

def plot_all_fitness_stats(filename, output_file='fitness_plot.png'):
    df = pd.read_csv(filename)
    x = df[INTERATION_HEADER]
    avg_overall = df[get_header(FITNESS_HEADER, 'avg')]
    ridership = df[get_header(RIDERSHIP_HEADER, 'avg')]
    num_routes = df[get_header(NUM_ROUTES_HEADER, 'avg')].apply(lambda x: abs(x))
    coverage = df[get_header(COVERAGE_HEADER, 'avg')]
    ridership_density = df[get_header(RIDERSHIP_DENSITY_HEADER, 'avg')]

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    print(ridership)
    ax1.scatter(x, avg_overall, c='black', marker="o", label='overall')
    ax1.scatter(x, ridership, c='blue', marker="o", label='ridership')
    ax1.scatter(x, num_routes, c='green', marker="o", label='num_routes(-1)')
    ax1.scatter(x, coverage, c='red', marker="o", label='coverage')
    ax1.scatter(x, ridership_density, c='orange', marker="o", label='ridership_density')

    plt.legend(loc='upper left')
    plt.savefig(output_file)
    plt.clf()
    

def plot_all_stats(filename, output_file='plot_comb.png'):
    df = pd.read_csv(filename)
    x = df[INTERATION_HEADER]
    avg = df[get_header(FITNESS_HEADER, 'avg')]
    best = df[get_header(FITNESS_HEADER, 'best')]
    med = df[get_header(FITNESS_HEADER, 'med')]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(x, best, c='b', marker="o", label='best')
    ax1.scatter(x, avg, c='r', marker="o", label='average')
    ax1.scatter(x, med, c='g', marker="o", label='med')
    plt.legend(loc='upper left')
    plt.savefig(output_file)
    plt.clf()

def plot_time(filename, output_file='time.png'):
    df = pd.read_csv(filename)
    plt.plot(df[INTERATION_HEADER], df[TIME_HEADER])
    plt.savefig(output_file)