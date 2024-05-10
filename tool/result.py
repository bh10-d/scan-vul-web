array = []


result = {
    "id": 1,
    "vul": False,
    "link": "http://localhost:8080/",
    "countPayload": 10,
    # "namePayload": "asdhasd"
}
result1 = {
    "id": 2,
    "vul": True,
    "link": "http://localhost:8080/",
    "countPayload": 100,
    "payload": "asasdgajgshdhjagsgdadhasd"
}


from prettytable import PrettyTable

def showResult(result):
    # Create a PrettyTable object
    table = PrettyTable()

    # Set column names with descriptive headers
    table.field_names = ["ID", "Vulnerable", "Link", "Payload Count", "Payload"]

    array.append(result)
    # array.append(result1)

    # Add data to the table (modify if you have multiple results)
    for a in array:
        table.add_row(a.values())

    # Optional: Customize table formatting (explore PrettyTable documentation)
    # table.align = "center"  # Center-align text within columns
    # table.border = True  # Add borders around the table

    # Print the table
    print(table)
