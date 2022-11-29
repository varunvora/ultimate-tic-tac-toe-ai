"""
A lot of this currently holds place holders for things like the parents and children. They will
be replaced once the needed portions of the genetic agent have been fleshed out.
"""

import random
from agent.genetic_agent import GeneticAgent
from playground.evaluator import evaluate
from typing import Optional, Tuple, List


class GeneticProgram:

    def __init__(self):
        self.current_agent_number = 0

    def generate_random_agent(self) -> GeneticAgent:
        """
        Creates a new genetic agent with randomly generated traits.
        @return: A genetic agent object
        """
        new_agent = GeneticAgent("GeneticAgent"+str(self.current_agent_number))
        self.current_agent_number += 1
        new_agent.set_traits(self.generate_random_traits())
        return new_agent

    def generate_random_traits(self) -> List[float]:
        """
        Generates a new set of 9 traits for a genetic agent with random values between 0 and 1 as traits
        @return: A list of floats that are between 0 and 1
        """
        traits = []
        for num in range(0, 9):
            traits.append(random.random())
        return traits

    def reproduce(self, parent_pool: List[GeneticAgent]) -> List[GeneticAgent]:
        """
        Will randomly select two parent agents from the parent pool and use them to create two
        new children. Once the number of children is greater than or equal to the number of parents
        the reproduction will stop and the list of children will be returned. Note that each
        parent in the pool to reproduce multiple times or not at all.

        @param parent_pool: A list of parent genetic agents
        @return: A list of child genetic agents created from the pool of parent agents
        """

        def select_random_parents() -> Tuple[GeneticAgent, GeneticAgent]:
            """
            Selects two random unique positions from the parent_pool and returns the parents at
            the corresponding indices.

            @return: A tuple of parent agents from the parent pool
            """
            first_parent_index = random.randint(0, len(parent_pool)-1)

            second_parent_index = first_parent_index
            while second_parent_index != first_parent_index:
                second_parent_index = random.randint(0, len(parent_pool))

            return parent_pool[first_parent_index], parent_pool[second_parent_index]

        children = []

        while len(children) < len(parent_pool):
            parent1, parent2 = select_random_parents()

            children.extend(self.selection(parent1.traits, parent2.traits))

        return children

    def selection(self, parent1_traits: List[float], parent2_traits: List[float]) -> Tuple[
        GeneticAgent, GeneticAgent]:
        """
        Selects a point to split each parents list of traits. Then calls crossover to
        cross the traits at the selected point to create 2 new children.

        @param parent1_traits: A list of trait values from one parent
        @param parent2_traits: A list of trait values from the other parent
        @return: The children that resulted from the crossover event
        """
        cross_point = random.randint(1, len(parent1_traits)-2)
        return self.crossover(parent1_traits, parent2_traits, cross_point)

    def crossover(self, parent1_traits: List[float], parent2_traits: List[float], cross_point:
    int) -> Tuple[GeneticAgent, GeneticAgent]:
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

        # Create the traits for the new child agents
        child1_traits = []
        child2_traits = []

        child1_traits.extend(parent1_left)
        child1_traits.extend(parent2_right)

        child2_traits.extend(parent2_left)
        child2_traits.extend(parent1_right)

        # Create the new child agents
        child1 = GeneticAgent(existing_traits=child1_traits)
        child2 = GeneticAgent(existing_traits=child2_traits)

        # Mutate the child agents
        child1 = self.mutation(child1)
        child2 = self.mutation(child2)

        return child1, child2

    def mutation(self, child: GeneticAgent) -> GeneticAgent:
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

    def fitness(self, pool, top_k_num):
        """
        Takes in a list of agents and finds the top k agents in the list using the agents total
        win score and if there is a tie then their average running time.
        @param pool: A list of genetic agent to be evaluated for fitness
        @param top_k_num: The max number of agents to allow through
        @return: A list of the top k genetic agents from the given pool
        """
        #pool.sort(key=lambda x: (x.total_win_score, x.average_time), reverse=True)
        pool.sort(key=lambda x: x.average_time)
        pool.sort(key=lambda x: x.total_win_score, reverse=True)
        return pool[0:top_k_num]

    def generation(self, pool, top_k_num):
        """
        Evaluate all the agents in the generation by playing them against each other. After every agent
        has play each other get the fittest agents and return them
        @param pool: A list the genetic agents in the current generation
        @param top_k_num: The number of agents that should remain at the end of the generation
        @return: A list of the top k agents from the generation
        """

        def generation_runner(player, competition):
            """
            Plays one agents against all of the other agents
            @param player: The main genetic agent being tested
            @param competition: The remaining agents in the pool
            @return: None
            """
            for opponent in competition:
                player_score = evaluate(player, opponent, 15)
                player.total_win_score += player_score
                opponent.total_win_score += (1 - player_score)
                player.total_genetic_rounds += 1

        finished_agents = []
        for num in range(0, len(pool)):
            current_agent = pool.pop()
            generation_runner(current_agent, pool)
            finished_agents.append(current_agent)

        remaining = self.fitness(finished_agents, top_k_num)

        return remaining

    def evolution(self, generation_num, agent_num, top_k_num):
        """
        Perform evolution over the specified number of generations and return the top agent after evolution
        @param generation_num: The number of generations the evolution process should occur over
        @param agent_num: The number of agents that should be in each generation
        @param top_k_num: The max number of agents from each generation to accept into the parent pool
        @return: The top genetic agent after evolution has concluded
        """

        def evolution_runner(current_pool, generations_left):
            """
            A recursive function that actually runs the evolution process for the specified
            number of generations
            @param current_pool: A list of genetic agents that represents the current generation
            of agents
            @param generations_left: The number of remaining generations before evolutions concludes
            @return: A list of the final generation of agents
            """
            if generations_left <= 0:
                return current_pool
            winners = self.generation(current_pool, top_k_num)
            next_gen = self.reproduce(winners)

            if len(next_gen) < agent_num:
                for nm in range(len(next_gen), agent_num):
                    next_gen.append(self.generate_random_agent())
            elif len(next_gen) > agent_num:
                next_gen = next_gen[0:agent_num]

            return evolution_runner(next_gen, generations_left-1)

        pool = []

        # Generate the initial agent pool
        for num in range(0, agent_num):
            pool.append(self.generate_random_agent())

        # Run for the specified number of generations
        final_gen = evolution_runner(pool, generation_num)

        # Perform fitness on final generation
        remaining = self.fitness(final_gen, top_k_num)

        # Find best
        top_agent = remaining[0]
        print(top_agent.traits)
        return top_agent



