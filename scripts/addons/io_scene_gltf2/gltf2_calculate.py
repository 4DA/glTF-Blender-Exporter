# Copyright (c) 2017 The Khronos Group Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Imports
#

import mathutils

from .gltf2_debug import *

#
# Globals
#

#
# Functions
#

def calculate_tangent(internal_primitive, texcoord_id = 'TEXCOORD_0'):
    if internal_primitive is None:
        return None
    
    internal_attributes = internal_primitive['attributes']
    
    if internal_attributes.get(texcoord_id) is None:
        return None
    
    #
    
    indices = internal_primitive['indices']
    
    position = internal_attributes['POSITION']

    normal = internal_attributes['NORMAL']
    
    texcoord = internal_attributes[texcoord_id]
    
    #
    
    index_to_tangent = {}
    
    for i in range(0, len(indices), 3):
        t0 = indices[i + 0] 
        t1 = indices[i + 1]
        t2 = indices[i + 2]
        
        vi0 = t0 * 3
        vi1 = t1 * 3
        vi2 = t2 * 3

        p0 = mathutils.Vector((position[vi0 + 0], position[vi0 + 1], position[vi0 + 2])) 
        p1 = mathutils.Vector((position[vi1 + 0], position[vi1 + 1], position[vi1 + 2]))
        p2 = mathutils.Vector((position[vi2 + 0], position[vi2 + 1], position[vi2 + 2]))
        
        uv0 = mathutils.Vector((texcoord[t0 * 2 + 0], texcoord[t0 * 2 + 1])) 
        uv1 = mathutils.Vector((texcoord[t1 * 2 + 0], texcoord[t1 * 2 + 1]))
        uv2 = mathutils.Vector((texcoord[t2 * 2 + 0], texcoord[t2 * 2 + 1]))
        
        #
        
        deltaP0 = p1 - p0
        deltaP1 = p2 - p0 

        deltaUV0 = uv1 - uv0
        deltaUV1 = uv2 - uv0
        
        #
        
        divisor = deltaUV0.x * deltaUV1.y - deltaUV0.y * deltaUV1.x 
        
        if divisor == 0.0:
            continue
        
        tangent = ((deltaP0 * deltaUV1.y - deltaP1 * deltaUV0.y) / divisor)
        tangent.normalize()
        
        if index_to_tangent.get(vi0) is None:
            index_to_tangent[vi0] = tangent
        else: 
            index_to_tangent[vi0] += tangent
        
        if index_to_tangent.get(vi1) is None:
            index_to_tangent[vi1] = tangent
        else: 
            index_to_tangent[vi1] += tangent

        if index_to_tangent.get(vi2) is None:
            index_to_tangent[vi2] = tangent
        else: 
            index_to_tangent[vi2] += tangent
    
    #
    
    if len(index_to_tangent) * 3 != len(normal):
        return None
    
    #
    
    result = [0.0] * len(index_to_tangent) * 4
    
    for vi, tangent in index_to_tangent.items():
        n = mathutils.Vector((normal[vi + 0], normal[vi + 1], normal[vi + 2]))
        t = mathutils.Vector((n.z, n.x, n.y))
        
        if tangent.length != 0.0:
            tangent.normalize()
            t = tangent
        
        ti = (vi // 3) * 4
        
        result[ti + 0] = t.x
        result[ti + 1] = t.y
        result[ti + 2] = t.z
        result[ti + 3] = 1.0
     
    return result
