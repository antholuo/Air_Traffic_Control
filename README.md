# SpaceRyde ATC Challenge
Hi there! My name is Anthony Luo and this is my submission for the SpaceRyde ATC Challenge.

The code was written in Python, simply because of the simplicity and speed with which it was possible to finish the challenge. Functionally, the code should be able to translate to C++ as we make use of many of the same fundamental concepts.

> **_NOTE_**: This submission is out of the regular timeframe, and so the priority was getting a submission on time. Given more time, more elements could have been completed, see [Future Improvements](#future-improvements), for example.

If you are from SpaceRyde and you are reading this, I hope you at least find my submission interesting, and if you are not from SpaceRyde, I suggest you look elsewhere, maybe the Blob-Project (if you're reading this post 2022), for more consistent and articulate code regarding path planning, geometrical bounding in path generation, as well as better decision making regarding interactions between objects in 3d spaces.
# Table of Contents

1. [Breaking Down the Challenge](#breaking-down-the-challenge)
2. [Structuring The Code](#structuring-the-code)
   1. [The Controller Class](#the-controller-class)
   2. [The Plane, HoldingLoc, and Runway Classes](#the-plane-holdingloc-and-runway-classes)
3. [Putting it together](#putting-it-together)
   1. [The good](#the-good)
   2. [The bad](#the-bad)
4. [Future improvements](#future-improvements)
## Breaking Down the Challenge
The challenge is fairly simple, we have a set radius (10'000m) of which we need a controller to manage the 2d airspace. Planes are spawned randomly at the edges of the airspace, and act instantly at a constant speed of 140m/s, updating their positions at a constant 10Hz.

We also need to keep track of all airplanes and make sure that they maintain a safe distance, no matter if they're in flight or in a holding pattern.

Overall, this gives a few clear components we want to consider:
- The flight paths of planes
  - How do we communicate with the planes?
  - What kind of data do we want to communicate with the planes?
- The usage of airspace
  - Efficiency vs Simplicity? What good is a fancy holding pattern if nobody can understand what to do when it goes wrong?
- Landing
  - The prompt says that planes can turn at any angle instantly, and they can land as such, but we know that planes largely can't do this. Do we need to worry about this in our scenario?

In the end, there was an attempt to maintain as-close to realistic scenarios as possible, so after listening to some aviation communication, we decided on the following assumptions:
- ATC gives planes a heading to fly whenever it deems fit.
- Planes respond to the ATC every 10Hz.
- Planes should land roughly collinear to the runway
- Distances are described in x-y instead of latittude and longitude. At this distance, it may start to matter but a translational function could allow the conversion between lat/lon and x/y fairly easily.
## Structuring The Code
Originally, I attempted to make an ROS implementation, but quickly realized that it was not feasible within the constrained timeframe (especially since I did not want this to take any longer than it needed to). Then I turned to my next idea, make every object a class, and have our main controller handle all the interactions. This means that each plane, runway, has it's own potential for decision making, but the Controller is responsible for delegating instructions and usages to each of those objects.
### The Controller Class
Fundamentally, the controller class handles all function pertinent to the function of the airport. It can be initialized once and never again, or initialized everyday when the airport wakes up. Runways, planes, etc can be changed on the fly, as you might have in real life scenarios where weather conditions remove runways or new planes enter/leave our airspace.
### The Plane, HoldingLoc, and Runway Classes
>**`class Plane`**:
The Plane class is designed to be a plane. It transmits locations, it tells the ATC what it's intentions (`state`) is, and otherwise flies as it has been told to do. We assume that when a plane is holding, the plane does not need constant instructions from the ATC.

Summary: Plane class holds and operates a single plane

>**`class HoldingLoc`**:
The HoldingLoc class is interesting in the sense that it does not need to exist, but exists merely as a way to define definitive holding locations. It can hold a single plan, covers a single area of the specified holding radius, and allows multiple classes to interact and communicate effectively. It can be replaced with a list, dictionary, or any other data type, but we've chosen to make it a class simply for simplicity when coding. For example, if we're trying to get the state and id
```Python
myHoldingLoc.getStateAndId() # clear (albiet slightly more complicated in the class definition)
myHoldingLoc[index][state_location], HoldingLoc[index][id_location] # very confusing when we start to have multiple HoldingLoc
```
Summary: HoldingLoc defines a holding position for one plane. Can functionally be any type, is a class for simplicity.

> **`class Runway`**:
Similar to the HoldingLoc class, there is no need for the runway class to exist, other than to make our life simple and subscriptable.
## Putting it Together

### The Good

### The Bad

## Future Improvements