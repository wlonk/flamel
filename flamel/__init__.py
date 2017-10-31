from enum import Enum
from typing import List

import svgwrite


class Element(Enum):
    EARTH = 1
    FIRE = 2
    AIR = 3
    WATER = 4


class Bracing(Enum):
    NONE = 0
    HOLDING = 1
    FOCUSING = 2
    REDIRECTING_SUNWISE = 3
    REDIRECTING_WIDDERSHINS = 4


class FocalLine:
    def __init__(self, element: Element, extended: bool) -> None:
        self.element = element
        self.extended = extended

    def render_into(self, drawing: svgwrite.Drawing) -> None:
        ORIENT_X = 0
        ORIENT_Y = 10
        # The radius of the circumcircle of an equilateral triangle:
        #
        # s/sqrt(3) = r
        #
        # So, for r = 10, s = 17.321.
        #
        # Then, the coordinates of the back points:
        #
        # (s * cos(270+/-30), s * sin(270+/-30))
        #
        # This gives us 8.661 for the x value. That's fine.
        #
        # Which gives 15 for the y value; but because we're starting at
        # 10, not 0, on that dimension, we need to subtract 10 from it,
        # and that gives us:
        BACK_X = 8.661
        BACK_Y = 5
        if self.element == Element.EARTH:
            # Down, bar
            points = [
                (ORIENT_X, -ORIENT_Y),
                (BACK_X, BACK_Y),
                (-BACK_X, BACK_Y),
            ]
        elif self.element == Element.FIRE:
            # Up
            points = [
                (ORIENT_X, ORIENT_Y),
                (BACK_X, -BACK_Y),
                (-BACK_X, -BACK_Y),
            ]
        elif self.element == Element.AIR:
            # Up, bar
            points = [
                (ORIENT_X, ORIENT_Y),
                (BACK_X, -BACK_Y),
                (-BACK_X, -BACK_Y),
            ]
        elif self.element == Element.WATER:
            # Down
            points = [
                (ORIENT_X, -ORIENT_Y),
                (BACK_X, BACK_Y),
                (-BACK_X, BACK_Y),
            ]
        drawing.add(
            drawing.polygon(
                points=points,
                fill_opacity=0,
                stroke_width=0.2,
                stroke="black",
            ),
        )


class Plexus:
    def __init__(self, sigil: str, bracing: Bracing) -> None:
        self.sigil = sigil
        self.bracing = bracing

    def render_into(self, drawing: svgwrite.Drawing) -> None:
        pass


class Node:
    def __init__(self, sigil: str, bracing: Bracing) -> None:
        self.sigil = sigil
        self.bracing = bracing

    def render_into(self, drawing: svgwrite.Drawing) -> None:
        pass


class Circle:
    def __init__(
        self,
        focal_lines: List[FocalLine],
        plexuses: List[Plexus],
        nodes: List[Node],
        bracing: Bracing,
    ) -> None:
        self.focal_lines = focal_lines
        # The plexuses may not be evenly distributed; there's an
        # implicit set of points around the circle, and you can have
        # multiple plexuses at one spot. The spots are evenly
        # distributed based on how many spots exist (whatever the
        # underlying polygon is) but each spot can then have zero, one,
        # or two plexuses at it.
        self.plexuses = plexuses
        # Ditto all that with nodes, but they're further out.
        self.nodes = nodes
        self.bracing = bracing

    def render_into(self, drawing: svgwrite.Drawing) -> None:
        drawing.add(
            drawing.circle(
                center=(0, 0),
                r=10,
                fill_opacity=0,
                stroke_width=0.5,
                stroke="black",
            ),
        )
        if self.bracing == Bracing.NONE:
            pass
        elif self.bracing == Bracing.HOLDING:
            drawing.add(
                drawing.circle(
                    center=(0, 0),
                    r=8,
                    fill_opacity=0,
                    stroke_width=0.6,
                    stroke="black",
                ),
            )
        elif self.bracing == Bracing.FOCUSING:
            drawing.add(
                drawing.circle(
                    center=(0, 0),
                    r=9.5,
                    fill_opacity=0,
                    stroke_width=1,
                    stroke="black",
                ),
            )
            # Add three bumpers
        elif self.bracing == Bracing.REDIRECTING_SUNWISE:
            # Add swirlies
            pass
        elif self.bracing == Bracing.REDIRECTING_WIDDERSHINS:
            # Add swirlies
            pass

        for plexus in self.plexuses:
            plexus.render_into(drawing)
        for node in self.nodes:
            node.render_into(drawing)
        for focal_line in self.focal_lines:
            focal_line.render_into(drawing)


def generate_transmutation_circle() -> Circle:
    return Circle(
        [
            FocalLine(Element.EARTH, False),
            FocalLine(Element.FIRE, False),
        ],
        [],
        [],
        Bracing.NONE,
    )


if __name__ == "__main__":
    c = generate_transmutation_circle()
    drawing = svgwrite.Drawing(
        filename="foo.svg",
        debug=True,
        viewBox="-20 -20 40 40",
    )
    c.render_into(drawing)
    drawing.save()
