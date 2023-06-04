import neat
from dump.train_utilities_old import MazeRep

config_path = "path/to/your/config-file"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

# Define the fitness function
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = MAZE.evaluate_score(net)

# Create the population
population = neat.Population(config)

# Add reporters (optional)
stats = neat.StatisticsReporter()
population.add_reporter(stats)
population.add_reporter(neat.Checkpointer(generation_interval=100))

# Run the evolution

MAZE = MazeRep()

generations = 10  # Number of generations to evolve
for _ in range(generations):
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
    test_maze = MAZE.set_random_training_maze()  # Replace with your own test maze generation logic
    score = MAZE.evaluate_score(net)  # Replace with your own evaluation logic

    print(f"Generation {_+1} - Best Fitness: {best_fitness} - Score: {score}")
