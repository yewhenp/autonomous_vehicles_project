import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import donkeycar as dk
from donkeycar.parts.interpreter import keras_model_to_tflite

# [
# high_resolution_enable
# high_resolution_steering
# throttle
# steering
# pedestrian_start
# pedestrian
# right_side_car
# stop_sign
# ]

if __name__ == '__main__':
    model_path = "models/new_car_3.h5"
    tf_lite_model_path = "models/new_car_3.tflite"
    keras_model_to_tflite(model_path, tf_lite_model_path)
    # tf.lite.experimental.Analyzer.analyze(model_path=tf_lite_model_path)
    # model = tf.keras.models.load_model(model_path)
    # model.compile()
    # model.save(h5_store_model_path)

    # cfg = dk.load_config()
    # kl = dk.utils.get_model_by_type("linear_with_stops_wide_cut_separate_v3_with_high_resolution", cfg)
