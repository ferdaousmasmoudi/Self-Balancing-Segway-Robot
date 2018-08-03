# Balancing-Robot-RaspberryPi
This is my project for balancing an inverted pendulum using a Raspberry Pi. The main aim of the project is to learn about the following topics
- Gain an insight into the physics of the problem and understand the equation of motions. I have used [this](https://content.sciendo.com/view/journals/meceng/61/2/article-p331.xml) paper and followed [this](https://www.coursera.org/learn/mobile-robot) course. 
- Learn about classic and modern control theories. [Source](https://www.youtube.com/watch?v=Pi7l8mMjYVE&list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m)
- Learn about concepts like controllability, observability, LQR technique to derive controller gain. [Source](https://www.youtube.com/watch?v=Pi7l8mMjYVE&list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m)
- Learn and code my own Kalman Filter for Sensor Fusion. I struggled a lot to find sources that explained it from the very basics and finally found some good reads. Sources [1](https://home.wlu.edu/~levys/kalman_tutorial/), [2](http://blog.tkjelectronics.dk/2012/09/a-practical-approach-to-kalman-filter-and-how-to-implement-it/) and [3](https://github.com/balzer82/Kalman/blob/master/Kalman-Filter-CV.ipynb?create=1).
- Check how do Kalman and Complimentary filters compare with each other.
- Learn how to implement the learned concepts on actual hardware and understand the problems encountered.
- Learn how to make RaspberryPi communicate with arduino over Serial port. [Source](http://forum.arduino.cc/index.php?topic=396450)
- Learn how to use rotory encoders to get RPM of a motor and smoothen the data. Info about using encoders can be found [here](https://www.youtube.com/watch?v=oLBYHbLO8W0). For smoothing I have used exponential averaging filter.
- Info about dc motor control can be found [here](https://www.bluetin.io/python/gpio-pwm-raspberry-pi-h-bridge-dc-motor-control/). Info about using MPU6050 library on a RaspberryPi can be found [here](https://libraries.io/pypi/mpu6050-raspberrypi). Info about using various builtin classes on RaspPi can be found [here](https://projects.raspberrypi.org/en/projects/physical-computing/16). 
