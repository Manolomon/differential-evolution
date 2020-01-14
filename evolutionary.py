import numpy
import random
import pandas as pd

def aptitud(individuo):
    return (individuo[0]**2) + (individuo[1]**2)

def ed_rand_1_bin(np, max_gen, f, cr, execution):
    EVOLUTION = pd.DataFrame()
    g = 0 # Contador de generación
    population = numpy.random.uniform(low=-5, high=5, size=(np,2)) # Crear una población inicial aleatoria
    print(population)
    print("---------------")
    aptitudes = numpy.apply_along_axis(aptitud, 1, population) # Evaluar población
    order = numpy.argsort(aptitudes)
    population = population[order]
    for g in range(max_gen):
        for i in range (np):
            # Mutación
            no_parent = numpy.delete(population, i, 0)
            row_i = numpy.random.choice(no_parent.shape[0], 3, replace=False) # Selección de donantes diferentes al padre r1 =/= r2 =/= r3
            r = no_parent[row_i, :]
            v_mutacion = ((r[0]-r[1]) * f) + r[2] # Vector Mutación v
            # Recombinación
            jrand = random.randint(0, 1) # Posición en la que padre e hijo diferirán
            v_hijo = numpy.empty([1, 2])
            for j in range(2):
                t = random.uniform(0, 1)
                if t < cr or j is jrand:
                    v_hijo[0,j] = v_mutacion[jrand]
                else:
                    v_hijo[0,j] = population[i,j]
            population = numpy.concatenate((population, v_hijo), axis=0)
            # Remplazo por aptitud
            aptitudes = numpy.apply_along_axis(aptitud, 1, population) # Evaluar población
            order = numpy.argsort(aptitudes)
            population = population[order]
            # Se descartan los extras de la población
        population = population[:np]
        aptitudes = aptitudes[:np]
        
        generation = pd.DataFrame({'x1': population[:, 0], 'x2': population[:, 1], 'f(x1,x2)': aptitudes})
        generation['gen'] = g + 1
        EVOLUTION = pd.concat([EVOLUTION, generation], ignore_index=True)
    EVOLUTION.to_csv('./datasources/execution_' + str(execution + 1) + '.csv') 

if __name__ == "__main__":
    for i in range (30):
        ed_rand_1_bin(np=50, max_gen=50, f=0.7, cr=0.0001, execution=i)