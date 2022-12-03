from genetic import GeneticProgram
import sys

if __name__ == '__main__':

    gen_num = int(sys.argv[1])
    agent_num = int(sys.argv[2])
    top_k_num = int(sys.argv[3])

    gen = GeneticProgram()

    print(gen_num)
    print(agent_num)
    print(top_k_num)

    print("Working")

    top_agent, duration = gen.evolution(gen_num, agent_num, top_k_num)
    genetic_file = open("top_agent_stats.txt", "w")
    agent_info = ""
    agent_info += "Top agent name: " + top_agent.agent_name + "\n"
    agent_info += "Traits: " + str(top_agent.traits) + "\n"
    agent_info += "Average move time: " + str(top_agent.average_time) + " milliseconds" + "\n"
    agent_info += "Total competition score: " + str(top_agent.total_win_score) + "\n"
    agent_info += "Evolution completed in " + str(duration) + " seconds" + "\n"
    genetic_file.write(agent_info)