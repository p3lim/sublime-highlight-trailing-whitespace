# [Highlight Trailing Whitespace](//packagecontrol.io/packages/Highlight%20Trailing%20Whitespace)

This plugin will highlight any trailing whitespace.

You can enable this through the preferences (or syntax-specific) like so:
```json
{
	"highlight_trailing_whitespace": true,
	"highlight_trailing_whitespace_non_cursor": false,
	"highlight_trailing_whitespace_color": "#FF0000",
	"highlight_trailing_whitespace_fill": false
}
```

Supported color formats (from [official docs](https://www.sublimetext.com/docs/3/color_schemes.html#colors)):
- Hex RGB (`#RRGGBB`)
- Hex RGBA (`#RRGGBBAA`)
- RGB (`rgb(255, 0, 0)`)
- RGBA (`rgba(255, 255, 255, 0.5)`)
- HSL (`hsl(0, 100%, 100%)`)
- HSLA (`hsl(0, 100%, 100%, 0.5)`)
- [CSS color names](https://www.sublimetext.com/docs/3/color_schemes.html#css_colors) (`cyan`)

## Installation

##### Using the package manager

1. Install the [Sublime Text Package Control](//packagecontrol.io/installation) plugin if you haven't already.
2. Open up the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Package Control: Install Package`
3. Search for `Highlight Trailing Whitespace` and hit <kbd>Enter</kbd> to install.
4. Follow the instructions that appears on the screen.

##### Manual installation with Git

1. Click the `Preferences > Browse Packages` menu.
2. Open up a terminal and execute the following:
    - `git clone https://github.com/p3lim/sublime-highlight-trailing-whitespace Highlight\ Trailing\ Whitespace`
3. Restart Sublime Text.
