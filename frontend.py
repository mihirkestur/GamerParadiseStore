from numpy.core.fromnumeric import prod
from numpy.lib.function_base import select
import streamlit as st
from streamlit.type_util import pyarrow_table_to_bytes
st.set_page_config(page_title='GamerParadiseStore', layout = 'wide', initial_sidebar_state = 'auto')
import dbcommands
import psycopg2
import decimal
choice = st.radio("Who are you?", (
    "Developer",
    "Gamer",
    "Manager"
))

if(choice == "Developer"):
    conn = psycopg2.connect(**st.secrets["postgres"])
    cursor = conn.cursor()
    command = st.text_area(label="Enter command")
    execute = st.button(label="Execute")
    if(command != "" and execute):  
        try:
            st.table(dbcommands.execute_any_command(cursor, command))
        except Exception as e:
            st.write("Not a valid command:")
            st.error(f"{e}")
    conn.commit()
    conn.close()

elif(choice == "Gamer"):
    conn = psycopg2.connect(**st.secrets["customer"])
    cursor = conn.cursor()

    operation = st.radio("What do you want to do?", (
    "Execute any command as customer",
    "Insert Gamer Info",
    "Update Gamer Info",
    "Delete Gamer Info",
    "Purchase",
    "Participate in Contest",
    "Register Complaint"
    ))

    if(operation == "Execute any command as customer"):
        command = st.text_area(label="Enter command")
        execute = st.button(label="Execute")
        if(command != "" and execute):  
            try:
                st.table(dbcommands.execute_any_command(cursor, command))
            except Exception as e:
                st.write("Not a valid command:")
                st.error(f"{e}")

    elif(operation == "Insert Gamer Info"):
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

    elif(operation == "Update Gamer Info"):
        col_name_dict = {'First name':"first_name", 'Last name':"last_name", 'E-mail':"e_mail", 'Phone':"phone", 'Address':'address'}
        with st.form(key='Update users'):
            user_id = st.text_input(label='User id whose details are to be updated')
            option = st.selectbox(
            'What do you want to update?',
            ('None','First name', 'Last name', 'E-mail','Phone','Address'))
            if(option != 'None'):
                updated_val = st.text_input(label='Enter new value')
                if(option == 'Address'):
                    address_num = st.text_input(label='Enter address which is to be updated')
            update_button = st.form_submit_button(label='Submit')
        if(update_button):
            if(option == "Address"):

                dbcommands.update_table(cursor, "address", f"{col_name_dict[option]} = '{updated_val}'", f"user_id = {user_id} and address = '{address_num}'")
                st.success("Updated successfully!")
            else:
                print(col_name_dict[option])
                dbcommands.update_table(cursor, "users", f"{col_name_dict[option]} = '{updated_val}'", f"user_id = {user_id}")
                st.success("Updated successfully!")


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
        if (submit_button):
            values = f"('{user_id}','{comp_desc}','{comp_date}')"
            column_names = '(user_id, complaint_description, complaint_date)'
            comp_id = dbcommands.insert_into_table(cursor,'complaint',column_names,values,'complaint_id')
            st.success(f"Complaint registered, your complaint ID is {comp_id}")
    
    elif(operation == "Purchase"):
        one = decimal.Decimal(1)
        cursor.execute("""select a.product_id, accessory_name, length, breadth, width, sub_category, price
                          from accessory a, product p
                          where a.product_id = p.product_id"""
               )
        result = cursor.fetchall()
        result = [tuple(float(item) if(type(item) == type(one)) else item for item in t) for t in result]
        result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in result]
        st.table(result)

        cursor.execute("""select g.product_id, game_name, genre, specifications, platform, release_date, price
                          from game g, product p
                          where g.product_id = p.product_id"""
               )
        result = cursor.fetchall()
        result = [tuple(float(item) if(type(item) == type(one)) else item for item in t) for t in result]
        result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in result]
        st.table(result)

        user_id = st.text_input(label='User id')

        if(st.button(label="View my cart")):
            # NOTE: user_id should be cart_id. Needs to be obtained
            if user_id == '': 
                st.error("Please Enter UserID")
            else:
                command = f"""select cart_id from cart where user_id = {user_id}"""
                cursor.execute(command)
                cart_id = cursor.fetchall()[0][0]
                cursor.execute(f"""
                    select p.product_id, game_name as name, price * quantity_wished as cost, quantity_wished as QTY from 
                    product p, cart_item c, game g
                    where p.product_id = c.product_id and p.product_id = g.product_id and cart_id = {cart_id}

                    union

                    select p.product_id, accessory_name as name, price * quantity_wished as cost, quantity_wished as QTY from 
                    product p, cart_item c, accessory a
                    where p.product_id = c.product_id and p.product_id = a.product_id and cart_id = {cart_id};
                """)
                cart_contents = cursor.fetchall()
                cart_contents = [tuple(float(item) if(type(item) == type(one)) else item for item in t) for t in cart_contents]
                cart_contents = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cart_contents]
                st.table(cart_contents)

        with st.form(key='Cart item'):
            product_id = st.text_input(label='Product id')
            date_add = st.text_input(label='Date Added') ## TODO: Generate automatically
            quant_wish = st.text_input(label='Quantity wished')
            add_to_cart = st.form_submit_button(label='Add to cart')

        if(add_to_cart):
            if user_id:
                command = f"""select cart_id from cart where user_id = {user_id}"""
                cursor.execute(command)
                cart_id = cursor.fetchall()[0][0]
                if product_id and cart_id and date_add and quant_wish:
                    values = f"({product_id},{cart_id},'{date_add}','{quant_wish}')"
                    column_names = '(Product_ID, Cart_ID, Date_Added, Quantity_Wished)'
                    dbcommands.insert_into_table(cursor,"cart_item",column_names,values,'cart_id')
                    command2 = f"""select * from cart_item where cart_id = {cart_id}"""
                    st.success(f"Successfully added to cart!")
                    #st.table(dbcommands.execute_any_command(cursor,command2))
                else: st.error("Please fill all the details")
            else: st.error("Please enter UserID")
        
        with st.form(key='remove from cart'):
            product_id = st.text_input(label='Product id')
            num_item = st.text_input(label = 'count')
            remove_from_cart = st.form_submit_button(label='Remove from cart')
        
        if(remove_from_cart):
            count = int(num_item)
            command = f"""select cart_id from cart where user_id = {user_id}"""
            cursor.execute(command)
            cart_id = cursor.fetchall()[0][0]
            cursor.execute(f"select quantity_wished from cart_item where cart_id = {cart_id}")
            cur_count = cursor.fetchall()[0][0]

            if cur_count == count:
                dbcommands.delete_entry_from_table(cursor, "cart_item", "product_id", product_id)
                st.success(f"Successfully removed from cart!")
            else:
                dbcommands.update_table(cursor, "cart_item", f"quantity_wished = '{cur_count - count}'", f"cart_id = {cart_id} and product_id = {product_id}")
                st.success(f"Successfully removed from cart!") # TODO: Not working??

        if(st.button(label="View Details")):
            #select * from product as p left outer join game as g on p.product_id = g.product_id left outer join product_offers as po on po.product_id = p.product_id left outer join offers as o on o.offer_id = po.offer_id
            #select * from product as p left outer join accessory as g on p.product_id = g.product_id left outer join product_offers as po on po.product_id = p.product_id left outer join offers as o on o.offer_id = po.offer_id
            st.table(dbcommands.execute_any_command(cursor, "select p.product_id, price, rating, description, type, game_name,  genre, specifications, platform, release_date, accessory_name,  length, breadth, width, quantity, sub_category, offer_description, end_time from product as p left outer join game as g on p.product_id = g.product_id left outer join accessory as a on a.product_id = p.product_id left outer join product_offers as po on po.product_id = p.product_id left outer join offers as o on o.offer_id = po.offer_id"))
            #st.table(dbcommands.execute_any_command(cursor, "select p.product_id, price, rating, description, type, accessory_name,  length, breadth, width, quantity, sub_category, offer_description, end_time  from product as p left outer join accessory as g on p.product_id = g.product_id left outer join product_offers as po on po.product_id = p.product_id left outer join offers as o on o.offer_id = po.offer_id"))
            st.table(dbcommands.select_from_table(cursor, "product"))
            st.table(dbcommands.select_from_table(cursor, "game"))
            st.table(dbcommands.select_from_table(cursor, "accessory"))
            st.table(dbcommands.select_from_table(cursor, "product_offers"))
            st.table(dbcommands.select_from_table(cursor, "offers"))

            
        with st.form(key='Cart/Payment'):
            user_id = st.text_input(label='Confirm User id')
            pay_mode = st.text_input(label='Payment Mode')
            pay_date = st.text_input(label='Payment Date')
            buy = st.form_submit_button(label='Make payment on cart')
        if(buy):
            # insert to transaction
            command = f"""select cart_id from cart where user_id = {user_id}"""
            cursor.execute(command)
            cart_id = cursor.fetchall()[0][0]

            command3 = f"""select sum(p.price*c.quantity_wished) from product as p,cart_item as c where p.product_id = c.product_id and c.cart_id = {cart_id}"""
            amt = dbcommands.execute_any_command(cursor,command3)
            amnt_paid = amt[0][0]
            values = f"('{cart_id}','{pay_mode}','{pay_date}',{amnt_paid})"
            column_names = '(cart_id, payment_mode, payment_date, amount_paid)'
            payment_id = dbcommands.insert_into_table(cursor,'payment',column_names,values,'payment_id')
            st.success(f"your payment id is {payment_id}")
            st.table(dbcommands.select_from_table(cursor, "payment", "*", f"where payment_id = {payment_id}"))

    elif(operation == "Participate in Contest"):
        with st.form(key='Participates/Team/Belongs_to'):
            # points gained, prize won, total points
            #user_id = st.text_input(label='User id')
            contest_id = st.text_input(label='Contest Id')
            team_id = st.text_input(label='Team Id')
            submit_button = st.form_submit_button(label='Submit')
        
        if(submit_button):
            values = f"('{contest_id}','{team_id}',0,0)"
            column_names = '(contest_id, team_id, points_gained, prize_won)'
            c_id = dbcommands.insert_into_table(cursor,'participates',column_names,values, 'contest_id')
            st.success(f"team {team_id} added to contest {c_id}")
        
        st.table(dbcommands.select_from_table(cursor, "contest"))
        st.table(dbcommands.select_from_table(cursor, "team"))
    conn.commit()
    conn.close()



elif(choice == "Manager"):
    conn = psycopg2.connect(**st.secrets["manager"])
    cursor = conn.cursor()

    operation = st.radio("Select operation", (
    "Execute any command as manager",
    "Insert Product Supplier Details",
    "Update Product Supplier Details",
    "Insert Product Details",
    "Update Product Details",
    "Insert Offer",
    "Delete Offer",
    "Insert contest details",
    "Delete contest",
    "Delete a product"
    ))

    if(operation == "Execute any command as manager"):
        command = st.text_area(label="Enter command")
        execute = st.button(label="Execute")
        if(command != "" and execute):  
            try:
                st.table(dbcommands.execute_any_command(cursor, command))
            except Exception as e:
                st.write("Not a valid command:")
                st.error(f"{e}")

    elif(operation == "Insert Product Supplier Details"):
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

    
    elif(operation == "Update Product Supplier Details"):
        col_name_dict = {'Supplier Phone':"supplier_phone", 'Supplier Name':"supplier_name", 'Country of origin':"country_of_origin"}
        
        with st.form(key='Update supplier details'):
            supplier_id = st.text_input(label='supplier id whose details are to be updated')
            option = st.selectbox(
            'What do you want to update?',
            ('None','Supplier Name', 'Supplier Phone', 'Country of origin'))
            if(option != 'None'):
                updated_val = st.text_input(label='Enter new value')
            update_button = st.form_submit_button(label='Submit')
        
        st.table(dbcommands.select_from_table(cursor, "product_supplier"))
        
        if(update_button):
            print(col_name_dict[option])
            dbcommands.update_table(cursor, "product_supplier", f"{col_name_dict[option]} = '{updated_val}'", f"supplier_id = {supplier_id}")
            st.success("Updated successfully!")

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

                if(submit_button):
                    # product
                    values = f"('{supplier_id}','{price}','{rating}','{desc}','{product_type}')"
                    column_names = '(supplier_id, price, rating, description, type)'
                    product_id = dbcommands.insert_into_table(cursor, "product", column_names, values, 'product_id')
                    # product and game
                    values = f"('{game_name}','{product_id}','{genre}','{specs}','{platform}','{rel_date}')"
                    column_names = ''
                    dbcommands.insert_into_table(cursor, "game", column_names, values, 'game_name')
                    
                    
                    st.success(f"Your product_id is : {product_id}")
        
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
                dbcommands.insert_into_table(cursor, "accessory", column_names, values, 'accessory_name')
                
                
                st.success(f"Your product_id is : {product_id}")
        st.table(dbcommands.select_from_table(cursor, "product_supplier"))

    elif(operation == "Update Product Details"):
        
        col_name_dict = {'Price':"price", 'Rating':"rating",'Product description':"description",'Type':"type",
        'Game Name':"game_name", 'Genre':"genre",'Specifications':"specifications",'Platform':"platform",'Release Date':"release_date", 
        'Accessory Name':"accessory_name", 'Length':"length",'Breadth':"breadth",'Width':"width",'Quantity':"quantity", "Sub Category": "sub_category"
        }
        
        with st.form(key='Update product details'):
            product_id = st.text_input(label='Product id whose details are to be updated')
            
            option = st.selectbox(
            'What do you want to update?',
            ('None','Price', 'Rating','Product description','Type'))
            
            #if(option != 'None'):
            updated_val = st.text_input(label='Enter new value')
            update_product = st.form_submit_button(label='Update product')

            if(update_product):
                dbcommands.update_table(cursor, "product", f"{col_name_dict[option]} = '{updated_val}'", f"product_id = {product_id}")
                st.success("Updated successfully!")
                
            st.table(dbcommands.select_from_table(cursor, "product"))

        which_type = st.radio("Update type specific details, choose one", (
            "Game",
            "Accessory"
            ))

        if(which_type == "Game"):
            with st.form(key='Update game details'):
                
                option = st.selectbox(
                'What do you want to update?',
                ('None','Game Name', 'Genre','Specifications','Platform','Release Date'))
                
                #if(option != 'None'):
                updated_val = st.text_input(label='Enter new value for game details')
                update_button = st.form_submit_button(label='Update game details')
            
                if(update_button):
                    
                    dbcommands.update_table(cursor, "game", f"{col_name_dict[option]} = '{updated_val}'", f"product_id = {product_id}")
                    st.success("Updated successfully!")
            
            st.table(dbcommands.select_from_table(cursor, "game"))
        
        elif(which_type == "Accessory"):
            with st.form(key='Update accessory details'):
                option = st.selectbox(
                'What do you want to update?',
                ('None','Accessory Name', 'Length','Breadth','Width','Quantity', "Sub Category"))
                
                #if(option != 'None'):
                updated_val = st.text_input(label='Enter new value for accessory details')
                update_button = st.form_submit_button(label='Update accessory details')
            
                if(update_button):
                    
                    dbcommands.update_table(cursor, "accessory", f"{col_name_dict[option]} = '{updated_val}'", f"product_id = {product_id}")
                    st.success("Updated successfully!")
            
            st.table(dbcommands.select_from_table(cursor, "accessory"))
    
    
    elif(operation == "Insert contest details"):

        with st.form(key='Contest details'):
            game_name = st.text_input(label='Game name')
            contest_desc = st.text_input(label='Contest Description')
            start_date = st.text_input(label='Start Date')
            end_date = st.text_input(label='End Date')
            submit_button = st.form_submit_button(label='Submit')
        if(submit_button):
            values = f"('{game_name}','{contest_desc}','{start_date}','{end_date}')"
            column_names = '(game_name, contest_description, start_date, end_date)'
            contest_id = dbcommands.insert_into_table(cursor, "contest", column_names, values, 'contest_id')
            
            st.success(f"Your contest_id is : {contest_id}")

    elif(operation == "Insert Offer"):

        with st.form(key="offer"):
            off_desc = st.text_input(label='Offer description')
            submit_button = st.form_submit_button(label='Submit')

        if(submit_button):
            values = f"('{off_desc}')"
            column_names = '(offer_description)'
            user_id = dbcommands.insert_into_table(cursor, "offers", column_names, values, 'offer_id')
            st.success(f"The offer_id is : {user_id}")
    
    elif(operation == "Delete a product"):
        with st.form(key='delete product'):
            product_id = st.text_input(label='product id')
            st.table(dbcommands.select_from_table(cursor, "product"))
            submit_button = st.form_submit_button(label='Delete product')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "product", "product_id", product_id))
    
    elif(operation == "Delete Offer"):
        with st.form(key='delete offer'):
            offer_id = st.text_input(label='offer id')
            st.table(dbcommands.select_from_table(cursor, "offers"))
            submit_button = st.form_submit_button(label='Delete offer')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "offers", "offer_id", offer_id))

    elif(operation == "Delete contest"):
        with st.form(key='delete contest'):
            contest_id = st.text_input(label='contest id')
            st.table(dbcommands.select_from_table(cursor, "contest"))
            submit_button = st.form_submit_button(label='Delete contest')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "contest", "contest_id", contest_id))

    conn.commit()
    conn.close()
