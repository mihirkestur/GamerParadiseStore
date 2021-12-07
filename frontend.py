from numpy.core.fromnumeric import prod
from numpy.lib.function_base import select
import streamlit as st
st.set_page_config(page_title='GamerParadiseStore', layout = 'wide', initial_sidebar_state = 'auto')
import dbcommands
import psycopg2
conn = psycopg2.connect(**st.secrets["postgres"])
cursor = conn.cursor()

choice = st.radio("Who are you?", (
    "Developer",
    "Gamer",
    "Manager"
))

if(choice == "Developer"):
    command = st.text_area(label="Enter command")
    execute = st.button(label="Execute")
    if(command != "" and execute):  
        try:
            st.dataframe(dbcommands.execute_any_command(cursor, command))
        except Exception as e:
            st.write("Not a valid command:")
            st.error(f"{e}")

elif(choice == "Gamer"):
    operation = st.radio("What do you want to do?", (
    "Insert Gamer Info",
    #"Update Gamer Info",
    "Delete Gamer Info",
    "Purchase",
    "Participate in Contest",
    "Register Complaint"
    ))
    if(operation == "Insert Gamer Info"):
        with st.form(key='Users'):
            first_name = st.text_input(label='First name')
            last_name = st.text_input(label='Last name')
            email = st.text_input(label='E-mail')
            phone = st.text_input(label='Phone')
            addr = st.text_input(label='Address')
            submit_button = st.form_submit_button(label='Submit')
        if(submit_button):
            values = f"('{first_name}','{last_name}','{email}','{phone}')"
            column_names = '(first_name, last_name, e_mail, phone)'
            user_id = dbcommands.insert_into_table(cursor, "users",column_names, values,'user_id')
            
            values = f"('{user_id}','{addr}')"
            column_names = '(user_id, address)'
            dbcommands.insert_into_table(cursor, "address",column_names, values,'user_id')
            st.success(f"Your user id is : {user_id}")

    # elif(operation == "Update Gamer Info"):
    #     with st.form(key='Users'):
    #         first_name = st.text_input(label='First name')
    #         last_name = st.text_input(label='Last name')
    #         email = st.text_input(label='E-mail')
    #         phone = st.text_input(label='Phone')
    #         addr = st.text_input(label='Address')
    #         submit_button = st.form_submit_button(label='Submit')

    elif(operation == "Delete Gamer Info"):
        with st.form(key='delete user'):
            user_id = st.text_input(label='Enter user id')
            submit_button = st.form_submit_button(label='Delete user')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "users", "user_id", user_id))
    
    elif(operation == "Register Complaint"):
        with st.form(key='complaint'):
            user_id = st.text_input(label='User id')
            comp_desc = st.text_input(label='Complaint Description')
            comp_date = st.text_input(label='Complaint Date')
            submit_button = st.form_submit_button(label='Submit')
    
    elif(operation == "Purchase"):

        with st.form(key='Cart item'):
            user_id = st.text_input(label='User id')
            product_id = st.text_input(label='Product id')
            date_add = st.text_input(label='Date Added')
            quant_wish = st.text_input(label='Quantity wished')
            add_to_cart = st.form_submit_button(label='Add to cart')

        if(st.button(label="View my cart")):
            # NOTE: user_id should be cart_id. Needs to be obtained
            st.dataframe(dbcommands.select_from_table(cursor, "cart_item", "*", f"where cart_id = {user_id}"))

        if(st.button(label="View Details")):
            st.dataframe(dbcommands.select_from_table(cursor, "product"))
            st.dataframe(dbcommands.select_from_table(cursor, "game"))
            st.dataframe(dbcommands.select_from_table(cursor, "accessory"))
            st.dataframe(dbcommands.select_from_table(cursor, "product_offers"))
            st.dataframe(dbcommands.select_from_table(cursor, "offers"))

        if(add_to_cart):
            # insert to cart_item
            pass
            
        with st.form(key='Cart/Payment'):
            user_id = st.text_input(label='Confirm User id')
            pay_mode = st.text_input(label='Payment Mode')
            pay_date = st.text_input(label='Payment Date')
            amnt_paid = st.text_input(label='Amount Paid')
            buy = st.form_submit_button(label='Make payment on cart')
        if(buy):
            # insert to transaction
            pass

    elif(operation == "Participate in Contest"):
        with st.form(key='Participates/Team/Belongs_to'):
            # points gained, prize won, total points
            user_id = st.text_input(label='User id')
            contest_id = st.text_input(label='Contest Id')
            team_id = st.text_input(label='Team Id')
            submit_button = st.form_submit_button(label='Submit')
        if(st.button(label="Browse Contests and Teams")):
            st.dataframe(dbcommands.select_from_table(cursor, "contest"))
            st.dataframe(dbcommands.select_from_table(cursor, "team"))

elif(choice == "Manager"):

    operation = st.radio("Select operation", (
    "Insert Product Supplier Details",
    #"Update Product Supplier Details",
    "Insert Product Details",
    #"Update Product Details",
    "Insert Offer",
    #"Update Offer",
    "Contest details",
    "Delete a product"
    ))

    if(operation == "Insert Product Supplier Details"):
        # product_supplier
        with st.form(key="supplier"):
            sup_name = st.text_input(label='Supplier Name')
            sup_phone = st.text_input(label='Supplier Phone')
            coo = st.text_input(label='Country of origin')
            submit_button = st.form_submit_button(label='Submit')

        if(submit_button):
            values = f"('{sup_phone}','{sup_name}','{coo}')"
            column_names = '(supplier_phone, supplier_name, country_of_origin)'
            supplier_id = dbcommands.insert_into_table(cursor, "product_supplier", column_names, values, 'supplier_id')
            st.success(f"Your supplier id is : {supplier_id}")

    
    # elif(operation == "Update Product Supplier Details"):
    #     # product_supplier
    #     with st.form(key="supplier"):
    #         sup_name = st.text_input(label='Supplier Name')
    #         sup_phone = st.text_input(label='Supplier Phone')
    #         coo = st.text_input(label='Country of origin')
    #         submit_button = st.form_submit_button(label='Submit')

    #     if(submit_button):
    #         values = f"('{sup_phone}','{sup_name}','{coo}')"
    #         column_names = '(supplier_phone, supplier_name, country_of_origin)'
    #         supplier_id = dbcommands.insert_into_table(cursor, "product_supplier", column_names, values, 'supplier_id')
    #         st.success(f"Your supplier id is : {supplier_id}")

    elif(operation == "Insert Product Details"):
        # product
        supplier_id = st.text_input(label='Supplier_id')
        price = st.text_input(label='Price')
        rating = st.text_input(label='Rating')
        desc = st.text_input(label='Description')

        off_id = st.text_input(label='Offer ID')
        off_et = st.text_input(label='Offer end-time')

        product_type = st.selectbox("Product type", (
        "None",
        "Game",
        "Accessory"
        ))

        if(product_type == "Game"):
            with st.form(key='Game'):
                game_name = st.text_input(label='Game name')
                genre = st.text_input(label='Genre')
                specs = st.text_input(label='Specifications')
                platform = st.text_input(label='Platform')
                rel_date = st.text_input(label='Release Date')
                submit_button = st.form_submit_button(label='Submit')
        elif(product_type == "Accessory"):
            with st.form(key='Accessory'):
                accessory_name = st.text_input(label='Accessory name')
                length = st.text_input(label='Length')
                breadth = st.text_input(label='Breadth')
                width = st.text_input(label='Width')
                quant = st.text_input(label='Quantity')
                sub_cat = st.text_input(label='Sub-Category')
                submit_button = st.form_submit_button(label='Submit')

        if(submit_button):
            # product
            values = f"('{supplier_id}','{price}','{rating}','{desc}','{product_type}')"
            column_names = '(supplier_id, price, rating, description, type)'
            product_id = dbcommands.insert_into_table(cursor, "product", column_names, values, 'product_id')
            
            # product and accessory
            values = f"('{accessory_name}','{product_id}','{length}','{breadth}','{width}','{quant}','{sub_cat}')"
            column_names = ''
            dbcommands.insert_into_table(cursor, "address", column_names, values, 'accessory_name')
            
            # product and game
            values = f"('{game_name}','{product_id}','{genre}','{specs}','{platform}','{rel_date}')"
            column_names = ''
            dbcommands.insert_into_table(cursor, "address", column_names, values, 'accessory_name')
            
            
            st.success(f"Your product_id is : {product_id}")

    
    elif(operation == "Contest details"):
            with st.form(key='Contest'):
                game_name = st.text_input(label='Game name')
                contest_desc = st.text_input(label='Contest Description')
                start_date = st.text_input(label='Start Date')
                end_date = st.text_input(label='End Date')
                quant = st.text_input(label='Quantity')
                sub_cat = st.text_input(label='Sub-Category')
                submit_button = st.form_submit_button(label='Submit')


    elif(operation == "Insert Offer"):
        with st.form(key="offer"):
            off_desc = st.text_input(label='Offer description')
            submit_button = st.form_submit_button(label='Submit')

        if(submit_button):
            values = f"('{off_desc}')"
            column_names = '(offer_description)'
            user_id = dbcommands.insert_into_table(cursor, "offers", column_names, values, 'offer_id')
            st.success(f"The offer_id is : {user_id}")

    # elif(operation == "Update Product Details"):
    #     sup_name = st.text_input(label='Supplier Name')
    #     sup_phone = st.text_input(label='Supplier Phone')
    #     coo = st.text_input(label='Country of origin')
    #     price = st.text_input(label='Price')
    #     rating = st.text_input(label='Rating')
    #     desc = st.text_input(label='Description')
    #     off_desc = st.text_input(label='Offer description')
    #     off_et = st.text_input(label='Offer end-time')
    #     product_type = st.selectbox("Product type", (
    #     "None",
    #     "Game",
    #     "Accessory",
    #     "Contest details"
    #     ))
    #     if(product_type == "Game"):
    #         with st.form(key='Game'):
    #             game_name = st.text_input(label='Game name')
    #             genre = st.text_input(label='Genre')
    #             specs = st.text_input(label='Specifications')
    #             platform = st.text_input(label='Platform')
    #             rel_date = st.text_input(label='Release Date')
    #             submit_button = st.form_submit_button(label='Submit')
    #     elif(product_type == "Accessory"):
    #         with st.form(key='Accessory'):
    #             accessory_name = st.text_input(label='Accessory name')
    #             length = st.text_input(label='Length')
    #             breadth = st.text_input(label='Breadth')
    #             width = st.text_input(label='Width')
    #             quant = st.text_input(label='Quantity')
    #             sub_cat = st.text_input(label='Sub-Category')
    #             submit_button = st.form_submit_button(label='Submit')
    #     elif(product_type == "Contest details"):
    #         with st.form(key='Contest'):
    #             game_name = st.text_input(label='Game name')
    #             contest_desc = st.text_input(label='Contest Description')
    #             start_date = st.text_input(label='Start Date')
    #             end_date = st.text_input(label='End Date')
    #             quant = st.text_input(label='Quantity')
    #             sub_cat = st.text_input(label='Sub-Category')
    #             submit_button = st.form_submit_button(label='Submit')
    
    elif(operation == "Delete a product"):
        with st.form(key='delete product'):
            product_id = st.text_input(label='product id')
            st.dataframe(dbcommands.select_from_table(cursor, "product"))
            # delete_what = st.selectbox("Delete what?", (
            # "None",
            # "Product",
            # "Contest"
            # ))
            submit_button = st.form_submit_button(label='Delete product')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "product", "product_id", product_id))
conn.commit()
conn.close()