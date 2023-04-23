# About this folder

This folder does not contain any code that makes the robot do anything.
This code doesn't make the robot faster. It doesn't make the robot more accurate.

Rather, this code is purely some modifications / abstractions upon wpilib to make it easier
to understand for our students and easier to teach by our mentors.

### coroutine
This is a full wrapper around the command framework that makes it more pythonic by
accepting coroutines (generators) wherever callbacks or commands are accepted.
Vasista hopes to get this stuff officially into robotpy for 2024.

### customcontroller
This is a custom implementation of WPILib's CommandXboxController that works with the
coroutine commands wrapper.

### robotview
This makes a read-only view of any object passed into it.