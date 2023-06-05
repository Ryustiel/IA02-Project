import neat
from train_utilities import MazeRep, MAX_SIZE
from generateur import get_random_maze

config_path = "neat_config.ini"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

# Define the fitness function
def eval_genomes(genomes, config):
    
    # generates 1 random maze for testing
    grid, starting = get_random_maze(max_size = MAX_SIZE)
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = MazeRep(grid, starting).evaluate(net)


# Create the population
population = neat.Population(config)

# Add reporters (optional)
stats = neat.StatisticsReporter()
population.add_reporter(stats)
population.add_reporter(neat.Checkpointer(generation_interval=100))


# Run the evolution

generations = 10  # Number of generations to evolve
for i in range(generations):
    # Evaluate fitness and run NEAT algorithm for one generation
    genomes = population.run(eval_genomes, 1)

    # Get the best genome from the current generation
    best_genome = None
    best_fitness = 0.0
    for genome_id, genome in genomes:
        if genome.fitness > best_fitness:
            best_fitness = genome.fitness
            best_genome = genome

    # Evaluate the best genome further if needed
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    grid, starting = get_random_maze(MAX_SIZE)  # Replace with your own test maze generation logic
    score = MazeRep(grid, starting).evaluate_score(net)  # Replace with your own evaluation logic

    print(f"Generation {i + 1} - Best Fitness: {best_fitness} - Score: {score}")
