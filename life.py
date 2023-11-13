class Life:
    """
    Represents an individual in the population, storing gene information and fitness proxy.

    Attributes:
    - gene: Stores information related to the optimization task.
    - fitness_proxy: The metric to be minimized or maximized for this individual.

    Methods:
    - calculate_fitness_proxy(): Calculates the fitness proxy based on the gene.
    - mutation(): Mutates the gene.
    """

    def __init__(
        self,
        gene,
        ga_calculate_fitness_proxy,
        ga_generate_random_life,
        ga_mutation,
    ):
        """
        Initialize a Life instance.

        Args:
        - gene: Gene information relevant to the optimization problem.
        - ga_calculate_fitness_proxy: Function to calculate the fitness proxy.
        - ga_generate_random_life: Function to generate random gene information.
        - ga_mutation: Function for gene mutation.
        """
        # Store the functions for calculating fitness and mutation.
        self.calculate_fitness_proxy_func = ga_calculate_fitness_proxy
        self.generate_random_life = ga_generate_random_life
        self.calculate_mutation = ga_mutation
        # Initialize gene with random data.
        self.gene = self.generate_random_life(gene)
        self.fitness_proxy = None
        # Calculate the initial fitness proxy.
        self.calculate_fitness_proxy()

    def calculate_fitness_proxy(self):
        self.fitness_proxy = self.calculate_fitness_proxy_func(self.gene)

    def mutation(self):
        self.gene = self.calculate_mutation(self.gene)
        self.calculate_fitness_proxy()

    def to_dict(self):
        return {"gene": self.gene, "fitness_proxy": self.fitness_proxy}
