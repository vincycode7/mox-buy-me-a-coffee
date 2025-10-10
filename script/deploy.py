from moccasin.config import get_active_network
from src import buy_me_a_coffee as bmc
from script.deploy_mocks import deploy_feed
from moccasin.boa_tools import VyperContract

active_network = get_active_network()

def deploy_coffee(price_feed: str):
    coffee: VyperContract = bmc.deploy(price_feed)
    
    # if active_network.has_explorer() and active_network.is_local_or_forked_network is False:
    #     result = active_network.moccasin_verify(coffee)
    #     result.wait_for_verification()
    return coffee

def moccasin_main(): 
    price_feed = active_network.manifest_named("price_feed")
    print(f"Using price feed at {price_feed.address} on {active_network.name}")
    coffee = deploy_coffee(price_feed.address)
    print(f"Contract deployed to {coffee.address} on {active_network.name}")
    print(coffee.get_eth_to_usd_rate(int(1000)))
    return coffee
