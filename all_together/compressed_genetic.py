from typing import List

from GeneticProgram.genetic import GeneticAgent


class CompressedGeneticAgent(GeneticAgent):
    """
    An agent with 3 traits that uses the Genetic Agent
    """
    def __init__(self, agent_name: str, center: float, corner: float, side: float):
        super().__init__(agent_name, [corner, side, corner, side, center, side, corner, side, corner])

    def set_traits(self, new_traits: List[float]) -> None:
        center, corner, side = new_traits
        super().set_traits([corner, side, corner, side, center, side, corner, side, corner])
