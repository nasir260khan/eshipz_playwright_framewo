from utils.shopify_API import (
    create_order,
    verify_fulfillment
)



from utils.eshipz_custom_flow import eshipz_custom_flow


def test_saleschannel_update_shipmentflow(page):

    order_id, order_name = create_order()

    eshipz_custom_flow(page, order_name)

    verify_fulfillment(order_id)