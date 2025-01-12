import random
import matplotlib.pyplot as plt
import obj_fit_functions
from GA_Initialize import Initialization, Create_First_Generation
from GA_Evaluate import Evaluate_Generation
from GA_Selection import (
    Roulette_Wheel_Selection,
    Classified_Roulette_Wheel_Selection,
    Linear_scaling,
)
from numpy import mean
from GA_Crossover import One_Point_Crossover
from GA_Mutation import Mutation

algorithm_parameters = Initialization()
population = Create_First_Generation(algorithm_parameters)

best_solution = []
average_solution = []

objective = input(
    """\nWhich of the following functions do you wish to optimize?
                   1) fGriewank
                   2) griewank
                   3) michalewicz
                   4) rastrigin
                   5) booth
                   6) bukin_n6
                   7) cross_in_tray
                   8) holder_table
                   9) mccormick
                   10) poloni
                   11) viennet
                   Answer : """
)
match objective:
    case "1":
        Fitness_Function = obj_fit_functions.fGriewank
    case "2":
        Fitness_Function = obj_fit_functions.griewank
    case "3":
        Fitness_Function = obj_fit_functions.michalewicz
    case "4":
        Fitness_Function = obj_fit_functions.rastrigin
    case "5":
        Fitness_Function = obj_fit_functions.booth
    case "6":
        Fitness_Function = obj_fit_functions.bukin_n6
    case "7":
        Fitness_Function = obj_fit_functions.cross_in_tray
    case "8":
        Fitness_Function = obj_fit_functions.holder_table
    case "9":
        Fitness_Function = obj_fit_functions.mccormick
    case "10":
        Fitness_Function = obj_fit_functions.poloni
    case "11":
        Fitness_Function = obj_fit_functions.viennet

answer = int(
    input(
        """\nHow would you like the Roulette Wheel to function? 
        1) Normal 
        2) Linear Scaled 
        3) Linear Classified
        Answer : """
    )
)
if answer == 3:
    q = int(
        input("\nWhat will the possibality of choosing the best solution be ?  q = ")
    )
    q0 = (2 / algorithm_parameters.get("num_Genes")) - q
    print("q = ", q, " q0 = ", q0)

best_so_far = float("-inf")  # Initialize best_so_far to negative infinity

for i in range(algorithm_parameters.get("num_Generations")):

    fitness_list = Evaluate_Generation(population, Fitness_Function)

    if answer == 1:
        parents = Roulette_Wheel_Selection(fitness_list)
    elif answer == 2:
        scaled_fitness_list = Linear_scaling(fitness_list)
        parents = Roulette_Wheel_Selection(scaled_fitness_list)
    elif answer == 3:
        parents = Classified_Roulette_Wheel_Selection(fitness_list, q, q0)

    population = One_Point_Crossover(
        population, parents, algorithm_parameters.get("Pc")
    )
    population = Mutation(
        population, algorithm_parameters, algorithm_parameters.get("Pm")
    )
    best_solution_index = fitness_list.index(max(fitness_list))
    best_fitness = fitness_list[best_solution_index]
    best_solution.append(best_fitness)
    best_so_far = max(best_so_far, best_fitness)  # Update best_so_far
    average_fitness = mean(fitness_list)
    average_solution.append(average_fitness)

print("\nThe final population is: \n", *population, sep="\n")
plt.plot(best_solution, label="Best Solution")
plt.plot(average_solution, label="Average Solution")
plt.axhline(y=best_so_far, color="r", linestyle="--", label="Best So Far")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Best and Average Fitness over Generations")
plt.legend()
plt.grid(True)
plt.show()
