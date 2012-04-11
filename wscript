#!/usr/bin/env python

import Options

from os import unlink, symlink
from os.path import exists, lexists

srcdir = "."
blddir = "build"
VERSION = "0.1.1"

def set_options(opt):
    opt.tool_options("compiler_cxx")

def configure(conf):
    conf.check_tool("compiler_cxx")
    conf.check_tool("node_addon")
    conf.check_cfg(package='libsparsehash', mandatory=1, args='--cflags --libs')
    conf.env.append_value('CXXFLAGS', ['-O2'])

def build(bld):
    obj = bld.new_task_gen("cxx", "shlib", "node_addon")

    obj.target = "irf"

    obj.source = ['irf/MurmurHash3.cpp', 'irf/randomForest.cpp', 'irf/node.cpp'];

def shutdown(): #HACK to get binding.node out of build directory.#better way to do this ?
    if Options.commands['clean']:
        if lexists('irf.node'):
            unlink('irf.node')
    else:
        if not lexists('irf.node'):
            if lexists('./build/Release/irf.node'):
                symlink('./build/Release/irf.node', 'irf.node')
            elif lexists('./build/default/default/irf.node'):
                symlink('./build/default/irf.node', 'irf.node')
