import pygame


def draw_rounded_rect(surface, rect, color, radius=10, width=0):
    """
    Draw a filled rounded rectangle onto `surface`.

    Args:
        surface: pygame.Surface to draw on.
        rect: (x, y, w, h) or pygame.Rect.
        color: (R, G, B) or (R, G, B, A).
        radius: corner radius in pixels (clamped to min(w,h)/2).
    """
    # Normalize rect
    if isinstance(rect, pygame.Rect):
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
    else:
        x, y, w, h = rect

    # clamp radius
    radius = int(max(0, min(radius, min(w, h) // 2)))

    # quick path: if radius is 0, just draw a normal filled rect
    if radius == 0:
        pygame.draw.rect(surface, color, (x, y, w, h))
        return

    # create temporary surface with per-pixel alpha
    temp = pygame.Surface((w, h), pygame.SRCALPHA)

    # draw central rectangles (these cover edges so circles fill corners cleanly)
    pygame.draw.rect(temp, color, (radius, 0, w - 2 *
                     radius, h))        # horizontal core
    pygame.draw.rect(temp, color, (0, radius, w, h -
                     2 * radius))        # vertical core

    # draw corner circles (filled)
    pygame.draw.circle(temp, color, (radius, radius), radius)
    pygame.draw.circle(temp, color, (w - radius, radius), radius)
    pygame.draw.circle(temp, color, (radius, h - radius), radius)
    pygame.draw.circle(temp, color, (w - radius, h - radius), radius)

    # blit temp onto target surface
    surface.blit(temp, (x, y))
