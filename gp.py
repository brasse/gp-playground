import copy
import pprint
import random

def gp(population, fitness, selection, operations):
    '''
    gp([individual] * 50,
       10,
       eval_fitness,
       [(p1, mutate), (p2, cross)])
    '''
    pass

def _gp_helper(population, fitness, selection, operations):
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
        op = _pick_operation(operations)
        # TODO: how many argunents does op take?
        
def truncation_selection(n):
    def f(evaluated_population):
        assert(len(evaluated_population) >= n)
        return evaluated_population[random.randrange(n)][1]
    
def mutate(get_mutation):
    def f(individual):
        m = copy.copy(individual)
        start = random.randrange(0, len(m))
        end = random.randrange(start + 1, len(m))
        m[start : end] = get_mutation()
        return m
    return f

def _reproduce(inividual):
    return indiviual

def _pick_operation_helper(operations, rnd):
    '''
    >>> _pick_operation_helper([(0.2, 1), (0.3, 2)], 0.2)
    1
    >>> _pick_operation_helper([(0.2, 1), (0.3, 2)], 0.5)
    2
    >>> _pick_operation_helper([(0.2, 1), (0.3, 2)], 0.6) # doctest:+ELLIPSIS
    <function _reproduce at 0x...>
    '''
    for p, operation in operations:
        if rnd <= p:
            return operation
        else:
            rnd -= p
    return _reproduce

def _pick_operation(operations):
    ps = [p for p, op in operations]
    if sum(ps) > 1.0:
        raise Exception('Sum of probabilities is greater than 1.')
    return _pick_operation_helper(operations, random.random())

if __name__ == '__main__':
    import doctest
    doctest.testmod()
