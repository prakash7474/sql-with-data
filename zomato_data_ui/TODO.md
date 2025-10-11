# Task: Add User-Defined Name, ID, Email, Phone for Orders - Fix Logic and UI/UX

## Steps to Complete:

1. **Edit templates/home.html**  
   - Add input fields for first_name, last_name, email, phone in the order summary section.  
   - Make these fields visible only when the cart has items (update updateOrderSummary() to show/hide).  
   - Update checkout() function to collect these values, validate (required fields), and include them in the JSON payload along with cart and address.  

2. **Edit app_index.py**  
   - In /place_order endpoint, receive user details (first_name, last_name, email, phone) from JSON.  
   - Query customers table for existing user by email; if found, use that user_id.  
   - If not found, query MAX(user_id) + 1 for new_id, insert new customer record with that id, first_name, last_name, phone_number, email.  
   - Use the determined user_id to insert orders for each cart item.  
   - Return success message including the user's full name. Handle exceptions (e.g., duplicate email).  

3. **Test the Changes**  
   - Use browser_action to launch http://127.0.0.1:5000/, load menu, add items to cart.  
   - Fill user details with a new email, enter address, checkout - verify success alert with name, and check DB for new customer and order.  
   - Test with existing email to ensure it uses the same user_id.  
   - Verify error handling for missing fields or invalid data.  

4. **Update TODO.md**  
   - Mark steps as completed after each one.  

[x] Step 1: Edit templates/home.html  
[x] Step 2: Edit app_index.py  
[x] Step 3: Test the Changes  
[x] Step 4: Final verification and completion
