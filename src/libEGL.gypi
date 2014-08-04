# Copyright (c) 2013 The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
    'variables':
    {
        'angle_enable_d3d9%': 1,
        'angle_enable_d3d11%': 1,
        # This file list is shared with the GN build.
        'angle_libegl_sources':
        [
            '../include/EGL/egl.h',
            '../include/EGL/eglext.h',
            '../include/EGL/eglplatform.h',
            '../include/GLES2/gl2.h',
            '../include/GLES2/gl2ext.h',
            '../include/GLES2/gl2platform.h',
            '../include/GLES3/gl3.h',
            '../include/GLES3/gl3ext.h',
            '../include/GLES3/gl3platform.h',
            '../include/GLSLANG/ShaderLang.h',
            '../include/GLSLANG/ShaderVars.h',
            '../include/KHR/khrplatform.h',
            '../include/angle_gl.h',
            'common/RefCountObject.cpp',
            'common/RefCountObject.h',
            'common/angleutils.h',
            'common/blocklayout.cpp',
            'common/blocklayout.h',
            'common/debug.cpp',
            'common/debug.h',
            'common/event_tracer.cpp',
            'common/event_tracer.h',
            'common/mathutil.cpp',
            'common/mathutil.h',
            'common/platform.h',
            'common/shadervars.cpp',
            'common/surfacehost.h',
            'common/tls.cpp',
            'common/tls.h',
            'common/utilities.cpp',
            'common/utilities.h',
            'common/version.h',
            'libEGL/Config.cpp',
            'libEGL/Config.h',
            'libEGL/Display.cpp',
            'libEGL/Display.h',
            'libEGL/Surface.cpp',
            'libEGL/Surface.h',
            'libEGL/libEGL.cpp',
            'libEGL/libEGL.def',
            'libEGL/libEGL.rc',
            'libEGL/main.cpp',
            'libEGL/main.h',
            'libEGL/resource.h',
        ],
        'angle_libegl_win32_sources':
        [
            'common/win32/hwndhost.cpp',
        ],
        'angle_libegl_winrt_sources':
        [
            'common/winrt/corewindowhost.cpp',
            'common/winrt/corewindowhost.h',
            'common/winrt/iinspectablehost.cpp',
            'common/winrt/iinspectablehost.h',
            'common/winrt/swapchainpanelhost.cpp',
            'common/winrt/swapchainpanelhost.h',
            'common/winrt/winrtutils.cpp',
            'common/winrt/winrtutils.h',
            'third_party/threademulation/ThreadEmulation.cpp',
            'third_party/threademulation/ThreadEmulation.h',
        ],
    },
    # Everything below this is duplicated in the GN build. If you change
    # anything also change angle/BUILD.gn
    'conditions':
    [
        ['OS=="win"',
        {
            'targets':
            [
                {
                    'target_name': 'libEGL',
                    'type': 'shared_library',
                    'dependencies': [ 'libGLESv2', 'commit_id' ],
                    'include_dirs':
                    [
                        '.',
                        '../include',
                        'libGLESv2',
                    ],
                    'sources':
                    [
                        '<@(angle_libegl_sources)',
                    ],
                    'defines':
                    [
                        'GL_APICALL=',
                        'GL_GLEXT_PROTOTYPES=',
                        'EGLAPI=',
                    ],
                    'conditions':
                    [
                        ['angle_build_winrt==0',
                        {
                            'defines':
                            [
                                'GL_APICALL=',
                                'GL_GLEXT_PROTOTYPES=',
                                'EGLAPI=',
                            ],
                            'sources':
                            [
                                '<@(angle_libegl_win32_sources)',
                            ],
                        }],
                        ['angle_build_winrt==1',
                        {
                            'defines':
                            [
                                'GL_APICALL=',
                                'GL_GLEXT_PROTOTYPES=',
                                'EGLAPI=',
                                'NTDDI_VERSION=NTDDI_WINBLUE',
                                'ANGLE_ENABLE_RENDER_TO_BACK_BUFFER',
                            ],
                            'sources':
                            [
                                '<@(angle_libegl_winrt_sources)',
                            ],
                            'msvs_enable_winrt' : '1',
                            'msvs_requires_importlibrary' : '1',
                            'msvs_settings':
                            {
                                'VCLinkerTool':
                                {
                                    'EnableCOMDATFolding': '1',
                                    'OptimizeReferences': '1',
                                }
                            },
                        }],
                        ['angle_build_winphone==1',
                        {
                            'msvs_enable_winphone' : '1',
                        }],
                    ],
                    'includes': [ '../build/common_defines.gypi', ],
                    'msvs_settings':
                    {
                        'VCLinkerTool':
                        {
                            'conditions':
                            [
                                ['angle_build_winrt==0',
                                {
                                    'AdditionalDependencies':
                                    [
                                        'd3d9.lib',
                                    ],
                                }],
                            ],
                        },
                    },
                    'configurations':
                    {
                        'Debug':
                        {
                            'defines':
                            [
                                'ANGLE_ENABLE_PERF',
                            ],
                        },
                    },
                },
            ],
        },
        ],
    ],
}
