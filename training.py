import neat

config_path = "path/to/your/config-file"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
population = neat.Population(config)

