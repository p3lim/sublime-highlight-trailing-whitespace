import sublime
import sublime_plugin

def highlight_whitespace(view):
	if(view.size() > 1e5):
		# avoid crashing on large files
		return

	if(view.settings().get('highlight_trailing_whitespace', False)):
		regions = view.find_all('[\t ]+$')
		if regions:
			if view.settings().get('highlight_trailing_whitespace_non_cursor', False):
				selection = view.sel()[0]
				for region in regions:
					if region.contains(selection):
						regions.remove(region)
						break

			view.add_regions('HighlightTrailingWhitespace', regions,
				'invalid', '', sublime.DRAW_EMPTY | sublime.DRAW_NO_FILL | sublime.HIDE_ON_MINIMAP)
		else:
			view.erase_regions('HighlightTrailingWhitespace')

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
			view.settings().add_on_change('HighlightTrailingWhitespace', lambda: highlight_whitespace(view))
