from utils.shopify_API import (
    create_order,
    verify_fulfillment
)

from utils.eshipz_custom_flow import eshipz_createpage_flow

from utils.eshipz_custom_flow import verify_shipment_moved_to_shipped


def test_saleschannel_update_createshipmentflow(page):

    order_id, order_name = create_order()

    eshipz_createpage_flow(page, order_name)

    verify_fulfillment(order_id)

    verify_shipment_moved_to_shipped(
        page,
        order_name
    )