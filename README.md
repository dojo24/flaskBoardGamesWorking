# Flask Store Working Version

## Clone the code and run the app
- Forward Engineer the ERD
- Use the app 1st then look at the code to find the errors
- There are 12 Errors (injected errors)

# Errors by Type

## ERD Errors:
- Product Table - AI was not checked
- User Table - updatedAT has NN checked and no defaults

## SQL Errors:
- User Table/user.py - updatedAT vs updatedAt
- Ordered Table/ordered.py - orderd vs ordered
- product.py save function query ends with : not ;

## Route Errors:
- Dashboard Route - Session is missing (html will need fixing too)
- Delete Route - the Data dict is wrong
- Order Route - no post method

## HTML Errors:
- editProduct.html - no post method

## Rendering/Visual Errors:
- Dashboard.html - lists the product id not who added the product
- Dashboard.html - View/Edit/Delete buttons always show as they are based on if there is a user_id not session
- viewProduct.html - Doesn't list who has ordered the product should be order.who.firstName

# Errors in order may be encountered:
- User Table - updatedAT has NN checked and no defaults
- User Table/user.py - updatedAT vs updatedAt
- Dashboard Route - Session is missing (html will need fixing too)
- product.py save function query ends with : not ;
- Product Table - AI was not checked
- Dashboard.html - lists the product id not who added the product
- Dashboard.html - View/Edit/Delete buttons always show as they are based on if there is a user_id not session
- editProduct.html - no post method
- Delete Route - the Data dict is wrong
- Order Route - no post method
- Ordered Table/ordered.py - orderd vs ordered
- viewProduct.html - Doesn't list who has ordered the product should be order.who.firstName
