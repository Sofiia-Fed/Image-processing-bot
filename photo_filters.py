filters_names = [
	'negative', 'shades of gray', 'solar filter', 'water filter',
	'raspberry filter',
	'shades of red', 'shades of green', 'shades of blue',
]

filters = {

	'negative': lambda r, g, b: (255-r, 255-g, 255-b),

	'shades of gray': lambda r, g, b: (int(r*0.216 + g*0.7152 + b*0.072),)*3,

	'shades of red': lambda r, g, b: (r+75 if r+75 <= 255 else 255, g, b),

	'shades of green': lambda r, g, b: (r, g+75 if g+75 <= 255 else 255, b),

	'shades of blue': lambda r, g, b: (r, g, b+75 if b+75 <= 255 else 255),

	'solar filter': lambda r, g, b: (r, g, 0),

	'water filter': lambda r, g, b: (0, g, b),

	'raspberry filter': lambda r, g, b: (r, 0, b),
}


