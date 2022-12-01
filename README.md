# self-driving-donkey-car

_**Main contributors: Yevhen Pankevych, Volodymyr Savchuk**_
![IMG_0892_11zon](https://user-images.githubusercontent.com/56469845/204942743-5209e196-49d0-4a67-8e27-e92aac59e632.png)



## Introduction 

This blogpost is a project report from the Autonomous vehicles project course, and the actual participation 
in the DeltaX Competition and the creation of an autopilot for a donkey car built on the basis of a Raspberry pi 4 and a camera.  
Project requirements:
 * control of car turns (1)
 * passing a static route in a circle in both directions (2)
 * bypassing obstacles with an unfixed location (3)
 * stopping the car at a stop sign (4)
 * stopping the car in the presence of a pedestrian at the crossing (5)
 * stopping the car on the condition of passing another car at the intersection according to the right-of-way rule (6)

We decided to start from the basics and to solve the tasks 1-3, which allow the car to just follow the 
track avoiding the obstacles and without any stopping conditions. The next challenge we solved was for a car to handle stopping conditions. 


## Data collection

Actually, data collection took us 70% percent of time working on a project. 
![IMG_0868_11zon](https://user-images.githubusercontent.com/56469845/204942878-5e86f6eb-b8b6-450d-9bb6-880d23cb9634.png)
![IMG_0865_11zon](https://user-images.githubusercontent.com/56469845/204942893-948a8531-8143-4526-84cd-7fe615125c14.png)
In the first iteration, we collected a rather unbalanced dataset - there were many images with forward motion, and a certain number with motion to extreme rotation angles, and almost no images with intermediate values of rotation. As it turned out during training, when supplementing with data from intermediate values, the model began to work a little smoother and more stably. Therefore, the additional collection of datasets was aimed at diversifying the data.

Sometimes we noticed that on some part of the track our car makes the mistake again and again. The simplest solution was to collect more data exactly on that place of the track. We trained the model again with additional data and it improved the performance in that particular place. We iterated dozens of times and it helped to collect a balanced dataset. I mean we really go through all the possible cases!

![IMG_0879_11zon](https://user-images.githubusercontent.com/56469845/204942907-5877f83d-3517-4de6-9043-f178e7ca6edb.png)
Okay last one is a joke)))

In addition to data for actual driving, we collected data for stops (pedestrians on the crosswalk, another car on the right, stop sign). We collected them without adjusting the angle of rotation of the wheels (just holding the machine in place by hand), so the steering data on these samples is invalid and may affect the behavior of the turning model.

Also we did some data augmentation. We have done vertical flip(data mirroring), which allowed us to make the dataset 2 times bigger. In the result we got around 130k images.

## Models

During the training, we had two stages of working with the models. 
The first is working with driving models that form turning angles, 
and the second is stopping models under different conditions. 
Let's start with the first stage.

### Driving models

The first iteration of the work was the use of built-in model architectures from the Donkey library. We worked with a linear model. The architecture of the model can be seen below.

![our team](https://drive.google.com/uc?export=view&id=1sDtR4qYvJ4_bACUYD3hufAK4r5M2o_hI)

A slightly modified [PilotNet model](https://github.com/lhzlhz/PilotNet) was also tested. The architecture is shown below.
![our team](https://drive.google.com/uc?export=view&id=1FjW0Ll2-wysLdldq7viJbHsSVT23fqmL)

As the tests showed, although the PilotNet performed on average faster than the linear model, the linear model gave more timely turns and less interference with obstacles. In addition, after converting to tflite format, the execution time of both models decreased and became quite similar, so it was decided to continue to use the linear model architecture as the model to control the turns.

### Stop models

The second stage was the introduction of additional logic to recognize stop conditions. The first attempt was to simply add a branch after a few convolutional layers and introduce additional layers and one additional output that simply predicts whether to stop at the current moment. The architecture is shown below.
![our team](https://drive.google.com/uc?export=view&id=1_J7q17I9999dRoozSq4z7W5EvA5fcSqF)

### Separate stop models for every stop conditions

Previous models with introduced stop conditions had quite good results, but there were still a lot of mistakes before the crosswalk. For example, sometimes it stops, but there was no pedestrian on a crosswalk, same mistakes were for other stop conditions. We decided to introduce the new logic in building our model. Actually we have made four separate models. First predicts steering, second predicts the Stop Sign presence, third predicts Pedestrian presence on a crosswalk, fourth predicts Right Side Car presence. We created four models, but DonkeyCar perceives it still as the one model, because it could work only with one. Also we added a separate cropping layer to each of the models. For example: for the Right Side Car we added cropping only the right-bottom part of the image, for Stop Sign we didn’t add any cropping, for Pedestrian on a crosswalk we added only crop to the upper half of the image. This model performed a lot better than the previous, but there were still some mistakes according to the Pedestrian on a crosswalk stopping condition.

![our team](https://drive.google.com/uc?export=view&id=1I-1pKCJ9ZUCGO2zQIjtubc8Pufu-miKH)

### Improved separate stop models
We decided to add one more convolution layer and adjusted the crop of the “Pedestrian on a crosswalk” model. This worked well! Now the model stops correctly at all stopping conditions and drives smoothly on a track!
![our team](https://drive.google.com/uc?export=view&id=1xqpjrsOSi8iPTB2ehCgxMnDoca77RDDK)


## Training points

### GPU problems
For training, we wanted to use the GPU installed in our laptop, an RTX 3060 Laptop, which is built on the Ampere architecture and uses CUDA 11 and cuDNN 8. However, during the training process, we encountered a strange problem. The training process itself was quite strange - the loss was too high and almost did not change (you can see in the graphs below).
![our team](https://drive.google.com/uc?export=view&id=17_ynJcmxcs-fhLSJVo9U0VDx2ll8yiV1)
After training, the model "froze" - when we tried to predict values ​​on any input data, it gave almost identical results. When we ran the trained model on the CPU, we got NaN instead of the results. We got the same NaN values when we ran the trained model on Raspberry.

Then we tried to train the model on the CPU and the problem disappeared - the loss started to behave normally (see graph below) and real values started to appear on the CPU and Raspberry.
![our team](https://drive.google.com/uc?export=view&id=1sImHECWQAtlSLLNC9qKlnP73XsL5ruS4)
For a while, we couldn't solve the problem with the GPU. However, reinstalling the environment manually and changing the version of Tensorflow to a newer version solved the problem. As it turns out, the donkey environment uses Tensorflow 2.2, which only works with CUDA 10 and cuDNN 7. There was a conflict and probably the graphics card was loading the data incorrectly, causing the training to work incorrectly. So when we installed the new version of Tensorflow 2.9, the training process started working. However, a new problem arose - the model format between Tensorflow 2.9 (on the laptop) and Tensorflow 2.2 (on the Raspberry) is incompatible. This was solved by installing the latest available version of Tensorflow 2.4 on Raspberry.

### Training on cluster 

In order to speed up the work process and to be able to train several model variants at the same time, we requested access to the university's rocket cluster.  Access was granted. Then, with the help of the SLURM system, we started to create training tasks on the nodes of the pegasus type, since they are equipped with Nvidia Tesla GPUs.

### Two-Step Training

For solving the problem of stopping before stopping conditions we introduced two-step training. In the first stage, we train only the part of the model that is responsible for turning angles and use the data that contains only the driving process. At this point, we freeze the parts of the model corresponding to the stopping condition. After this training, we retrain the model with the same weights, but freeze the driving part of the model, instead updating the weights only for the stop models, using data with different stop conditions. In this way, we get a trained movement model and stop models.

## Results:

![Stop Sign One Direction](https://drive.google.com/file/d/1d9yG5tPl3bv6fO8Gf8YeWWMEOVZfkkrR/view?usp=sharing)
![Stop Sign Opposite Direction](https://drive.google.com/file/d/1WjwqWQXFzXb_H83h1KCs5WmSLjcpooNP/view?usp=sharing)
![Right Side Car](https://drive.google.com/file/d/1_67PnDQh4MBNoINuRF0GStAnFWP8zUZJ/view?usp=sharing)
![Pedestrian + Left Side Car](https://drive.google.com/file/d/1tIgGxVGBcvRxKx16Cb20XLj2pQ7n4EjN/view?usp=sharing)
![Pedestrian Opposite Direction](https://drive.google.com/file/d/1usGlsu0dj1t3P98rFtADU2WxV-SoUWGR/view?usp=sharing)
![Just Following Track](https://drive.google.com/file/d/1r8IeQSGxHCGHfuOi6e6oSKZ1Ox_PXmbJ/view?usp=sharing)
