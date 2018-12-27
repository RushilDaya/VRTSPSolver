# VRTSPSolver
MoAI TSP Genetic Algorithm Project

## Immediate Concerns
### Victor J
1. x-opt local heuristic
2. Hibrid Mutation Technics

### Rushil
1. Stop Criteria Review

##Original Task
1. ~~On Toledo, you can find the GA Toolbox, the template program and tutorials about Matlab. Test the Matlab program to solve a TSP.~~
2. Perform a limited set of experiments by varying the parameters of the existing genetic algorithm (population size, probabilities, . . . ) and evaluate the performance.
3. Implement a stopping criterion that avoids that rather useless iterations (generations) are computed.
4. Implement and use another representation and appropriate crossover and mutation operators. Perform some parameter tuning to identify proper combinations of the parameters.
5. Test to which extent a local optimisation heuristic can improve the result.
6. Test the performance of your algorithm using some benchmark problems (available on Toledo) and critically evaluate the achieved performance.
7. You should select at least one task from the list below:
	- (a) ~~Implement and use two other parent selection methods, i.e. fitness proportional selection and tournament selection.~~ Compare the results with those obtained using the default rank- based selection.
  - (b) ~~Implement one survivor selection strategy (besides the already implemented elitism). Per- form experiments and evaluate the results.~~
  - (c) Implement and use one of the techniques aimed at preserving population diversity (e.g. subpopulations/islands, crowding, . . . ). Perform experiments and evaluate the results.
  - (d) Incorporate an adaptive or self-adaptive parameter control strategy (e.g. parameters that depend on the state of the population, parameters that co-evolve with the population,...). Perform experiments and evaluate the results.
8. Write a short report (≈ 10 pages, appendices and code not included), discussing your implemen- tation and explaining your results. Include your code in the appendix.
Note: A carefully written report of ≈ 10 pages can contain a lot of information, if well written. Be precise but concise! Do not repeat information from the handbook or slides.


###Plan For Genetic Algorithms Project.
1. ~~Get familiar with the genetic algorithm toolbox and the tsp code, run basic experiments, no need to record results at this stage. (2 hours).~~
2. Setup a pipeline for automating the recording of results and changing parameters, this will save a lot of time if we need to run ~ 50 tests for each configuration and make gradual adjustments to ~10 parameters (5 hours).
3. Research stopping criteria, implement the best one. (3 hours).
4. Review other representations and crossover methods, find the combination which seems to be the most promising (4 hours).
5. Implement the new representation and crossover method as generic functions (5 hours).
6. Implement local heuristics (2-opt, 3-opt, 4-opt, ...) (3 hours).
7. Sweep the parameter spaces of BOTH the original method and our method to find optimal parameters of BOTH algorithms on smaller problems (6 hours).
8. Test these 2 optimized models on benchmarked problems (6 hours).
9. ~~Research and implement other parent selection schema (5 hours).~~
10. Research and implement Niching (6 hours).
11. ~~Research and implement a survivor strategy other than elitism (5 hours).~~
12. Repeat step 7,8 for the new algorithms generated in (9,10,11) (6 hours).
13. Based on the results pick the best strategies from all previous stages and make a combined model, optimize and test this model (6 hours).
14. Additional problem which can be solved as a TSP type problem with GA (Extra).

__Write the report:__

* Literature review (2 pages) (6 hours).
* Discuss the implementation , all the different techniques we have tried (3 pages) (8 hours).
* Methodology (how did we test the models - pipeline/ parameter sweep / etc) (1 page) (2 hours).
* Results, the performance of all models. (3 pages) (6 hours).
* Analysis (3 pages) (10 hours).

Estimated Project time: 93 hours (~ 50h/pp).
