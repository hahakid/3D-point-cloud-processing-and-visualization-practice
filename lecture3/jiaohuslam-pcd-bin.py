import os
import numpy as np
import open3d as o3d

def pcd_to_bin(pcd_file_path, bin_file_path):
    """
    Convert a .pcd file to .bin format (KITTI format).
    :param pcd_file_path: Path to the input .pcd file.
    :param bin_file_path: Path to the output .bin file.
    """
    # Load the PCD file using Open3D
    pcd = o3d.io.read_point_cloud(pcd_file_path)
    # Convert Open3D point cloud to numpy array (N, 3)
    points = np.asarray(pcd.points)

    # Add an intensity value of 0.0 for each point (KITTI format requires [x, y, z, intensity])
    # Assuming that the intensity is not available in the PCD, we use a default value of 0.0
    intensity = np.zeros((points.shape[0], 1), dtype=np.float32)
    points_with_intensity = np.hstack((points, intensity))

    # Write the points to a .bin file in KITTI format
    points_with_intensity.astype(np.float32).tofile(bin_file_path)

def traverse_and_convert(directory):
    """
    Traverse the directory, find each .pcd file in subfolders, and convert it to .bin format.
    """
    for root, dirs, files in os.walk(directory):
        # Sort directories to ensure consistent processing order
        dirs.sort()

        # Iterate over sorted directories
        for subdir in dirs:
            pcd_file_path = os.path.join(root, subdir, 'cloud.pcd')
            if os.path.exists(pcd_file_path):
                # Define the output .bin file path (same name as the folder)
                bin_file_path = os.path.join(root, "kitti/{subdir}.bin")
                # Convert .pcd to .bin
                pcd_to_bin(pcd_file_path, bin_file_path)
                print("Converted: {pcd_file_path} -> {bin_file_path}")

if __name__ == "__main__":
    # Replace 'your_directory_path' with the actual directory path containing the folders 000000, 000001, etc.
    directory_path = '/home/ty/catkin_ws/data/aloam_graph_refin'

    # Traverse the directory and convert all .pcd files to .bin files
    traverse_and_convert(directory_path)
    print("Conversion completed.")
