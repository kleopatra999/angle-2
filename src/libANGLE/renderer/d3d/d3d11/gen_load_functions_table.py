#!/usr/bin/python
# Copyright 2015 The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# gen_load_functions_table.py:
#  Code generation for the load function tables used for texture formats
#

import json, sys

sys.path.append('../..')
import angle_format

template = """// GENERATED FILE - DO NOT EDIT.
// Generated by gen_load_functions_table.py using data from load_functions_data.json
//
// Copyright 2015 The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// load_functions_table:
//   Contains the GetLoadFunctionsMap for texture_format_util.h
//

#include "libANGLE/renderer/d3d/d3d11/load_functions_table.h"

#include "image_util/copyimage.h"
#include "image_util/generatemip.h"
#include "image_util/loadimage.h"

#include "libANGLE/renderer/d3d/d3d11/formatutils11.h"
#include "libANGLE/renderer/d3d/d3d11/texture_format_table.h"

using namespace angle;

namespace rx
{{

namespace d3d11
{{

namespace
{{

// ES3 image loading functions vary based on:
//    - the GL internal format (supplied to glTex*Image*D)
//    - the GL data type given (supplied to glTex*Image*D)
//    - the target DXGI_FORMAT that the image will be loaded into (which is chosen based on the D3D
//    device's capabilities)
// This map type determines which loading function to use, based on these three parameters.
// Source formats and types are taken from Tables 3.2 and 3.3 of the ES 3 spec.
void UnimplementedLoadFunction(size_t width,
                               size_t height,
                               size_t depth,
                               const uint8_t *input,
                               size_t inputRowPitch,
                               size_t inputDepthPitch,
                               uint8_t *output,
                               size_t outputRowPitch,
                               size_t outputDepthPitch)
{{
    UNIMPLEMENTED();
}}

void UnreachableLoadFunction(size_t width,
                             size_t height,
                             size_t depth,
                             const uint8_t *input,
                             size_t inputRowPitch,
                             size_t inputDepthPitch,
                             uint8_t *output,
                             size_t outputRowPitch,
                             size_t outputDepthPitch)
{{
    UNREACHABLE();
}}

}}  // namespace

// TODO we can replace these maps with more generated code
const std::map<GLenum, LoadImageFunctionInfo> &GetLoadFunctionsMap(GLenum {internal_format},
                                                                   DXGI_FORMAT {dxgi_format})
{{
    // clang-format off
    switch ({internal_format})
    {{
{data}
        default:
        {{
            static std::map<GLenum, LoadImageFunctionInfo> emptyLoadFunctionsMap;
            return emptyLoadFunctionsMap;
        }}
    }}
    // clang-format on

}}  // GetLoadFunctionsMap

}}  // namespace d3d11

}}  // namespace rx
"""

internal_format_param = 'internalFormat'
dxgi_format_param = 'dxgiFormat'
dxgi_format_unknown = "DXGI_FORMAT_UNKNOWN"

def get_function_maps_string(typestr, function):
    requiresConversion = str('LoadToNative<' not in function).lower()
    return '    { ' + typestr + ', LoadImageFunctionInfo(' + function + ', ' + requiresConversion + ') },\n'

def get_unknown_format_string(s, dxgi_to_type_map, dxgi_unknown_string):
     if dxgi_unknown_string not in dxgi_to_type_map:
        return ''

     table_data = ''

     for gl_type, load_function in sorted(dxgi_to_type_map[dxgi_unknown_string].iteritems()):
        table_data += s + get_function_maps_string(gl_type, load_function)

     return table_data

def get_load_function_map_snippet(s, insert_map_string):
    load_function_map_snippet = ''
    load_function_map_snippet += s + 'static const std::map<GLenum, LoadImageFunctionInfo> loadFunctionsMap = {\n'
    load_function_map_snippet += insert_map_string
    load_function_map_snippet += s + '};\n\n'
    load_function_map_snippet += s + 'return loadFunctionsMap;\n'

    return load_function_map_snippet

def parse_json_into_switch_string(json_data):
    table_data = ''
    for internal_format, dxgi_to_type_map in sorted(json_data.iteritems()):

        s = '        '

        table_data += s + 'case ' + internal_format + ':\n'

        do_switch = len(dxgi_to_type_map) > 1 or dxgi_to_type_map.keys()[0] != dxgi_format_unknown

        if do_switch:
            table_data += s + '{\n'
            s += '    '
            table_data += s + 'switch (' + dxgi_format_param + ')\n'
            table_data += s + '{\n'
            s += '    '

        for dxgi_format, type_functions in sorted(dxgi_to_type_map.iteritems()):

            if dxgi_format == dxgi_format_unknown:
                continue

            # Main case statements
            table_data += s + 'case ' + dxgi_format + ':\n'
            table_data += s + '{\n'
            s += '    '
            insert_map_string = ''

            if dxgi_format_unknown in dxgi_to_type_map:
                for gl_type, load_function in dxgi_to_type_map[dxgi_format_unknown].iteritems():
                    if gl_type not in type_functions:
                        type_functions[gl_type] = load_function

            for gl_type, load_function in sorted(type_functions.iteritems()):
                insert_map_string += s + get_function_maps_string(gl_type, load_function)

            table_data += get_load_function_map_snippet(s, insert_map_string)
            s = s[4:]
            table_data += s + '}\n'

        if do_switch:
            table_data += s + 'default:\n'

        if dxgi_format_unknown in dxgi_to_type_map:
            table_data += s + '{\n'
            s += '    '
            dxgi_unknown_str = get_unknown_format_string(
                s, dxgi_to_type_map, dxgi_format_unknown);
            table_data += get_load_function_map_snippet(s, dxgi_unknown_str)
            s = s[4:]
            table_data += s + '}\n'
        else:
            table_data += s + '    break;\n'

        if do_switch:
            s = s[4:]
            table_data += s + '}\n'
            s = s[4:]
            table_data += s + '}\n'

    return table_data

json_data = angle_format.load_json('load_functions_data.json')

table_data = parse_json_into_switch_string(json_data)
output = template.format(internal_format = internal_format_param,
                         dxgi_format = dxgi_format_param,
                         data=table_data)

with open('load_functions_table_autogen.cpp', 'wt') as out_file:
    out_file.write(output)
    out_file.close()
