import os
import random
import zipfile

def modify_segmentation_file(seg_file_pat):
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

# Set the directory path
dir_path = '/Users/ephraimmeiri/gitEtc/nnUNet/resized1/all_cases'

# Get a list of all files in the directory
# all_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
subdirs   = [os.path.join(dir_path, d) for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

print(len(subdirs))
# Select 100 random files
random_dirs = random.sample(subdirs, 100)

# Create a zip file
zip_filename = '/Users/ephraimmeiri/gitEtc/nnUNet/resized1/random_files.zip'
with zipfile.ZipFile(zip_filename, 'w') as zip_file:
    # Add the selected files to the zip file
    for dir in random_dirs:
        for root, dirs, files in os.walk(dir):
            case= root.split('/')[-1]
            print(case)
            for file in files:
                # print()
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dir_path)
                if(file.split(".")=="segmentation"):
                    modified_img= modify_segmentation_file(file_path)
                    with io.BytesIO() as buffer:
                        nib.save(modified_img, buffer)
                        buffer.seek(0)
                        zip_file.writestr(arcname, buffer.read())
                else:   
                    zip_file.write(file_path,arcname)

print(f'Created {zip_filename} with 100 random files from {dir_path}')

