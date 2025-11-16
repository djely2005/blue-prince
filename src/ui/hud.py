import pygame
from src.settings import MAP_WIDTH, INFO_WIDTH, HEIGHT, GRAY, DARK_BLUE


class HUD:
	"""Heads-Up Display: shows inventory and player info on the right panel."""

	def __init__(self, rect: tuple, font: pygame.font.Font = None):
		"""
		Initialize HUD.
        
		Args:
			rect: (x, y, width, height) for the HUD area
			font: pygame Font object; if None, creates default font lazily
		"""
		self.rect = pygame.Rect(rect)
		self.font = font
		self.line_height = 30
		self.padding = 10
		# Transient message state
		self._message = None
		self._message_expire = 0.0
		# OtherItems state for clicking/consuming
		self._other_items_rects = []  # List of (rect, item) for click detection

	def draw(self, screen: pygame.Surface, player):
		"""Draw the HUD panel with player inventory and stats."""
		# Ensure a default font exists
		if self.font is None:
			try:
				self.font = pygame.font.Font(None, 24)
			except Exception:
				self.font = pygame.font.SysFont(None, 24)

		# Draw background
		pygame.draw.rect(screen, GRAY, self.rect)
		pygame.draw.rect(screen, DARK_BLUE, self.rect, 2)

		x = self.rect.x + self.padding
		y = self.rect.y + self.padding

		# Title
		title = self.font.render("INVENTORY", True, DARK_BLUE)
		screen.blit(title, (x, y))
		y += self.line_height + 5

		# Player inventory stats
		inventory = player.inventory
		stats = [
			f"Steps: {inventory.steps.quantity}",
			f"Money: {inventory.money.quantity}",
			f"Gems: {inventory.gems.quantity}",
			f"Keys: {inventory.keys.quantity}",
			f"Dice: {inventory.dice.quantity}",
		]

		for stat in stats:
			text_surface = self.font.render(stat, True, (0, 0, 0))
			screen.blit(text_surface, (x, y))
			y += self.line_height

		# Permanent items
		if inventory.permanentItems:
			y += 10
			perm_title = self.font.render("PERMANENT ITEMS:", True, DARK_BLUE)
			screen.blit(perm_title, (x, y))
			y += self.line_height

		for item in inventory.permanentItems:
			item_text = self.font.render(f"- {item.name}", True, (0, 0, 0))
			screen.blit(item_text, (x + 10, y))
			y += self.line_height

		# OtherItems (consumables)
		if hasattr(inventory, 'otherItems') and inventory.otherItems:
			y += 10
			other_title = self.font.render("CONSUMABLES:", True, DARK_BLUE)
			screen.blit(other_title, (x, y))
			y += self.line_height

			self._other_items_rects = []
			for item in inventory.otherItems:
				item_text = self.font.render(f"- {item.name} (click to use)", True, (100, 200, 100))
				item_rect = item_text.get_rect(topleft=(x + 10, y))
				self._other_items_rects.append((item_rect, item))
				screen.blit(item_text, (x + 10, y))
				y += self.line_height

		# Draw transient message if present
		if self._message and pygame.time.get_ticks() / 1000.0 < self._message_expire:
			# Render message at bottom of HUD
			msg_surf = self.font.render(self._message, True, (255, 255, 255))
			msg_bg = pygame.Rect(self.rect.x + self.padding, self.rect.bottom - self.line_height - self.padding, self.rect.width - self.padding * 2, self.line_height + 4)
			pygame.draw.rect(screen, DARK_BLUE, msg_bg)
			screen.blit(msg_surf, (msg_bg.x + 4, msg_bg.y + 2))
		else:
			self._message = None

	def show_message(self, text: str, duration: float = 3.0):
		"""Show a transient message on the HUD for `duration` seconds."""
		self._message = str(text)
		self._message_expire = pygame.time.get_ticks() / 1000.0 + float(duration)

	def handle_click(self, pos: tuple) -> 'OtherItem | None':
		"""Check if click is on a consumable item and return it. Otherwise return None."""
		for item_rect, item in self._other_items_rects:
			if item_rect.collidepoint(pos):
				return item
		return None

