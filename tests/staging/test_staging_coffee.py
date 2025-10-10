from moccasin.config import get_active_network
import pytest
import boa
from script.deploy import deploy_coffee
from eth_utils import to_wei

SENT_VALUE = to_wei(1, "ether")


@pytest.mark.staging
@pytest.mark.ignore_isolation
def test_can_fund_and_withdraw_live():
    active_network = get_active_network()
    price_feed = active_network.manifest_named("price_feed")
    coffee = deploy_coffee(price_feed.address)
    coffee.fund(value=SENT_VALUE)
    amount_funded = coffee.funder_to_amount_funded(boa.env.eoa)
    assert amount_funded == SENT_VALUE
    coffee.withdraw()
    assert boa.env.get_balance(coffee.address) == 0