import csv
import pandas as pd
import ast

row_count = 0

"""
Extracts Goal and Feedback from Ned2 CSV file
Returns number of rows in CSV file
"""

def processCsv(input_file: str):
    output_file = "../csv_files/clean.csv"
    global row_count
    row_count = 0

    with open(input_file, newline='') as f_input, open(output_file, 'w', newline='') as f_output:
        reader = csv.DictReader(f_input)
        fieldnames = ['goal_x', 'goal_y', 'goal_z', 'goal_roll', 'goal_pitch', 'goal_yaw',
                    'feedback_x', 'feedback_y', 'feedback_z', 'feedback_roll', 'feedback_pitch', 'feedback_yaw']
        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                # Check if has missing fields
                if not row.get('goal') or not row.get('feedback'):
                    continue

                # Parse goal
                try:
                    goal_list = ast.literal_eval(row['goal'])  # converts string "[...]" to Python list
                    goal_data = {
                        'goal_x': goal_list[0],
                        'goal_y': goal_list[1],
                        'goal_z': goal_list[2],
                        'goal_roll': goal_list[3],
                        'goal_pitch': goal_list[4],
                        'goal_yaw': goal_list[5]
                    }
                except:
                    goal_data = {}
                    for line in row['goal'].splitlines():
                        for part in line.split(','):
                            key, val = part.strip().split('=')
                            goal_data[f'goal_{key.strip()}'] = float(val.strip())

                # Parse feedback
                feedback_data = {}
                for line in row['feedback'].splitlines():
                    for part in line.split(','):
                        key, val = part.strip().split('=')
                        feedback_data[f'feedback_{key.strip()}'] = float(val.strip())

                # Combine and write
                output_row = {
                    **goal_data,
                    **feedback_data
                }
                writer.writerow(output_row)
                row_count += 1

            except Exception as e:
                print(f"\n\nSkipping row due to error: {e}")
                continue 

    print(f"Clean CSV saved to {output_file}.")
    return row_count


"""
Gets the row from the given index number
Returns row as a dictionary
"""
def get_row(num: int):
    df = pd.read_csv("../csv_files/clean.csv")
    if(num > -1 and num < row_count):
        row = df.iloc[num]
        return row
    else:
        print("Invalid row. Row count is: ", row_count)
        return 