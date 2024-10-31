from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from constant import ClientNumber


instance_name = 'R101'
clients_number = ClientNumber.TwentyFive.value
info = CVRPTWInfo(f'instances/{instance_name}.{clients_number}.txt',clients_number)
ng_generation = 1000000
AG = CVRPTW(info,ng_generation)
AG.optimize()