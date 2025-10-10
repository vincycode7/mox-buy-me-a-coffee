from src import buy_me_a_coffee as bmc
from moccasin.config import get_active_network

def withdraw():
    active_network = get_active_network()
    coffee = active_network.manifest_named("coffee")
    print(f"Withdrawing from contract {coffee.address} on {active_network.name}")
    coffee.withdraw()
    return coffee

def moccasin_main(): 
    return withdraw()