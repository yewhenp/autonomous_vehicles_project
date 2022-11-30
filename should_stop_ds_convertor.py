import os

import tqdm


def main(tub_path: str, inserter="user/should_stop"):
    manifest_path = tub_path + "/manifest.json"
    with open(manifest_path) as f:
        lines = f.readlines()
    lines[0] = lines[0][:-2] + f", \"{inserter}\"]\n"
    lines[1] = lines[1][:-2] + ", \"int\"]\n"
    with open(manifest_path, "w") as f:
        f.writelines(lines)

    for file in tqdm.tqdm(os.listdir(tub_path)):
        if file.endswith(".catalog"):
            total_path = tub_path + "/" + file
            with open(total_path) as f:
                lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i][:-2] + f", \"{inserter}\": 1" + "}\n"
            with open(total_path, "w") as f:
                f.writelines(lines)


if __name__ == '__main__':
    # main("data/pedestrian", inserter="user/pedestrian")
    # main("data/pedestrian_mirrored", inserter="user/pedestrian")
    # main("data/right_side_car", inserter="user/right_side_car")
    # main("data/stop_sign", inserter="user/stop_sign")
    # main("data/pedestrian_5", inserter="user/pedestrian")
    # main("data/right_side_car_4", inserter="user/right_side_car")
    main("data/stop_sign_2", inserter="user/stop_sign")
