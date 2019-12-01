#!/usr/bin/env python

import multiprocessing as mp
import sys
import time

# strikers
from aigent.agent_1 import Agent as A1
# defenders
from aigent.agent_2 import Agent as A2
# goalie
from aigent.agent_3 import Agent as A3


def run(team_name: str, number_of_players: int):
    print(f"Running team: '{team_name}' with {number_of_players} players")

    # return type of agent: midfield, striker etc.
    def agent_type(position):
        return {
            2: A2,
            3: A3,
            4: A2,
            6: A2,
            7: A2,
            8: A2,
        }.get(position, A1)

    # spawn an agent of team_name, with position
    def spawn_agent(team_name, position):
        """
        Used to run an agent in a seperate physical process.
        """
        # return type of agent by position, construct
        a = agent_type(position)()
        a.connect("localhost", 6000, team_name)
        a.play()

        # we wait until we're killed
        while 1:
            # we sleep for a good while since we can only exit if terminated.
            time.sleep(1)

    # spawn all agents as separate processes for maximum processing efficiency
    agentthreads = []
    for position in range(1, number_of_players + 1):
        print(f"  Spawning agent {position}...")

        at = mp.Process(target=spawn_agent, args=(team_name, position))
        at.daemon = True
        at.start()

        agentthreads.append(at)

    print(f"Spawned {len(agentthreads)} agents.")
    print()
    print("Playing soccer...")

    # wait until killed to terminate agent processes
    try:
        while 1:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print()
        print("Killing agent threads...")

        # terminate all agent processes
        count = 0
        for at in agentthreads:
            print(f"  Terminating agent {count}...")
            at.terminate()
            count += 1
        print("Killed {(count - 1)} agent threads.")

        print()
        print("Exiting.")
        sys.exit()


class Runner:

    @staticmethod
    def run_a():
        run("A", 11)

    @staticmethod
    def run_b():
        run("B", 11)
