#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("module", help="the module to generate the badges")
args = parser.parse_args()

def print_travis(module):
    print(".. image:: https://travis-ci.org/bibi21000/{:s}.svg?branch=master".format(module))
    print("  :target: https://travis-ci.org/bibi21000/{:s}").format(module)
    print("  :alt: Travis status")

def print_circle(module):
    print(".. image:: https://circleci.com/gh/bibi21000/{:s}.png?style=shield".format(module))
    print("  :target: https://circleci.com/gh/bibi21000/{:s}").format(module)
    print("  :alt: CircleCI status")

def print_coveralls(module):
    print(".. image:: https://coveralls.io/repos/bibi21000/{:s}/badge.svg?branch=master&service=github".format(module))
    print("  :target: https://coveralls.io/github/bibi21000/{:s}?branch=master").format(module)
    print("  :alt: Coveralls results")

def print_landscape(module):
    print(".. image:: https://landscape.io/github/bibi21000/{:s}/master/landscape.svg?style=flat".format(module))
    print("  :target: https://landscape.io/github/bibi21000/{:s}/master").format(module)
    print("  :alt: Code Health")

def print_docker(module):
    print(".. image:: https://img.shields.io/imagelayers/image-size/bibi21000/{:s}/latest.svg".format(module))
    print("  :target: https://hub.docker.com/r/bibi21000/{:s}/").format(module)
    print("  :alt: Docker size")
    print("")
    print(".. image:: https://img.shields.io/imagelayers/layers/bibi21000/{:s}/latest.svg".format(module))
    print("  :target: https://hub.docker.com/r/bibi21000/{:s}/").format(module)
    print("  :alt: Docker layers")

def print_gitter(module):
    print(".. image:: https://badges.gitter.im/bibi21000/{:s}.svg".format(module))
    print("  :target: https://gitter.im/bibi21000/{:s}?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge").format(module)
    print("  :alt: Join the chat at https://gitter.im/bibi21000/{:s}")

print_travis(args.module)
