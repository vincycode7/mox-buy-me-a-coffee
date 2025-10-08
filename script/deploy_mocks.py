from src.mocks import mock_v3_aggregator as mva
from moccasin.boa_tools import VyperContract, ZksyncContract
from typing import Any

STARTING_DECIMALS = 8
START_PRICE = int(2000e8)

def deploy_feed():
    res: VyperContract = mva.deploy(STARTING_DECIMALS, START_PRICE)
    print(f"Deployed mock price feed to {res.address}")
    return res

def moccasin_main():
    res = deploy_feed()
    print(f"Price feed at {res.address}")
    return res
