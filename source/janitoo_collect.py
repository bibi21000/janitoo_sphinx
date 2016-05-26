#!/usr/bin/env python
# -*- coding: utf-8 -*-
from janitoo_packaging import packaging

package = packaging.Package(setuppy='setup', directory="../../..")#~ package = packaging.Package(setuppy='setup', directory="../../janitoo")

def print_header(name):
    title = "%s package"%name
    print title
    print "=" * len(title)
    print
    print "Show janitoo's extensions."
    print

def print_section(section):
    print section
    print "-" * len(section)
    print

def print_sub_section(section, items):
    print section
    print "^" * len(section)
    print
    for item in items:
        print " - %s (%s)"%(item, items[item])
    print

print_header(package.get_name())
if len(package.get_janitoo_threads())>0 or \
       len(package.get_janitoo_components())>0 or \
       len(package.get_janitoo_values())>0:
    print_section('Core extensions')
    if len(package.get_janitoo_models())>0:
        print_sub_section('Models', package.get_janitoo_models())
    if len(package.get_janitoo_threads())>0:
        print_sub_section('Threads', package.get_janitoo_threads())
    if len(package.get_janitoo_components())>0:
        print_sub_section('Components', package.get_janitoo_components())
    if len(package.get_janitoo_bus_extensions())>0:
        print_sub_section('Bus extensions ', package.get_janitoo_bus_extensions())
    if len(package.get_janitoo_values())>0:
        print_sub_section('Values', package.get_janitoo_values())
if len(package.get_janitoo_web_socketio())>0 or \
       len(package.get_janitoo_web_views())>0 or \
       len(package.get_janitoo_web_template())>0 or \
       len(package.get_janitoo_web_network())>0:
    print_section('Web extensions')
    if len(package.get_janitoo_web_socketio())>0:
        print_sub_section('Socketio', package.get_janitoo_web_socketio())
    if len(package.get_janitoo_web_views())>0:
        print_sub_section('Views', package.get_janitoo_web_views())
    if len(package.get_janitoo_web_template())>0:
        print_sub_section('Template', package.get_janitoo_web_template())
    if len(package.get_janitoo_web_network())>0:
        print_sub_section('Network', package.get_janitoo_web_network())
if len(package.get_janitoo_admin_socketio())>0 or \
       len(package.get_janitoo_admin_views())>0 or \
       len(package.get_janitoo_admin_template())>0 or \
       len(package.get_janitoo_admin_widget())>0 or \
       len(package.get_janitoo_admin_network())>0:
    print_section('Admin extensions')
    if len(package.get_janitoo_admin_socketio())>0:
        print_sub_section('Socketio', package.get_janitoo_admin_socketio())
    if len(package.get_janitoo_admin_views())>0:
        print_sub_section('Views', package.get_janitoo_admin_views())
    if len(package.get_janitoo_admin_template())>0:
        print_sub_section('Template', package.get_janitoo_admin_template())
    if len(package.get_janitoo_admin_widget())>0:
        print_sub_section('Widget', package.get_janitoo_admin_widget())
    if len(package.get_janitoo_admin_network())>0:
        print_sub_section('Network', package.get_janitoo_admin_network())
if len(package.get_janitoo_manager_socketio())>0 or \
       len(package.get_janitoo_manager_blueprint())>0 or \
       len(package.get_janitoo_manager_network())>0:
    print_section('Manager extensions')
    if len(package.get_janitoo_manager_views())>0:
        print_sub_section('Blueprint', package.get_janitoo_manager_blueprint())
    if len(package.get_janitoo_manager_network())>0:
        print_sub_section('Network', package.get_janitoo_manager_network())
    if len(package.get_janitoo_manager_socketio())>0:
        print_sub_section('Socketio', package.get_janitoo_manager_socketio())
