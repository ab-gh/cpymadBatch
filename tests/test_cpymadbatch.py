import numpy
import sys

sys.path.append('../cpymadbatch')

import cpymadbatch as cmb

def test_version():
    assert cmb.__version__ == '0.1.0'


config = cmb.Config("test")
parameters = cmb.Parameters({"test": [1, 2, 3], "foo": [4, 5, 6], "bar": [10]})
def test_function(a):
    return a
job = cmb.Job(config=config, parameters=parameters, function=test_function)

job.generate()