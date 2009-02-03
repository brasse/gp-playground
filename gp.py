import copy
import random

def gp(population, fitness, selection, operations, termination_condition):
    '''
    gp([individual] * 50,
       eval_fitness,
       trunction_selection(10),
       [(p1, mutate), (p2, cross)],
       condition)
    '''
    generation = 0
    while True:
        evaluated_population, next_generation = \
            _gp_generation(population, fitness, selection, operations)
        generation += 1
        if termination_condition(evaluated_population, generation):
            break
        population = next_generation
    return [i for _, i in evaluated_population]
    
def _gp_generation(population, fitness, selection, operations):
    evaluated_population = []
    # Evaluate each indiviual.
    for i in population:
        f = fitness(i)
        evaluated_population.append((f, i))
    evaluated_population.sort()
    evaluated_population.reverse()

    # Vary and build next generation.
    next_generation = []
    while len(next_generation) < len(population):
        operation = _pick_operation(operations)
        arity = operation.func_code.co_argcount
        individuals = (selection(evaluated_population) for _ in xrange(arity))
        next_generation.extend(operation(*individuals))
        
    return evaluated_population, next_generation

def truncation_selection(n):
    def f(evaluated_population):
        return random.choice(evaluated_population[:n])[1]
    return f

def _random_slice(sequence_length):
    start = random.randrange(0, sequence_length - 1)
    end = random.randrange(start + 1, sequence_length)
    return slice(start, end)

def mutate(get_mutation):
    def f(individual):
        m = copy.copy(individual)
        m[_random_slice(len(m))] = get_mutation()
        yield m
    return f

def crossover(individual1, individual2):
    i1 = random.randrange(len(individual1))
    i2 = random.randrange(len(individual2))
    yield individual1[:i1] + individual2[i2:]
    yield individual2[:i2] + individual1[i1:] 

def _reproduce(individual):
    yield individual

def _pick_operation(operations, random=random.random):
    '''
    >>> _pick_operation([(0.2, 1), (0.3, 2)], lambda: 0.2)
    1
    >>> _pick_operation([(0.2, 1), (0.3, 2)], lambda: 0.5)
    2
    >>> _pick_operation([(0.2, 1), (0.3, 2)], lambda: 0.6) # doctest:+ELLIPSIS
    <function _reproduce at 0x...>
    '''
    if sum([p for p, _ in operations]) > 1.0:
        raise Exception('Sum of probabilities is greater than 1.')
    r = random()
    for p, operation in operations:
        if r <= p:
            return operation
        else:
            r -= p
    return _reproduce

if __name__ == '__main__':
    import doctest
    doctest.testmod()
