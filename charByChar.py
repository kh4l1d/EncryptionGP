import operator
import math
import random
import numpy
import textwrap

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

messageText = raw_input("Enter message char : ")
messageAscii = ""
keyText = raw_input("Enter key : ")
keyAscii = ""

for messageCharacter in messageText :
    messageAscii = messageAscii + str(ord(messageCharacter))

for keyCharacter in keyText :
    keyAscii = keyAscii + str(ord(keyCharacter))

keyInt = int(keyAscii)
messageInt = int(messageAscii)

pset = gp.PrimitiveSet("MAIN",1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.neg, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1000,1000))

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("compile", gp.compile, pset=pset)
def evalSymbReg(individual):
    func = toolbox.compile(expr=individual)

    error = abs(func(keyInt) - messageInt)

    return error,

toolbox.register("evaluate",evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)

toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    random.seed(318)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 514, stats=mstats,
                                   halloffame=hof, verbose=True)

    print '\n'
    print 'The cipher text is ->'
    print '\n'
    print hof[0]
    print '\n'
    print 'Reversing the process to get back the message -> '
    function = toolbox.compile(expr=hof[0])
    obtainedIntAscii = function(keyInt)
    print '\n'
    obtainedAscii = str(obtainedIntAscii)
    print obtainedAscii
    print '\n'
    print 'Initial message ascii was -> '
    print '\n'
    print messageAscii
    print '\n'
    return pop, log, hof

if __name__ == "__main__":
    main()
