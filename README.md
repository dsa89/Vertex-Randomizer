# Vertex-Randomizer

Version 1.0

Blender Minimal version: 2.8+


Vertex Randomizer is a blender addon that can translate vertices on an object at different random points. The changes that are being made to the mesh are non-destructive because it uses shape keys. As aforementioned, this addon is highly dependable on shape keys and will not function without at one. If there are no shape keys, just simply add one. It will make adjustments to the current selected shape key even if there are multiple ones on a single object.

TERMINOLOGY

Key intensity amount:
   The level of distortion of the key using float numbers.
    0.0 is the least - non-existent
    1.0 is the most - maximum transformation for the current instance for that shape key

Shape distortion amount:
   Floating range for distortion.
   -1.0 is the lowest default
   1.0 is the highest default


In both cases, the mean number is found in minimum and maximum values as defined by the user. The addon selects a random number from the input values and uses it to distort the key intensity and shape distortion. As a result of the values being float numbers, the input can be in very minute amounts. 


** KNOWN ISSUES **

Addon will not initiate without a present shape key. Please do not report it as the addon needs shape keys to function
