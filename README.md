# quick-address
A command line utility to generate repetitive HTML forms/code resulting from Shipping/Billing First Name, Last Name, Address 1... etc...

### Installation
1. Clone this repo.
2. `pip install requirements.txt`

### Example usage:
````bash
$ python quick-address.py --section-template true
Provide template to wrap each section:
1: array(      
2: {{section}}
3: );
4: 
Provide template for each section:
1:      "{{field|c_c}}" => $customer->get_{{field|c_c}}(),
2: 
array(
	"shipping_first_name" => $customer->get_shipping_first_name(),
	"shipping_last_name" => $customer->get_shipping_last_name(),
	"shipping_address" => $customer->get_shipping_address(),
	"shipping_address" => $customer->get_shipping_address(),
	"shipping_city" => $customer->get_shipping_city(),
	"shipping_state" => $customer->get_shipping_state(),
	"shipping_zip" => $customer->get_shipping_zip(),
	"shipping_country" => $customer->get_shipping_country(),
	"billing_first_name" => $customer->get_billing_first_name(),
	"billing_last_name" => $customer->get_billing_last_name(),
	"billing_address" => $customer->get_billing_address(),
	"billing_address" => $customer->get_billing_address(),
	"billing_city" => $customer->get_billing_city(),
	"billing_state" => $customer->get_billing_state(),
	"billing_zip" => $customer->get_billing_zip(),
	"billing_country" => $customer->get_billing_country(),
);
$ 
```
