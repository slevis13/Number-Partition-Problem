# Number-Partition-Problem

The purpose of this project was to experiment with a few randomized heuristic algorithms for the Number Partition Problem, which is NP-Complete. 

## Usage

To test out the main program, clone the repository and run "python3 all.py". The program will print the average time taken by each method to solve a random instance of the number partition problem. To change the test parameters (number of trials, size of partition problem, and number of iterations done by each heuristic method), edit the values "size", "max_iter", and "trials" at the top of main (near line 160). 

## Background

In the standard representation of the problem, a solution *S* consists of two sets of numbers -- one in which all signs are negative and one in which all signs are positive. The total difference between the two solution sets gives the "residue" of the problem. The aim of the number partition problem is to find the minimum such residue in a given set of numbers. Stated in a different way, the aim of the problem is to partition the problem space into two sets, such that the sums of the two sets are as close to equal as possible.

A deterministic algorithm, Karmarkar-Karp, is examined in comparison to the heuristic methods, explained below. Karmarkar-Karp repeatedly takes the two largest elements remaining in the problem space and uses differencing, i.e. assigns one element to the positive solution set and the other element to the negative solution set. In this way, KK repeatedly "splits" the two largest elements into opposing solution sets. 

The heuristic algorithms used here are: a repeated random method; a hill-climbing method; and simulated annealing. 

Repeated random simply generates a random solution and compares its residue to the current residue. If the new solution has a lower residue, it replaces the current solution. Otherwise, the current solution remains and a new random solution is generated.

Hill climbing repeatedly attempmts to "climb" to a better, neighboring solution, by randomly choosing a neighbor in the solution space and comparing its residue to the current. A solution's "neighbor" is simply a solution that differs from the current solution in either one or two places.

Simulated annealing attempts to move to neighboring solutions as well, though it also allows occasional moves to "worse" solutions. This is done so that the algorithm might avoid trapping itself in a local optimum, as hill climbing is apt to do.

# Pre-partitioning

The program examines each of the heuristic algorithms and, concurrently, the effect of "pre-partitioning" on the problem instance. Pre-partitioning is not an algorithm itself, but an alternate way of representing the problem. You can think of pre-partitioning as the opposite of differencing; where differencing splits two values into opposite solution sets, pre-partitioning forces two values into the same solution set.

The program first generates a random instance of the number partition problem. This instance is run through each of the four algorithms. For the three heuristics (repeated random, hill climbing, and simulated annealing), the instance runs first in its standard representation, then in a pre-partitioned representation. 


