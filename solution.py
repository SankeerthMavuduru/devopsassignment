import os
import xml.etree.ElementTree as ET
import pandas as pd
from zipfile import ZipFile
import shutil

# Directory containing XML files
data_dir = 'C:/Users/saisa/Downloads/devops-assignment-main/devops-assignment-main/programming/assignment-1/data'
# entries = os.listdir(data_dir)
# print(entries)
# Dictionary to store aggregated time by classname
time_by_classname = {}

# Parse XML files and aggregate time
for filename in os.listdir(data_dir):
    if filename.endswith('.xml'):
        file_path = os.path.join(data_dir, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        classname = filename[5:len(filename)-4]
        total_time = 0

        for testcase in root.findall('testcase'):
            time = float(testcase.get('time'))
            total_time += time
        
        if classname in time_by_classname:
            time_by_classname[classname] += total_time
        else:
            time_by_classname[classname] = total_time

# Convert dictionary to DataFrame
df = pd.DataFrame(list(time_by_classname.items()), columns=['classname', 'time'])

# Sort DataFrame by time in descending order
df = df.sort_values(by='time', ascending=False).reset_index(drop=True)

# Create groups
df['groupNo'] = pd.qcut(df['time'].cumsum(), q=5, labels=False) + 1

# Output to CSV
csv_output_path = 'C:/Users/saisa/Downloads/devops-assignment-main/devops-assignment-main/programming/assignment-1/data/sample_output.csv'
df.to_csv(csv_output_path, index=False)
print("csv is done")
# Zip the programming folder
directory_path='C:/Users/saisa/Downloads/devops-assignment-main/devops-assignment-main/programming'
zip_file_path='C:/Users/saisa/Downloads/programming.zip'
with ZipFile(zip_file_path, 'w') as zipf:
    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        # Add the directory (and its subdirectories and files) to the ZIP file
        for file in files:
            # Create the full file path
            file_path = os.path.join(root, file)
            # Create a relative path within the ZIP file
            relative_path = os.path.relpath(file_path, directory_path)
            # Write the file to the ZIP file
            zipf.write(file_path, relative_path)

print(f"CSV file has been created at {csv_output_path}")
print(f"ZIP file has been created at {zip_file_path}")
