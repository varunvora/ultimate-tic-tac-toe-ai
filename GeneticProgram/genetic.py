"""
A lot of this currently holds place holders for things like the parents and children. They will
be replaced once the needed portions of the genetic agent have been fleshed out.
"""

import random


class GeneticProgram:

    def __init__(self):
        pass

    def selection(self, parent1_traits, parent2_traits):
        """
        Selects a point to split each parents list of traits. Then calls crossover to
        cross the traits at the selected point to create 2 new children.

        @param parent1_traits: A list of trait values from one parent
        @param parent2_traits: A list of trait values from the other parent
        @return: The children that resulted from the crossover event
        """
        cross_point = random.randint(1, len(parent1_traits)-2)
        return self.crossover(parent1_traits, parent2_traits, cross_point)

    def crossover(self, parent1_traits, parent2_traits, cross_point):
        """
        Splits the given parent's trait lists at the crossing point creating a left half and
        right half of the traits. Combines the first parent's left half with the second
        parent's right half to create the first child then, combines the second parent's left
        half with the first parent's right half to create the second child. Mutation will be
        called on each child to possibly mutate one of their traits.

        @param parent1_traits: A list of trait values from one parent
        @param parent2_traits: A list of trait values from the other parent
        @param cross_point: The dividing point in the trait lists to use when splitting and crossing
        the parent's traits to create new children
        @return: A tuple of the created children
        """

        # Split the first parent into left and right parts at the cross point
        parent1_left = parent1_traits[0:cross_point]
        parent1_right = parent1_traits[cross_point:len(parent1_traits)]

        # Split the second parent into left and right parts at the cross point
        parent2_left = parent2_traits[0:cross_point]
        parent2_right = parent2_traits[cross_point:len(parent2_traits)]

        # Create the new child agents
        child1 = []
        child2 = []

        child1.extend(parent1_left)
        child1.extend(parent2_right)

        child2.extend(parent2_left)
        child2.extend(parent1_right)

        return child1, child2

    def mutation(self, child):
        """
        Will randomly mutate the given child object's traits. Currently there is a 35% chance
        that the mutation will happen. If the mutation does happen then a new trait value between
        0 and 1 will be generated and a random trait will be selected to be replaced by the new
        trait value.

        @param child: A child agent created by crossover
        @return: A child agent that may have a mutated trait value
        """

        mutation_chance = random.randrange(0, 10)

        if mutation_chance <= 3.5:
            new_value = random.random()
            mutated_trait_pos = random.randint(0, len(child.traits)-1)
            child.traits[mutated_trait_pos] = new_value

        return child
