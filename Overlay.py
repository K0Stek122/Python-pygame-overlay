import pygame
import win32api
import win32con
import win32gui
import sys
import os
import keyboard

TRANSPARENT = (255, 0, 128)
NOSIZE = 1
NOMOVE = 2
TOPMOST = -1
NOT_TOPMOST = -2

class Vector:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	def __ne__(self, other):
		this = self.x + self.y + self.w + self.h
		_other = other.x + other.y + other.w + other.h
		return this != _other

class Figure:
	def __init__(self, vector, color):
		self.vector = vector
		self.color = color

class Rectangle(Figure):
	def __init__(self, vector, color):
		self.type = "Rectangle"
		super().__init__(vector, color)

class Circle(Figure):
	def __init__(self, vector, color, thickness, radius):
		self.type = "Circle"
		self.thickness = thickness
		self.radius = radius
		super().__init__(vector, color)

class Line(Figure):
	def __init__(self, vector, color, thickness): #x = x1, y = y1, w = x2, h = y2
		self.type = "Line"
		self.thickness = thickness
		super().__init__(vector, color)

class Text(Figure):
	def __init__(self, vector, color, text, fontObject):
		self.type = "Text"
		self.text = text
		self.fontObject = fontObject
		super().__init__(vector, color)

class Overlay:
	def __init__(self, WindowTitle):
		self.figuresToDraw = []

		#Get Target Window And Rect
		self.targetHwnd = win32gui.FindWindow(None, WindowTitle)
		if not self.targetHwnd:
			sys.exit(f"Window Not Found: {WindowTitle}")
		self.targetRect = self.GetTargetWindowRect()

		#Init Pygame
		os.environ['SDL_VIDEO_WINDOW_POS'] = str(self.targetRect.x) + "," + str(self.targetRect.y)
		pygame.init()
		self.screen = pygame.display.set_mode((self.targetRect.w, self.targetRect.h), pygame.NOFRAME)
		self.hWnd = pygame.display.get_wm_info()['window']
		win32gui.SetWindowLong(self.hWnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hWnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
		win32gui.SetLayeredWindowAttributes(self.hWnd, win32api.RGB(*TRANSPARENT), 0, win32con.LWA_COLORKEY)
		win32gui.BringWindowToTop(self.hWnd)
		win32gui.SetWindowPos(self.hWnd, TOPMOST, 0, 0, 0, 0, NOMOVE | NOSIZE)
		self.window = True

	def GetTargetWindowRect(self):
		rect = win32gui.GetWindowRect(self.targetHwnd)
		ret = Vector(rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])
		return ret

	def handle(self):
		win32gui.SetWindowPos(self.hWnd, TOPMOST, self.targetRect.x, self.targetRect.y, 0, 0, NOMOVE | NOSIZE)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.window = False
		if self.targetRect != self.GetTargetWindowRect():
			self.targetRect = self.GetTargetWindowRect()
			win32gui.SetWindowPos(self.hWnd, TOPMOST, 0, 0, 0, 0, NOMOVE | NOSIZE)
			win32gui.MoveWindow(self.hWnd, self.targetRect.x, self.targetRect.y, self.targetRect.w, self.targetRect.h, True)

		self.screen.fill(TRANSPARENT)
		for figure in self.figuresToDraw:
			if figure.type == "Rectangle":
				pygame.draw.rect(self.screen, figure.color, pygame.Rect(figure.vector.x, figure.vector.y, figure.vector.w, figure.vector.h))
			elif figure.type == "Circle":
				pygame.draw.circle(self.screen, figure.color, (figure.vector.x, figure.vector.y), figure.radius, figure.thickness)
			elif figure.type == "Line":
				pygame.draw.line(surface=self.screen, color=figure.color, start_pos=(figure.vector.x, figure.vector.y), end_pos=(figure.vector.w, figure.vector.h), width=figure.thickness)
			elif figure.type == "Text":
				self.screen.blit(figure.fontObject.render(figure.text, 1, figure.color), (figure.vector.x, figure.vector.y))
		self.figuresToDraw[:] = []
		pygame.display.update()
		pygame.time.Clock().tick(60)

	def draw(self, figure : str, vector : Vector, color, thickness=None, radius=None, text=None, fontObject=None):
		if figure == "fillRect":
			self.figuresToDraw.append(Rectangle(vector, color))
		elif figure == "Circle":
			self.figuresToDraw.append(Circle(vector, color, thickness, radius))
		elif figure == "Line":
			self.figuresToDraw.append(Line(vector, color, thickness))
		elif figure == "Text":
			self.figuresToDraw.append(Text(vector, color, text, fontObject))

	def CreateFont(self, fontName, fontSize, bold=False, italic=False):
		return pygame.font.SysFont(name=fontName, size=fontSize, bold=bold, italic=italic)


targetWindow = input("Enter Window Title: ")
overlay = Overlay(targetWindow)

font = overlay.CreateFont("Fixedsys", 15)

while overlay.window:
	overlay.draw("fillRect", vector=Vector(30, 30, 60, 60), color=(255, 255, 255))
	overlay.draw("Circle", vector=Vector(150, 150, 0, 0), color=(255, 0, 0), thickness=0, radius=20)
	overlay.draw("Line", vector=Vector(100, 100, 600, 600), color=(255, 255, 255), thickness=5)
	overlay.draw("Text", vector=Vector(overlay.targetRect.w / 2, overlay.targetRect.h / 2, 0, 0), color=(255, 255, 255), text="+", fontObject=font)
	overlay.handle()
