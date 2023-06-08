import neat
from hitman.hitman import world_example
from train_utilities import MazeRep, MAX_SIZE
from generateur import get_random_maze

config_path = "neat_config.ini"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

N_MAZE = 1

# Define the fitness function
def eval_genomes(genomes, config):
    
    # generates X random maze for testing
    mazes = []
    for _ in range(N_MAZE):
        grid, starting = get_random_maze(max_size = MAX_SIZE)
        mazes.append((world_example, (0, 0)))
        # tester avec world example + un random

    # grid, starting = get_random_maze(max_size = MAX_SIZE)

    # for (grid, starting) in mazes: <= checking
        # print(grid[0][0], starting)

    i = 0
    best = genomes[0][1]
    for genome_id, genome in genomes:
        i += 1

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0

        for (grid, starting) in mazes:
            genome.fitness += MazeRep(grid, starting).evaluate_neat(net)

        # genome.fitness = MazeRep(grid, starting).evaluate(net)

        if genome.fitness > best.fitness:
            best = genome

    # EVALUATING BEST ON TEST GRID
    trial_net = neat.nn.FeedForwardNetwork.create(genome, config)
    mz = MazeRep(world_example, (5, 0))
    print(f"DONE (Best : {best.fitness})")
    print(mz)


# Create the population
population = neat.Population(config)

# Add reporters (optional)
stats = neat.StatisticsReporter()
population.add_reporter(stats)
population.add_reporter(neat.Checkpointer(generation_interval=100))


# Running

genomes = population.run(eval_genomes, 100)

# Evaluate the best genome further if needed
net = neat.nn.FeedForwardNetwork.create(population.best_genome, config)
grid, starting = get_random_maze(MAX_SIZE)  # Replace with your own test maze generation logic
game = MazeRep(grid, starting)
score = game.evaluate(net)  # Replace with your own evaluation logic

print(f"Best Fitness: {score} - Cumulated Penalties: {game.penalties} - Game complete: {not game.not_yet_complete()}")