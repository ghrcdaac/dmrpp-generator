from os import listdir
from os.path import isfile, join
from dmrpp_generator.main import DMRPPGenerator

if __name__ == "__main__":
    workstation_path = "/workstation/"
    join_path = lambda x: join(workstation_path, x)
    input_files = [join_path(f) for f in listdir(workstation_path) if isfile(join_path(f))]
    dmrpp = DMRPPGenerator(input=input_files)
    dmrpp.path = workstation_path
    dmrpp.dmrpp_generate(input_files)