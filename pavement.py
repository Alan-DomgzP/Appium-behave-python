import os
import sys
from paver.easy import task, consume_nargs

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(parent_dir)

from utils.pavement_functions import PavementFunctions
pavement = PavementFunctions()


@task
@consume_nargs(6)
def run_feature(args):
    pavement.run_behave(*args)
