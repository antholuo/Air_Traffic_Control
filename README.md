# SpaceRyde ATC Challenge
Hi there! My name is Anthony Luo and this is my submission for the SpaceRyde ATC Challenge. Thanks so much for taking the time to look at my submission.

The code was written in Python, simply because of the simplicity and speed with which it was possible to finish the challenge. Functionally, the code should be able to translate to C++ as we make use of many of the same fundamental concepts. There are multiple files, so skip to [Putting it Together](#putting-it-together) to get a proper breakdown of the code structure.

> **_NOTE_**: This submission is out of the regular timeframe, and so the priority was getting a submission on time. Given more time, more elements could have been completed, see [Future Improvements](#future-improvements), for example.

If you are from SpaceRyde and you are reading this, I hope you at least find my submission interesting, and if you are not from SpaceRyde, I suggest you look elsewhere, maybe the Blob-Project (if you're reading this post 2022), for more consistent and articulate code regarding path planning, geometrical bounding in path generation, as well as better decision making regarding interactions between objects in 3d spaces.
# Table of Contents

1. [Breaking Down the Challenge](#breaking-down-the-challenge)
2. [Structuring The Code](#structuring-the-code)
   1. [The Controller Class](#the-controller-class)
   2. [The Plane, HoldingLoc, and Runway Classes](#the-plane-holdingloc-and-runway-classes)
3. [Putting it Together](#putting-it-together)
   1. [The Good](#the-good)
   2. [The Bad](#the-bad)
   3. [The Ugly](#the-ugly)
4. [Future improvements](#future-improvements)
5. [Development Log](#development-log)
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
**`class Plane`**:
The Plane class is designed to be a plane. It transmits locations, it tells the ATC what it's intentions (`state`) is, and otherwise flies as it has been told to do. We assume that when a plane is holding, the plane does not need constant instructions from the ATC.

>Summary: Plane class holds and operates a single plane

**`class HoldingLoc`**:
The HoldingLoc class is interesting in the sense that it does not need to exist, but exists merely as a way to define definitive holding locations. It can hold a single plan, covers a single area of the specified holding radius, and allows multiple classes to interact and communicate effectively. It can be replaced with a list, dictionary, or any other data type, but we've chosen to make it a class simply for simplicity when coding. For example, if we're trying to get the state and id
```Python
myHoldingLoc.getStateAndId() # clear (albiet slightly more complicated in the class definition)
myHoldingLoc[index][state_location], HoldingLoc[index][id_location] # very confusing when we start to have multiple HoldingLoc
```
>Summary: HoldingLoc defines a holding position for one plane. Can functionally be any type, is a class for simplicity.

**`class Runway`**:
Similar to the HoldingLoc class, there is no need for the runway class to exist, other than to make our life simple and subscriptable. It contains functions to find the runway, get state of the runway, and allows us to identify and pass around an individual runway without having to pass large combined tuples (see the example from HoldingLoc)

>Summary: Does not need to exist, but does because it makes coding faster
## Putting it Together

There are a few different files that have been used, I'll list them all (in no particular order) and explain their purpose briefly.
- **classes.py** : Contains our auxilliary classes including the Plane, HoldingLoc, Runway, etc.
- **consts.py** : This file contains all of our constants, meaning that if we need to change one thing (ie, radius, runway length, etc), they can be changed here and changes will be reflected globally.
- **main.py** : Main file, contains the Control class, imports everything else and actually runs our Tower code.
- **utils.py** : Utility functions that don't necessarily belong to any particular function, things like operator overrides, getting distances, finding paths, etc.
- **test.py** : Testing file used to verify functionality of some Python elements.
- **visualization.py** : Non-functional attempt at visualization.

> **_Note_**: Throughout the entire project, there was no concerted attempt at structuring the code. I spent a bit of time architecting everything and placed function where I think they should be, and if I were to continue this project I would start to add subdirectories, splitting up files (especially utils.py and my classes), just to make everything clearer. For now though, fewer files == more simplicity.

**Code runs in the following steps:**
1) Tower is initialized with global parameters
2) Runways are added (these are seperate so they can be added/removed at any time)
3) Tower is functional, enter the main while loop
4) Scan for new planes
   1) Planes that are new are given a path to a holding location.
      1) The program finds the nearest open holding locations
      2) The program navigates the plane using headings and waypoints to the location (more on this later)
5) Check paths of planes.
   1) Any plane that is near a waypoint is redirected to a new heading until it reaches the new waypoint
   2) Any plane that has reached it's final destination has it's state changed.
6) Check if a safe number of planes are flying:
   1) If it is safe, the next plane (first in the queue) will be asked to land.
7) Repeat steps 4 through 6

### The Good

I really like the way waypoints and headings are handled. I think it gives a fresh approach to the problem and is definitely something out of the ordinary compared to the regular x-y map based a-star searches.

The code is also easily adaptable to changing conditions, different airfields, etc etc. There are simple ways to add more or less constraints, for example pilots can request to land on a runway, and there can be multiple queues for each runway very easily. There can be changes to runway locations, number of runways, etc, without any code restructuring needed. Holding radius, safety radius, etc, can also all be changed without having to alter the code significantly (beyond the constants being changed).

### The Bad

Unfortunately, with any project, there are parts that we wish we could hide, for me, that would be the search algorithm and holding location generation. These two go hand in hand, and in my code comments you can see my contemplation for multiple search algorithms before deciding to settle and update my holding location generation to support a simpler search algorithm. Breaking this down, there are two components:
1) **The Search algorithm.** I spent a ridiculously long time trying to think about how I could have planes navigate this complex airspace with various other moving planes, and the solution given is definitely suboptimal. We could definitely improve this just by allowing our plane to do a propre A* search, but this becomes difficult when we consider the erratic nature of other moving planes (that are also constantly being updated). The only solution I came up with was for the ATC to map the trajectories of all the planes far into the future, which is not only incredibly difficult to do, but also not entirely viable since we don't know if there will be new planes disrupting the airspace and then causing potential unsafe interactions.
2) **The holding locations**: This is definitely not an optimal solution, although I think it works well enough. Ideally, we have some holding location generation that factors in proximity to the aircraft, proximity to landing location, as well as a generator that can actually pack in as many holding cells as possible. Maybe a system that updates the holding cells live, working with the ATC to move every single plane multiple times a second.

Also, the visualization system does not work. Runways/planes were too small to show up when also viewing the entire ATC radius, and I couldn't figure out how to zoom. In the same vein, I also have a mismatch of accessing member variables directly versus using getters and setters. I'm not sure what happened, but it turns out that in Python, it doesn't really matter!

### The Ugly

Now, we get to the gnarly. This definitely needs to be changed, but doing so would require at least another 5-10 hours. I'll highlight some code, and you'll see fairly quickly why this is an issue:
```python
# lines 161-181 in main.py
    for flier in planes:
        if flier[0].get_state() == 4:
            planes.remove(flier)  # remove any landed planes
        if flier[0].get_state() == 3:  # in flight
            if (equals(flier[0].get_location(), flier[1][0][1])):
                flier[1].pop()  # removes first/current instruction from the list.
                if (flier[1][0][0]):  # if there is a new instruction
                    flier[0].update_heading(flier[1][0][0])  # sets new heading
                else:
                    flier[0].set_landed()  # no more instructions, we have landed?
            in_flight += 1
        if flier[0].get_state() == 1:  # to hold
            if (equals(flier[0].get_location(), flier[1][0][1])):
                flier[1].pop()  # removes first/current instruction from the list.
                if (flier[1][0][0]):  # if there is a new instruction
                    flier[0].update_heading(flier[1][0][0])  # sets new heading
                else:
                    flier[0].set_holding()  # no more instructions, we have reached holding cell?
            in_flight += 1

    return in_flight
```
It's not hard to see that I have way too many nested lists on my planes, like, why the heck am I calling `flier[1][0][1]`?!?!?
If we know that There are plane, instruction pairs for each plane in our list of planes, something like this:
```python
planes = []
new_plane = Plane, ([list_of_headings], [list_of_waypoints])
planes.append(new_plane)
```
Then we know that we're looking for the waypoints or headings for each plane. Unfortunately, in my pursuit of cleanliness and not creating extraneous classes, I ended up overcomplicating something that could have easily been solved by properly adding definitions within the plane class, or even by creating instruction and heading classes.

> **Too Long, Didn't Read:** _In the pursuit of simplicity, I overcomplicated something else that will now take me even longer to undo. And that's ok._
## Future Improvements

This brings me to my favourite list in any project, the list of things-we-could-do, things-we-should-do, things-we-can't-do, and things-we-really-really-want-to-do. Within reason, and at the risk of sounding repetitive, here are some changes I'd make:
- Structure the code nicely! I'm used to one class = one file, and for me, that feels a lot more comfortable. Plus, it just seems to make more sense to have utils seperated out into different sections (for flight, for operator overloading, for cleaning up data, etc)
- Improve the holdinglocation generation. See [The Bad](#the-bad).
- Improve our plane navigation & handling. In addition to what was mentioned in [The Bad](#the-bad), I also want to say that my system doesn't run as optimally as it should. In an ideal world, I wish I could control every plane constantly so that they can be in "holding patterns" but also fluid enough to move from one area to another, or change the center of their holding pattern such that they continue in a holding pattern but move out of the way for a passing plane. This way, we would be able to optimize our airspace to the most (even though it's completely unecessary).
- Visualization! I'm not good with pygame, so I didn't really want to sink countless hours into getting something that wasn't super core to this particular project working. It doesn't seem hard though, and it does seem super valuable if you were to actually use the system.
- Operator overrides. Nowhere in my system can the user override a decision that the computer has made, leaving it as a black box that ... well, could very easily go out of control. And we don't want that, not with giant flying metal tubes.

## Development Log:
- Feb 4, 2022: Added Navigation Instruction Determiners (search algorithms). Added main running script to allow our tower to control aircraft. Updated readme.
- Feb 3, 2022: Added functions to my base classes, introduced new classes, added definitions to utils.
- Feb 2, 2022: Began work on Visualization, defining constants, and classes for our Plane and Controller. Wrote draft function to generate spots
- Feb 1, 2022: Received the project. 