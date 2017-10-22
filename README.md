# Hiroko
System written in pure Python for task organization based in two independent criterias, the task organization algorithm is a genetic algorithm data uses a weighted fitness function to consider both parameters. Head to `docs` to see the formal proposition of the problem, here is an outline.

## Problem proposition
An energy provider wants to schedule the revisions of its clients in a city in a number of days (10 to 20), with to criterias:

* The number of clients should be similar from one day to another (minimize standard deviation)
* The distance traveled by the employees must be minimized as well

As an input you are given the location of each neighborhood of the city and the clients per neighborhood, no further information is given.

## Dependencies
To run the application you should have in your system the following:

* Python 3.5+
* Scipy

## Usage
Hiroko execution is straight foward, access `hiroko` sub-directory and run the following command:

    python hiroko.py

Current version of Hiroko implements a Buffer class that enables the user to receive in realtime the results of the genetic algorithm, also, when a process is finished, a `.dump` is generated containing all the pertinent information. For that to work, it is mandatory that you create a sub-directory inside `data`:

    cd data
    mkdir dump

A simple jupyter notebook was created to visualize the behaviour of the algorithm, the script resides in `extra`.

### Refining Interaction
Although the command mentioned previously is enough to get the application working, you can refine the execution via command line arguments, or by modifing the configuration file in `config`. The command line arguments are:

* `-d` selects the number of days in which the neighborhoods are distributed.
* `-s` selects the size output of each generation, larger size outputs may lead to better results but it takes more time.
* `-m` selects the method of execution: whether you want to execute the genetic algorithm or a randomized version of it.

For further detail consult the `help` command:

    python hiroko.py --help
