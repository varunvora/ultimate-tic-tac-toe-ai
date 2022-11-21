from agent.agent import Agent


class GeneticAgent(Agent):

    def __init__(self, agent_name="", existing_traits=None):
        super().__init__(agent_name)
        if existing_traits is None:
            existing_traits = []
        self.traits = existing_traits
        self.win_count = 0
        self.lose_count = 0

    def set_traits(self, new_traits):
        """
        Sets the traits list of the agent to the new traits list given.

        @param new_traits: A list of traits representing traits for the genetic agent
        @return: None
        """
        self.traits = new_traits

    def set_specific_trait(self, trait_pos, new_trait):
        """
        Will set the value of a specific trait in the agent's trait list to the given value.

        @param trait_pos: The int index of the trait will be set
        @param new_trait: The float representing the trait that will replace the existing trait
        at trait_pos
        @return: None
        """

        self.traits[trait_pos] = new_trait