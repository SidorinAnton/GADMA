import unittest
from gadma import *
import itertools

TEST_STRUCTURES = [(1,), (2,),
                   (1,1), (2,1), (1,2),
                   (1,1,1)]


class TestModelStructure(unittest.TestCase):
    def test_initialization(self):
        for structure in TEST_STRUCTURES:
            for create_migs, create_sels, create_dyns, sym_migs, fracs in\
                    list(itertools.product([False, True],repeat=5)):
                dm = StructureDemographicModel(structure, structure,
                                               have_migs=create_migs,
                                               have_sels=create_sels,
                                               have_dyns=create_dyns,
                                               sym_migs=sym_migs,
                                               frac_split=fracs)
                # for splits variables
                n_par = (1 + int(not fracs)) * (len(structure) - 1)
                for i, str_val in enumerate(structure):
                    if i == 0:
                        # for each interval (except first) there is time,
                        # size of population, selection and dynamic
                        n_par += (str_val - 1) * (2 + int(create_sels)\
                                 + int(create_dyns))
                    else:
                        # for other intervals there are also migrations
                        n_pop = i + 1
                        n_migs = int(create_migs) * (n_pop * (n_pop - 1))
                        if sym_migs:
                            n_migs /= 2
                        n_par += str_val * (n_pop * (1 + int(create_dyns)\
                                 + int(create_sels)) + n_migs + 1)
                msg = f"Parameters are not equal for dem model with structure "\
                      f"{structure} and create_migs ({create_migs}), "\
                      f"create_sels ({create_sels}), create_dyns ({create_dyns}), "\
                      f"sym_migs ({sym_migs}), fracs ({fracs}) {dm.variables}"
                self.assertEqual(len(dm.variables), n_par, msg=msg)

    def test_likelihood_after_increase(self):
        for structure in TEST_STRUCTURES:
            for create_migs, create_sels, create_dyns, sym_migs, fracs in\
                    list(itertools.product([False, True],repeat=5)):
                create_sels = False
                def model_generator(structure):
                    return StructureDemographicModel(structure,
                                                     np.array(structure) + 1,
                                                     have_migs=create_migs,
                                                     have_sels=create_sels,
                                                     have_dyns=create_dyns,
                                                     sym_migs=sym_migs,
                                                     frac_split=fracs)
 
                dm = model_generator(structure)
                variables = dm.variables
                x = [var.resample() for var in variables]


                for engine in all_engines():
                    engine.set_model(dm)
                    if engine.id == 'dadi':
                        sizes = [20 for _ in range(len(structure))]
                        args = ([5, 10, 15],)  # pts
                    else:
                        sizes = [4 for _ in range(len(structure))]
                        args = ()
                    # simulate data
                    data = engine.simulate(x, sizes, *args)
                    engine.set_data(data)
#                    print(data)
#                    print(type(data))

                    # get ll of data
                    ll_true = engine.evaluate(x, *args)

                    # increase structure
                    for i in range(len(structure)):
                        new_structure = list(copy.copy(structure))
                        new_structure[i] += 1
                        msg = f"Increase structure from {structure} to "\
                              f"{new_structure} for engine {engine.id}. "\
                              f"create_migs: {create_migs}, "\
                              f"create_sels: {create_sels}, "\
                              f"create_dyns: {create_dyns}, "\
                              f"sym_migs: {sym_migs}, "\
                              f"fracs: {fracs}"
#                        print(msg)
                        new_dm = copy.deepcopy(dm)
                        new_dm, new_X = new_dm.increase_structure(
                            new_structure, [x])
                        engine.set_model(new_dm)
#                        print("!!!", dm.var2value(x), new_dm.var2value(new_X[0]))
                        new_ll = engine.evaluate(new_X[0], *args)
                        self.assertTrue(np.allclose(ll_true, new_ll),
                                        msg=f"{ll_true} != {new_ll} : " + msg)

    def test_fails(self):
        bad_struct = [[0], [0, 1], [1, 0]]

        bad_cur_init_final_structs = [([1, 1], [2, 1], [3, 1]),
                                      ([2, 2], [1, 1], [1, 2]),
                                      ([1, 2], [1, 1], [1, 1])]


        for create_migs, create_sels, create_dyns, sym_migs, fracs in\
                list(itertools.product([False, True],repeat=5)):
            def build_model(init_struct, final_struct):
                return StructureDemographicModel(init_struct, final_struct,
                                                 have_migs=create_migs,
                                                 have_sels=create_sels,
                                                 have_dyns=create_dyns,
                                                 sym_migs=sym_migs,
                                                 frac_split=fracs)
            # bad strcutures
            for struct in bad_struct:
                self.assertRaises(ValueError, build_model, struct, struct)

            # bad final structure
            for struct in TEST_STRUCTURES:
                for i in range(len(struct)):
                    final_struct = list(struct)
                    final_struct[i] -= 1
                    self.assertRaises(ValueError, build_model,
                                      struct, final_struct)

            # bigger or lesser structure in from_structure
            for cur_str, init_str, final_str in bad_cur_init_final_structs:
                model = build_model(init_str, final_str)
                self.assertRaises(ValueError, model.from_structure, cur_str)

            # not possible to increase structure
            for _, init_str, final_str in bad_cur_init_final_structs:
                model = build_model(init_str, final_str)
                model.from_structure(final_str)
                self.assertRaises(ValueError, model.increase_structure)
            init_str, final_str = [2, 3], [3, 4]
            model = build_model(init_str, final_str)
            self.assertRaises(ValueError, model.increase_structure, [1, 3])
            self.assertRaises(ValueError, model.increase_structure, [2, 2])
