from opcua import Client
from csvProcessor import processCsv, get_row

# CSV Reader
csv_path = "../csv_files/output.csv"                            # Put file path to your CSV file here

row_count = processCsv(csv_path)
print(f"There are {row_count} rows.")

# OPC UA Client
client = Client("opc.tcp://localhost:4840")
client.connect()

objects = client.get_objects_node()
operationalData = objects.get_child(["2:OperationalData"])
variables = operationalData.get_variables()

ua_x = operationalData.get_child(["2:Position_x"])
ua_y = operationalData.get_child(["2:Position_y"])
ua_z = operationalData.get_child(["2:Position_z"])
ua_roll = operationalData.get_child(["2:Roll"])
ua_pitch = operationalData.get_child(["2:Pitch"])
ua_yaw = operationalData.get_child(["2:Yaw"])

print("x = ", ua_x.get_value())
print("y = ", ua_y.get_value())
print("z = ", ua_z.get_value())
print("roll = ", ua_roll.get_value())
print("pitch = ", ua_pitch.get_value())
print("yaw = ", ua_yaw.get_value())

print("Client connected. There are ", row_count, " rows.")
print('Type "exit" to exit.')

while True:
    row_num = input("Select a row from CSV file: ")

    if row_num.lower() == "exit":
        break

    try:
        row_n = int(row_num)
        row = get_row(row_n)

        settings = input("Load Goal or Actual?: ")

        if settings.lower() == "goal" or settings.lower() == "g":
            ua_x.set_value(row["goal_x"])
            ua_y.set_value(row["goal_y"])
            ua_z.set_value(row["goal_z"])
            ua_roll.set_value(row["goal_roll"])
            ua_pitch.set_value(row["goal_pitch"])
            ua_yaw.set_value(row["goal_yaw"])
            print("Updated OperationalData to Goal values.")

        elif settings.lower() == "actual" or settings.lower() == "a":
            ua_x.set_value(row["feedback_x"])
            ua_y.set_value(row["feedback_y"])
            ua_z.set_value(row["feedback_z"])
            ua_roll.set_value(row["feedback_roll"])
            ua_pitch.set_value(row["feedback_pitch"])
            ua_yaw.set_value(row["feedback_yaw"])
            print("Updated OperationalData to Acutal values.")
            
        else:
            print("Invalid input.")
            print("OperationalData:")


        print("x = ", ua_x.get_value())
        print("y = ", ua_y.get_value())
        print("z = ", ua_z.get_value())
        print("roll = ", ua_roll.get_value())
        print("pitch = ", ua_pitch.get_value())
        print("yaw = ", ua_yaw.get_value())

    except ValueError:
        print("Invalid number, try again.")

client.disconnect()
