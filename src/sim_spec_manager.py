""" Simulation Spec Parser (from SEDML)

:Author: Akhil Teja  < akhilmteja@gmail.com >
:Date: 2020-01-28
:Copyright: 2019, UCONN Health
:License: MIT

"""

import sys
import os
from COPASI import *
from config import Config
import xmltodict


class SimulationSpecManager:
    def __init__(self, job_id=Config.JOB_ID, jobhook_url=Config.JOBHOOK_URL, sedml_dir_path=Config.SEDML_DIR):
        self.ALGORITHMS_MAP = {
            "0000089": CTaskEnum.Method_DsaLsodar,
            "0000304": CTaskEnum.Method_RADAU5,
            "0000027": CTaskEnum.Method_stochastic,
            "0000038": CTaskEnum.Method_directMethod,
            "0000039": CTaskEnum.Method_tauLeap,
            "0000333": CTaskEnum.Method_adaptiveSA,
            "0000064": CTaskEnum.Method_hybrid,
            "0000088": CTaskEnum.Method_hybridLSODA,
            "0000032": CTaskEnum.Method_hybridODE45,
            "0000318": CTaskEnum.Method_stochasticRunkeKuttaRI5
        }
        self.JOB_ID = job_id
        self.JOBHOOK_URL = jobhook_url
        self.ALGORITHM = None
        self.INITIAL_TIME = None
        self.NUMBER_OF_POINTS = None
        self.OUTPUT_START_TIME = None
        self.OUTPUT_END_TIME = None
        self.sedml = None
        self.sbml_path = None
        self.simulation = None
        self.task = None
        self.out_path = None

        self.parse_status = self.parse_sim_config_from_sedml(path=sedml_dir_path)

    def parse_sim_config_from_sedml(self, path: str):
        sedml = self.__get_sedml__(dir_path=path)
        if sedml:
            self.sedml = xmltodict.parse(sedml)
            self.simulation = self.sedml['sedML']['listOfSimulations']['uniformTimeCourse']
            self.task = self.sedml['sedML']['listOfTasks']['task']
            model = self.sedml['sedML']['listOfModels']['model']
            self.ALGORITHM = self.ALGORITHMS_MAP[self.simulation['algorithm']['@kisaoID'].split(':')[1]]
            self.INITIAL_TIME = self.simulation['@initialTime']
            self.NUMBER_OF_POINTS = self.simulation['@numberOfPoints']
            self.OUTPUT_START_TIME = self.simulation['@outputStartTime']
            self.OUTPUT_END_TIME = self.simulation['@outputEndTime']
            self.sbml_path = os.path.join(path, model['@source'])

            # Create directory for output
            self.out_path = os.path.join(path, 'out', self.task['@id'])
            os.makedirs(self.out_path, exist_ok=True)

            return True
        else:
            return False

    def __get_sedml__(self, dir_path):
        files = list()
        path = dir_path
        for file_path in os.listdir(path):
            if file_path.endswith(".sedml"):
                files.append(os.path.join(path, file_path))
        
        if len(files) > 1:
            return False
        
        else:
            with open(files[0], 'r') as f:
                return f.read()
