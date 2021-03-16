# Audio latency testing
Measuring hardware audio latency using ZEP and/or Python, using an oscilloscope.


## Hardware requirements

* Parallel port on PC
* Oscilloscope with (at least) 2 channels
  * Jumper cables for your parallel port are highly advisable
* An audiocard to test
* 3.5mm TRS jack cable

## Software requirements

* Linux (Ubuntu 20.04 used in testing)
* ZEP 2.4 (https://beexy.nl/zep/)
* Python 3 (any version should do, tested with 3.8)
  * pyparralel
  * pyaudio
    
## Hardware setup

We start by configuring your oscilloscope. This document is made with the Rigol 
DS1054 as a reference, some steps may differ if you're using something else.

You'll need 2 channels, one for the signal from the parallel port and one for 
the signal from your audio card.

### Channel 1
This channel will be used for the parallel port signal.

#### Physical connection

First, connect the probe to one of the eight data pins and the probe's ground
to one of the ground pins on your parallel port. 

In this example, the probe is connected to data pin 2 and ground pin 7:

![Channel 1 connection](readme_images/Channel1_connection.png?raw=true)

Reference pin-out:

![Parallel port pinout](
https://upload.wikimedia.org/wikipedia/commons/e/e1/25_Pin_D-sub_pinout.svg
)

#### Settings

Set these settings on your oscilloscope (press the CH1 button to get the 
settings menu):

* Coupling: DC
* Probe: 10x (Your probe might also have slider, set this to the 10x 
  position too)
* Vertical scale: 1V
* Vertical position: Doesn't really matter, but I'd recommend an offset of 
  -2V or -2.5V

Example:

![Channel 1 settings](readme_images/Channel1_settings.png?raw=true)

#### Trigger

We want to put a trigger on Channel 1, so we record from the moment the
parallel port gives a signal.

To do this, press 'Menu' in the trigger sections. Then set the following 
settings:

* Type: edge
* Source: CH1
* Slope: up
* Sweep: normal

Then, using the dial in the trigger section, set the trigger level to
a value above 1V and under 5V. A safe value to use is 4V. (I've used 3.8V in my
testing).

Lastly, set the mode to "Normal" instead of "Auto', by pressing the "Mode" 
button.

Example:

![trigger settings](readme_images/Trigger_settings.png?raw=true)


### Channel 2
This channel will be used to measure the output of the audio interface

#### Physical connection

Plug the audio cable into your interface. Then, connect the probe to the other
end. Connect the probe itself to the outer-most section, and the ground to the
inner most:

![Channel 2 connection](readme_images/Channel2_connection.png?raw=true)

#### Settings

Set these settings on your oscilloscope (press the CH2 button to get the 
settings menu):

* Coupling: AC
* Probe: 10x (Your probe might also have slider, set this to the 10x 
  position too)
* Vertical scale: 500mV
* Vertical position: 0V (thus: no offset)
  
Example:

![Channel 2 settings](readme_images/Channel2_settings.png?raw=true)

## Testing

Now that we've setup the hardware, we can start testing. This repository 
contains two different test scripts, one written in Python and the other written
using ZEP. 

The ZEP script is more consistent, but it's recommended to also run the Python
version to validate your results. 

### ZEP

First, set your horizontal scale to ``1s`` in your oscilloscope. You can zoom in 
afterwards. 

Open a terminal in the ``zep`` folder and run ``zep-2.4 audiotest.zp 
<device-id>``. 

This device ID indicates which audio device should be tested. It can be 
retrieved by running the ``zepsndinfo`` command. (The ID is the number after 
``device``).

The script will send a pulse on the parallel port at the same time the 
test-sound will be played. The script will do 4 trails, so wait till all 4 are 
done.

Once the script has run, you can zoom in by using the horizontal scale dial. 
(The scale determines the amount of time one block on the screen represents)
You can also use the horizontal position dial to scroll through the entire 
recorded signal once zoomed in.

Note: This script will only sent a small pulse on the parallel port, while 
the Python script will keep the signal 'high' for the duration of the trial.

### Python

First, set your horizontal scale to ``1s`` in your oscilloscope. You can zoom in 
afterwards. 

Open a terminal in the ``python`` folder and run ``python3 test.py
<device-index>``. 

This device index indicates which audio device should be tested. It can be 
retrieved by running the ``get_audio_devices.py`` script in the ``utils`` 
directory. 

The script will send a pulse on the parallel port at the same time the 
test-sound will be played. The script will do 4 trails, so wait till all 4 are 
done. (The number of trials can be changes by adding ``-t <number>`` as a 
parameter to the script).

Once the script has run, you can zoom in by using the horizontal scale dial. 
(The scale determines the amount of time one block on the screen represents)
You can also use the horizontal position dial to scroll through the entire 
recorded signal. 

Note: This script will keep the parallel port  signal 'high' for the duration of 
the trial, while the ZEP version will only sent a small pulse at the start 
of the trial once zoomed in.

You'll get something like this:

![Example output](readme_images/Output_example.png?raw=true)

As you can see, this card achieves a latency of ~3ms. The horizontal scale 
is set to 2s, and the signal starts about 1,5 blocks from the start of the 
signal.

## Utils

The following utility scripts are provided in the ``utils`` folder:
* ``get_audio_devices.py``: Prints all supported audio devices and their 
  device ID/index.
* ``reset_parport.py``: Resets the current value on the parallel port to 0. 
  The scripts do this themselves before running their tests, but it might be 
  handy.
* ``get_partport_value.py``: Gets the current value on the parallel port.

## Troubleshooting

### Weird signal on Channel 1
If you don't get a nice square signal on channel 1, you might've accidentally
connected the probe mirrored. The pin-out provided is misleading, when 
you're using a cable the pin-out is mirroed on it's length.

### (Python) Not authorized when opening the parallel port
Make sure your Linux user account is a member of the ``lp`` group.

You can check by running the ``groups`` command.

You can add your user to that group using this command:
``sudo adduser <full-username> lp``

### (Python) ``OSError: [Errno 6] No such device or address``
By default, the Linux kernel loads the Parallel port printer driver, which
blocks you from using the parport in the python script.

Unload this driver by running ``sudo rmmod lp``