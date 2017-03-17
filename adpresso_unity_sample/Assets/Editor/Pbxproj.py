#!/usr/bin/env python
# encoding: utf-8
"""
Pbxproj.py

Copyright 2012 GREE, Inc.
  
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  
http://www.apache.org/licenses/LICENSE-2.0
  
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import hashlib
import logging
import os
import re
import sys
import Paths

pbxproj_cache = {}

# The following relative path methods recyled from:
# http://code.activestate.com/recipes/208993-compute-relative-path-from-one-directory-to-anothe/
# Author: Cimarron Taylor
# Date: July 6, 2003
def pathsplit(p, rest=[]):
    (h,t) = os.path.split(p)
    if len(h) < 1: return [t]+rest
    if len(t) < 1: return [h]+rest
    return pathsplit(h,[t]+rest)

def commonpath(l1, l2, common=[]):
    if len(l1) < 1: return (common, l1, l2)
    if len(l2) < 1: return (common, l1, l2)
    if l1[0] != l2[0]: return (common, l1, l2)
    return commonpath(l1[1:], l2[1:], common+[l1[0]])

def relpath(p1, p2):
    (common,l1,l2) = commonpath(pathsplit(p1), pathsplit(p2))
    p = []
    if len(l1) > 0:
        p = [ '../' * len(l1) ]
    p = p + l2
    return os.path.join( *p )

class Pbxproj(object):

	@staticmethod
	def get_pbxproj_by_name(name, xcode_version = None):
		if name not in pbxproj_cache:
			pbxproj_cache[name] = Pbxproj(name, xcode_version = xcode_version)

		return pbxproj_cache[name]

	# Valid names
	# /path/to/project.xcodeproj/project.pbxproj
	def __init__(self, name, xcode_version = None):
		self._project_data = None

		parts = name.split(':')
		self.name = parts[0]

		if len(parts) > 1:
			self.target = parts[1]
		else:
			valid_file_chars = '[a-zA-Z0-9\.\-:+ "\'!@#$%^&*\(\)]';
			if re.match('^'+valid_file_chars+'+$', self.name):
				self.target = self.name
			else:
				result = re.search('('+valid_file_chars+'+)\.xcodeproj', self.name)
				if not result:
					self.target = self.name
				else:
					(self.target, ) = result.groups()

		match = re.search('([^/\\\\]+)\.xcodeproj', self.name)
		if not match:
			self._project_name = self.name
		else:
			(self._project_name, ) = match.groups()

		self._guid = None
		self._deps = None
		self._xcode_version = xcode_version
		self._projectVersion = None
		self.guid()

	def __str__(self):
		return str(self.name)+" target:"+str(self.target)+" guid:"+str(self._guid)+" prodguid: "+self._product_guid+" prodname: "+self._product_name

	def uniqueid(self):
		return self.name + ':' + self.target

	def path(self):
		# TODO: No sense calculating this every time, just store it when we get the name.
		if re.match('^[a-zA-Z0-9\.\-:+"]+$', self.name):
			return os.path.join(Paths.src_dir, self.name.strip('"'), self.name.strip('"')+'.xcodeproj', 'project.pbxproj')
		elif not re.match('project.pbxproj$', self.name):
			return os.path.join(self.name, 'project.pbxproj')
		else:
			return self.name

	# A pbxproj file is contained within an xcodeproj file.
	# This method simply strips off the project.pbxproj part of the path.
	def xcodeprojpath(self):
		return os.path.dirname(self.path())

	def guid(self):
		if not self._guid:
			self.dependencies()

		return self._guid

	def version(self):
		if not self._projectVersion:
			self.dependencies()

		return self._projectVersion

	# Load the project data from disk.
	def get_project_data(self):
		if self._project_data is None:
			if not os.path.exists(self.path()):
				logging.info("Couldn't find the project at this path:")
				logging.info(self.path())
				return None

			project_file = open(self.path(), 'r')
			self._project_data = project_file.read()

		return self._project_data

	# Write the project data to disk.
	def set_project_data(self, project_data):
		if self._project_data != project_data:
			self._project_data = project_data
			project_file = open(self.path(), 'w')
			project_file.write(self._project_data)

	# Get and cache the dependencies for this project.
	def dependencies(self):
		if self._deps is not None:
			return self._deps

		project_data = self.get_project_data()
		
		if project_data is None:
			logging.error("Unable to open the project file at this path (is it readable?): "+self.path())
			return None

		# Get project file format version

		result = re.search('\tobjectVersion = ([0-9]+);', project_data)

		if not result:
			logging.error("Can't recover: unable to find the project version for your target at: "+self.path())
			return None
	
		(self._projectVersion,) = result.groups()
		self._projectVersion = int(self._projectVersion)

		# Get configuration list guid

		result = re.search('[A-Z0-9]+ \/\* '+re.escape(self.target)+' \*\/ = {\n[ \t]+isa = PBXNativeTarget;(?:.|\n)+?buildConfigurationList = ([A-Z0-9]+) \/\* Build configuration list for PBXNativeTarget "'+re.escape(self.target)+'" \*\/;',
		                   project_data)

		if result:
			(self.configurationListGuid, ) = result.groups()
		else:
			self.configurationListGuid = None


		# Get configuration list
		
		if self.configurationListGuid:
			match = re.search(re.escape(self.configurationListGuid)+' \/\* Build configuration list for PBXNativeTarget "'+re.escape(self.target)+'" \*\/ = \{\n[ \t]+isa = XCConfigurationList;\n[ \t]+buildConfigurations = \(\n((?:.|\n)+?)\);', project_data)
			if not match:
				logging.error("Couldn't find the configuration list.")
				return False

			(configurationList,) = match.groups()
			self.configurations = re.findall('[ \t]+([A-Z0-9]+) \/\* (.+) \*\/,\n', configurationList)

		# Get build phases

		result = re.search('([A-Z0-9]+) \/\* '+re.escape(self.target)+' \*\/ = {\n[ \t]+isa = PBXNativeTarget;(?:.|\n)+?buildPhases = \(\n((?:.|\n)+?)\);',
		                   project_data)
	
		if not result:
			logging.error("Can't recover: Unable to find the build phases from your target at: "+self.path())
			return None
	
		(self._guid, buildPhases, ) = result.groups()

		# Get the build phases we care about.

		match = re.search('([A-Z0-9]+) \/\* Resources \*\/', buildPhases)
		if match:
			(self._resources_guid, ) = match.groups()
		else:
			self._resources_guid = None
		
		match = re.search('([A-Z0-9]+) \/\* Frameworks \*\/', buildPhases)
		if not match:
			logging.error("Couldn't find the Frameworks phase from: "+self.path())
			logging.error("Please add a New Link Binary With Libraries Build Phase to your target")
			logging.error("Right click your target in the project, Add, New Build Phase,")
			logging.error("  \"New Link Binary With Libraries Build Phase\"")
			return None

		(self._frameworks_guid, ) = match.groups()

		# Get the dependencies

		result = re.search(re.escape(self._guid)+' \/\* '+re.escape(self.target)+' \*\/ = {\n[ \t]+isa = PBXNativeTarget;(?:.|\n)+?dependencies = \(\n((?:[ \t]+[A-Z0-9]+ \/\* PBXTargetDependency \*\/,\n)*)[ \t]*\);\n',
		                   project_data)
	
		if not result:
			logging.error("Unable to get dependencies from: "+self.path())
			return None
	
		(dependency_set, ) = result.groups()
		dependency_guids = re.findall('[ \t]+([A-Z0-9]+) \/\* PBXTargetDependency \*\/,\n', dependency_set)

		# Parse the dependencies

		dependency_names = []

		for guid in dependency_guids:
			result = re.search(guid+' \/\* PBXTargetDependency \*\/ = \{\n[ \t]+isa = PBXTargetDependency;\n[ \t]*name = (["a-zA-Z0-9\.\-]+);',
			                   project_data)
		
			if result:
				(dependency_name, ) = result.groups()
				dependency_names.append(dependency_name)

		self._deps = dependency_names


		# Get the product guid and name.

		result = re.search(re.escape(self._guid)+' \/\* '+re.escape(self.target)+' \*\/ = {\n[ \t]+isa = PBXNativeTarget;(?:.|\n)+?productReference = ([A-Z0-9]+) \/\* (.+?) \*\/;',
		                   project_data)
	
		if not result:
			logging.error("Unable to get product guid from: "+self.path())
			return None
	
		(self._product_guid, self._product_name, ) = result.groups()

		return self._deps

	# Add a line to the PBXBuildFile section.
	#
	# <default_guid> /* <name> in Frameworks */ = {isa = PBXBuildFile; fileRef = <file_ref_hash> /* <name> */; };
	#
	# Returns: <default_guid> if a line was added.
	#          Otherwise, the existing guid is returned.
	def add_buildfile(self, name, file_ref_hash, default_guid, is_optional):
		project_data = self.get_project_data()

		match = re.search('\/\* Begin PBXBuildFile section \*\/\n((?:.|\n)+?)\/\* End PBXBuildFile section \*\/', project_data)

		if not match:
			logging.error("Couldn't find PBXBuildFile section.")
			return None

		(subtext, ) = match.groups()

		buildfile_hash = None
		
		match = re.search('([A-Z0-9]+).+?fileRef = '+re.escape(file_ref_hash), subtext)
		if match:
			(buildfile_hash, ) = match.groups()
			logging.info("This build file already exists: "+buildfile_hash)
		
		if buildfile_hash is None:
			match = re.search('\/\* Begin PBXBuildFile section \*\/\n', project_data)

			buildfile_hash = default_guid
		
			libfiletext = "\t\t"+buildfile_hash+" /* "+name+" in Frameworks */ = {isa = PBXBuildFile; fileRef = "+file_ref_hash+" /* "+name+" */; };\n"
			if is_optional:
				libfiletext = "\t\t"+buildfile_hash+" /* "+name+" in Frameworks */ = {isa = PBXBuildFile; fileRef = "+file_ref_hash+" /* "+name+" */; settings = {ATTRIBUTES = (Weak, ); }; };\n"
			
			project_data = project_data[:match.end()] + libfiletext + project_data[match.end():]
		
		self.set_project_data(project_data)
		
		return buildfile_hash

	def add_bundlefile(self, name, file_ref_hash, default_guid):
		project_data = self.get_project_data()

		match = re.search('\/\* Begin PBXBuildFile section \*\/\n((?:.|\n)+?)\/\* End PBXBuildFile section \*\/', project_data)

		if not match:
			logging.error("Couldn't find PBXBuildFile section.")
			return None

		(subtext, ) = match.groups()

		buildfile_hash = None
		
		match = re.search('([A-Z0-9]+).+?fileRef = '+re.escape(file_ref_hash), subtext)
		if match:
			(buildfile_hash, ) = match.groups()
			logging.info("This build file already exists: "+buildfile_hash)
		
		if buildfile_hash is None:
			match = re.search('\/\* Begin PBXBuildFile section \*\/\n', project_data)

			buildfile_hash = default_guid
		
			libfiletext = "\t\t"+buildfile_hash+" /* "+name+" in Resource */ = {isa = PBXBuildFile; fileRef = "+file_ref_hash+" /* "+name+" */; };\n"
			project_data = project_data[:match.end()] + libfiletext + project_data[match.end():]
		
		self.set_project_data(project_data)
		
		return buildfile_hash

	# Add a line to the PBXFileReference section.
	#
	# <default_guid> /* <name> */ = {isa = PBXFileReference; lastKnownFileType = "wrapper.<file_type>"; name = <name>; path = <rel_path>; sourceTree = <source_tree>; };
	#
	# Returns: <default_guid> if a line was added.
	#          Otherwise, the existing guid is returned.
	def add_filereference(self, name, file_type, default_guid, rel_path, source_tree):
		project_data = self.get_project_data()

		quoted_rel_path = '"'+rel_path.strip('"')+'"'

		fileref_hash = None

		match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; name = '+re.escape(name)+'; path = '+re.escape(rel_path)+';', project_data)

		if not match:
			# Check again for quoted versions, just to be sure.
			match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; name = '+re.escape(name)+'; path = '+re.escape(quoted_rel_path)+';', project_data)

		if match:
			logging.info("This file has already been added.")
			(fileref_hash, ) = match.groups()
			
		else:
			match = re.search('\/\* Begin PBXFileReference section \*\/\n', project_data)

			if not match:
				logging.error("Couldn't find the PBXFileReference section.")
				return False

			fileref_hash = default_guid
			
			pbxfileref = "\t\t"+fileref_hash+" /* "+name+" */ = {isa = PBXFileReference; lastKnownFileType = \""+file_type+"\"; name = "+name+"; path = "+quoted_rel_path+"; sourceTree = "+source_tree+"; };\n"

			project_data = project_data[:match.end()] + pbxfileref + project_data[match.end():]

		self.set_project_data(project_data)

		return fileref_hash

	def add_headerreference(self, name, file_type, default_guid, rel_path, source_tree):
		project_data = self.get_project_data()

		quoted_rel_path = '"'+rel_path.strip('"')+'"'
		quoted_source_tree = '"'+source_tree.strip('"')+'"'

		fileref_hash = None

		match = re.search('([A-Z0-9]+) \/\* '+name+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = '+file_type+'; name = '+name+'; path = '+rel_path+'; sourceTree = '+source_tree+';', project_data)

		if match:
			logging.info("This file has already been added.")
			(fileref_hash, ) = match.groups()
			
		else:
			match = re.search('\/\* Begin PBXFileReference section \*\/\n', project_data)

			if not match:
				logging.error("Couldn't find the PBXFileReference section.")
				return False

			fileref_hash = default_guid
			
			pbxfileref = "\t\t"+fileref_hash+" /* "+name+" */ = {isa = PBXFileReference; lastKnownFileType = "+file_type+"; name = "+name+"; path = "+rel_path+"; sourceTree = "+source_tree+"; };\n"

			project_data = project_data[:match.end()] + pbxfileref + project_data[match.end():]

		self.set_project_data(project_data)

		return fileref_hash

	def add_archivereference(self, name, file_type, default_guid, rel_path, source_tree):
		project_data = self.get_project_data()

		quoted_rel_path = '"'+rel_path.strip('"')+'"'
		quoted_source_tree = '"'+source_tree.strip('"')+'"'

		fileref_hash = None

		match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; name = '+name+'; path = '+re.escape(rel_path)+';', project_data)
		#match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; path = '+re.escape(rel_path)+';', project_data)

		if not match:
			# Check again for quoted versions, just to be sure.
			match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; name = '+name+'; path = '+re.escape(quoted_rel_path)+';', project_data)
			#match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; path = '+re.escape(quoted_rel_path)+';', project_data)

		if match:
			logging.info("This file has already been added.")
			(fileref_hash, ) = match.groups()
			
		else:
			match = re.search('\/\* Begin PBXFileReference section \*\/\n', project_data)

			if not match:
				logging.error("Couldn't find the PBXFileReference section.")
				return False

			fileref_hash = default_guid
			
			pbxfileref = "\t\t"+fileref_hash+" /* "+name+" */ = {isa = PBXFileReference; lastKnownFileType = \""+file_type+"\"; name = "+name+"; path = "+rel_path+"; sourceTree = "+quoted_source_tree+"; };\n"
			#pbxfileref = "\t\t"+fileref_hash+" /* "+name+" */ = {isa = PBXFileReference; lastKnownFileType = \""+file_type+"\"; path = "+rel_path+"; sourceTree = "+quoted_source_tree+"; };\n"

			project_data = project_data[:match.end()] + pbxfileref + project_data[match.end():]

		self.set_project_data(project_data)

		return fileref_hash

	def add_bundlereference(self, name, file_type, default_guid, rel_path, source_tree):
		project_data = self.get_project_data()

		quoted_rel_path = '"'+rel_path.strip('"')+'"'
		quoted_source_tree = '"'+source_tree.strip('"')+'"'

		fileref_hash = None

		match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; path = '+re.escape(rel_path)+';', project_data)

		if not match:
			# Check again for quoted versions, just to be sure.
			match = re.search('([A-Z0-9]+) \/\* '+re.escape(name)+' \*\/ = \{isa = PBXFileReference; lastKnownFileType = "'+file_type+'"; path = '+re.escape(quoted_rel_path)+';', project_data)

		if match:
			logging.info("This file has already been added.")
			(fileref_hash, ) = match.groups()
			
		else:
			match = re.search('\/\* Begin PBXFileReference section \*\/\n', project_data)

			if not match:
				logging.error("Couldn't find the PBXFileReference section.")
				return False

			fileref_hash = default_guid
			
			pbxfileref = "\t\t"+fileref_hash+" /* "+name+" */ = {isa = PBXFileReference; lastKnownFileType = \""+file_type+"\"; path = "+rel_path+"; sourceTree = "+quoted_source_tree+"; };\n"

			project_data = project_data[:match.end()] + pbxfileref + project_data[match.end():]

		self.set_project_data(project_data)

		return fileref_hash

	# Add a file to the given PBXGroup.
	#
	# <guid> /* <name> */,
	def add_file_to_group(self, name, guid, group):
		project_data = self.get_project_data()

		match = re.search('\/\* '+re.escape(group)+' \*\/ = \{\n[ \t]+isa = PBXGroup;\n[ \t]+children = \(\n((?:.|\n)+?)\);', project_data)
		if not match:
			logging.error("Couldn't find the "+group+" children.")
			return False

		(children,) = match.groups()
		match = re.search(re.escape(guid), children)
		if match:
			logging.info("This file is already a member of the "+name+" group.")
		else:
			match = re.search('\/\* '+re.escape(group)+' \*\/ = \{\n[ \t]+isa = PBXGroup;\n[ \t]+children = \(\n', project_data)

			if not match:
				logging.error("Couldn't find the "+group+" group.")
				return False

			pbxgroup = "\t\t\t\t"+guid+" /* "+name+" */,\n"
			project_data = project_data[:match.end()] + pbxgroup + project_data[match.end():]

		self.set_project_data(project_data)

		return True

	# Add a file to the Frameworks PBXGroup.
	#
	# <guid> /* <name> */,
	def add_file_to_frameworks(self, name, guid):
		return self.add_file_to_group(name, guid, 'Frameworks')

	# Add a file to the Resources PBXGroup.
	#
	# <guid> /* <name> */,
	def add_file_to_resources(self, name, guid):
		match = re.search('\/\* '+re.escape('Libraries')+' \*\/ = \{\n[ \t]+isa = PBXGroup;\n[ \t]+children = \(\n((?:.|\n)+?)\);', self.get_project_data())
		if not match:
			return self.add_file_to_group(name, guid, 'Supporting Files')

		return self.add_file_to_group(name, guid, 'Libraries')

	def add_file_to_phase(self, name, guid, phase_guid, phase):
		project_data = self.get_project_data()

		match = re.search(re.escape(phase_guid)+" \/\* "+re.escape(phase)+" \*\/ = {(?:.|\n)+?files = \(((?:.|\n)+?)\);", project_data)

		if not match:
			logging.error("Couldn't find the "+phase+" phase.")
			return False

		(files, ) = match.groups()

		match = re.search(re.escape(guid), files)
		if match:
			logging.info("The file has already been added.")
		else:
			match = re.search(re.escape(phase_guid)+" \/\* "+phase+" \*\/ = {(?:.|\n)+?files = \(\n", project_data)
			if not match:
				logging.error("Couldn't find the "+phase+" files")
				return False

			frameworktext = "\t\t\t\t"+guid+" /* "+name+" in "+phase+" */,\n"
			project_data = project_data[:match.end()] + frameworktext + project_data[match.end():]

		self.set_project_data(project_data)

		return True

	def get_rel_path_to_products_dir(self):
		project_path = os.path.dirname(os.path.abspath(self.xcodeprojpath()))
		build_path = os.path.join(os.path.join(os.path.dirname(Paths.src_dir), 'Build'), 'Products')
		return relpath(project_path, build_path)

	def add_file_to_frameworks_phase(self, name, guid):
		return self.add_file_to_phase(name, guid, self._frameworks_guid, 'Frameworks')

	def add_file_to_resources_phase(self, name, guid):
		if self._resources_guid is None:
			logging.error("No resources build phase found in the destination project")
			logging.error("Please add a New Copy Bundle Resources Build Phase to your target")
			logging.error("Right click your target in the project, Add, New Build Phase,")
			logging.error("  \"New Copy Bundle Resources Build Phase\"")
			return False

		return self.add_file_to_phase(name, guid, self._resources_guid, 'Resources')

	def add_build_setting(self, configuration, setting_name, value):
		project_data = self.get_project_data()

		match = re.search('\/\* '+configuration+' \*\/ = {\n[ \t]+isa = XCBuildConfiguration;\n(?:.|\n)+?[ \t]+buildSettings = \{\n((?:.|\n)+?)\};', project_data)
		if not match:
			print "Couldn't find the "+configuration+" configuration in "+self.path()
			return False

		settings_start = match.start(1)
		settings_end = match.end(1)

		(build_settings, ) = match.groups()

		match = re.search(re.escape(setting_name)+' = ((?:.|\n)+?);', build_settings)

		if not match:
			# Add a brand new build setting. No checking for existing settings necessary.
			settingtext = '\t\t\t\t'+setting_name+' = '+value+';\n'

			project_data = project_data[:settings_start] + settingtext + project_data[settings_start:]
		else:
			# Build settings already exist. Is there one or many?
			(search_paths,) = match.groups()
			if re.search('\(\n', search_paths):
				# Many
				match = re.search(re.escape(value), search_paths)
				if not match:
					# If value has any spaces in it, Xcode will split it up into
					# multiple entries.
					escaped_value = re.escape(value).replace(' ', '",\n[ \t]+"')
					match = re.search(escaped_value, search_paths)
					if not match and not re.search(re.escape(value.strip('"')), search_paths):
						match = re.search(re.escape(setting_name)+' = \(\n', build_settings)

						build_settings = build_settings[:match.end()] + '\t\t\t\t\t'+value+',\n' + build_settings[match.end():]
						project_data = project_data[:settings_start] + build_settings + project_data[settings_end:]
			else:
				# One
				if search_paths.strip('"') != value.strip('"'):
					existing_path = search_paths
					path_set = '(\n\t\t\t\t\t'+value+',\n\t\t\t\t\t'+existing_path+'\n\t\t\t\t)'
					build_settings = build_settings[:match.start(1)] + path_set + build_settings[match.end(1):]
					project_data = project_data[:settings_start] + build_settings + project_data[settings_end:]

		self.set_project_data(project_data)

		return True

	def get_hash_base(self, uniquename):
		examplehash = '320FFFEEEDDDCCCBBBAAA000'
		uniquehash = hashlib.sha224(uniquename).hexdigest().upper()
		uniquehash = uniquehash[:len(examplehash) - 4]
		return '320'+uniquehash
	
	def add_framework(self, framework, is_optional):
		hash_base = self.get_hash_base(framework)
		
		fileref_hash = self.add_filereference(framework, 'wrapper.frameworks', hash_base+'0', 'System/Library/Frameworks/'+framework, 'SDKROOT')
		libfile_hash = self.add_buildfile(framework, fileref_hash, hash_base+'1', is_optional)
		if not self.add_file_to_frameworks(framework, fileref_hash):
			return False
		
		if not self.add_file_to_frameworks_phase(framework, libfile_hash):
			return False
		
		return True

	def add_my_framework(self, framework):
		hash_base = self.get_hash_base(framework)

		fileref_hash = self.add_filereference(framework, 'wrapper.framework', hash_base + '0', 'Libraries/' + framework, 'SOURCE_ROOT')
		libfile_hash = self.add_buildfile(framework, fileref_hash, hash_base + '1', False)
		if not self.add_file_to_frameworks(framework, fileref_hash):
			return False

		if not self.add_file_to_frameworks_phase(framework, libfile_hash):
			return False

		return True

	def add_lib(self, framework):
		hash_base = self.get_hash_base(framework)
		
		fileref_hash = self.add_filereference(framework, 'compiled.mach-o.dylib', hash_base+'0', 'usr/lib/'+framework, 'SDKROOT')
		libfile_hash = self.add_buildfile(framework, fileref_hash, hash_base+'1', False)
		if not self.add_file_to_frameworks(framework, fileref_hash):
			return False
		
		if not self.add_file_to_frameworks_phase(framework, libfile_hash):
			return False
		
		return True

	def add_archive(self, library):
		hash_base = self.get_hash_base(library)
		
		fileref_hash = self.add_archivereference(library, 'archive.ar', hash_base+'0', 'Libraries/'+library, 'SOURCE_ROOT')
		libfile_hash = self.add_buildfile(library, fileref_hash, hash_base+'1', False)
		if not self.add_file_to_resources(library, fileref_hash):
			return False
		
		if not self.add_file_to_frameworks_phase(library, libfile_hash):
			return False
		
		return True

	def add_header(self, header):
		hash_base = self.get_hash_base(header)

		headerref_hash = self.add_headerreference(header, 'sourcecode.c.h', hash_base+'0', 'Libraries/include/'+header, 'SOURCE_ROOT')
		self.add_file_to_group(header, headerref_hash, 'Headers')

		return True

	def add_bundle(self, bundle):
		hash_base = self.get_hash_base(bundle)

		fileref_hash = self.add_bundlereference(bundle, 'wrapper.plug-in', hash_base+'0', bundle, '<group>')

		libfile_hash = self.add_buildfile(bundle, fileref_hash, hash_base+'1', False)

		if not self.add_file_to_resources(bundle, fileref_hash):
			return False

		if not self.add_file_to_resources_phase(bundle, libfile_hash):
			return False

		return True

	def add_plist(self, plist):
		hash_base = self.get_hash_base(plist)

		fileref_hash = self.add_bundlereference(plist, 'text.plist.xml', hash_base+'0', plist, '<group>')

		libfile_hash = self.add_buildfile(plist, fileref_hash, hash_base+'1', False)

		if not self.add_file_to_resources(plist, fileref_hash):
			return False

		if not self.add_file_to_resources_phase(plist, libfile_hash):
			return False

		return True

	# Get the PBXFileReference from the given PBXBuildFile guid.
	def get_filerefguid_from_buildfileguid(self, buildfileguid):
		project_data = self.get_project_data()
		match = re.search(buildfileguid+' \/\* .+ \*\/ = {isa = PBXBuildFile; fileRef = ([A-Z0-9]+) \/\* .+ \*\/;', project_data)

		if not match:
			logging.error("Couldn't find PBXBuildFile row.")
			return None

		(filerefguid, ) = match.groups()
		
		return filerefguid

	def get_filepath_from_filerefguid(self, filerefguid):
		project_data = self.get_project_data()
		match = re.search(filerefguid+' \/\* .+ \*\/ = {isa = PBXFileReference; .+ path = (.+); .+ };', project_data)

		if not match:
			logging.error("Couldn't find PBXFileReference row.")
			return None

		(path, ) = match.groups()
		
		return path


	# Get all source files that are "built" in this project. This includes files built for
	# libraries, executables, and unit testing.
	def get_built_sources(self):
		project_data = self.get_project_data()
		match = re.search('\/\* Begin PBXSourcesBuildPhase section \*\/\n((?:.|\n)+?)\/\* End PBXSourcesBuildPhase section \*\/', project_data)

		if not match:
			logging.error("Couldn't find PBXSourcesBuildPhase section.")
			return None
		
		(buildphasedata, ) = match.groups()
		
		buildfileguids = re.findall('[ \t]+([A-Z0-9]+) \/\* .+ \*\/,\n', buildphasedata)
		
		project_path = os.path.dirname(os.path.abspath(self.xcodeprojpath()))
		
		filenames = []
		
		for buildfileguid in buildfileguids:
			filerefguid = self.get_filerefguid_from_buildfileguid(buildfileguid)
			filepath = self.get_filepath_from_filerefguid(filerefguid)

			filenames.append(os.path.join(project_path, filepath.strip('"')))

		return filenames


	# Get all header files that are "built" in this project. This includes files built for
	# libraries, executables, and unit testing.
	def get_built_headers(self):
		project_data = self.get_project_data()
		match = re.search('\/\* Begin PBXHeadersBuildPhase section \*\/\n((?:.|\n)+?)\/\* End PBXHeadersBuildPhase section \*\/', project_data)

		if not match:
			logging.error("Couldn't find PBXHeadersBuildPhase section.")
			return None
		
		(buildphasedata, ) = match.groups()

		buildfileguids = re.findall('[ \t]+([A-Z0-9]+) \/\* .+ \*\/,\n', buildphasedata)
		
		project_path = os.path.dirname(os.path.abspath(self.xcodeprojpath()))
		
		filenames = []
		
		for buildfileguid in buildfileguids:
			filerefguid = self.get_filerefguid_from_buildfileguid(buildfileguid)
			filepath = self.get_filepath_from_filerefguid(filerefguid)
			
			filenames.append(os.path.join(project_path, filepath.strip('"')))

		return filenames


	def add_group(self, group):
		hash_base = self.get_hash_base(group)
		self.add_file_to_group(group, hash_base+'0', 'CustomTemplate')

		project_data = self.get_project_data()
		
		if project_data is None:
			return False

		project_path = os.path.dirname(os.path.abspath(self.xcodeprojpath()))
	
		hash_base = self.get_hash_base(group)
	
		###############################################
		match = re.search('\/\* Begin PBXGroup section \*\/\n', project_data)
		if not match:
			logging.error("Couldn't find the group section.")
			return False
		
		group_start = match.end()

		lib_hash = hash_base+'0'

		match = re.search(re.escape(lib_hash)+" \/\* "+group+" \*\/ = \{\n[ \t]+isa = PBXGroup;\n[ \t]+children = \(\n((?:.|\n)+?)\);", project_data)
		if match:
			logging.info("This "+group+" group already exists.")
		else:
			grouptext = "\t\t"+lib_hash+" /* " + group +" */ = {\n\t\t\tisa = PBXGroup;\n\t\t\tchildren = (\n\t\t\t);\n\t\t\tname = "+group+";\n\t\t\tpath = "+group+";\n\t\t\tsourceTree = \"<group>\";\n\t\t};\n"
			project_data = project_data[:group_start] + grouptext + project_data[group_start:]

		self.set_project_data(project_data)

		return True
