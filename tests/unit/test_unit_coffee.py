from eth_utils import to_wei
from tests.conftest import SEND_VALUE
import boa

RANDOM_USER = boa.env.generate_address()

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address
    
def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()
        
def test_fund_with_money(coffee_funded, account):
    # Assert
    funder = coffee_funded.funders(0)
    assert funder == account.address
    assert coffee_funded.funder_to_amount_funded(funder) == SEND_VALUE
    
def test_non_owner_cannot_withdraw(coffee_funded, account):    
    # ACT & ASSERT
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()
            
def test_owner_can_withdraw(coffee_funded):
    # Arrange - fund the contract
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0
    
def test_withdraw_multiple_funders(coffee, account):
    # Arrange - fund the contract
    number_of_funders = 10
    starting_balance = boa.env.get_balance(coffee.OWNER())
    funders = []
    for i in range(number_of_funders):
        funder = boa.env.generate_address()
        funders.append(funder)
        boa.env.set_balance(funder, SEND_VALUE)
        with boa.env.prank(funder):
            coffee.fund(value=SEND_VALUE)
            
    # Act - Withdraw as the owner
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()
        # Assert - Make sure that the owner got the money
        # assert boa.env.get_balance(coffee.OWNER()) == starting_balance + SEND_VALUE * number_of_funders

    # Assert - Make sure that the contract balance is 0 and the owner got all the money
    assert boa.env.get_balance(coffee.address) == 0
        
    # Make sure that the funders are reset properly
    for funder in funders:
        assert coffee.funder_to_amount_funded(funder) == 0
        
def test_get_rate(coffee):
    # Arrange / Act
    rate = coffee.get_eth_to_usd_rate(SEND_VALUE)
    
    # Assert
    assert rate > 0
    assert type(rate) == int
    
# def test