# TransitGA
Application of evolutionary computing techniques to explore algorithmic optimization of transit networks. 

## Abstract 
This project leverages artificial intelligence techniques from the field of evolutionary computing to investigate the task of optimizing the geometry of urban transit systems. Working with the San Francisco Municipal Transporation Agency (SFMTA) bus network, we attempt to optimize the shape and organization of the routes using a custom genetic algorithm (GA). Due to the complexity of the problem, multiple iterations of the model are proposed to incorporate new ideas, and address shortcomings in previous versions. The results exemplify both the GAs ability to consistently find unexpected ways to maximize its objective function and the nuanced complexities in the problem of transit optimization. 
<br>

## Basic Setup

### Clone the Repository
`git clone https://github.com/Hweinstock/Math-thesis.git`

### Virtual Environment Setup
Set up virtual environment:  
`python3 -m venv /path/to/new/virtual/environment`

### Minicoda setup
`conda create -n {name} python=3.9.16 pip`
`conda activate {name}`

### Install Dependencies
Make sure you are in root-directory of the project, then install requirements:  
`pip install -r requirements.txt`

## Running the Program 

### Main Model
Parameter usage:

```
usage: main.py [-h] -p POPULATION_SIZE -g NUM_GENERATIONS [-in INITIAL_NETWORK] [-o OUTPUT] [-bp] [-te TIME_ESTIMATE] [-v {0,1,2,3}]
               [-fv {0,1,2,3}] [--coverage_lambda COVERAGE_LAMBDA] [--ridership_density_lambda RIDERSHIP_DENSITY_LAMBDA]
               [--zone_lambda ZONE_LAMBDA] [--extreme_trip_lambda EXTREME_TRIP_LAMBDA]

optional arguments:
  -h, --help            show this help message and exit

model parameters:
  -p POPULATION_SIZE, --population_size POPULATION_SIZE
                        size of population.
  -g NUM_GENERATIONS, --num_generations NUM_GENERATIONS
                        number of generations.
  -in INITIAL_NETWORK, --initial_network INITIAL_NETWORK
                        initial network to use to generate population. defaults to ../data/new_initial_net.pkl
  -o OUTPUT, --output OUTPUT
                        path to output directory, defaults to ../output/
  -bp, --best_performer
                        include to enable graphing the best performer after finishing.

additional options:
  -te TIME_ESTIMATE, --time_estimate TIME_ESTIMATE
                        get an estimate of running with these parameters. Integer passed in serves as number of test runs to
                        estimate.

logging options:
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        increase output verbosity (default: 0)
  -fv {0,1,2,3}, --file_verbosity {0,1,2,3}
                        decrease output log file verbosity (default: 3)

lambda parameters:
  --coverage_lambda COVERAGE_LAMBDA
                        weight associated with coverage score (default: 0)
  --ridership_density_lambda RIDERSHIP_DENSITY_LAMBDA
                        weight associated with ridership density score (default: 1)
  --zone_lambda ZONE_LAMBDA
                        weight associated zone lambda score (default: 1)
  --extreme_trip_lambda EXTREME_TRIP_LAMBDA
                        weight associated extreme trip lambda score (default: -1)
```
Example run:  
`python3 main.py -p 10 -g 10 -v 2`  
This command would run the model with a population size of 10 for 10 generations, with a console logging level of 2. 

Next: run preprocessing. and outline data requirements. 
### Network Simplification
```
usage: simplify_gtfs.py [-h] [-n NAME] [-r RIDERSHIP_SOURCE] [-g GTFS_SOURCE] [-v {0,1,2,3}] [-fv {0,1,2,3}]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  name of network
  -r RIDERSHIP_SOURCE, --ridership_source RIDERSHIP_SOURCE
                        path to ridership data (.csv) [route_id,route_name,total_ridership]
  -g GTFS_SOURCE, --gtfs_source GTFS_SOURCE
                        path to gtfs source data (.zip)

logging options:
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        increase output verbosity (default: 0)
  -fv {0,1,2,3}, --file_verbosity {0,1,2,3}
                        decrease output log file verbosity (default: 3)
```
The name parameter is what the final network should be called on export. 
This run also assumes some data has been put in place:
- `../data/ridership_data/SFMTA.xlsx`: should contain the SFMTA ridership data. 
- `../data/gtfs_data/SFMTA.zip`: should contain the SFMTA gtfs network. 
