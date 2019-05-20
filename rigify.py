"""
Uefy Script v1.2.1

Copyright (c) 2019 Rakiz Farooq
https://www.rakiz.com

Created by Rakiz Farooq

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Uefy Script enables Blender's Rigify addon to export the epic skeleton. Allowing 
creation of animations meant to be used with Unreal Engine 4 assets.

This script is available for sale at https://www.rakiz.com/uefy

Purchasing a copy financially supports the developer and helps ensure continued 
developement.
"""


import bpy
import math
import mathutils
from math import degrees
from bpy.props import *


DeformLayers = [ 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    True, False, False, False, False, False, False, False
]

FaceLayers = [ 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, True, False, False, False, False, False, False
]

IKLayers = [ 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, True, False, False, False, False, False
]

TweakArmLeftLayers = [
    False, False, False, False, False, False, False, False, 
    False, True, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False
]

TweakArmRightLayers = [
    False, False, False, False, False, False, False, False, 
    False, False, False, False, True, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False
]

TweakLegLeftLayers = [
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, True, 
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False
]

TweakLegRightLayers = [
    False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, 
    False, False, True, False, False, False, False, False, 
    False, False, False, False, False, False, False, False
]


BoneLookup = {
    "DEF-spine" : "pelvis",
    "DEF-spine.001" : "spine_01",
    "DEF-spine.002" : "spine_02",
    "DEF-spine.003" : "spine_03",
    "DEF-shoulder.L" : "clavicle_l",
    "DEF-upper_arm.L" : "upperarm_l",
    "DEF-forearm.L" : "lowerarm_l",
    "DEF-hand.L" : "hand_l",
    "DEF-f_index.01.L" : "index_01_l",
    "DEF-f_index.02.L" : "index_02_l",
    "DEF-f_index.03.L" : "index_03_l",
    "DEF-f_middle.01.L" : "middle_01_l",
    "DEF-f_middle.02.L" : "middle_02_l",
    "DEF-f_middle.03.L" : "middle_03_l",
    "DEF-f_pinky.01.L" : "pinky_01_l",
    "DEF-f_pinky.02.L" : "pinky_02_l",
    "DEF-f_pinky.03.L" : "pinky_03_l",
    "DEF-f_ring.01.L" : "ring_01_l",
    "DEF-f_ring.02.L" : "ring_02_l",
    "DEF-f_ring.03.L" : "ring_03_l",
    "DEF-thumb.01.L" : "thumb_01_l",
    "DEF-thumb.02.L" : "thumb_02_l",
    "DEF-thumb.03.L" : "thumb_03_l",
    "DEF-shoulder.R" : "clavicle_r",
    "DEF-upper_arm.R" : "upperarm_r",
    "DEF-forearm.R" : "lowerarm_r",
    "DEF-hand.R" : "hand_r",
    "DEF-f_index.01.R" : "index_01_r",
    "DEF-f_index.02.R" : "index_02_r",
    "DEF-f_index.03.R" : "index_03_r",
    "DEF-f_middle.01.R" : "middle_01_r",
    "DEF-f_middle.02.R" : "middle_02_r",
    "DEF-f_middle.03.R" : "middle_03_r",
    "DEF-f_pinky.01.R" : "pinky_01_r",
    "DEF-f_pinky.02.R" : "pinky_02_r",
    "DEF-f_pinky.03.R" : "pinky_03_r",
    "DEF-f_ring.01.R" : "ring_01_r",
    "DEF-f_ring.02.R" : "ring_02_r",
    "DEF-f_ring.03.R" : "ring_03_r",
    "DEF-thumb.01.R" : "thumb_01_r",
    "DEF-thumb.02.R" : "thumb_02_r",
    "DEF-thumb.03.R" : "thumb_03_r",
    "DEF-spine.004" : "neck_01",
    "DEF-spine.006" : "head_01",
    "DEF-thigh.L" : "thigh_l",
    "DEF-shin.L" : "calf_l",
    "DEF-foot.L" : "foot_l",
    "DEF-toe.L" : "ball_l",
    "DEF-thigh.R" : "thigh_r",
    "DEF-shin.R" : "calf_r",
    "DEF-foot.R" : "foot_r",
    "DEF-toe.R" : "ball_r"
}

RenameMapping = {
    "mixamorig:Hips" : "ORG-hips",
    "mixamorig:Spine" : "ORG-spine1",
    "mixamorig:Spine1" : "ORG-spine2",
    "mixamorig:Spine2" : "ORG-spine3",
    "mixamorig:LeftShoulder" : "ORG-shoulder.L",
    "mixamorig:LeftArm" : "ORG-upper_arm.L",
    "mixamorig:LeftForeArm" : "ORG-forearm.L",
    "mixamorig:LeftHand" : "ORG-hand.L",
    "mixamorig:LeftHandIndex1" : "ORG-f_index.01.L",
    "mixamorig:LeftHandIndex2" : "ORG-f_index.02.L",
    "mixamorig:LeftHandIndex3" : "ORG-f_index.03.L",
    "mixamorig:LeftHandMiddle1" : "ORG-f_middle.01.L",
    "mixamorig:LeftHandMiddle2" : "ORG-f_middle.02.L",
    "mixamorig:LeftHandMiddle3" : "ORG-f_middle.03.L",
    "mixamorig:LeftHandPinky1" : "ORG-f_pinky.01.L",
    "mixamorig:LeftHandPinky2" : "ORG-f_pinky.02.L",
    "mixamorig:LeftHandPinky3" : "ORG-f_pinky.03.L",
    "mixamorig:LeftHandRing1" : "ORG-f_ring.01.L",
    "mixamorig:LeftHandRing2" : "ORG-f_ring.02.L",
    "mixamorig:LeftHandRing3" : "ORG-f_ring.03.L",
    "mixamorig:LeftHandThumb1" : "ORG-thumb.01.L",
    "mixamorig:LeftHandThumb2" : "ORG-thumb.02.L",
    "mixamorig:LeftHandThumb3" : "ORG-thumb.03.L",
    "mixamorig:RightShoulder" : "ORG-shoulder.R",
    "mixamorig:RightArm" : "ORG-upper_arm.R",
    "mixamorig:RightForeArm" : "ORG-forearm.R",
    "mixamorig:RightHand" : "ORG-hand.R",
    "mixamorig:RightHandIndex1" : "ORG-f_index.01.R",
    "mixamorig:RightHandIndex2" : "ORG-f_index.02.R",
    "mixamorig:RightHandIndex3" : "ORG-f_index.03.R",
    "mixamorig:RightHandMiddle1" : "ORG-f_middle.01.R",
    "mixamorig:RightHandMiddle2" : "ORG-f_middle.02.R",
    "mixamorig:RightHandMiddle3" : "ORG-f_middle.03.R",
    "mixamorig:RightHandPinky1" : "ORG-f_pinky.01.R",
    "mixamorig:RightHandPinky2" : "ORG-f_pinky.02.R",
    "mixamorig:RightHandPinky3" : "ORG-f_pinky.03.R",
    "mixamorig:RightHandRing1" : "ORG-f_ring.01.R",
    "mixamorig:RightHandRing2" : "ORG-f_ring.02.R",
    "mixamorig:RightHandRing3" : "ORG-f_ring.03.R",
    "mixamorig:RightHandThumb1" : "ORG-thumb.01.R",
    "mixamorig:RightHandThumb2" : "ORG-thumb.02.R",
    "mixamorig:RightHandThumb3" : "ORG-thumb.03.R",
    "mixamorig:Neck" : "ORG-neck",
    "mixamorig:Head" : "ORG-head",
    "mixamorig:LeftUpLeg" : "ORG-thigh.L",
    "mixamorig:LeftLeg" : "ORG-shin.L",
    "mixamorig:LeftFoot" : "ORG-foot.L",
    "mixamorig:LeftToeBase" : "ORG-toe.L",
    "mixamorig:RightUpLeg" : "ORG-thigh.R",
    "mixamorig:RightLeg" : "ORG-shin.R",
    "mixamorig:RightFoot" : "ORG-foot.R",
    "mixamorig:RightToeBase" : "ORG-toe.R"
}

RenameMappingUE = {
    "pelvis" : "ORG-hips",
    "spine_01" : "ORG-spine1",
    "spine_02" : "ORG-spine2",
    "spine_03" : "ORG-spine3",
    "clavicle_l" : "ORG-shoulder.L",
    "upperarm_l" : "ORG-upper_arm.L",
    "lowerarm_l" : "ORG-forearm.L",
    "hand_l" : "ORG-hand.L",
    "index_01_l" : "ORG-f_index.01.L",
    "index_02_l" : "ORG-f_index.02.L",
    "index_03_l" : "ORG-f_index.03.L",
    "middle_01_l" : "ORG-f_middle.01.L",
    "middle_02_l" : "ORG-f_middle.02.L",
    "middle_03_l" : "ORG-f_middle.03.L",
    "pinky_01_l" : "ORG-f_pinky.01.L",
    "pinky_02_l" : "ORG-f_pinky.02.L",
    "pinky_03_l" : "ORG-f_pinky.03.L",
    "ring_01_l" : "ORG-f_ring.01.L",
    "ring_02_l" : "ORG-f_ring.02.L",
    "ring_03_l" : "ORG-f_ring.03.L",
    "thumb_01_l" : "ORG-thumb.01.L",
    "thumb_02_l" : "ORG-thumb.02.L",
    "thumb_03_l" : "ORG-thumb.03.L",
    "clavicle_r" : "ORG-shoulder.R",
    "upperarm_r" : "ORG-upper_arm.R",
    "lowerarm_r" : "ORG-forearm.R",
    "hand_r" : "ORG-hand.R",
    "index_01_r" : "ORG-f_index.01.R",
    "index_02_r" : "ORG-f_index.02.R",
    "index_03_r" : "ORG-f_index.03.R",
    "middle_01_r" : "ORG-f_middle.01.R",
    "middle_02_r" : "ORG-f_middle.02.R",
    "middle_03_r" : "ORG-f_middle.03.R",
    "pinky_01_r" : "ORG-f_pinky.01.R",
    "pinky_02_r" : "ORG-f_pinky.02.R",
    "pinky_03_r" : "ORG-f_pinky.03.R",
    "ring_01_r" : "ORG-f_ring.01.R",
    "ring_02_r" : "ORG-f_ring.02.R",
    "ring_03_r" : "ORG-f_ring.03.R",
    "thumb_01_r" : "ORG-thumb.01.R",
    "thumb_02_r" : "ORG-thumb.02.R",
    "thumb_03_r" : "ORG-thumb.03.R",
    "neck_01" : "ORG-neck",
    "head" : "ORG-head",
    "thigh_l" : "ORG-thigh.L",
    "calf_l" : "ORG-shin.L",
    "foot_l" : "ORG-foot.L",
    "ball_l" : "ORG-toe.L",
    "thigh_r" : "ORG-thigh.R",
    "calf_r" : "ORG-shin.R",
    "foot_r" : "ORG-foot.R",
    "ball_r" : "ORG-toe.R"
}


metarig_head_name = 'spine.006'
metarig_neckextra_name = 'spine.005'
metarig_neck_name = 'spine.004'
custom_bone_prefix = 'u_'

epic_rolls = {
    'shoulder.L' : 0,
    'upper_arm.L' : -90.0,
    'forearm.L' : -90.0,
    'hand.L' : 0,
    'thumb.01.L' : 90.0,
    'thumb.02.L' : 90.0,
    'thumb.03.L' : 90.0,
    'f_index.01.L' : 90.0,
    'f_index.02.L' : 90.0,
    'f_index.03.L' : 90.0,
    'f_middle.01.L' : 90.0,
    'f_middle.02.L' : 90.0,
    'f_middle.03.L' : 90.0,
    'f_ring.01.L' : 90.0,
    'f_ring.02.L' : 90.0,
    'f_ring.03.L' : 90.0,
    'f_pinky.01.L' : 90.0,
    'f_pinky.02.L' : 90.0,
    'f_pinky.03.L' : 90.0,
    'thigh.L' : 90.0,
    'shin.L' : 90.0,
    'foot.L' : 0,
    'toe.L' : 90.0,
}


custom_rolls = {
    'shoulder.L' : 0,
    'upper_arm.L' : -90.0,
    'forearm.L' : -90.0,
    'hand.L' : -90.0,
    'thumb.01.L' : 90.0,
    'thumb.02.L' : 90.0,
    'thumb.03.L' : 90.0,
    'f_index.01.L' : 0,
    'f_index.02.L' : 0,
    'f_index.03.L' : 0,
    'f_middle.01.L' : 0,
    'f_middle.02.L' : 0,
    'f_middle.03.L' : 0,
    'f_ring.01.L' : 0,
    'f_ring.02.L' : 0,
    'f_ring.03.L' : 0,
    'f_pinky.01.L' : 0,
    'f_pinky.02.L' : 0,
    'f_pinky.03.L' : 0,
    'thigh.L' : 180,
    'shin.L' : 180,
    'foot.L' : 180,
    'toe.L' : 0,
}

custom_mk_rolls = {
    'shoulder.L' : 0,
    'upper_arm.L' : 0,
    'forearm.L' : 0,
    'hand.L' : -45.0,
    'thumb.01.L' : 0,
    'thumb.02.L' : 0,
    'thumb.03.L' : 0,
    'f_index.01.L' : 0,
    'f_index.02.L' : 0,
    'f_index.03.L' : 0,
    'f_middle.01.L' : 0,
    'f_middle.02.L' : 0,
    'f_middle.03.L' : 0,
    'f_ring.01.L' : 0,
    'f_ring.02.L' : 0,
    'f_ring.03.L' : 0,
    'f_pinky.01.L' : 0,
    'f_pinky.02.L' : 0,
    'f_pinky.03.L' : 0,
    'thigh.L' : 0,
    'shin.L' : 0,
    'foot.L' : 0,
    'toe.L' : 180.0,
}

mk_cpose_rolls = {
    'shoulder.L' : -90.0,
    'upper_arm.L' : -90.0,
    'forearm.L' : -90.0,
    'hand.L' : 45.0,
    'thumb.01.L' : 90.0,
    'thumb.02.L' : 90.0,
    'thumb.03.L' : 90.0,
    'f_index.01.L' : 90,
    'f_index.02.L' : 90,
    'f_index.03.L' : 90,
    'f_middle.01.L' : 90,
    'f_middle.02.L' : 90,
    'f_middle.03.L' : 90,
    'f_ring.01.L' : 90,
    'f_ring.02.L' : 90,
    'f_ring.03.L' : 90,
    'f_pinky.01.L' : 90,
    'f_pinky.02.L' : 90,
    'f_pinky.03.L' : 90,
    'thigh.L' : 90.0,
    'shin.L' : 90.0,
    #'foot.L' : 180,
    #'toe.L' : 0,
}


epic_cpose_rolls = {
    'shoulder.L' : 0,
    'upper_arm.L' : 0,
    'forearm.L' : 0,
    'hand.L' : 0,
    'thumb.01.L' : 0,
    'thumb.02.L' : 0,
    'thumb.03.L' : 0,
    'f_index.01.L' : 0,
    'f_index.02.L' : 0,
    'f_index.03.L' : 0,
    'f_middle.01.L' : 0,
    'f_middle.02.L' : 0,
    'f_middle.03.L' : 0,
    'f_ring.01.L' : 0,
    'f_ring.02.L' : 0,
    'f_ring.03.L' : 0,
    'f_pinky.01.L' : 0,
    'f_pinky.02.L' : 0,
    'f_pinky.03.L' : 0,
    'thigh.L' : 0,
    'shin.L' : 0,
    #'foot.L' : 180,
    #'toe.L' : 0,
}

custom_cpose_rolls = {
    'shoulder.L' : 0,
    'upper_arm.L' : 0,
    'forearm.L' : 0,
    'hand.L' : 90.0,
    'thumb.01.L' : 0,
    'thumb.02.L' : 0,
    'thumb.03.L' : 0,
    'f_index.01.L' : 90.0,
    'f_index.02.L' : 90.0,
    'f_index.03.L' : 90.0,
    'f_middle.01.L' : 90.0,
    'f_middle.02.L' : 90.0,
    'f_middle.03.L' : 90.0,
    'f_ring.01.L' : 90.0,
    'f_ring.02.L' : 90.0,
    'f_ring.03.L' : 90.0,
    'f_pinky.01.L' : 90.0,
    'f_pinky.02.L' : 90.0,
    'f_pinky.03.L' : 90.0,
    'thigh.L' : -90,
    'shin.L' : -90,
    #'foot.L' : 180,
    #'toe.L' : 0,
}

MetaRigMapping = {
#    "ORG-hips" : "spine",
#    "ORG-spine1" : "spine.001",
#    "ORG-spine2" : "spine.002",
#    "ORG-spine3" : "spine.003",
    "ORG-shoulder.L" : "shoulder.L",
    "ORG-upper_arm.L" : "upper_arm.L",
    "ORG-forearm.L" : "forearm.L",
    "ORG-hand.L" : "hand.L",
    "ORG-f_index.01.L" : "f_index.01.L",
    "ORG-f_index.02.L" : "f_index.02.L",
    "ORG-f_index.03.L" : "f_index.03.L",
    "ORG-f_middle.01.L" : "f_middle.01.L",
    "ORG-f_middle.02.L" : "f_middle.02.L",
    "ORG-f_middle.03.L" : "f_middle.03.L",
    "ORG-f_pinky.01.L" : "f_pinky.01.L",
    "ORG-f_pinky.02.L" : "f_pinky.02.L",
    "ORG-f_pinky.03.L" : "f_pinky.03.L",
    "ORG-f_ring.01.L" : "f_ring.01.L",
    "ORG-f_ring.02.L" : "f_ring.02.L",
    "ORG-f_ring.03.L" : "f_ring.03.L",
    "ORG-thumb.01.L" : "thumb.01.L",
    "ORG-thumb.02.L" : "thumb.02.L",
    "ORG-thumb.03.L" : "thumb.03.L",
    "ORG-shoulder.R" : "shoulder.R",
    "ORG-upper_arm.R" : "upper_arm.R",
    "ORG-forearm.R" : "forearm.R",
    "ORG-hand.R" : "hand.R",
    "ORG-f_index.01.R" : "f_index.01.R",
    "ORG-f_index.02.R" : "f_index.02.R",
    "ORG-f_index.03.R" : "f_index.03.R",
    "ORG-f_middle.01.R" : "f_middle.01.R",
    "ORG-f_middle.02.R" : "f_middle.02.R",
    "ORG-f_middle.03.R" : "f_middle.03.R",
    "ORG-f_pinky.01.R" : "f_pinky.01.R",
    "ORG-f_pinky.02.R" : "f_pinky.02.R",
    "ORG-f_pinky.03.R" : "f_pinky.03.R",
    "ORG-f_ring.01.R" : "f_ring.01.R",
    "ORG-f_ring.02.R" : "f_ring.02.R",
    "ORG-f_ring.03.R" : "f_ring.03.R",
    "ORG-thumb.01.R" : "thumb.01.R",
    "ORG-thumb.02.R" : "thumb.02.R",
    "ORG-thumb.03.R" : "thumb.03.R",
#    "ORG-neck" : "spine.004",
#    "ORG-head" : "spine.006",
    "ORG-thigh.L" : "thigh.L",
    "ORG-shin.L" : "shin.L",
    "ORG-foot.L" : "foot.L",
    "ORG-toe.L" : "toe.L",
    "ORG-thigh.R" : "thigh.R",
    "ORG-shin.R" : "shin.R",
    "ORG-foot.R" : "foot.R",
    "ORG-toe.R" : "toe.R"
}

VertexGroupLookup = {
    "ORG-hips" : "pelvis",
    "ORG-spine1" : "spine_01",
    "ORG-spine2" : "spine_02",
    "ORG-spine3" : "spine_03",
    "ORG-shoulder.L" : "clavicle_l",
    "ORG-upper_arm.L" : "upperarm_l",
    "ORG-forearm.L" : "lowerarm_l",
    "ORG-hand.L" : "hand_l",
    "ORG-f_index.01.L" : "index_01_l",
    "ORG-f_index.02.L" : "index_02_l",
    "ORG-f_index.03.L" : "index_03_l",
    "ORG-f_middle.01.L" : "middle_01_l",
    "ORG-f_middle.02.L" : "middle_02_l",
    "ORG-f_middle.03.L" : "middle_03_l",
    "ORG-f_pinky.01.L" : "pinky_01_l",
    "ORG-f_pinky.02.L" : "pinky_02_l",
    "ORG-f_pinky.03.L" : "pinky_03_l",
    "ORG-f_ring.01.L" : "ring_01_l",
    "ORG-f_ring.02.L" : "ring_02_l",
    "ORG-f_ring.03.L" : "ring_03_l",
    "ORG-thumb.01.L" : "thumb_01_l",
    "ORG-thumb.02.L" : "thumb_02_l",
    "ORG-thumb.03.L" : "thumb_03_l",
    "ORG-shoulder.R" : "clavicle_r",
    "ORG-upper_arm.R" : "upperarm_r",
    "ORG-forearm.R" : "lowerarm_r",
    "ORG-hand.R" : "hand_r",
    "ORG-f_index.01.R" : "index_01_r",
    "ORG-f_index.02.R" : "index_02_r",
    "ORG-f_index.03.R" : "index_03_r",
    "ORG-f_middle.01.R" : "middle_01_r",
    "ORG-f_middle.02.R" : "middle_02_r",
    "ORG-f_middle.03.R" : "middle_03_r",
    "ORG-f_pinky.01.R" : "pinky_01_r",
    "ORG-f_pinky.02.R" : "pinky_02_r",
    "ORG-f_pinky.03.R" : "pinky_03_r",
    "ORG-f_ring.01.R" : "ring_01_r",
    "ORG-f_ring.02.R" : "ring_02_r",
    "ORG-f_ring.03.R" : "ring_03_r",
    "ORG-thumb.01.R" : "thumb_01_r",
    "ORG-thumb.02.R" : "thumb_02_r",
    "ORG-thumb.03.R" : "thumb_03_r",
    "ORG-neck" : "neck_01",
    "ORG-head" : "head",
    "ORG-thigh.L" : "thigh_l",
    "ORG-shin.L" : "calf_l",
    "ORG-foot.L" : "foot_l",
    "ORG-toe.L" : "ball_l",
    "ORG-thigh.R" : "thigh_r",
    "ORG-shin.R" : "calf_r",
    "ORG-foot.R" : "foot_r",
    "ORG-toe.R" : "ball_r"
}

UEBoneAlignMapping = {
    "pelvis" : ('z', -1.0, 1.0),
    "spine_01" : ('z', -1.0, 1.0),
    "spine_02" : ('z', -1.0, 1.0),
    "spine_03" : ('z', -1.0, 1.0),
    "clavicle_l" : ('x', -1.0, 1.0),
    "upperarm_l" : ('z', -1.0, 1.0),
    "lowerarm_l" : ('z', -1.0, 1.0),
    "hand_l" : ('x', 1.0, 1.0),
    "index_01_l" : ('z', 1.0, 1.0),
    "index_02_l" : ('z', 1.0, 1.0),
    "index_03_l" : ('z', 1.0, 1.0),
    "middle_01_l" : ('z', 1.0, 1.0),
    "middle_02_l" : ('z', 1.0, 1.0),
    "middle_03_l" : ('z', 1.0, 1.0),
    "pinky_01_l" : ('z', 1.0, 1.0),
    "pinky_02_l" : ('z', 1.0, 1.0),
    "pinky_03_l" : ('z', 1.0, 1.0),
    "ring_01_l" : ('z', 1.0, 1.0),
    "ring_02_l" : ('z', 1.0, 1.0),
    "ring_03_l" : ('z', 1.0, 1.0),
    "thumb_01_l" : ('z', 1.0, 1.0),
    "thumb_02_l" : ('z', 1.0, 1.0),
    "thumb_03_l" : ('z', 1.0, 1.0),
    "clavicle_r" : ('x', -1.0, -1.0),
    "upperarm_r" : ('z', 1.0, -1.0),
    "lowerarm_r" : ('z', 1.0, -1.0),
    "hand_r" : ('x', 1.0, -1.0),
    "index_01_r" : ('z', -1.0, -1.0),
    "index_02_r" : ('z', -1.0, -1.0),
    "index_03_r" : ('z', -1.0, -1.0),
    "middle_01_r" : ('z', -1.0, -1.0),
    "middle_02_r" : ('z', -1.0, -1.0),
    "middle_03_r" : ('z', -1.0, -1.0),
    "pinky_01_r" : ('z', -1.0, -1.0),
    "pinky_02_r" : ('z', -1.0, -1.0),
    "pinky_03_r" : ('z', -1.0, -1.0),
    "ring_01_r" : ('z', -1.0, -1.0),
    "ring_02_r" : ('z', -1.0, -1.0),
    "ring_03_r" : ('z', -1.0, -1.0),
    "thumb_01_r" : ('z', -1.0, -1.0),
    "thumb_02_r" : ('z', -1.0, -1.0),
    "thumb_03_r" : ('z', -1.0, -1.0),
    "neck_01" : ('z', -1.0, 1.0),
    "head" : ('z', -1.0, 1.0),
    "thigh_l" : ('z', 1.0, -1.0),
    "calf_l" : ('z', 1.0, -1.0),
    #"foot_l" : ('z', 1.0, -1.0),
    "ball_l" : ('z', 1.0, 1.0),
    "thigh_r" : ('z', -1.0, 1.0),
    "calf_r" : ('z', -1.0, 1.0),
    #"foot_r" : ('z', -1.0, 1.0),
    "ball_r" : ('z', -1.0, -1.0),
    "upperarm_twist_01_l" : ('z', -1.0, 1.0),
    "upperarm_twist_02_l" : ('z', -1.0, 1.0),
    "lowerarm_twist_01_l" : ('z', -1.0, 1.0),
    "lowerarm_twist_02_l" : ('z', -1.0, 1.0),
    "thigh_twist_01_l" : ('z', 1.0, -1.0),
    "thigh_twist_02_l" : ('z', 1.0, -1.0),
    "calf_twist_01_l" : ('z', 1.0, -1.0),
    "calf_twist_02_l" : ('z', 1.0, -1.0),
    "upperarm_twist_01_r" : ('z', 1.0, -1.0),
    "upperarm_twist_02_r" : ('z', 1.0, -1.0),
    "lowerarm_twist_01_r" : ('z', 1.0, -1.0),
    "lowerarm_twist_02_r" : ('z', 1.0, -1.0),
    "thigh_twist_01_r" : ('z', -1.0, 1.0),
    "thigh_twist_02_r" : ('z', -1.0, 1.0),
    "calf_twist_01_r" : ('z', -1.0, 1.0),
    "calf_twist_02_r" : ('z', -1.0, 1.0)
}

character_types = [ 
                    ('2', 'Custom Mapping - MakeHuman', 'Character based on custom mapping for MakeHuman'),
                    ('1', 'Custom Mapping - Fuse Character', 'Character based on custom mapping for Fuse'),
                    ('0', 'Epic Skeleton', 'Default skeleton of UE4 mann.')]

axis_types = [
                ('0', '+ x-axis', 'Align to positive X-Axis'),
                ('1', '- x-axis', 'Align to negative X-Axis'),
                ('2', '+ z-axis', 'Align to positive Z-Axis'),
                ('3', '- z-axis', 'Align to negative Z-Axis')]

class UEFY_armature_item(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="Armature")

class UEFY_bone_item(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="Bone")

class UEFY_scene_properties(bpy.types.PropertyGroup):
    
    bpy.types.Scene.uefy_character_name = StringProperty(name = "Character", default="Armature")
    bpy.types.Scene.uefy_uemann_name = StringProperty(name = "UE4 Mann.", default="root")    
    bpy.types.Scene.uefy_metarig_name = StringProperty(name = "Metarig", default="metarig")
    
    bpy.types.Scene.uefy_org_name = StringProperty(name = "Select Bone", default="")
    bpy.types.Scene.uefy_epic_name = StringProperty(name = "Parent To", default="")
        
    bpy.types.Scene.uefy_character_type = EnumProperty(
        name = "Type ",
        description = "Select the type of character to process",
        items = character_types,
        default = '0'
    )
    
    bpy.types.Scene.uefy_axis_type = EnumProperty(
        name = "Axis ",
        description = "Align axis to",
        items = axis_types,
        default = '0'
    )
    
    
    bpy.types.Scene.uefy_fix_metarig = BoolProperty(
        name = "Fix Metarig",
        description = "Remove metarig plam and neck bones",
        default = True
    )
    
    bpy.types.Scene.uefy_remove_face = BoolProperty(
        name = "Remove Face",
        description = "Remove metarig face bones",
        default = True
    )
    
    bpy.types.Scene.uefy_remove_extras_chest = BoolProperty(
        name = "Remove Extras: Chest",
        description = "Remove metarig breast bones",
        default = True
    )

    bpy.types.Scene.uefy_remove_extras_pelvis = BoolProperty(
        name = "Remove Extras: Pelvis",
        description = "Remove metarig pelvis bones",
        default = True
    )

    bpy.types.Scene.uefy_add_twist = BoolProperty(
        name = "Add Twist",
        description = "Add twist bones to the rig",
        default = True
    )
    
    bpy.types.Scene.uefy_add_second_twist = BoolProperty(
        name = "Second Twist",
        description = "Add second twist bones to the rig",
        default = False
    )
    
    bpy.types.Scene.uefy_add_face = BoolProperty(
        name = "Face",
        description = "Add face deformation bones for UE export",
        default = False
    )
    
    bpy.types.Scene.uefy_add_extras_chest = BoolProperty(
        name = "Extras: Chest",
        description = "Add extra chest deformation bones for UE export.",
        default = False
    )
    
    bpy.types.Scene.uefy_add_extras_pelvis = BoolProperty(
        name = "Extras: Pelvis",
        description = "Add extra pelvis deformation bones for UE export",
        default = False
    )

    bpy.types.Scene.uefy_move_thigh_twist = BoolProperty(
        name = "Move Thigh Twist",
        description = "Move the thigh twist to Original UE4 Mannequin location. Set this to false if you have double twists per leg segment",
        default = True
    )    
    
class UEFY_PT_build_skeleton_panel(bpy.types.Panel):
    bl_idname = "UEFY_PT_build_skeleton_panel"
    bl_label = "Uefy Script Panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    
    #@classmethod
    #def poll(cls, context):
    #    return context.armature
    
    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        
        layout.prop_search(scene, "uefy_character_name", scene, "uefy_character_objects")
        row = layout.row()
        layout.prop_search(scene, "uefy_uemann_name", scene, "uefy_character_objects")
        row = layout.row()
        layout.prop_search(scene, "uefy_metarig_name", scene, "uefy_character_objects")
        row = layout.row()
        row.alignment = 'RIGHT'
        row.operator("uefy.refresh_armature_list")
        
        row = layout.row()
        row.label(text="Metarig Functions")
        
        row = layout.row()
        box = row.box()
        row = box.row()
        row.prop(scene, 'uefy_character_type') 
        row = box.row()
        props = row.operator("uefy.setup_character_bones")
        props.target_name = scene.uefy_character_name
        props.character_type = int(scene.uefy_character_type)
        
        row = box.row()
        props = row.operator("uefy.setup_character_pose")
        props.source_name = scene.uefy_uemann_name
        props.target_name = scene.uefy_character_name
        props.character_type = int(scene.uefy_character_type)
        
        row = layout.row()
        box = row.box()
        row = box.row()
        col = row.column()
        props = col.operator("uefy.setup_metarig_pose")
        props.source_name = scene.uefy_character_name
        props.target_name = scene.uefy_metarig_name
        props.character_type = int(scene.uefy_character_type)
        props.fix_metarig = scene.uefy_fix_metarig
        props.remove_face = scene.uefy_remove_face
        props.remove_extras_chest = scene.uefy_remove_extras_chest
        props.remove_extras_pelvis = scene.uefy_remove_extras_pelvis
        props.add_twist = scene.uefy_add_twist
        props.add_second_twist = scene.uefy_add_second_twist
        col = row.column()
        col.alignment = 'RIGHT'
        col.enabled = False
        col.prop(scene, 'uefy_fix_metarig')        
        row = box.row()
        row.prop(scene, 'uefy_remove_face')
        row = box.row()
        row.prop(scene, 'uefy_remove_extras_chest')
        row = box.row()
        row.prop(scene, 'uefy_remove_extras_pelvis')
        row = box.row()
        row.prop(scene, 'uefy_add_twist')
        row = box.row()
        row.prop(scene, 'uefy_add_second_twist')
        
        row = layout.row()
        row.label(text="Generated Rig Functions")
        
        row = layout.row()
        box = row.box()
        row = box.row()
        props = row.operator("uefy.duplicate_bone")
        props.add_face = scene.uefy_add_face
        props.add_extras_chest = scene.uefy_add_extras_chest
        props.add_extras_pelvis = scene.uefy_add_extras_pelvis
        props.add_twist = scene.uefy_add_twist
        props.add_second_twist = scene.uefy_add_second_twist
        row = box.row()
        row.prop(scene, 'uefy_add_face')
        row = box.row()
        row.prop(scene, 'uefy_add_extras_chest')
        row = box.row()
        row.prop(scene, 'uefy_add_extras_pelvis')
        row = box.row()
        row.prop(scene, 'uefy_add_twist')
        row.prop(scene, 'uefy_add_second_twist')

        row = layout.row()
        box = row.box()
        row = box.row()
        row.operator("uefy.weight_paint")

        row = layout.row()
        row.label(text="Extra Bone Tools")

        row = layout.row()
        box = row.box()
        row = box.row()
        row.prop_search(scene, "uefy_org_name", scene, "uefy_org_bone_objects")
        row = box.row()
        row.prop_search(scene, "uefy_epic_name", scene, "uefy_epic_bone_objects")
        row = box.row()
        row.alignment = 'RIGHT'
        row.operator("uefy.refresh_bone_list")
        row = box.row()
        props = row.operator("uefy.add_custom_bones")
        props.org_bone_name = scene.uefy_org_name
        props.parent_bone_name = scene.uefy_epic_name
        
        row = layout.row()
        row.label(text="Bone Roll Tools")
        row = layout.row()
        box = row.box()
        row = box.row()
        row.prop(scene, 'uefy_axis_type') 
        row = box.row()
        props = row.operator("uefy.roll_bone")
        props.axis_type = int(scene.uefy_axis_type)
        row = box.row()
        props = row.operator("uefy.swap_y_axis")
        props.axis_type = int(scene.uefy_axis_type)
        
        
        row = layout.row()
        box = row.box()
        row = box.row()
        row.label(text="Caution: Incompatible for Rigify!", icon='ERROR')
        row = box.row()
        props = row.operator("uefy.ue_export_align")
        props.move_thigh_twist = scene.uefy_move_thigh_twist
        row = box.row()
        row.prop(scene, 'uefy_move_thigh_twist')
        #props = row.operator("uefy.test_button")
        
        
class UEFY_OT_refresh_armature_list(bpy.types.Operator):
    bl_idname = "uefy.refresh_armature_list"
    bl_label = "Refresh List"
    bl_description = "Refresh available Armatures (needed if some armature objects were renamed)"
    
    def execute(self, context):
        
        scene = context.scene
        scene.uefy_character_objects.clear()
        
        for ob in scene.objects:
            if ob.type == 'ARMATURE':
                print('refresh armature list: ' + ob.name)
                scene.uefy_character_objects.add().name = ob.name
            
        return {"FINISHED"}     
        
class UEFY_OT_refresh_bone_list(bpy.types.Operator):
    bl_idname = "uefy.refresh_bone_list"
    bl_label = "Refresh List"
    bl_description = "Refresh available bones"
    
    @classmethod
    def poll(cls, context):
        return context.armature
    
    def execute(self, context):
        
        scene = context.scene
        scene.uefy_org_bone_objects.clear()
        scene.uefy_epic_bone_objects.clear()
        
        bones = context.object.data.bones
        
        for bone in bones:
            if bone.layers[24] is True or bone.layers[25] is True or bone.layers[26] is True:
                scene.uefy_epic_bone_objects.add().name = bone.name
            if bone.layers[29] is True:
                scene.uefy_org_bone_objects.add().name = bone.name
        
        return {"FINISHED"} 
        
class UEFY_OT_setup_character_bones(bpy.types.Operator):
    bl_idname = "uefy.setup_character_bones"
    bl_label = "Setup Character Bone Names"
    bl_description = "Rename character bones to allow Uefy script to function"
    
    target_name : StringProperty()
    character_type : IntProperty()
    
    @classmethod
    def poll(cls, context):
        return context.armature
    
    def get_mapping(self):
        
        mapping = list()
        
        if self.character_type == 0:
            mapping = RenameMappingUE
            print("Got 0 in mapping .. Using Epic Mapping")
        elif self.character_type == 1:
            mapping = RenameMapping
            print("Got 1 in mapping .. Using Custom Mapping - Fuse")
        elif self.character_type == 2:
            mapping = RenameMappingUE
            print("Got 2 in mapping .. Using Custom Mapping - MK")
            
        return mapping
    
    def execute(self, context):
                
        target = bpy.data.objects.get(self.target_name)        
        if target is None:
            self.report({'ERROR'}, 'Invalid Target. Refresh List and select target Character armature again')
            return {'FINISHED'}
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
       
        context.view_layer.objects.active = target
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        
        edit_bones = target.data.edit_bones
                
        mapping = self.get_mapping()
        
        for k, v in mapping.items():
            print("k :" + k + "v :" + v)
            t_bone = edit_bones.get(k)
            if t_bone is None:
                self.report({'INFO'}, 'Bone Not Found. Target might already have updated names or Wrong Character type was selected')
            else:
                t_bone.name = v

        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        return {'FINISHED'}
        
        
class UEFY_OT_setup_character_pose(bpy.types.Operator):
    bl_idname = "uefy.setup_character_pose"
    bl_label = "Pose Character"
    bl_description = "Change the Character Armature pose to match the UE4 Mann. armature pose"
    
    source_name : bpy.props.StringProperty()
    target_name : bpy.props.StringProperty()
    
    character_type : IntProperty()
    
    def select_bone_hierarchy(self, bone):
        bone.select = True
        for child in bone.children:
            self.select_bone_hierarchy(child)
        return
    
    def update_metabone(self, s_bone_name, t_bone_name, angle=0):
        
        source = bpy.data.objects[self.source_name]
        target = bpy.data.objects[self.target_name]
                
        s_bone = source.pose.bones[s_bone_name]
        t_bone = target.pose.bones.get(t_bone_name)
        
        if t_bone is None:
            return
        
        s_bone_world_matrix = source.matrix_world @ s_bone.matrix
        t_bone_world_matrix = target.matrix_world @ t_bone.matrix
                
        reverse = t_bone_world_matrix.inverted() @ s_bone_world_matrix
        
        if angle == 0:
            final = reverse
        else:
            fix_mat = mathutils.Matrix.Rotation(math.radians(angle), 4, 'Y')
            reverse_fixed = reverse @ fix_mat
            final = reverse_fixed
            
        loc, rot, sca = final.decompose()
        t_bone.rotation_quaternion = rot.copy()
        #t_bone.location = loc.copy()
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    @classmethod
    def poll(cls, context):
        return context.armature
    
    def execute(self, context):
        global epic_cpose_rolls, custom_cpose_rolls
        
        print("Setup character pose")
        
        #source: Mann. and Target: Character
        
        source = bpy.data.objects.get(self.source_name)
        target = bpy.data.objects.get(self.target_name)
        
        if source is None:
            self.report({'ERROR'}, 'Invalid Source. UE_Mann. Armature in the dropdown list if not valid. Refresh and select again')
            return {'FINISHED'}
        if target is None:
            self.report({'ERROR'}, 'Invalid Target. Character Armature in the dropdown list if not valid. Refresh and select again')
            return {'FINISHED'}
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.object.mode_set(mode = 'POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        
        s_pose_bones = source.pose.bones
        t_pose_bones = target.pose.bones
        
        if self.character_type == 0:
            bone_rolls = epic_cpose_rolls
            print("Got 0 in mapping .. Using Epic Mapping")
        elif self.character_type == 1:
            bone_rolls = custom_cpose_rolls
            print("Got 1 in mapping .. Using Custom Mapping")
        elif self.character_type == 2:
            bone_rolls = mk_cpose_rolls
            print("Got 2 in mapping .. Using Custom Mapping - MK")
        
        self.update_metabone('clavicle_l', 'ORG-shoulder.L', bone_rolls['shoulder.L'])
        self.update_metabone('upperarm_l', 'ORG-upper_arm.L', bone_rolls['upper_arm.L'])
        self.update_metabone('lowerarm_l', 'ORG-forearm.L', bone_rolls['forearm.L'])
        self.update_metabone('hand_l', 'ORG-hand.L', bone_rolls['hand.L'])
        self.update_metabone('thumb_01_l', 'ORG-thumb.01.L', bone_rolls['thumb.01.L'])
        self.update_metabone('thumb_02_l', 'ORG-thumb.02.L', bone_rolls['thumb.02.L'])
        self.update_metabone('thumb_03_l', 'ORG-thumb.03.L', bone_rolls['thumb.03.L'])
        self.update_metabone('index_01_l', 'ORG-f_index.01.L', bone_rolls['f_index.01.L'])
        self.update_metabone('index_02_l', 'ORG-f_index.02.L', bone_rolls['f_index.02.L'])
        self.update_metabone('index_03_l', 'ORG-f_index.03.L', bone_rolls['f_index.03.L'])
        self.update_metabone('middle_01_l', 'ORG-f_middle.01.L', bone_rolls['f_middle.01.L'])
        self.update_metabone('middle_02_l', 'ORG-f_middle.02.L', bone_rolls['f_middle.02.L'])
        self.update_metabone('middle_03_l', 'ORG-f_middle.03.L', bone_rolls['f_middle.03.L'])
        self.update_metabone('ring_01_l', 'ORG-f_ring.01.L', bone_rolls['f_ring.01.L'])
        self.update_metabone('ring_02_l', 'ORG-f_ring.02.L', bone_rolls['f_ring.02.L'])
        self.update_metabone('ring_03_l', 'ORG-f_ring.03.L', bone_rolls['f_ring.03.L'])
        self.update_metabone('pinky_01_l', 'ORG-f_pinky.01.L', bone_rolls['f_pinky.01.L'])
        self.update_metabone('pinky_02_l', 'ORG-f_pinky.02.L', bone_rolls['f_pinky.02.L'])
        self.update_metabone('pinky_03_l', 'ORG-f_pinky.03.L', bone_rolls['f_pinky.03.L'])
        self.update_metabone('thigh_l', 'ORG-thigh.L', bone_rolls['thigh.L'])
        self.update_metabone('calf_l', 'ORG-shin.L', bone_rolls['shin.L'])
                    
        bpy.ops.pose.select_all(action='DESELECT')
        
        self.select_bone_hierarchy(target.data.bones['ORG-shoulder.L'])
        self.select_bone_hierarchy(target.data.bones['ORG-thigh.L'])
        
        bpy.ops.pose.copy()
        bpy.ops.pose.paste(flipped=True)
        
        bpy.ops.pose.select_all(action='DESELECT')
        
        return {'FINISHED'}
        
class UEFY_OT_setup_metarig_pose(bpy.types.Operator):
    bl_idname = "uefy.setup_metarig_pose"
    bl_label = "Pose Metarig"
    bl_description = "Pose the metarig to match character"
    
    # source: Character target: Metarig
    
    source_name : bpy.props.StringProperty()
    target_name : bpy.props.StringProperty()
    
    character_type : IntProperty()
    
    fix_metarig : BoolProperty()
    remove_face : BoolProperty()
    remove_extras_chest : BoolProperty()
    remove_extras_pelvis : BoolProperty()
    add_twist : BoolProperty()
    add_second_twist : BoolProperty()
    
    def delete_bone(self, bone_name, edit_bones):
        
        b = edit_bones.get(bone_name)
        if b is not None:
            edit_bones.remove(b)
        return
    
    def do_remove_face(self, context):
        global metarig_head_name
        
        target = bpy.data.objects.get(self.target_name)
        
        print('Remove Extras')
                
        ebones = target.data.edit_bones
        
        face_bone = ebones.get('face')
        if face_bone is None:
            self.report({'WARNING'}, "Face bone not found")
            return
        
        show_face_layers = [ 
            True, False, False, False, False, False, False, False, 
            False, False, False, False, False, False, False, False, 
            False, False, False, False, False, False, False, False, 
            False, False, False, False, False, False, False, False
        ] 
        
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.ops.armature.armature_layers(layers=show_face_layers)
        bpy.ops.armature.select_all(action='SELECT')
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        bpy.ops.armature.delete()
        
        bpy.ops.armature.layers_show_all(all=True)
        bpy.ops.armature.select_all(action='DESELECT')
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    def do_remove_extras_chest(self):
    
        target = bpy.data.objects.get(self.target_name)
        
        print('Remove Extras: Chest')
                
        ebones = target.data.edit_bones
        self.delete_bone('breast.L', ebones)
        self.delete_bone('breast.R', ebones)
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    def do_remove_extras_pelvis(self):
    
        target = bpy.data.objects.get(self.target_name)
        
        print('Remove Extras: Pelvis')
                
        ebones = target.data.edit_bones
        self.delete_bone('pelvis.L', ebones)
        self.delete_bone('pelvis.R', ebones)
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    
    def do_fix_neck(self):
        global metarig_head_name, metarig_neckextra_name, metarig_neck_name
        
        target = bpy.data.objects.get(self.target_name)
        
        print('Fix Neck')
        ebones = target.data.edit_bones
        
        self.delete_bone('spine.005', ebones)
        
        head = ebones['spine.006']
        neck = ebones['spine.004']
        
        neck.tail = head.head.copy()
        head.use_connect = True
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    def do_fix_palm(self):
        target = bpy.data.objects.get(self.target_name)
        
        print('Remove Palm')
                
        ebones = target.data.edit_bones
        
        self.delete_bone('palm.01.L', ebones)
        self.delete_bone('palm.02.L', ebones)
        self.delete_bone('palm.03.L', ebones)
        self.delete_bone('palm.04.L', ebones)
        self.delete_bone('palm.01.R', ebones)
        self.delete_bone('palm.02.R', ebones)
        self.delete_bone('palm.03.R', ebones)
        self.delete_bone('palm.04.R', ebones)
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    def do_fix_metarig(self):
                
        print('Fixing metarig')
        
        self.do_fix_palm()
        self.do_fix_neck()
                
        return
    
    def select_bone_hierarchy(self, bone):
        bone.select = True
        for child in bone.children:
            self.select_bone_hierarchy(child)
        return
    
    def update_metabone(self, source, target, s_bone_name, t_bone_name, angle=0):
        
        t_bone = target.pose.bones[t_bone_name]
        s_bone = source.pose.bones.get(s_bone_name)
        
        if s_bone is None:
            return
        
        s_bone_world_matrix = source.matrix_world @ s_bone.matrix
        t_bone_world_matrix = target.matrix_world @ t_bone.matrix
                
        reverse = t_bone_world_matrix.inverted() @ s_bone_world_matrix
        
        if angle == 0:
            final = reverse.copy()
        else:
            fix_mat = mathutils.Matrix.Rotation(math.radians(angle), 4, 'Y')
            reverse_fixed = reverse @ fix_mat
            final = reverse_fixed.copy()
            
        loc, rot, sca = final.decompose()
        t_bone.rotation_quaternion = rot.copy()
        t_bone.location = loc.copy()
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return
    
    def move_bone(self, source, target, s_bone_name, t_bone_name):
        global MetaRigMapping
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        sp_bone = source.pose.bones.get(s_bone_name)
        if sp_bone is None:
            return
        
        head = sp_bone.head.copy()
        tail = sp_bone.tail.copy()
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        te_bone = target.data.edit_bones[t_bone_name]
        
        te_bone.head = head.copy()
        te_bone.tail = tail.copy()
        
        return
        
    @classmethod
    def poll(cls, context):
        return context.armature
    
    def add_twist_bone(self, bone_name, owning_bone_name, layers):
        
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = bpy.data.objects.get(self.target_name)
        print(target.name)
        
        edit_bones = target.data.edit_bones
        print("Owner: " + owning_bone_name)
        owner = edit_bones.get(owning_bone_name)
        
        if owner is None:
            self.report({'WARNING'}, "Missing twist parent bones. Make sure this operator is run only on the metarig")
            return

        bone = edit_bones.new(bone_name)
        bone.parent = owner
        bone.head = owner.head.copy()
        bone.tail = owner.tail.copy()
        bone.roll = owner.roll
        bone.use_connect = False
        bone.layers = layers
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        bpy.ops.object.mode_set(mode = 'POSE')
        target.pose.bones[bone_name].rigify_type = "basic.super_copy"
                
        return
    
    def cancel_controller(self, bone_name):
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        pbones = target.pose.bones
        pbones[bone_name].rigify_parameters.make_deform = False
        pbones[bone_name].rigify_parameters.make_widget = False
        pbones[bone_name].rigify_parameters.make_control = False
        
        return
    
    def resize_half_bone(self, bone_name):
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = bpy.data.objects.get(self.target_name)
        
        edit_bones = target.data.edit_bones
        
        bone = edit_bones[bone_name]
        
        direction = bone.vector.copy()
        direction.normalize()
        
        offset = direction * (bone.length / 2.0)
        
        bone.tail = bone.tail - offset
        
        return
    
    def do_add_second_twist(self):
        
        target = bpy.data.objects.get(self.target_name)
        
        print('Add twist bones')
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        
        
        self.add_twist_bone('ccalf_twist_02_l', 'shin.L', TweakLegLeftLayers)
        self.add_twist_bone('ccalf_twist_02_r', 'shin.R', TweakLegRightLayers)
        
        self.add_twist_bone('clowerarm_twist_02_l', 'forearm.L', TweakArmLeftLayers)
        self.add_twist_bone('clowerarm_twist_02_r', 'forearm.R', TweakArmRightLayers)
        
        self.resize_half_bone('ccalf_twist_02_l')
        self.resize_half_bone('ccalf_twist_02_r')
        
        self.resize_half_bone('clowerarm_twist_02_l')
        self.resize_half_bone('clowerarm_twist_02_r')
        
        return
    
    def do_add_twist(self):
        global TweakArmLeftLayers, TweakArmRightLayers, TweakLegLeftLayers, TweakLegRightLayers
        
        target = bpy.data.objects.get(self.target_name)
        
        print('Add twist bones')
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        
        edit_bones = target.data.edit_bones
        
        self.add_twist_bone('cupperarm_twist_01_l', 'upper_arm.L', TweakArmLeftLayers)
        self.add_twist_bone('cupperarm_twist_01_r', 'upper_arm.R', TweakArmRightLayers)
        
        self.add_twist_bone('cthigh_twist_01_l', 'thigh.L', TweakLegLeftLayers)
        self.add_twist_bone('cthigh_twist_01_r', 'thigh.R', TweakLegRightLayers)
        
        return
    
    def do_fix_axis(self):
        
        target = bpy.data.objects.get(self.target_name)
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        pbones = target.pose.bones
        
        pbones['upper_arm.L'].rigify_parameters.rotation_axis = 'x'
        pbones['upper_arm.R'].rigify_parameters.rotation_axis = 'x'
        pbones['thigh.L'].rigify_parameters.rotation_axis = 'x'
        pbones['thigh.R'].rigify_parameters.rotation_axis = 'x'
        
        return
    
    def execute(self, context):
        global epic_rolls, custom_rolls
        
        source = bpy.data.objects.get(self.source_name)
        target = bpy.data.objects.get(self.target_name)
        
        if source is None:
            self.report({'ERROR'}, "Source is Invalid")
            return {'FINISHED'}
        if target is None:
            self.report({'ERROR'}, "Target is Invalid")
            return {'FINISHED'}        
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
       
        context.view_layer.objects.active = target        
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')        
        
        if self.fix_metarig == True:
            self.do_fix_metarig()
        
        if self.remove_extras_chest == True:
            self.do_remove_extras_chest()
        
        if self.remove_extras_pelvis == True:
            self.do_remove_extras_pelvis()

        if self.remove_face == True:
            self.do_remove_face(context)
        
        self.do_fix_axis()
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        target.select_set(True)
        bpy.ops.object.duplicate(False)
        temp_rig = bpy.context.active_object
        
        for k, v in MetaRigMapping.items():
            self.move_bone(source, temp_rig, k,v)
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        if self.character_type == 0:
            bone_rolls = epic_rolls
            print("Got 0 in mapping .. Using Epic Mapping")
        elif self.character_type == 1:
            bone_rolls = custom_rolls
            print("Got 1 in mapping .. Using Custom Mapping - Fuse")
        elif self.character_type == 2:
            bone_rolls = custom_mk_rolls
            print("Got 2 in mapping .. Using Custom Mapping- MK")
        
        for k, v in bone_rolls.items():
            sbone_name = 'ORG-' + k
            tbone_name = k
            roll = v
            self.update_metabone(source, temp_rig, sbone_name, tbone_name, roll)
        
        self.select_bone_hierarchy(temp_rig.data.bones['shoulder.L'])
        self.select_bone_hierarchy(temp_rig.data.bones['thigh.L'])
        
        bpy.ops.pose.copy()
        bpy.ops.pose.paste(flipped=True)
        bpy.ops.pose.armature_apply()
        
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        target.select_set(True)
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        for s_bone in temp_rig.data.edit_bones:
            t_bone = target.data.edit_bones[s_bone.name]
            t_bone.head = s_bone.head.copy()
            t_bone.tail = s_bone.tail.copy()
            t_bone.roll = s_bone.roll
                
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        if self.add_twist == True:
            self.do_add_twist()
            if self.add_second_twist == True:
                self.do_add_second_twist()
        
        target.select_set(False)

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.data.objects.remove(temp_rig, do_unlink=True)
        
        target.select_set(True)
        
        return {'FINISHED'}
    
    
class UEFY_OT_duplicate_bone(bpy.types.Operator):
    bl_idname = "uefy.duplicate_bone"
    bl_label = "Build Unreal Skeleton"
    bl_description = "Build export skeleton"
    
    add_face : bpy.props.BoolProperty()
    add_extras_chest : bpy.props.BoolProperty()
    add_extras_pelvis : bpy.props.BoolProperty()
    add_twist : bpy.props.BoolProperty()
    add_second_twist : bpy.props.BoolProperty()
    
    def process_bone(self, context, source, name, parent):
        global DeformLayers
        
        bones = context.object.data.bones
        pose_bones = context.object.pose.bones
        edit_bones = context.object.data.edit_bones
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = edit_bones.get(source)
        
        if target is None:
            return
        
        print("Target Bone: ", target, "Source Name:", source)
        
        bone = edit_bones.new(name)
        
        print("New Bone: ", bone)
        bone.parent = edit_bones.get(parent)
        bone.head = target.head.copy()
        bone.tail = target.tail.copy()
        bone.roll = target.roll
        bone.use_connect = target.use_connect
        bone.matrix = target.matrix.copy()
        bone.layers = DeformLayers
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        pbone = pose_bones.get(name)
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = source
        
        return {"FINISHED"}

    def do_build_skeleton(self, context):
        global BoneLookup
        
        # Root Chain
        
        parent = "root"
        source = "DEF-spine"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
                
        parent = BoneLookup[source]
        source = "DEF-spine.001"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)

        parent = BoneLookup[source]
        source = "DEF-spine.002"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)

        parent = BoneLookup[source]
        source = "DEF-spine.003"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Shoulder Chain
        
        parent = BoneLookup[source]
        source = "DEF-shoulder.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-upper_arm.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-forearm.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Hand Chain
        
        parent = BoneLookup[source]
        source = "DEF-hand.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Index Finger Chain
        
        parent = "hand_l"
        source = "DEF-f_index.01.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_index.02.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_index.03.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Middle Finger Chain
        
        parent = "hand_l"
        source = "DEF-f_middle.01.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_middle.02.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_middle.03.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Pinky Finger Chain
        
        parent = "hand_l"
        source = "DEF-f_pinky.01.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_pinky.02.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_pinky.03.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Ring Finger Chain
        
        parent = "hand_l"
        source = "DEF-f_ring.01.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_ring.02.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_ring.03.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Thumb Chain
        
        parent = "hand_l"
        source = "DEF-thumb.01.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-thumb.02.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-thumb.03.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Shoulder Chain
        
        parent = "spine_03"
        source = "DEF-shoulder.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-upper_arm.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-forearm.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-hand.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Index Finger Chain
        
        parent = "hand_r"
        source = "DEF-f_index.01.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_index.02.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_index.03.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Middle Finger Chain
        
        parent = "hand_r"
        source = "DEF-f_middle.01.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_middle.02.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_middle.03.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Pinky Finger Chain
        
        parent = "hand_r"
        source = "DEF-f_pinky.01.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_pinky.02.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_pinky.03.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Ring Finger Chain
        
        parent = "hand_r"
        source = "DEF-f_ring.01.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_ring.02.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-f_ring.03.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Thumb Chain
        
        parent = "hand_r"
        source = "DEF-thumb.01.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-thumb.02.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-thumb.03.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Neck Chain
        
        parent = "spine_03"
        source = "DEF-spine.004"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-spine.006"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Left Thigh Chain
        
        parent = "pelvis"
        source = "DEF-thigh.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-shin.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        #
        #
        if self.add_twist:
            self.duplicate_twist_bone(context, 'calf_twist_01_l', 'calf_l', 'DEF-shin.L.001')
            self.offset_lower_twist(context, 'calf_twist_01_l')
        
        parent = BoneLookup[source]
        source = "DEF-foot.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-toe.L"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        # Right Thigh Chain
        
        parent = "pelvis"
        source = "DEF-thigh.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-shin.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        #
        #
        if self.add_twist:
            self.duplicate_twist_bone(context, 'calf_twist_01_r', 'calf_r', 'DEF-shin.R.001')
            self.offset_lower_twist(context, 'calf_twist_01_r')
        
        parent = BoneLookup[source]
        source = "DEF-foot.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        parent = BoneLookup[source]
        source = "DEF-toe.R"
        name = BoneLookup[source]
        self.process_bone(context, source, name, parent)
        
        if self.add_extras_chest == True:
            self.do_add_extras_chest(context)
        
        if self.add_extras_pelvis == True:
            self.do_add_extras_pelvis(context)
        
        return {"FINISHED"}

    def do_add_extras_chest(self, context):
        
        print("Adding Extras: Chest")
        
        parent = 'spine_03'
        source = "DEF-breast.L"
        name = "chest_l"
        self.process_bone(context, source, name, parent)
        
        parent = 'spine_03'
        source = "DEF-breast.R"
        name = "chest_r"
        self.process_bone(context, source, name, parent)
                
        return

    def do_add_extras_pelvis(self, context):
        
        print("Adding Extras: Pelvis")

        parent = 'pelvis'
        source = "DEF-pelvis.L"
        name = "pelvis_l"
        self.process_bone(context, source, name, parent)

        parent = 'pelvis'
        source = "DEF-pelvis.R"
        name = "pelvis_r"
        self.process_bone(context, source, name, parent)
        
        return
    
    def do_add_ik(self, context):
        global IKLayers
        
        bones = context.object.data.bones
        pose_bones = context.object.pose.bones
        edit_bones = context.object.data.edit_bones
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        print("Adding IK bones")
        
        root = edit_bones.get('root')
        
        ik_foot_root = edit_bones.new('ik_foot_root')
        ik_foot_root.parent = root
        ik_foot_root.head = root.head.copy()
        ik_foot_root.tail = root.tail.copy()
        ik_foot_root.use_connect = root.use_connect
        ik_foot_root.matrix = root.matrix.copy()
        ik_foot_root.layers = IKLayers
        ik_foot_root.use_deform = True
        
        
        foot_l = edit_bones.get('foot_l')
        foot_r = edit_bones.get('foot_r')
        
        ik_foot_l = edit_bones.new('ik_foot_l')
        ik_foot_l.parent = ik_foot_root
        ik_foot_l.head = foot_l.head.copy()
        ik_foot_l.tail = foot_l.tail.copy()
        #ik_foot_l.use_connect = False
        ik_foot_l.layers = IKLayers
        ik_foot_l.use_deform = True
        
        ik_foot_r = edit_bones.new('ik_foot_r')
        ik_foot_r.parent = ik_foot_root
        ik_foot_r.head = foot_r.head.copy()
        ik_foot_r.tail = foot_r.tail.copy()
        #ik_foot_r.use_connect = foot_r.use_connect
        ik_foot_r.layers = IKLayers
        ik_foot_r.use_deform = True
        
        hand_r = edit_bones.get('hand_r')
        hand_l = edit_bones.get('hand_l')
        
        ik_hand_root = edit_bones.new('ik_hand_root')
        ik_hand_root.parent = root
        ik_hand_root.head = root.head.copy()
        ik_hand_root.tail = root.tail.copy()
        #ik_hand_root.use_connect = root.use_connect
        ik_hand_root.layers = IKLayers
        ik_hand_root.use_deform = True
        
        
        ik_hand_gun = edit_bones.new('ik_hand_gun')
        ik_hand_gun.parent = ik_hand_root
        ik_hand_gun.head = hand_r.head.copy()
        ik_hand_gun.tail = hand_r.tail.copy()
        #ik_hand_gun.tail = hand_l.head.copy()
        #ik_hand_gun.use_connect = hand_r.use_connect
        ik_hand_gun.layers = IKLayers
        ik_hand_gun.use_deform = True
        
        
        ik_hand_l = edit_bones.new('ik_hand_l')
        ik_hand_l.parent = ik_hand_gun
        ik_hand_l.head = hand_l.head.copy()
        ik_hand_l.tail = hand_l.tail.copy()
        #ik_hand_l.use_connect = True
        ik_hand_l.layers = IKLayers
        ik_hand_l.use_deform = True

        ik_hand_r = edit_bones.new('ik_hand_r')
        ik_hand_r.parent = ik_hand_gun
        ik_hand_r.head = hand_r.head.copy()
        ik_hand_r.tail = hand_r.tail.copy()
        #k_hand_r.use_connect = True
        ik_hand_r.layers = IKLayers
        ik_hand_r.use_deform = True
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        pbone = pose_bones.get('ik_foot_root')
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = 'root'
        
        pbone = pose_bones.get('ik_foot_l')
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = 'foot_l'
        
        pbone = pose_bones.get('ik_foot_r')
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = 'foot_r'
        
        pbone = pose_bones.get('ik_hand_gun')
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = 'hand_r'
        
        #pbone = pose_bones.get('ik_hand_gun')
        #c = pbone.constraints.new(type='STRETCH_TO')
        #c.target = context.object
        #c.subtarget = 'hand_l'
                
        pbone = pose_bones.get('ik_hand_r')
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = 'hand_r'
        
        pbone = pose_bones.get('ik_hand_l')
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = 'hand_l'
        
        return {"FINISHED"}

    def duplicate_face_bone(self, context, bone_name):
        global FaceLayers
        
        edit_bones = context.object.data.edit_bones
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        parent = edit_bones['fc_face']
        
        bone = edit_bones[bone_name]
        
        deform_bone = edit_bones.new('fc_' + bone_name[4:])
        deform_bone.parent = parent
        deform_bone.head = bone.head.copy()
        deform_bone.tail = bone.tail.copy()
        deform_bone.use_connect = False
        deform_bone.matrix = bone.matrix.copy()
        deform_bone.layers = FaceLayers
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return

    def add_deform_set(self, context, bone_name):
        
        edit_bones = context.object.data.edit_bones
        bones = context.object.data.bones
        
        bone = bones[bone_name]
        
        children = list()
        
        for child in bone.children:
            if (child.name.find('DEF-') == 0):
                self.duplicate_face_bone(context, child.name)
            self.add_deform_set(context, child.name)        
        
        return
    
    def add_face_other(self, context):
        
        self.process_face_bone(context, 'fc_face', 'MCH-eye.L', 'fc_eye_L')
        self.process_face_bone(context, 'fc_face', 'MCH-eye.R', 'fc_eye_R')
        self.process_face_bone(context, 'fc_face', 'teeth.T', 'fc_jaw_T')
        self.process_face_bone(context, 'fc_face', 'teeth.B', 'fc_jaw_B')
        
        return
    
    def process_face_bone(self, context, parent_name, source_name, bone_name):
        global FaceLayers
        
        edit_bones = context.object.data.edit_bones
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        parent = edit_bones[parent_name]
        source = edit_bones[source_name]
        
        f_bone = edit_bones.new(bone_name)
        f_bone.parent = parent
        f_bone.head = source.head.copy()
        f_bone.tail = source.tail.copy()
        f_bone.use_connect = False
        f_bone.matrix = source.matrix.copy()
        f_bone.layers = FaceLayers
        
        return

        
    def do_add_face(self, context):
        global FaceLayers
        
        bones = context.object.data.bones
        pose_bones = context.object.pose.bones
        edit_bones = context.object.data.edit_bones
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        print("Adding Face bones")
        
        oface_bone = bones['ORG-face']
        eface_bone = edit_bones['ORG-face']
        ehead_bone = edit_bones['head_01']
        
        head_deform_bone = edit_bones.new('fc_face')
        head_deform_bone.parent = ehead_bone
        head_deform_bone.head = eface_bone.head.copy()
        head_deform_bone.tail = eface_bone.tail.copy()
        head_deform_bone.use_connect = False
        head_deform_bone.matrix = eface_bone.matrix.copy()
        head_deform_bone.layers = FaceLayers
        
        self.add_deform_set(context, 'ORG-face')
        self.add_face_other(context)
        
        
        bpy.ops.object.mode_set(mode = 'POSE')
        pface_bone = pose_bones['fc_face']
                
        for pbone in pface_bone.children:
            c = pbone.constraints.new(type='COPY_TRANSFORMS')
            c.target = context.object
            if pbone.name == 'fc_eye_L':
                c.subtarget = 'MCH-eye.L'
            elif pbone.name == 'fc_eye_R':
                c.subtarget = 'MCH-eye.R'
            elif pbone.name == 'fc_jaw_T':
                c.subtarget = 'teeth.T'
            elif pbone.name == 'fc_jaw_B':
                c.subtarget = 'teeth.B'
            else:
                c.subtarget = 'DEF-' + pbone.name[3:]
        
        return
    
    def duplicate_twist_bone(self, context, bone_name, parent_name, cbone_name):
        global DeformLayers
        
        if self.add_twist == False:
            return
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = context.object
        
        edit_bones = target.data.edit_bones
        
        parent = edit_bones.get(parent_name)
        cbone = edit_bones.get(cbone_name)
        
        if parent is None:
            self.report({'WARNING'}, "Missing twist parent bones. Make sure this operator is run only on the metarig")
            return

        bone = edit_bones.new(bone_name)
        bone.parent = parent
        bone.head = parent.head.copy()
        bone.tail = parent.tail.copy()
        bone.roll = parent.roll
        bone.use_connect = False
        bone.layers = DeformLayers
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        pose_bones = target.pose.bones
        
        pbone =  pose_bones[bone_name]
        c = pbone.constraints.new(type='COPY_ROTATION')
        c.target = target
        c.subtarget = cbone_name
        c.owner_space = 'LOCAL'
        c.target_space = 'LOCAL'
        
        return
    
    def offset_lower_twist(self, context, bone_name):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = context.object
        
        edit_bones = target.data.edit_bones
        
        bone = edit_bones[bone_name]
        
        direction = bone.vector.copy()
        direction.normalize()
        
        offset = direction * (bone.length / 2)
        
        bone.head = bone.head + offset
        #bone.tail = bone.tail + offset
        
        return
    
    def offset_lower_twist2(self, context, bone_name):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = context.object
        
        edit_bones = target.data.edit_bones
        
        bone = edit_bones[bone_name]
        
        direction = bone.vector.copy()
        direction.normalize()
        
        offset = direction * (bone.length)
        
        bone.head = bone.head + offset
        bone.tail = bone.tail + offset
        
        return
    
    def resize_half_bone(self, context, bone_name):
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = context.object
        
        edit_bones = target.data.edit_bones
        
        bone = edit_bones[bone_name]
        
        direction = bone.vector.copy()
        direction.normalize()
        
        offset = direction * (bone.length / 2.0)
        
        #bone.head = bone.head + offset
        bone.tail = bone.tail - offset
        
        return
    
    def do_add_second_twist(self, context):
        
        target = context.object
        
        print('Duplicate second twist bones')
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        
        edit_bones = target.data.edit_bones
        
        self.duplicate_twist_bone(context, 'upperarm_twist_02_l', 'upperarm_l', 'DEF-upper_arm.L.001')
        self.duplicate_twist_bone(context, 'upperarm_twist_02_r', 'upperarm_r', 'DEF-upper_arm.R.001')
        self.duplicate_twist_bone(context, 'thigh_twist_02_l', 'thigh_l', 'DEF-thigh.L.001')
        self.duplicate_twist_bone(context, 'thigh_twist_02_r', 'thigh_r', 'DEF-thigh.R.001')
        
        self.duplicate_twist_bone(context, 'lowerarm_twist_02_l', 'lowerarm_l', 'clowerarm_twist_02_l')
        self.duplicate_twist_bone(context, 'lowerarm_twist_02_r', 'lowerarm_r', 'clowerarm_twist_02_r')
        self.duplicate_twist_bone(context, 'calf_twist_02_l', 'calf_l', 'ccalf_twist_02_l')
        self.duplicate_twist_bone(context, 'calf_twist_02_r', 'calf_r', 'ccalf_twist_02_r')
        
        self.offset_lower_twist2(context, 'upperarm_twist_02_l')
        self.offset_lower_twist2(context, 'upperarm_twist_02_r')
        self.offset_lower_twist2(context, 'thigh_twist_02_l')
        self.offset_lower_twist2(context, 'thigh_twist_02_r')
        
        self.resize_half_bone(context, 'lowerarm_twist_02_l')
        self.resize_half_bone(context, 'lowerarm_twist_02_r')
        self.resize_half_bone(context, 'calf_twist_02_l')
        self.resize_half_bone(context, 'calf_twist_02_r')
        
        return
    
    def do_add_twist(self, context):
        
        target = context.object
        
        print('Duplicate twist bones')
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        
        edit_bones = target.data.edit_bones
        
        self.duplicate_twist_bone(context, 'upperarm_twist_01_l', 'upperarm_l', 'cupperarm_twist_01_l')
        self.duplicate_twist_bone(context, 'upperarm_twist_01_r', 'upperarm_r', 'cupperarm_twist_01_r')

        self.duplicate_twist_bone(context, 'lowerarm_twist_01_l', 'lowerarm_l', 'DEF-forearm.L.001')
        self.duplicate_twist_bone(context, 'lowerarm_twist_01_r', 'lowerarm_r', 'DEF-forearm.R.001')
        
        self.duplicate_twist_bone(context, 'thigh_twist_01_l', 'thigh_l', 'cthigh_twist_01_l')
        self.duplicate_twist_bone(context, 'thigh_twist_01_r', 'thigh_r', 'cthigh_twist_01_r')
        
        self.offset_lower_twist(context, 'lowerarm_twist_01_l')
        self.offset_lower_twist(context, 'lowerarm_twist_01_r')
        
        return
    
    def get_children(self, context, bone_name, parent_name, target_bones):
        
        edit_bones = context.object.data.edit_bones        
        
        target_bones.append((bone_name, parent_name))
        
        bone = edit_bones[bone_name]
        
        for child in bone.children:
            self.get_children(context, child.name, bone.name, target_bones)
                
        return
    
    def get_final_parent_name(self, context, parent_name):
        
        edit_bones = context.object.data.edit_bones
        
        if parent_name[:4] != 'DEF-':
            return parent_name
        
        new_parent = custom_bone_prefix + parent_name[4:]
        
        return new_parent
    
    def process_chain_bone(self, context, name, parent_name):
    
        bones = context.object.data.bones
        pose_bones = context.object.pose.bones
        edit_bones = context.object.data.edit_bones
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        target = edit_bones.get(name)
        if target is None:
            return
        
        deform_bone_name = custom_bone_prefix + name[4:]
        bone = edit_bones.new(deform_bone_name)
        
        final_parent = self.get_final_parent_name(context, parent_name)
        
        print("New Bone: ", bone)
        bone.parent = edit_bones.get(final_parent)
        bone.head = target.head.copy()
        bone.tail = target.tail.copy()
        bone.roll = target.roll
        bone.use_connect = target.use_connect
        bone.matrix = target.matrix.copy()
        bone.layers = DeformLayers
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        bpy.ops.object.mode_set(mode = 'POSE')
        
        pbone = pose_bones[deform_bone_name]
        c = pbone.constraints.new(type='COPY_TRANSFORMS')
        c.target = context.object
        c.subtarget = name
        
        return
    
    def process_chain(self, context, bone_name, parent_name):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        edit_bones = context.object.data.edit_bones
        
        bone = edit_bones.get(bone_name)
        parent = edit_bones.get(parent_name)
        
        if bone is None:
            return
        if parent is None:
            return
        
        target_bones = []
        self.get_children(context, bone_name, parent_name, target_bones)
        
        for tname, tparent in target_bones:
            if tname[:4] == "DEF-":
                # patch to support head bone
                if tparent == 'head':
                    tparent = 'head_01'
                self.process_chain_bone(context, tname, tparent)
        
        return
    
    def build_chains(self, context):
        
        data = context.object.data
        
        chains = data.get("uefy_chains")
        if chains is None:
            return
        
        for k, v in chains.items():
            self.process_chain(context, k, v)
        
        return

    def rename_head(self, context):
        
        edit_bones = context.object.data.edit_bones
        head = edit_bones.get('head_01')
        head_ctl = edit_bones.get('head')
        if head is not None and head_ctl is not None:
            head_ctl.name = 'head_ctl_temp'
            head.name = 'head'
            head_ctl.name = 'head_01'
        
            for ob in context.object.children:
                if ob.type == 'MESH':
                    for vg in ob.vertex_groups:
                        if vg.name == 'head_01':
                            vg.name = 'head'
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return

    @classmethod
    def poll(cls, context):
        return context.armature
    
    def execute(self, context):
        
        bones = context.object.data.bones
        pose_bones = context.object.pose.bones
        edit_bones = context.object.data.edit_bones
        
        print("+++++")
        
        if edit_bones.get("pelvis") is not None:
            self.report('WARNING', "This operator has already been run on this Rig")
            return {"FINISHED"}
        
        # Build New Deform Skeleton
        self.do_build_skeleton(context)
        self.do_add_ik(context)
        
        if self.add_face == True:
            self.do_add_face(context)
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        if self.add_twist == True:
            self.do_add_twist(context)
            if  self.add_second_twist == True:
                self.do_add_second_twist(context)
        
        self.build_chains(context)
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        for bone in edit_bones:
            if bone.name[:4] == 'DEF-':
                print("Turn off deform on: " + bone.name)
                bone.use_deform = False
        
        self.rename_head(context)
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        bpy.ops.object.mode_set(mode = 'POSE')
        
        return {'FINISHED'}
    
    
class UEFY_OT_transfer_weight_paint(bpy.types.Operator):
    bl_idname = "uefy.weight_paint"
    bl_label = "Weight Paint"
    bl_description = "Transfer exiting weights to new skeleton"
    
    @classmethod
    def poll(cls, context):
        return context.armature
        
    def execute(self, context):
        global VertexGroupLookup, BoneLookup
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        for ob in context.object.children:
            if ob.type == 'MESH':
                for vg in ob.vertex_groups:
                    if VertexGroupLookup.get(vg.name) is not None:
                        print("vg.name: ", vg.name)
                        print("Found vg: ", VertexGroupLookup[vg.name])
                        #vg.name = BoneLookup[vg.name]
                        vg.name = VertexGroupLookup[vg.name]
            
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        return {'FINISHED'}

class UEFY_OT_add_custom_bones(bpy.types.Operator):
    bl_idname = "uefy.add_custom_bones"
    bl_label = "Register Extra Bone Chain"
    bl_description = "Add Custom Bones"
    
    source_name : bpy.props.StringProperty()
    target_name : bpy.props.StringProperty()
    
    org_bone_name : bpy.props.StringProperty()
    parent_bone_name : bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return context.armature
        
    def execute(self, context):
        
        data = context.object.data
        
        if data.get("uefy_chains") is None:
            data["uefy_chains"] = {}
        
        data["uefy_chains"][self.org_bone_name] = self.parent_bone_name
        
        return {'FINISHED'}

# Based on stackexchange answer
# attribution url: https://blender.stackexchange.com/questions/76222/how-to-match-bone-orientation-between-two-objects-in-python
def UEFY_FUNC_align_x_axis(edit_bone, new_x_axis_input):
    new_x_axis = new_x_axis_input.copy()
    new_x_axis = new_x_axis.cross(edit_bone.y_axis)
    new_x_axis.normalize()
    dot = max(-1.0, min(1.0, edit_bone.z_axis.dot(new_x_axis)))
    angle = math.acos(dot)
    edit_bone.roll += angle
    dot1 = edit_bone.z_axis.dot(new_x_axis)
    edit_bone.roll -= angle * 2.0
    dot2 = edit_bone.z_axis.dot(new_x_axis)
    if dot1 > dot2:
        edit_bone.roll += angle * 2.0

class UEFY_OT_ue_export_align(bpy.types.Operator):
    bl_idname = "uefy.ue_export_align"
    bl_label = "Set Original Bone Rolls"
    bl_description = "(Experimental) Set export bones to Original UE4 Mannequin bone rolls. Only use on Generated Rig with built Unreal Skeleton. Destructive operation not compatible with rigify."
    
    move_thigh_twist : bpy.props.BoolProperty()
    
    @classmethod
    def poll(cls, context):
        return context.armature
    
    def setup_skeleton(self, context):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        bones = context.object.data.edit_bones
        pbone_names = []
        
        for bone in bones:
            if bone.layers[24] or bone.layers[25] or bone.layers[26]:
                bone.use_connect = False
                pbone_names.append(bone.name)
        
        bpy.ops.object.mode_set(mode = 'POSE')
        
        for pbone_name in pbone_names:
            pbone = context.object.pose.bones[pbone_name]
            for c in pbone.constraints:
                c.influence = 0.0
        
        return

    def fix_foot(self, context):
        
        edit_bones = context.object.data.edit_bones
        
        foot_l = edit_bones['foot_l']
        foot_r = edit_bones['foot_r']
        
        y = mathutils.Vector([0,1,0])
        
        self.process_bone(foot_l, y, 1.0, -1.0)
        self.process_bone(foot_r, y, -1.0, 1.0)
        
        return
    
    def copy_bone(self, source, target):
        
        target.head = source.head
        target.tail = source.tail
        target.roll = source.roll
        
        return
    
    def fix_ik(self, context):
        
        edit_bones = context.object.data.edit_bones
        
        ik_hand_l = edit_bones['ik_hand_l']
        ik_hand_r = edit_bones['ik_hand_r']
        ik_hand_gun = edit_bones['ik_hand_gun']
        #ik_hand_root = edit_bones['ik_hand_root']
        
        #ik_foot_root = edit_bones['ik_foot_root']
        ik_foot_l = edit_bones['ik_foot_l']
        ik_foot_r = edit_bones['ik_foot_r']
        
        hand_l = edit_bones['hand_l']
        hand_r = edit_bones['hand_r']
        foot_l = edit_bones['foot_l']
        foot_r = edit_bones['foot_r']
        
        self.copy_bone(hand_l, ik_hand_l)
        self.copy_bone(hand_r, ik_hand_r)
        self.copy_bone(hand_r, ik_hand_gun)
        self.copy_bone(foot_l, ik_foot_l)
        self.copy_bone(foot_r, ik_foot_r)
        
        return

    def get_axis(self, bone, input):
        
        if input == 'x':
            return bone.x_axis
        if input == 'y':
            return bone.y_axis
        if input == 'z':
            return bone.z_axis
        
        return bone.z_axis.copy()
    
    def process_bone(self, bone, axis, align, roll_align):
        
        head = bone.head.copy()
        tail = head + axis * bone.length * align
        
        vec = bone.y_axis.copy()
        vec.normalize()
        
        vec = vec * roll_align
        
        bone.tail = tail
        UEFY_FUNC_align_x_axis(bone, vec)
        
        return
            
    def update_rolls(self, context):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        edit_bones = context.object.data.edit_bones
        
        for bone_name, bone_data in UEBoneAlignMapping.items():
            bone = edit_bones.get(bone_name)
            if bone is not None:
                av, align, roll_align = bone_data
                axis = self.get_axis(bone, av)
                axis.normalize()
                self.process_bone(bone, axis, align, roll_align)
        
        self.fix_foot(context)
        self.fix_ik(context)
                
        return

    def update_thigh_twist(self, context):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        edit_bones = context.object.data.edit_bones
        
        thigh_twist_l = edit_bones.get('thigh_twist_01_l')
        thigh_twist_r = edit_bones.get('thigh_twist_01_r')
        
        calf_l = edit_bones.get('calf_l')
        calf_r = edit_bones.get('calf_r')
        
        thigh_l = edit_bones.get('thigh_l')
        thigh_r = edit_bones.get('thigh_r')
        
        if thigh_twist_l is None or thigh_twist_r is None or calf_l is None or calf_r is None or thigh_l is None or thigh_r is None:
            return
        
        a = thigh_l.head.copy()
        b = calf_l.head.copy()
        
        v = b - a
        v = v / 2
        
        thigh_twist_l.head += v
        thigh_twist_l.tail += v
        
        a = thigh_r.head.copy()
        b = calf_r.head.copy()
        
        v = b - a
        v = v / 2
        
        thigh_twist_r.head += v
        thigh_twist_r.tail += v
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        
        return

    def execute(self, context):
        
        self.setup_skeleton(context)
        self.update_rolls(context)
        
        if self.move_thigh_twist:
            self.update_thigh_twist(context)
        
        return {'FINISHED'}

class UEFY_OT_roll_bone(bpy.types.Operator):
    bl_idname = "uefy.roll_bone"
    bl_label = "Roll Bone"
    bl_description = "Align selected bone X-axis to chosen axis"
    
    axis_type : bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return context.armature and context.mode == 'EDIT_ARMATURE'

    def get_axis(self, bone):
        
        if self.axis_type == 0:
            return bone.x_axis
        elif self.axis_type == 1:
            return bone.x_axis * -1.0
        elif self.axis_type == 2:
            return bone.z_axis
        elif self.axis_type == 3:
            return bone.z_axis * -1.0
        
        return bone.x_axis
        
    def update_bone(self, context, bone):
                
        vec = self.get_axis(bone)
        UEFY_FUNC_align_x_axis(bone, vec)
        
        return

    def execute(self, context):
        
        print(context.selected_editable_bones)
        
        for bone in context.selected_editable_bones:
            self.update_bone(context, bone)
        
        return {'FINISHED'}

class UEFY_OT_swap_y_axis(bpy.types.Operator):
    bl_idname = "uefy.swap_y_axis"
    bl_label = "Swap Y-axis"
    bl_description = "Swap Y-axis with chosen axis"
    
    axis_type : bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return context.armature and context.mode == 'EDIT_ARMATURE'

    def get_axis(self, bone):
        
        if self.axis_type == 0:
            return bone.x_axis
        elif self.axis_type == 1:
            return bone.x_axis * -1.0
        elif self.axis_type == 2:
            return bone.z_axis
        elif self.axis_type == 3:
            return bone.z_axis * -1.0
        
        return bone.x_axis
        
    def update_bone(self, context, bone):
                
        axis = self.get_axis(bone)
        an = axis.normalized()

        head = bone.head.copy()
        tail = head + an * bone.length
        
        vec = bone.y_axis.copy()
        vec.normalize()
        
        bone.tail = tail
        UEFY_FUNC_align_x_axis(bone, vec)
        
        return

    def execute(self, context):
        
        for bone in context.selected_editable_bones:
            self.update_bone(context, bone)
        
        return {'FINISHED'}

class UEFY_OT_test_button(bpy.types.Operator):
    bl_idname = "uefy.test_button"
    bl_label = "Test Button"
    bl_description = "Test Button"
    
    source_name : bpy.props.StringProperty()
    target_name : bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return context.armature

    def execute(self, context):
        
        print("Hello World")
                
        return {'FINISHED'}
    
classes = ( UEFY_armature_item, UEFY_bone_item, UEFY_scene_properties,
            UEFY_PT_build_skeleton_panel,
            UEFY_OT_refresh_armature_list,
            UEFY_OT_refresh_bone_list,
            UEFY_OT_setup_character_bones,
            UEFY_OT_setup_character_pose,
            UEFY_OT_setup_metarig_pose,
            UEFY_OT_duplicate_bone,
            UEFY_OT_transfer_weight_paint,
            UEFY_OT_add_custom_bones,
            UEFY_OT_ue_export_align,
            UEFY_OT_roll_bone,
            UEFY_OT_swap_y_axis,
            UEFY_OT_test_button
            )

#register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.uefy_character_objects = CollectionProperty(type=UEFY_armature_item)
    bpy.types.Scene.uefy_org_bone_objects = CollectionProperty(type=UEFY_bone_item)
    bpy.types.Scene.uefy_epic_bone_objects = CollectionProperty(type=UEFY_bone_item)
    bpy.ops.uefy.refresh_armature_list()

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.uefy_character_objects
    del bpy.types.Scene.uefy_org_bone_objects
    del bpy.types.Scene.uefy_epic_bone_objects
    del bpy.types.Scene.uefy_character_name
    del bpy.types.Scene.uefy_uemann_name
    del bpy.types.Scene.uefy_metarig_name
    del bpy.types.Scene.uefy_character_type
    del bpy.types.Scene.uefy_axis_type
    del bpy.types.Scene.uefy_fix_metarig
    del bpy.types.Scene.uefy_remove_face
    del bpy.types.Scene.uefy_remove_extras_chest
    del bpy.types.Scene.uefy_remove_extras_pelvis
    del bpy.types.Scene.uefy_add_face
    del bpy.types.Scene.uefy_add_extras_chest
    del bpy.types.Scene.uefy_add_extras_pelvis
    del bpy.types.Scene.uefy_add_twist
    del bpy.types.Scene.uefy_add_second_twist
    del bpy.types.Scene.uefy_move_thigh_twist
    
if __name__ == "__main__":
    register()
