import os

def read_data_file(data_file_path):
    """
    Reads the 8th, 9th, and 10th lines from a given data file.
    Each line contains four numbers. This function returns these numbers as a single combined list.
    """
    lines = []
    try:
        with open(data_file_path, 'r') as f:
            all_lines = f.readlines()
            # Read the 8th, 9th, and 10th lines (index starts from 0)
            lines = all_lines[7:10]  # [7] = 8th line, [8] = 9th line, [9] = 10th line

    except Exception as e:
        print("Error reading file")
    
    combined_values = []
    for line in lines:
        print(line)
        # Split the line by whitespace and extend the combined values list
        combined_values.extend(line.strip().split())
    print(combined_values, "/n")
    return combined_values

def traverse_and_write(directory, output_file):
    """
    Traverse the directory, find each 'data' file in subfolders, read the required lines,
    and write them into the output file.
    """
    with open(output_file, 'w') as pose_file:
        for root, dirs, files in os.walk(directory):
            # Sort the directories to ensure the traversal order is consistent
            dirs.sort()  # Sort dirs in place to ensure consistent traversal
            if 'data' in files:
                data_file_path = os.path.join(root, 'data')
                # Read the 8th, 9th, and 10th lines from the data file
                values = read_data_file(data_file_path)
                # Write these values to the output file as a single line
                pose_file.write(' '.join(values) + '\n')

if __name__ == "__main__":
    # Replace 'your_directory_path' with the actual directory path containing the folders 000000, 000001, etc.
    directory_path = '/home/ty/catkin_ws/data/aloam_more_refin'
    output_pose_file = 'poses.txt'

    # Traverse the directory and write the pose file
    traverse_and_write(directory_path, output_pose_file)
    print("Data successfully written to {output_pose_file}")
