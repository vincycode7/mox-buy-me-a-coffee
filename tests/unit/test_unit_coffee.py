from eth_utils import to_wei
import boa

SEND_VALUE = to_wei(1, "ether")
RANDOM_USER = boa.env.generate_address()

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address
    
def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address
    
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()
        
def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE)
    
    # Act
    coffee.fund(value=SEND_VALUE)
    
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE
    
def test_non_owner_cannot_withdraw(coffee, account):
    # Arrange - fund the contract
    boa.env.set_balance(account.address, SEND_VALUE)
    coffee.fund(value=SEND_VALUE)
    
    # ACT & ASSERT
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee.withdraw()
            
def test_owner_can_withdraw(coffee):
    # Arrange - fund the contract
    boa.env.set_balance(coffee.OWNER(), SEND_VALUE)
    with boa.env.prank(coffee.OWNER()):
        coffee.fund(value=SEND_VALUE)
        coffee.withdraw()
        
    assert boa.env.get_balance(coffee.address) == 0
    
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
        
    # Assert - Make sure that the contract balance is 0 and the owner got all the money
    assert boa.env.get_balance(coffee.address) == 0
    assert boa.env.get_balance(coffee.OWNER()) == starting_balance + SEND_VALUE * number_of_funders
        
    # Make sure that the funders are reset properly
    for funder in funders:
        assert coffee.funder_to_amount_funded(funder) == 0