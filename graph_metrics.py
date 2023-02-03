import matplotlib.pyplot as plt 
import pandas as pd 

INTERATION_HEADER = 'iteration'
AVERAGE_FITNESS_HEADER = 'avg_score'
BEST_FITNESS_HEADER = 'best_fitness'
MEDIAN_FITNESS_HEADER = 'med_score'
TIME_HEADER = 'time'

def plot_per_round_metrics(filename, output_file='plot1.png'):
    df = pd.read_csv(filename)
    plt.plot(df[INTERATION_HEADER], df[AVERAGE_FITNESS_HEADER])
    plt.savefig(output_file)


def plot_all_stats(filename, output_file='plot_comb.png'):
    df = pd.read_csv(filename)
    x = df[INTERATION_HEADER]
    avg = df[AVERAGE_FITNESS_HEADER]
    best = df[BEST_FITNESS_HEADER]
    med = df[MEDIAN_FITNESS_HEADER]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.scatter(x, best, c='b', marker="s", label='best')
    ax1.scatter(x, avg, c='r', marker="o", label='average')
    ax1.scatter(x, med, c='g', marker="o", label='med')
    plt.legend(loc='upper left')
    plt.savefig(output_file)
    plt.clf()

def plot_time(filename, output_file='time.png'):
    df = pd.read_csv(filename)
    plt.plot(df[INTERATION_HEADER], df[TIME_HEADER])
    plt.savefig(output_file)