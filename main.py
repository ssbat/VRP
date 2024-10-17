from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from constant import ClientNumber


instance_name = 'C101'
clients_number = ClientNumber.Hundred.value
info = CVRPTWInfo(f'instances/{instance_name}.{clients_number}.txt',clients_number)
ng_generation = 100000
AG = CVRPTW(info,ng_generation)
AG.optimize()