from ..utils import PopulationSizeVariable, TimeVariable, MigrationVariable

# Main options. Output and input.
output_dir = None
input_file = None
#input_data = None
#number_of_populations = None
population_labels = None
projections = None
outgroup = None
sequence_length = None
linked_snp_s = True
directory_with_bootstrap = None
#boots = None

# Pipeline
theta0 = None
time_for_generation = None
#multinom = None
only_sudden = False
pts = None
engine = 'moments'
#relative_params = False
no_migrations = False

#Custom model
#model_func_file = None
#model_func = None
#lower_bound = None
#upper_bound = None
#p_ids = None

# Structure of models
initial_structure_unit = 1
initial_structure = None
final_structure = None

# Time bounds
#split_1_lim = None
#split_2_lim = None

# GA options
size_of_generation = 10

fractions = [0.2, 0.3, 0.3]
n_elitism = 2
p_mutation = 0.3
p_crossover = 0.3
p_random = 0.2

mean_mutation_strength = 0.2
const_for_mutation_strength = 1.01

mean_mutation_rate = 0.2
const_for_mutation_rate = 1.02

stuck_generation_number = 100
eps = 1e-2

# just for logging evaluations
#output_log_file = None
#max_num_of_eval = None # maximum number of logll eval.
#num_init_pts = None # can get value from Inference.optimize_ga

# Local search
local_optimizer = 'BFGS_log'

# Printing and drawing
print_models_code_every_n_iteration = 0
silence = False
draw_models_every_n_iteration = 0
units_of_time_in_drawing = 'generations'
const_of_time_in_drawing = 1.0
vmin = 1

number_of_repeats = 1
number_of_processes = 1
test = False
#resume_dir = None
#only_models = None

# Extra parameters

# Bounds on models parameters. They are relative to N_A (!)
min_n = PopulationSizeVariable.default_domain[0]
max_n = PopulationSizeVariable.default_domain[1]
min_t = TimeVariable.default_domain[0]
max_t = TimeVariable.default_domain[1]
min_m = MigrationVariable.default_domain[0]
max_m = MigrationVariable.default_domain[1]

# Parameters for local search alg
#ls_verbose = None
#ls_flush_delay = 0.5
#ls_epsilon = 1e-3
#ls_gtol = 1e-05
#ls_maxiter = None
# for hill climbing
#hc_mutation_rate = None
#hc_const_for_mutation_rate = None
#hc_stop_iter = None

# Options of mutation, crossing and random generating
#random_N_A = True
#multinom_cross = False
#multinom_mutate = False

# Options of printing summary information about repeats
time_to_print_summary= 1  # min

# Options of distributions
#distribution = 'normal'  # can be 'uniform'
#std = None  # std for normal dist

# Some options about drawing plots:
#matplotlib_available = False
#pil_available = False
#moments_available = False


