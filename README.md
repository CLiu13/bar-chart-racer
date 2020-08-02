# Animated Bar Chart Racer

## Description

This animated bar chart racer visualizes how a dataset changes over time. It displays bar charts for each point in time and maintains them in sorted order, so as the value of one bar surpasses another, the bars switch and they appear to be “racing” (see the example below). 

Our implementation provides an interface that allows the user to:
 - import data by uploading a csv file
 - choose values for parameters such as chart title, axis labels, and frame count (to customize the speed of animation)
 - choose a color to customize the chart theme
 - view and export the final animation as a gif or mp4 file

This program was coded in Python, using tkinter for the interface, pandas for data processing, and matplotlib for graphing and animation.

## Examples

### Animation gifs
![example gif](examples/example-1.gif)
![example gif](examples/example-4.gif)

You can find more examples of saved animations in the [examples](/examples) folder.

### Demonstration video
[![Demo Video](https://img.youtube.com/vi/Asjtc1Ev0e8/default.jpg)](https://youtu.be/Asjtc1Ev0e8)

This video was created for CodeLabs Demo Day and provides a brief demonstration of using the program.

## Authors and acknowledgement
This program was created as part of CodeLabs, an internship through CodeDay. Our interns are [Anusha Puri](https://github.com/puria123), [Lina Chihoub](https://github.com/linasc3-ai), and [Kirsten Graham](https://github.com/kirstenmg). Our mentor is [Charlie Liu](https://github.com/CLiu13).