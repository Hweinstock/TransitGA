import matplotlib.pyplot as plt 
import pandas as pd 

INTERATION_HEADER = 'iteration'
AVERAGE_FITNESS_HEADER = 'avg_score'

def plot_per_round_metrics(filename):
    df = pd.read_csv(filename)
    plt.plot(df[INTERATION_HEADER], df[AVERAGE_FITNESS_HEADER])
    plt.savefig('plot.png')
