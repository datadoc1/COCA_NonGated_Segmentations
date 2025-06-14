# COCA_Segmentations: Coronary Artery Calcium Segmentation Dataset

## Introduction
This repository contains a novel, publicly available dataset of 203 non-gated chest CT scans with expert-verified segmentations of coronary artery calcium (CAC) and adjacent structures. The dataset is designed to facilitate the development of AI models for opportunistic cardiovascular risk assessment by providing comprehensive, location-specific annotations.

### Key Features
- **203 non-gated chest CT scans** from the Stanford AIMI COCA dataset
- **1,649 distinct calcium instances** across 8 anatomical classes
- **Expert-verified segmentations** reviewed by a radiologist
- **Comprehensive annotations** covering both coronary arteries and adjacent structures
- **YOLO format labels** for machine learning applications

The dataset enables the development of next-generation AI models capable of anatomically precise, clinically relevant cardiovascular risk stratification.

## Dataset Structure
The repository contains the following directories:

- `/nrrd`: Contains original NRRD segmentation files (provided)
- `/yolo` directory will be automatically created when running the conversion script, containing:
  - `/train_labels`: YOLO format labels for training (171 scans)
  - `/val_labels`: YOLO format labels for validation (42 scans)

### Dataset Characteristics
The dataset contains 1,649 distinct calcium instances across 203 scans with the following distribution:

| Category               | Segmentations | Patients | Mean Volume (mm³) | Volume SD (mm³) | Segmentations/Scan | Dataset % | Patients % |
|------------------------|---------------|----------|-------------------|-----------------|---------------------|-----------|------------|
| Posterior Descending   | 21            | 5        | 566.3             | 701.5           | 4.20                | 1.27%     | 2.46%      |
| Left Main Coronary     | 29            | 12       | 220.2             | 247.9           | 2.42                | 1.76%     | 5.91%      |
| Left Anterior Descending | 115          | 40       | 271.6             | 439             | 2.88                | 6.97%     | 19.70%     |
| Left Circumflex        | 51            | 18       | 223.5             | 362.7           | 2.83                | 3.09%     | 8.87%      |
| Mitral Valve           | 50            | 13       | 834.5             | 1059.9          | 3.85                | 3.03%     | 6.40%      |
| Thoracic Aorta         | 1132          | 91       | 1525.2            | 3921.3          | 12.44               | 68.65%    | 44.83%     |
| Aortic Valve           | 108           | 23       | 963               | 2147.3          | 4.70                | 6.55%     | 11.33%     |
| Right Coronary         | 143           | 25       | 629.7             | 1060.6          | 5.72                | 8.67%     | 12.32%     |

*Table 1: Calcium Instances per Anatomical Classification*

Key observations:
- Significant class imbalance with Thoracic Aorta representing 68.65% of instances
- Posterior Descending and Left Main Coronary are the least represented classes
- Thoracic Aorta calcifications are largest on average (1525.2 mm³)
- Left Main Coronary calcifications are smallest on average (220.2 mm³)

## Converting NRRD to YOLO Format
The `nrrd_to_yolo.py` script converts NRRD segmentation files to YOLO format labels. This script is provided for transparency and to enable customization.

### Prerequisites
- Python 3.8+
- Required packages: `pynrrd`, `numpy`, `scipy`

Install dependencies:
```bash
pip install pynrrd numpy scipy
```

### Usage
Run the conversion script:
```bash
python nrrd_to_yolo.py
```

The script will:
1. Read `train_test_split.csv` to determine train/validation split
2. Process all NRRD files in `/nrrd`
3. Create the `/yolo` directory structure
4. Generate YOLO label files in `/yolo/train_labels` and `/yolo/val_labels`

### Output Format
Each YOLO label file (e.g., `9_1.txt`) contains:
- One line per calcium instance
- Each line: `class_id center_x center_y width height`
- Coordinates normalized to [0, 1]

## Using the Dataset for Training
To train a YOLO model using this dataset:

1. **Prepare images**: Convert DICOM to PNG/JPG (not included in this repo)
2. **Organize directories**:
   ```
   dataset/
     train/
        images/
        labels/
     val/
        images/
        labels/
   ```
3. **Create dataset.yaml**:
   ```yaml
   path: /path/to/dataset
   train: train/images
   val: val/images
   names:
     0: calcium
   ```

## Baseline Model Performance
A baseline YOLOv8-Seg model achieved:
- Mask mAP50: 14.4%
- Mask mAP50-95: 6.1%

This demonstrates the dataset's utility while highlighting the challenge of precise calcium segmentation.

## Citation
If you use this dataset, please cite the original paper:

```bibtex
@article{coca_segmentations_2025,
  title={An Open-Source Dataset for Coronary Artery Calcium Segmentation in Non-Gated Chest CT},
  author={},
  journal={},
  year={2025}
}
```

## License
This dataset and code are released under the MIT License.

## Acknowledgements
Data sourced from the Stanford AIMI COCA dataset: [https://aimi.stanford.edu/datasets/coca-coronary-calcium-chest-ct](https://aimi.stanford.edu/datasets/coca-coronary-calcium-chest-ct)