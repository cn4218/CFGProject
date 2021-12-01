import requests
import json


def get_availability_by_date(date):
    result = requests.get(
        "http://127.0.0.1:5001/availability/{}".format(date),
        headers={"content-type": "application/json"},
    )
    return result.json()


def add_new_booking(date, stylist, time, customer):

    booking = {
        "_date": date,
        "teamMember": stylist,
        "time": time,
        "customer": customer,
    }

    result = requests.put(
        "http://127.0.0.1:5001/booking",
        headers={"content-type": "application/json"},
        data=json.dumps(booking),
    )

    return result.json()


def display_availability(records):
    # Print the names of the columns.
    print(
        "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
            "NAME", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18"
        )
    )
    print("-" * 105)

    # print each data item.
    for item in records:
        print(
            "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
                item["name"],
                item["12-13"],
                item["13-14"],
                item["14-15"],
                item["15-16"],
                item["16-17"],
                item["17-18"],
            )
        )


# CALL`nano`.`filldates`(20210701,20210705,'Peter');
# CALL`nano`.`filldates`(20210703,20210707,'Maddie');

def run():
    print("############################")
    print("Hello, welcome to our salon")
    print("############################")
    print()
    date = input("What date you would like to book your appointment for (YYYY-MM-DD): ")
    print()
    slots = get_availability_by_date(date)
    print("####### AVAILABILITY #######")
    print()
    display_availability(slots)
    print()
    place_booking = input("Would you like to book an appointment (y/n)?  ")

    book = place_booking == "y"

    if book:
        cust = input("Enter your name: ")
        stylist = input("Choose stylist (Peter, Maddie, Dominic): ")
        time = input("Choose time based on availability (e.g 15-16): ")
        add_new_booking(date, stylist, time, cust)
        print("Booking is Successful")
        print()
        slots = get_availability_by_date(date)
        display_availability(slots)

    print()
    print("See you soon!")


if __name__ == "__main__":
    run()