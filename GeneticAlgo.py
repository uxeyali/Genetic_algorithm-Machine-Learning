import math
import random
from sklearn import preprocessing

class GA:

    def __init__(self, populationSize, pcross, pmutate, generations):
        # population array
        self.populationSize = populationSize
        self.pcross = pcross
        self.pmutate = pmutate
        self.generations = generations
        print("========= INITIAL==========")
        self.population = self.createPopulation(populationSize)
        self.start(self.population, self.populationSize)

    def start(self, population, populationsize):
        while self.generations > 0:
            print("======= GENERATION", self.generations,"==========")
            self.normalize(self.population)
            self.generate_children(populationsize, self.population)
            self.generations -= 1


    def createPopulation(self, size):
        pop = []
        for i in range(size):
            chromo = Chromosome(size = 6, min = -1, max = 5)
            pop.append(chromo)
            pop[i].decode(pop[i].x)
            # print("Fitness of chromosome", i , ": ", pop[i].fitness)
        return pop

    def normalize(self, pop):
        total = 0
        sum = 0
        min = 5
        max = 0
        x = 0.0
        y = 0.0
        for chromo in pop:
            if chromo.fitness < min:
                min = chromo.fitness
            if chromo.fitness > max:
                max = chromo.fitness
                x, y = chromo.decx , chromo.decy
        print("Max fitness is: ", max)
        print("Maximizing values: ", x, "and", y)
        for chromo in pop:
            chromo.halfNormal = chromo.fitness + abs(min)
            total += chromo.halfNormal
            # print("New fitness: ", chromo.halfNormal)

        for chromo in pop:
            chromo.normalized = chromo.halfNormal / total
            # print("Normalized: ", chromo.normalized)
            sum += chromo.normalized

    def roulette(self, pop):
        # gets random number between 0 and 1
        randoNum = random.random()
        current = 0
        normal_values = []

        for chromo in pop:
            current += chromo.normalized
            normal_values.append(current)
            # print("Wheel: ", normal_values)
            if current > randoNum:
                # print("Fitness of winner", chromo.fitness)
                return chromo

    def checkForCross(self, probability):
        rando = random.uniform(0, 1)
        if rando <= probability:
            # print(rando)
            return True
        else:
            return False

    def checkForMutation(self, probability):
        rando = random.uniform(0, 1)
        if rando <= probability:
            # print(rando)
            return True
        else:
            return False

    def cross(self, chromo1, chromo2):
        # print("Chromo A is: ", chromo1.x, "and ", chromo1.y)
        # print("Chromo B is: ", chromo2.x, "and ", chromo2.y)
        tempA = Chromosome(size=6, min=-1, max=5)
        tempB = Chromosome(size = 6, min = -1, max = 5)
        tempA.x = chromo1.x
        tempA.y = chromo2.y
        tempB.x = chromo2.x
        tempB.y = chromo1.y

        # print("Temp A is: ", tempA.x, "and ", tempA.y)
        # print("Temp B is: ", tempB.x, "and ", tempB.y)
        return tempA, tempB

    def mutate(self, chromo):
        rando = random.randint(0, chromo.size * 2 -1)
        # print("Random number: ", rando)
        # print("Before mutation: ", chromo.whole)
        if chromo.whole[rando]:
            chromo.whole[rando] = False
            # print("After Mutation: ", chromo.whole)
            return chromo
        else:
            chromo.whole[rando] = True
            return chromo

    def generate_children(self, size, pop):
        newpop = []
        children = []
        for i in range(size//2):
            chromoa = self.roulette(pop)
            # print()
            chromob = self.roulette(pop)
            # print(chromoa.whole)
            # print(chromob.whole)

            if self.checkForCross(self.pcross):
                # print("Crossing")
                newChromo1, newChromo2 = self.cross(chromoa,chromob)
                # print("NewChromo1.x: ", newChromo1.x)
                # print("NewChromo1.y: ", newChromo1.y)
                newpop.append(newChromo1)
                newpop.append(newChromo2)
                # print("===================================================")
            else:
                newChromo1, newChromo2 = chromoa, chromob
                # print("Not Crossing")
                # print("NewChromo1.x: ", newChromo1.x)
                # print("NewChromo1.y: ", newChromo1.y)
                newpop.append(newChromo1)
                newpop.append(newChromo2)
                # print("===================================================")

        for i in range(size):
            if self.checkForMutation(self.pmutate):
                # print("Mutating")
                child = self.mutate(newpop[i])
                children.append(child)
            else:
                # print("Not mutating")
                children.append(newpop[i])

        self.population = children

# ================= CHROMOSOME CLASS ============================
class Chromosome:
    size = 0
    normalized = 0.0
    halfNormal = 0

    def __init__(self, size, min, max):
        self.x = []
        self.y = []
        self.min = min
        self.max = max
        self.size = size
        self.normalized = 0
        self.halfNormal = 0
        self.decx = 0
        self.decy = 0

        for index in range(self.size):
            self.x.append(bool(random.randint(0, 1)))
            self.y.append(bool(random.randint(0, 1)))
        self.fitness = self.fitnessFunction()
        self.whole = self.x + self.y

    def decode(self, array):
        total = 0
        for i in range(len(array)):
            total += (array[i]* (2 ** (len(array)-i-1)))
        return total

    def fitnessFunction(self):
        mapping = (self.max - self.min) / (2 ** self.size - 1)
        self.decx = self.decode(self.x) * mapping - self.max
        # print("Decimal x:", decx)
        self.decy = self.decode(self.y) * mapping - self.max
        # print("Decimal y:", decy)
        func = (2 - self.decx) ** 2 * math.exp(-self.decx ** 2 - (self.decy + 3) ** 2) - (self.decx - self.decy ** 2) * math.exp(-self.decx ** 2 - self.decy ** 2) + self.decy ** 3 * math.exp(-self.decx ** 2 - self.decy ** 3)
        # print(func)
        return func


GA(populationSize=100, pcross=0.7, pmutate=0.01, generations=1000)