import os
import nrrd
import numpy as np
from scipy import ndimage
import csv

def main():
    # Read train/test split
    split_dict = {}
    with open('train_test_split.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exam_id = int(row['exam'])
            split_dict[exam_id] = row['split']
    
    # Create output directories
    os.makedirs('yolo/train_labels', exist_ok=True)
    os.makedirs('yolo/val_labels', exist_ok=True)
    
    # Process each NRRD file
    for filename in os.listdir('nrrd'):
        if not filename.endswith('.nrrd'):
            continue
            
        # Extract exam ID from filename
        try:
            exam_id = int(filename.split('_')[-1].split('.')[0])
        except ValueError:
            print(f"Skipping {filename} - could not extract exam ID")
            continue
            
        # Determine output directory based on split
        split = split_dict.get(exam_id)
        if not split:
            print(f"Skipping exam {exam_id} - not in train_test_split.csv")
            continue
            
        # Map 'test' to 'val' since our directory is 'val_labels'
        split_dir = 'val' if split == 'test' else split
        output_dir = f"yolo/{split_dir}_labels"
        
        # Read NRRD file
        data, header = nrrd.read(os.path.join('nrrd', filename))
        
        # Get segment names and label values
        segments = {}
        for key, value in header.items():
            if key.startswith('Segment') and key.endswith('_LabelValue'):
                seg_index = key.split('_')[0][7:]
                seg_name = header.get(f'Segment{seg_index}_Name')
                if seg_name:
                    segments[int(value)] = seg_name
        
        # Process each slice
        depth = data.shape[2]  # Z dimension
        for z in range(depth):
            slice_data = data[:, :, z]
            slice_filename = f"{exam_id}_{z+1}.txt"
            output_path = os.path.join(output_dir, slice_filename)
            
            with open(output_path, 'w') as f_out:
                # Find unique labels in slice (exclude background=0)
                unique_labels = np.unique(slice_data)
                for label in unique_labels:
                    if label == 0 or label not in segments:
                        continue
                        
                    # Create mask for this segment
                    mask = (slice_data == label)
                    
                    # Find connected components (individual instances)
                    labeled, num_instances = ndimage.label(mask)
                    for i in range(1, num_instances + 1):
                        instance_mask = (labeled == i)
                        
                        # Get bounding box coordinates
                        coords = np.argwhere(instance_mask)
                        y_min, x_min = coords.min(axis=0)
                        y_max, x_max = coords.max(axis=0)
                        
                        # Convert to YOLO format (normalized center x,y and width,height)
                        width = x_max - x_min
                        height = y_max - y_min
                        center_x = (x_min + width / 2) / slice_data.shape[1]
                        center_y = (y_min + height / 2) / slice_data.shape[0]
                        width_norm = width / slice_data.shape[1]
                        height_norm = height / slice_data.shape[0]
                        
                        # Write to file (class 0 for all segments since it's binary segmentation)
                        f_out.write(f"0 {center_x:.6f} {center_y:.6f} {width_norm:.6f} {height_norm:.6f}\n")

if __name__ == "__main__":
    main()