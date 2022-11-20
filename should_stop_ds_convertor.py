import os

import tqdm


def main(tub_path: str):
    manifest_path = tub_path + "/manifest.json"
    with open(manifest_path) as f:
        lines = f.readlines()
    lines[0] = lines[0][:-2] + ", \"user/should_stop\"]\n"
    lines[1] = lines[1][:-2] + ", \"int\"]\n"
    with open(manifest_path, "w") as f:
        f.writelines(lines)

    for file in tqdm.tqdm(os.listdir(tub_path)):
        if file.endswith(".catalog"):
            total_path = tub_path + "/" + file
            with open(total_path) as f:
                lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i][:-2] + ", \"user/should_stop\": 1}\n"
            with open(total_path, "w") as f:
                f.writelines(lines)


if __name__ == '__main__':
    main("data/pedestrian")
    main("data/pedestrian_mirrored")
    main("data/right_side_car")
