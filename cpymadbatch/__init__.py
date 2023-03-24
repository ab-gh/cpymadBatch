__version__ = '0.1.0'

import itertools
import os

from typing import Callable, Union, Optional

import numpy
from cpymad.madx import Madx

class Config:
    """
    Configuration class for a cpymad batch job
    """

    def __init__(self,
                 name: str,
                 madx_executable="/afs/cern.ch/user/m/mad/bin/madx",
                 directory=None,
                 local=False
                 ):
        """
        Initialise a configuration for a cpymad batch job.

            Parameters:
                name (str): Name of the job
                madx_executable (str): Path to a MAD-X executable (default: /afs/cern.ch/user/m/mad/bin/madx)
                dir (str): Path to the job directory (default: /eos/user/<u>/<username>/cpymadbatch/<name>)
                local (bool): If True, the job will be run locally, otherwise, it is submitted to HTCondor (default: False)

        """
        self.madx_executable = madx_executable
        self.name = name
        self.user = os.environ["USER"]
        i = 0
        if dir:
            while True:
                if os.path.exists(f"/eos/user/{self.user[0]}/{self.user}/cpymadbatch/{name}"):
                    i = i + 1
                else:
                    self.directory = f"/eos/user/{self.user[0]}/{self.user}/cpymadbatch/{self.name + str(i)}/output"
                    break
        else:
            self.directory = directory
        self.local = local


class Parameters:
    """
    A set of parameters for a simulation job
    """

    def __init__(self,
                 params: dict):
        for key, value in params.items():
            setattr(self, key, value)

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

class Job:
    """
    A single simulation job
    """

    def __init__(self,
                 config: Config,
                 function: Callable,
                 parameters: Parameters):
        self.template_function = function
        self.parameters = parameters
        self.config = config

    def generate(self,
                 directory: str = None):
        """
        Generate the batch jobs
        """
        if directory is None:
            self.batch_directory = self.config.directory+"/batch"
        else:
            self.batch_directory = directory

        print(self.parameters.keys())
        print(type(self.parameters))
