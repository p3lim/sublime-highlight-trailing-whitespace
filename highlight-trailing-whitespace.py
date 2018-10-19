import sublime
import sublime_plugin

import os
import json

NAMESPACE = 'HighlightTrailingWhitespace'
DEFAULT_COLOR_SCHEME = 'Monokai.sublime-color-scheme'
WHITESPACE_PATTERN = '[\t ]+$'

settings = None

def plugin_loaded():
	'''
	Called when the plugin is loaded, used to:
	- Load the settings for the package
	- Add callbacks for settings changes
	- Updates color scheme
	'''
	global settings
	settings = sublime.load_settings(NAMESPACE + '.sublime-settings')

	# refresh all views when a setting is changed
	settings.add_on_change('enabled', lambda: refresh_views())
	settings.add_on_change('never_on_cursor', lambda: refresh_views())
	settings.add_on_change('fill', lambda: refresh_views())

	# update color scheme when the color setting is changed
	settings.add_on_change('color', lambda: update_color_scheme())

	# update color scheme on load
	update_color_scheme()

def refresh_views():
	'''
	Iterates through all available views and updates the whitespace highlight.
	'''
	for window in sublime.windows():
		for view in window.views():
			highlight_whitespace(view)

def highlight_whitespace(view):
	'''
	Highlights any trailing whitespace in the given view.

	:param sublime.View view: The view of the file being highlighted.
	'''
	if view.size() > 1e5:
		# avoid crashing on large files
		return

	if view.settings().get('is_widget', False):
		# don't render in widget views
		return

	if settings.get('enabled'):
		regions = view.find_all(WHITESPACE_PATTERN)
		if regions:
			# whitespace was found, time to shine!
			if settings.get('never_on_cursor'):
				# check if the cursor is on one of the matched regions and remove it from the list
				selection = view.sel()[0]
				for region in regions:
					if region.contains(selection):
						regions.remove(region)
						break

			# determine if we should fill the region or just draw an outline
			draw_flag = sublime.DRAW_NO_FILL
			if settings.get('fill'):
				draw_flag = 0

			# draw on the region(s)
			view.add_regions(
				NAMESPACE,
				regions,
				NAMESPACE,
				'',
				sublime.DRAW_EMPTY | sublime.HIDE_ON_MINIMAP | draw_flag
			)
		else:
			# no whitespace, clear out
			view.erase_regions(NAMESPACE)
	else:
		# we're disabled, clean up
		view.erase_regions(NAMESPACE)

def update_color_scheme():
	'''
	Creates/updates a copy of the active color scheme with overloads for coloring
	the highlight regions.
	'''

	# get the first available view, as the color scheme is applied globally
	view = sublime.active_window().active_view()
	if not view:
		# there's no views open, bail out
		return

	# get the name of the current color scheme
	path = view.settings().get('color_scheme') or DEFAULT_COLOR_SCHEME
	if not path.startswith('Packages/'):
		path = 'Packages/Color Scheme - Default/' + path
	name = path.split('/')[-1].split('.')[0]

	# create directory we'll save our own color schemes
	scheme_path = os.path.join(sublime.packages_path(), 'User', NAMESPACE)
	if not os.path.exists(scheme_path):
		os.makedirs(scheme_path)

	# create our override color scheme
	style = {
		'name': 'Highlight Trailing Whitespace',
		'rules': [{
			'name': 'Outline',
			'scope': NAMESPACE,
			'foreground': settings.get('color'),
		}]
	}

	# attempt to create the color scheme, warning the user if it failed
	try:
		scheme_file = os.path.join(scheme_path, '{}.sublime-color-scheme'.format(name))
		with open(scheme_file, 'wb', buffering=0) as file:
			file.write(json.dumps(style, indent=4).encode('utf-8'))
	except PermissionError as e:
		sublime.ok_cancel_dialog('{} could not access file:\n{}'.format(NAMESPACE, e))
		raise e
	except OSError as e:
		sublime.ok_cancel_dialog('{} encountered an OS error:\n{}'.format(NAMESPACE, e))
		raise e

	# since the color was changed, also refresh all views
	refresh_views()

class HighlightTrailingWhitespaceListener(sublime_plugin.EventListener):
	def on_modified_async(self, view):
		'''
		Called when a view is modified, updating the highlight.
		'''
		highlight_whitespace(view)

	def on_activated_async(self, view):
		'''
		Called when a view is activated (selected), updating the highlight.
		'''
		highlight_whitespace(view)

	def on_load_async(self, view):
		'''
		Called when the view is loaded, updating the highlight.
		'''
		highlight_whitespace(view)

	def on_selection_modified_async(self, view):
		'''
		Called when the cursor has been moved in the view, updating the highlight.
		'''
		highlight_whitespace(view)
