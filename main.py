from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from constant import ClientNumber

from CVRPTW_params import *

info = CVRPTWInfo(FULL_INSTANCE_NAME,CLIENTS_NUMBER)
AG = CVRPTW(info)
AG.optimize()