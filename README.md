# Fairy Tale Mirror
> A project for the course "Human Computer Interaction" at Hochschule RheinMain in 5th semester involving a voice controlled smart mirror for children

## Features

- **Customization:** Customizable user profile to engage the user on a personal level
- **Brushing Teeth:** Motivates children to brush teeth
- **Fairy Tales:** Reads a number of locally stored fairy tales
- **Weather data:** Fetches real time weather data for responses based on that data
- **Learning Games:** Games that teach the child to read or do math

## Development

The application was build within one semester. The development process contained finding a topic, planning the software and developing this prototype.

## Hardware

- Raspberry Pi 3 Model B+
- 16GB SD-Card
- HDMI display
- Framed one-way mirror

## Requirements:

### Software requirements

Install Python and in any command line run:
```
pip install speechrecognition gtts requests pillow pyaudio playsound==1.2.2
```
You will need a window manager and desktop environment installed.

### Hardware requirements
- Speakers
- Microphone
## Usage:

Clone the repository.

In any command line, navigate to the project folder and start the program with:
```
python main.py
```