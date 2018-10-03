import sublime
import sublime_plugin

import os
import json

NAMESPACE = 'HighlightTrailingWhitespace'
DEFAULT_COLOR_SCHEME = 'Monokai.sublime-color-scheme'
DEFAULT_COLOR = '#FF0000'

def highlight_whitespace(view):
	if view.size() > 1e5:
		# avoid crashing on large files
		return

	settings = view.settings()
	if settings.get('is_widget', False):
		# don't render in widget views
		return

	if settings.get('highlight_trailing_whitespace', False):
		regions = view.find_all('[\t ]+$')
		if regions:
			if settings.get('highlight_trailing_whitespace_non_cursor', False):
				selection = view.sel()[0]
				for region in regions:
					if region.contains(selection):
						regions.remove(region)
						break

			view.add_regions(NAMESPACE, regions, NAMESPACE, '',
				sublime.DRAW_EMPTY | sublime.HIDE_ON_MINIMAP |
				0 if settings.get('highlight_trailing_whitespace_fill', False) else sublime.DRAW_NO_FILL)
		else:
			view.erase_regions(NAMESPACE)

def update_colors(view):
	# get the name of the current color scheme
	path = view.settings().get('color_scheme') or DEFAULT_COLOR_SCHEME
	if not path.startswith('Packages/'):
		path = 'Packages/Color Scheme - Default/' + path

	name = path.split('/')[-1].split('.')[0]

	# create directory we'll save our own color schemes
	scheme_path = os.path.join(sublime.packages_path(), 'User', NAMESPACE)
	scheme_file = os.path.join(scheme_path, '{}.sublime-color-scheme'.format(name))
	if not os.path.exists(scheme_path):
		os.makedirs(scheme_path)

	# create our override color scheme
	style = {
		'name': 'Highlight Trailing Whitespace',
		'rules': [{
			'name': 'Outline',
			'scope': NAMESPACE,
			'foreground': view.settings().get('highlight_trailing_whitespace_color', DEFAULT_COLOR),
		}]
	}

	# attempt to create the color scheme, warning the user if it failed
	try:
		with open(scheme_file, 'wb', buffering=0) as file:
			file.write(json.dumps(style, indent=4).encode('utf-8'))
	except PermissionError as e:
		sublime.ok_cancel_dialog('{} could not access file:\n{}'.format(NAMESPACE, e))
		raise e
	except OSError as e:
		sublime.ok_cancel_dialog('{} encountered an OS error:\n{}'.format(NAMESPACE, e))
		raise e

	highlight_whitespace(view)

class HighlightTrailingWhitespace(sublime_plugin.EventListener):
	def on_modified_async(self, view):
		highlight_whitespace(view)

	def on_activated_async(self, view):
		highlight_whitespace(view)

	def on_load_async(self, view):
		highlight_whitespace(view)

	def on_selection_modified_async(self, view):
		highlight_whitespace(view)

def plugin_loaded():
	for window in sublime.windows():
		for view in window.views():
			view.settings().add_on_change(NAMESPACE, lambda: highlight_whitespace(view))
			last_view = view

	if last_view:
		# no need to update colors for every view, it's global
		update_colors(last_view)
