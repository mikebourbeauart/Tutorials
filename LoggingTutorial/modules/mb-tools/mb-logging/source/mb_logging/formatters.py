import logging
import sys
import platform


class ColorFormatter(logging.Formatter):

	BLACK = (0, 30)
	RED = (0, 31)
	LRED = (1, 31)

	GREEN = (0, 32)
	LGREEN = (1, 32)

	YELLOW = (0, 33)
	LYELLOW = (1, 33)

	BLUE = (0, 34)
	MAGENTA = (0, 35)

	CYAN = (0, 36)
	LCYAN = (1, 36)

	WHITE = (0, 37)

	COLORS = {
		'WARNING': YELLOW,
		'INFO': CYAN,
		'DEBUG': WHITE,
		'CRITICAL': MAGENTA,
		'ERROR': RED,
	}

	RESET_SEQ = "\033[0m"
	COLOR_SEQ = "\033[%d;%dm"

	def format(self, record):
		levelname = record.levelname

		text_color = self.COLOR_SEQ % self.COLORS[levelname]

		# print text_color
		message = super(ColorFormatter, self).format(record)

		color_message = []
		color_message.append(text_color)
		color_message.append(message)
		color_message.append(self.RESET_SEQ)
		color_message = "".join(color_message)

		if 'win' not in platform.platform():
			if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
				return color_message
		return message
