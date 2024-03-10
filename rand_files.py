import sys
import os
import random
import zipfile
import nibabel as nib 
import numpy as np

def modify_segmentation_file(seg_file_path):
    # load the image
    img = nib.load(seg_file_path)
    # get the image data
    data = img.get_fdata()

    # Round the labels
    rounded_data = np.rint(data).astype(np.uint8)

    # Set all tumor labels (2) to 1 and everything else to 0
    # (have labels for only tumour vs no tumour)
    rounded_data[rounded_data != 2] = 0
    rounded_data[rounded_data == 2] = 1
    # create the new image
    modified_img = nib.Nifti1Image(rounded_data, img.affine, img.header)
    # save the image
    return modified_img

def create_random_files_zip(input_dir, output_zip):
    # Get a list of all subdirectories in the input directory
    subdirs = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    # Select random subdirectories
    random_dirs = random.sample(subdirs, min(100, len(subdirs)))

    # Create a zip file
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        # Add the selected files to the zip file
        for dir in random_dirs:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, input_dir)
                    if file.split(".")[-2] == "segmentation":
                        # Modify segmentation file
                        modified_img = modify_segmentation_file(file_path)
                        with io.BytesIO() as buffer:
                            nib.save(modified_img, buffer)
                            buffer.seek(0)
                            zip_file.writestr(arcname, buffer.read())
                    else:
                        zip_file.write(file_path, arcname)

    print(f'Created {output_zip} with {min(100, len(subdirs))} random files from {input_dir}')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_directory output_zip")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_zip = sys.argv[2]
    
    create_random_files_zip(input_dir, output_zip)