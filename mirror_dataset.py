import os
import json
from distutils.dir_util import copy_tree

import cv2
import tqdm


def main(tub_path: str):
    tub_mirrored_path = tub_path.rstrip("/") + "_mirrored"
    images_mirrored_path = tub_mirrored_path + "/images"
    copy_tree(tub_path, tub_mirrored_path)
    print("Copy to", tub_mirrored_path)
    for file in tqdm.tqdm(os.listdir(images_mirrored_path)):
        image_path = os.path.join(images_mirrored_path, file)
        img = cv2.imread(image_path)
        if img is not None:
            img = cv2.flip(img, 1)
            cv2.imwrite(image_path, img)
    for file in tqdm.tqdm(os.listdir(tub_mirrored_path)):
        if file.endswith("catalog"):
            catalog_path = os.path.join(tub_mirrored_path, file)
            output_lines = []
            with open(catalog_path) as catalog_file:
                catalog_file_lines = catalog_file.readlines()
            for line in catalog_file_lines:
                line_json = json.loads(line)
                line_json["user/angle"] *= -1
                output_lines.append(json.dumps(line_json))
            with open(catalog_path, "w") as catalog_file:
                catalog_file.write("\n".join(output_lines))


if __name__ == '__main__':
    main("data/no_car_or_pedestrian")
