from donkeycar.parts.interpreter import keras_model_to_tflite

if __name__ == '__main__':
    model_path = "models/linear_with_stops_wide_cut_separate_v2_2.h5"
    tf_lite_model_path = "models/linear_with_stops_wide_cut_separate_v2_2.tflite"
    keras_model_to_tflite(model_path, tf_lite_model_path)
