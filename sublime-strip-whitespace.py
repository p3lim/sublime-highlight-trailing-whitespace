import sublime
import sublime_plugin

def highlight_whitespace(view):
	if(view.settings().get('highlight_trailing_whitespace', False)):
		view.add_regions('HighlightTrailingWhitespace', view.find_all('[\t ]+$'),
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

def plugin_loaded():
	for window in sublime.windows():
		for view in window.views():
			view.settings().add_on_change('HighlightTrailingWhitespace', lambda: highlight_whitespace(view))
