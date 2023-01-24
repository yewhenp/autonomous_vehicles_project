import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf

if __name__ == '__main__':
    # model_from_path = "models/linear_with_stops_wide_cut_separate_v2_2.h5"
    model_from_path = "models/linear_with_stops_wide_cut_separate_v3_with_high_resolution_final_1.h5"
    model_to_path = "models/linear_with_stops_wide_cut_separate_v3_with_high_resolution_final_1.h5"
    model_save_path = "models/linear_with_stops_wide_cut_separate_v3_with_high_resolution_final_2.h5"
    layer_pattern = "stop_sign"

    model_from = tf.keras.models.load_model(model_from_path)
    model_to = tf.keras.models.load_model(model_to_path)

    for l_from in model_from.layers:
        if layer_pattern in l_from.name:
            weights = l_from.get_weights()
            for l_to in model_to.layers:
                if l_to.name == l_from.name:
                    l_to.set_weights(weights)
                    print(f"setting weights for {l_from.name}")
                    break

    model_to.save(model_save_path)
