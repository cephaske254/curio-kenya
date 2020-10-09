# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
from .paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest,OrdersCaptureRequest


class CaptureOrder(PayPalClient):
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print ('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
      print ("\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
        response.result.payer.name.given_name + " " + response.result.payer.name.surname,
        response.result.payer.phone.phone_number.national_number))
    return response


"""This driver function invokes the capture order function.
Replace Order ID value with the approved order ID. """
if __name__ == "__main__":
  order_id = 'REPLACE-WITH-APPORVED-ORDER-ID'
  CaptureOrder().capture_order(order_id, debug=True)

class CreateOrder(PayPalClient):
    # 2. Set up your server to receive a call from the client
    """ This is the sample function to create an order. It uses the
      JSON body returned by buildRequestBody() to create an order."""

    def create_order(self, debug=False):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        # 3. Call PayPal to set up a transaction
        request.request_body(self.build_request_body())
        response = self.client.execute(request)
        if debug:
            print ('Status Code: ', response.status_code)
            print ('Status: ', response.result.status)
            print ('Order ID: ', response.result.id)
            print ('Intent: ', response.result.intent)
            print ('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))
            print ('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,response.result.purchase_units[0].amount.value))

        return response

        """Setting up the JSON request body for creating the order. Set the intent in the
    request body to "CAPTURE" for capture intent flow."""
    @staticmethod
    def build_request_body():
        """Method to create body with CAPTURE intent"""
        return \
            {
                "intent": "CAPTURE",
                "application_context": {
                    "brand_name": "CURIO KENYA",
                    "landing_page": "BILLING",
                    "shipping_preference": "SET_PROVIDED_ADDRESS",
                    "user_action": "CONTINUE"
                },
                "purchase_units": [
                    {
                        "reference_id": "PUHF",
                        "description": "Sporting Goods",

                        "custom_id": "CUST-HighFashions",
                        "soft_descriptor": "HighFashions",
                        "amount": {
                            "currency_code": "USD",
                            "value": "230.00",
                            "breakdown": {
                                "item_total": {
                                    "currency_code": "USD",
                                    "value": "180.00"
                                },
                                "shipping": {
                                    "currency_code": "USD",
                                    "value": "30.00"
                                },
                                "handling": {
                                    "currency_code": "USD",
                                    "value": "10.00"
                                },
                                "tax_total": {
                                    "currency_code": "USD",
                                    "value": "20.00"
                                },
                                "shipping_discount": {
                                    "currency_code": "USD",
                                    "value": "10"
                                }
                            }
                        },
                        "items": [
                            {
                                "name": "T-Shirt",
                                "description": "Green XL",
                                "sku": "sku01",
                                "unit_amount": {
                                    "currency_code": "USD",
                                    "value": "90.00"
                                },
                                "tax": {
                                    "currency_code": "USD",
                                    "value": "10.00"
                                },
                                "quantity": "1",
                                "category": "PHYSICAL_GOODS"
                            },
                            {
                                "name": "Shoes",
                                "description": "Running, Size 10.5",
                                "sku": "sku02",
                                "unit_amount": {
                                    "currency_code": "USD",
                                    "value": "45.00"
                                },
                                "tax": {
                                    "currency_code": "USD",
                                    "value": "5.00"
                                },
                                "quantity": "2",
                                "category": "PHYSICAL_GOODS"
                            }
                        ],
                        "shipping": {
                            "method": "United States Postal Service",
                            "address": {
                                "name": {
                                    "full_name": "John",
                                    "surname": "Doe"
                                },
                                "address_line_1": "123 Townsend St",
                                "address_line_2": "Floor 6",
                                "admin_area_2": "San Francisco",
                                "admin_area_1": "CA",
                                "postal_code": "94107",
                                "country_code": "US"
                            }
                        }
                    }
                ]
            }



