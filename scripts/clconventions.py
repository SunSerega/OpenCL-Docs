#!/usr/bin/python3 -i
#
# Copyright 2013-2024 The Khronos Group Inc.
# SPDX-License-Identifier: Apache-2.0

# Working-group-specific style conventions,
# used in generation.

import re

from conventions import ConventionsBase


class OpenCLConventions(ConventionsBase):
    def formatExtension(self, name):
        """Mark up a name as an extension for the spec."""
        return '`<<{}>>`'.format(name)

    @property
    def null(self):
        """Preferred spelling of NULL."""
        return '`NULL`'

    @property
    def constFlagBits(self):
        """Returns True if static const flag bits should be generated, False if an enumerated type should be generated."""
        return False

    @property
    def struct_macro(self):
        return 'sname:'

    @property
    def external_macro(self):
        return 'code:'

    @property
    def structtype_member_name(self):
        """Return name of the structure type member"""
        return 'sType'

    @property
    def nextpointer_member_name(self):
        """Return name of the structure pointer chain member"""
        return 'pNext'

    @property
    def valid_pointer_prefix(self):
        """Return prefix to pointers which must themselves be valid"""
        return 'valid'

    def is_structure_type_member(self, paramtype, paramname):
        """Determine if member type and name match the structure type member."""
        return False

    def is_nextpointer_member(self, paramtype, paramname):
        """Determine if member type and name match the next pointer chain member."""
        return paramtype == 'void' and paramname == self.nextpointer_member_name

    def generate_structure_type_from_name(self, structname):
        """Generate a structure type name token from a structure name.
           This should never be called for OpenCL, just other APIs."""
        return ''

    @property
    def warning_comment(self):
        """Return warning comment to be placed in header of generated Asciidoctor files"""
        return '// WARNING: DO NOT MODIFY! This file is automatically generated from the cl.xml registry'

    @property
    def file_suffix(self):
        """Return suffix of generated Asciidoctor files"""
        return '.txt'

    def api_name(self, spectype='api'):
        """Return API or specification name for citations in ref pages.ref
           pages should link to for

           spectype is the spec this refpage is for: 'api' is the OpenCL API
           Specification, 'clang' is the OpenCL C Language specification.
           Defaults to 'api'. If an unrecognized spectype is given, returns
           None.
        """
        if spectype == 'api' or spectype is None:
            return 'OpenCL'
        elif spectype == 'clang':
            return 'OpenCL C'
        else:
            return None

    @property
    def xml_supported_name_of_api(self):
        """Return the supported= attribute used in API XML"""
        return 'opencl'

    @property
    def api_prefix(self):
        """Return API token prefix"""
        return 'CL_'

    @property
    def api_version_prefix(self):
        """Return API core version token prefix"""
        return 'CL_VERSION_'

    @property
    def KHR_prefix(self):
        """Return extension name prefix for KHR extensions"""
        return 'cl_khr_'

    @property
    def EXT_prefix(self):
        """Return extension name prefix for EXT extensions"""
        return 'cl_ext_'

    @property
    def write_contacts(self):
        """Return whether contact list should be written to extension appendices"""
        return True

    @property
    def write_refpage_include(self):
        """Return whether refpage include should be written to extension appendices"""
        return False

    def writeFeature(self, featureExtraProtect, filename):
        """Returns True if OutputGenerator.endFeature should write this feature.
           Used in COutputGenerator
        """
        return True

    def requires_error_validation(self, return_type):
        """Returns True if the return_type element is an API result code
           requiring error validation.
        """
        return False

    @property
    def required_errors(self):
        """Return a list of required error codes for validation."""
        return []

    def is_externsync_command(self, protoname):
        """Returns True if the protoname element is an API command requiring
           external synchronization
        """
        return False

    def is_api_name(self, name):
        """Returns True if name is in the reserved API namespace.
        For OpenCL, these are names with a case-insensitive 'cl' prefix.
        """
        return name[0:2].lower() == 'cl'

    def is_voidpointer_alias(self, tag, text, tail):
        """Return True if the declaration components (tag,text,tail) of an
           element represents a void * type
        """
        return tag == 'type' and text == 'void' and tail.startswith('*')

    def make_voidpointer_alias(self, tail):
        """Reformat a void * declaration to include the API alias macro.
           Vulkan doesn't have an API alias macro, so do nothing.
        """
        return tail

    def specURL(self, spectype = 'api'):
        """Return public registry URL which ref pages should link to for
           full Specification, so xrefs in the asciidoc source that aren't
           to ref pages can link into it instead.

           spectype is the spec this refpage is for: 'api' is the OpenCL API
           Specification, 'clang' is the OpenCL C Language specification.
           Defaults to 'api'. If an unrecognized spectype is given, returns
           None.
        """
        if spectype == 'api' or spectype is None:
            return 'https://www.khronos.org/registry/OpenCL/specs/3.0-unified/html/OpenCL_API.html'
        elif spectype == 'clang':
            return 'https://www.khronos.org/registry/OpenCL/specs/3.0-unified/html/OpenCL_C.html'
        else:
            return None

    @property
    def xml_api_name(self):
        """Return the name used in the default API XML registry for the default API"""
        return 'opencl'

    @property
    def registry_path(self):
        """Return relpath to the default API XML registry in this project."""
        return 'xml/cl.xml'

    @property
    def specification_path(self):
        """Return relpath to the Asciidoctor specification sources in this project."""
        return '../appendices/meta'

    @property
    def extra_refpage_headers(self):
        """Return any extra text to add to refpage headers."""
        return 'include::{config}/attribs.txt[]\n' + \
            'include::{config}/opencl.asciidoc[]\n' + \
            'include::{config}/version-full-links.asciidoc[]\n' + \
            'include::{generated}/api/api-dictionary-no-links.asciidoc[]\n' + \
            'include::{cspec}/feature-dictionary.asciidoc[]\n' + \
            'include::{apispec}/footnotes.asciidoc[]\n' + \
            'include::{cspec}/footnotes.asciidoc[]\n'

    @property
    def extension_index_prefixes(self):
        """Return a list of extension prefixes used to group extension refpages."""
        return ['cl_khr', 'cl_ext', 'cl']

    @property
    def unified_flag_refpages(self):
        """Return True if Flags/FlagBits refpages are unified, False if
           they're separate.
        """
        return False

    @property
    def spec_reflow_path(self):
        """Return the relative path to the spec source folder to reflow"""
        return '.'

    @property
    def spec_no_reflow_dirs(self):
        """Return a set of directories not to automatically descend into
           when reflowing spec text
        """
        return ('scripts', 'style')

    @property
    def should_skip_checking_codes(self):
        """Return True if more than the basic validation of return codes should
        be skipped for a command.

        OpenCL has a different style of error handling than OpenXR or
        Vulkan, so these checks are not appropriate."""

        return True
