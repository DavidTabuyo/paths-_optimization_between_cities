import random
import matplotlib.pyplot as plt
from map_print import print_in_map,print_final
def read_file(file_path:str)->list[list[int]]:
  # Initialize an empty list to store the distance matrix
  distance_matrix = []

  # Open the file for reading
  with open(file_path, "r") as open_file:
      # Read each line in the file
      for line in open_file:
          # Split the line into distances and convert them to floats with two decimal places
          distances = [round(float(distance), 2) for distance in line.split()]
          # Append the list of distances to the distance matrix
          distance_matrix.append(distances)
  
  return distance_matrix

Cromosome= list[int]
Population=list[Cromosome]

#number of samples
samples = 100

  #number of cities, from txt
cities=0
  
  #obtain data from txt
data=read_file("distances_matrix.txt")
  
cities=len(data)


def randomPopulation(samples:int, bits:int) -> Population:
  return[random.sample(range(bits),bits) for _ in range(samples)]


def selection(population:Population)->Population:
  #sort the population
  return sorted(population, key=fitness, reverse=False)


def crossover_parents(parent1:Cromosome,parent2:Cromosome)->Cromosome:
  crossover_rate=5
  for _ in range(0,crossover_rate):
    #size of sublist
    sublist_size=2 #i/n
    #sublist length
    subist_length=int(len(parent1)/sublist_size)
    first_index=random.randint(0,len(parent1)-(subist_length+1))
    first_parent_sublist=parent1[first_index:first_index+subist_length]
    #place sublist in other father, saving his sublist
    second_parent_sublist=parent2[first_index:first_index+subist_length]
    parent2[first_index:first_index+subist_length]=first_parent_sublist

    #if repeated elements, we delete it
    delete_elements=list(set(first_parent_sublist).intersection(second_parent_sublist))
    for element in delete_elements: 
      first_parent_sublist.remove(element)
      second_parent_sublist.remove(element)

    #we change repeated cities from changed ones
    for index,value in enumerate(parent2):
      if index<first_index or index>=first_index+subist_length:
        if value in first_parent_sublist:
          first_parent_sublist.remove(value)
          parent2[index] = second_parent_sublist.pop()
    
  return parent2
  


def crossover(population:Population,crossover_rate:float)->Population:
  population_copy=population[:]
  i=0
  while i < (len(population_copy) - 1)/2: 
    if random.random()< crossoverRate:
      son1= crossover_parents(population_copy[i+1], population_copy[i])
      son2 = crossover_parents(population_copy[i], population_copy[i + 1])
      
      population_copy[-(i + 1)] = son1
      population_copy[-(i + 2)] = son2
    else:
      population_copy[-(i + 1)] = population_copy[i]
      population_copy[-(i + 2)] = population_copy[i+1]
    i += 2
  
  return population_copy  
      

def mutate(population:Population, mutation_rate:float)->Population:
  if random.random()<mutation_rate:  
    population_copy=population[:]
    
    cromosome_index=random.randint(0,len(population_copy)-1)
    first_index=random.randint(0,len(population_copy[cromosome_index])-1)
    second_index=random.randint(0,len(population_copy[cromosome_index])-1)
    temp = population_copy[cromosome_index][first_index]
    population_copy[cromosome_index][first_index] = population_copy[cromosome_index][second_index]
    population_copy[cromosome_index][second_index] = temp

    return population_copy
  return population

def mutate2(population: Population, mutation_rate: float) -> Population:
  mutated_population = []

  for i, chromosome in enumerate(population):
    if i >= 10 and random.random() < mutation_rate:
      # Realiza una mutación en el cromosoma
      mutated_chromosome = chromosome.copy()
      index1, index2 = random.sample(range(len(chromosome)), 2)
      mutated_chromosome[index1], mutated_chromosome[index2] = (
          mutated_chromosome[index2],
          mutated_chromosome[index1],
      )
      mutated_population.append(mutated_chromosome)
    else:
      # Sin mutación, simplemente copia el cromosoma original
      mutated_population.append(chromosome)

  return mutated_population

def mutate3(population:Population,mutation_rate: float)->Population:
  population_copy =[]
  for cromosome in population:
    if random.random()<mutation_rate:  
      
      first_index=random.randint(0,len(cromosome)-1)
      second_index=random.randint(0,len(cromosome)-1)
      first_index,second_index=sorted([first_index,second_index])
      cromosome=cromosome[:first_index]+ cromosome[first_index:second_index][::-1]+ cromosome[second_index:]
    population_copy.append(cromosome)
  return population_copy


def meanmax(population:Population)->tuple[int,int]:
  max=0
  mean=0
  for pop in population:
    n=fitness(pop)
    if n>max:
      max=n
    mean+=n
  mean=mean/len(population)
  #print(max)
  return mean,max


def aptitude(param_list:list[list[int]]):
  iterations = [item[0] for item in param_list]
  mean_values = [item[1] for item in param_list]
  max_values = [item[2] for item in param_list]
  print(max_values[-1])

  plt.plot(iterations, mean_values, label='Media')
  plt.plot(iterations, max_values, label='Máximo')

  plt.xlabel('Iteración')
  plt.ylabel('Valor')
  plt.title('Evolución de la media y el máximo')
  plt.legend()

  plt.show()


def get_distance(city_a:int,city_b:int)->float:
  for distances in data:
    if distances[city_a]==0:
      return distances[city_b]

def fitness(cromosome:Cromosome)->float:
  sum=0
  for index in range(len(cromosome)):
    next_index = index + 1 if index + 1 < len(cromosome) else 0
    sum+=get_distance(cromosome[index],cromosome[next_index])
  return sum

if __name__ == "__main__":
  #crossover rate
  crossoverRate = 0.9
  #mutation rate
  mutationRate =0.4
  #Number of max iterations
  max_iterations=1000
  #mean,max,it
  mean,max,it=0,0,0
  #aptitude
  ap=[]
  #generate random population
  population =randomPopulation(samples, cities)
  fig, ax = plt.subplots(figsize=(10, 10))


  for _ in range(max_iterations):
    #selection
    population= selection(population)
    
    #crossover
    population = crossover(population, crossoverRate)
    #mutation
    population=mutate2(population,mutationRate)
    population= mutate3(population,mutationRate)
    #check if solution
    it+=1
    mean,max= meanmax(population)
    ap.append([it,mean,max])
    if it % 10 == 0:
      print_in_map(population[0],ax)
    
  #show graphic
  plt.close()
  aptitude(ap)
  #show map
  population= selection(population)
  print_final(population[0])


