import pandas as pd
from prettytable import PrettyTable
import datetime

customer_df = pd.DataFrame(columns=["c_id", "c_name", "phone_no", "city", "email_id"])
booking_df = pd.DataFrame(columns=["room_no", "c_id", "room_type", "checkin_date"])
room_df = pd.DataFrame(columns=["room_no", "room_type", "price_per_day", "status"])


def add_room():
    try:
        room_no = int(input("Enter room number: "))
        room_type = input("Enter room type --> (NORMAL / PREMIUM / DELUXE): ").upper()
        price_per_day = int(input("Enter price per day: "))
        
        global room_df
        if room_no in room_df["room_no"].values:
            print("Error: Room already exists.")
            return
        
        new_room = pd.DataFrame({"room_no": [room_no], "room_type": [room_type], "price_per_day": [price_per_day], "status": ["VACANT"]})
        room_df = room_df._append(new_room, ignore_index=True)
        
        print("\n****ROOM ADDED SUCCESSFULLY****")
        add_more = input("\nDo you want to add more rooms? (Y/N): ")
        if add_more.lower() == 'y':
            add_room()
        else:
            menu()
    except Exception:
        print("\n** SOME ERROR OCCURED **\n")



def add_customer():
    try:
        c_id = int(input("Enter the customer id: "))
        c_name = input("Enter the name of the customer: ")
        phone_no = input("Enter the mobile number of the customer: ")
        city = input("Enter the city of the customer: ")
        email_id = input("Enter the email id of the customer: ")
        
        global customer_df
        customer_df = customer_df._append({"c_id": c_id, "c_name": c_name, "phone_no": phone_no, "city": city, "email_id": email_id}, ignore_index=True)
        
        print("\n****CUSTOMER DATA ADDED SUCCESSFULLY****")
        
        add_more = input("\nDo you want to add more customers? (Y/N): ")
        if add_more.lower() == 'y':
            add_customer()
        else:
            menu()
    except Exception:
        print("\n** SOME ERROR OCCURED **\n")


def add_room_reservation():
    try:
        c_id = int(input("Enter the customer id: "))
        room_type = input("Enter the room type (NORMAL / PREMIUM / DELUXE): ").upper()
        checkin_date = input("Enter the check-in date (YYYY-MM-DD): ")

        global room_df, booking_df

        available_rooms = room_df[(room_df["room_type"] == room_type) & (room_df["status"] == "VACANT")]

        if available_rooms.empty:
            print("Error: No available rooms of this type.")
            return

        selected_room = available_rooms.iloc[0]["room_no"]

        booking_df = booking_df._append({"room_no": selected_room, "c_id": c_id,"room_type": room_type, "checkin_date": checkin_date}, ignore_index=True)

        room_df.loc[room_df["room_no"] == selected_room, "status"] = "OCCUPIED"

        print(f"\nRoom {selected_room} reserved successfully.")
    except Exception:
        print("\n** SOME ERROR OCCURED **\n")



def show_room_status():
    try:
        global room_df
        
        if room_df.empty:
            print("No rooms found.")
            menu()
            return

        table = PrettyTable(["Room Number", "Room Type", "Price Per Day", "Status"])
        for index, row in room_df.iterrows():
            table.add_row([row["room_no"], row["room_type"], row["price_per_day"], row["status"]])
        print(table)

        menu()  
    except Exception:
        print("\n** SOME ERROR OCCURED **\n")


def show_customer_record():
    try:
        global booking_df, customer_df

        merged_df = pd.merge(booking_df, customer_df, on="c_id")


        if merged_df.empty:
            print("No customer records found.")
            menu()
            return

        table = PrettyTable(["Customer ID", "Name", "Phone Number", "City", "Email ID", 
                             "Room Number", "Check-in Date"])

        for index, row in merged_df.iterrows():
            table.add_row([row["c_id"], row["c_name"], row["phone_no"], row["city"], row["email_id"], row["room_no"], row["checkin_date"]])
        print(table)

        menu()  
    except Exception:
        print("\n** SOME ERROR OCCURED **\n")


def make_bill():
    try:
        global customer_df, booking_df, room_df
        
        c_id = int(input("Enter customer id of customer: "))

        room_no = booking_df.loc[booking_df["c_id"] == c_id, "room_no"].iloc[0]

        checkout_date_str = input("Enter the date of checkout (YYYY-MM-DD): ")

        checkout_date = datetime.datetime.strptime(checkout_date_str, "%Y-%m-%d").date()
        checkout_datetime = datetime.datetime.combine(checkout_date, datetime.datetime.min.time())  # Convert to datetime.datetime

        checkin_date_str = booking_df.loc[(booking_df["c_id"] == c_id) & (booking_df["room_no"] == room_no), "checkin_date"].iloc[0]
        checkin_date = datetime.datetime.strptime(checkin_date_str, "%Y-%m-%d").date()

        no_of_days = (checkout_datetime - datetime.datetime.combine(checkin_date, datetime.datetime.min.time())).days  # Use the combined datetime for both dates

        price_per_day = room_df.loc[room_df["room_no"] == room_no, "price_per_day"].iloc[0]

        total_bill = no_of_days * price_per_day

        print("\nNo. of days stayed:", no_of_days)
        print("Total bill generated:", total_bill)
        print("Thanks for visiting!")

        customer_df = customer_df[customer_df["c_id"] != c_id]
        booking_df = booking_df[(booking_df["c_id"] != c_id) & (booking_df["room_no"] != room_no)]
        room_df.loc[room_df["room_no"] == room_no, "status"] = "VACANT"
        
    except Exception:
        print("\n** SOME ERROR OCCURED **\n")





def menu():
    menu_text = '''\n\t
    1. Add Rooms
    2. Add Customer Data
    3. Add Room Reservation
    4. Show Room Status
    5. Show Customer Details
    6. Make Bill
    7. Exit'''

    while True:
        print("\n\n")
        print("\t++++++++++++++++++++++++++++++++++++++++++++++++++++ ^_^  HOTEL MANAGEMENT SYSTEM  ^_^ ++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\n\n")
        print(menu_text)
        print("\n\n")
        choice = input("Enter your choice: ")
        if choice == '1':
            print('\n')
            add_room()
        elif choice == '2':
            print("\n")
            add_customer()
        elif choice == '3':
            print("\n")
            add_room_reservation()
        elif choice == '4':
            print("\n")
            show_room_status()
        elif choice == '5':
            print("\n")
            show_customer_record()
        elif choice == '6':
            print("\n")
            make_bill()
        elif choice == '7':
            print("\n")
            print("THANK YOU")
            exit()
        else:
            print("Invalid choice. Please try again.")


menu()
