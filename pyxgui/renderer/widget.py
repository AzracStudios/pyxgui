from __future__ import annotations
from dataclasses import dataclass
import pyray as raylib


@dataclass
class Vector2:
  x: int | float | Pixel
  y: int | float | Pixel


@dataclass
class ConstraintVector:
  x: Pixel | Aspect | Relational
  y: Pixel | Aspect | Relational


@dataclass
class Pixel:
  pixels: int


@dataclass
class Aspect:
  ratio: int | float


@dataclass
class Relational:
  percent: int | float


class Widget:

  def __init__(self):
    self.position = Vector2(0, 0)
    self.dimension = Vector2(0, 0)

    self.position_constraint = ConstraintVector(Pixel(0), Pixel(0))
    self.relative_translations: list[Vector2] = []
    self.dimension_constraint = ConstraintVector(Pixel(0), Pixel(0))

    self.parent: Widget = None
    self.children: list[Widget] = []

  def add_child(self, child: Widget):
    self.children.append(child)
    child.parent = self

  def update_children(self):
    for child in self.children:
      child.parent = self
      child.compute_dimension_from_constraint()
      child.compute_position_from_constraint()

  def set_position_constraint(self, constraint_vector: ConstraintVector):
    self.position_constraint = constraint_vector
    self.compute_position_from_constraint()

  def compute_position_from_constraint(self):
    def set_position(constraint, var):
      if isinstance(constraint, Pixel):
        self.position.__setattr__(var, constraint.pixels)

      if isinstance(constraint, Aspect):
        raise Exception("Position cannot be constrained by aspect ratio")

      if isinstance(constraint, Relational):
        self.position.__setattr__(
            var,
            constraint.percent * 0.01 * self.parent.dimension.__getattribute__(var),
        )

    set_position(self.position_constraint.x, "x")
    set_position(self.position_constraint.y, "y")

    self.position.x += self.parent.position.x
    self.position.y += self.parent.position.y
    self.compute_relative_vector_translations()

    self.update_children()

  def translate_position(self, value: Vector2):
    self.position.x += value.x.pixels
    self.position.y += value.y.pixels
    self.update_children()

  def translate_position_relative(self, value: ConstraintVector):
    if not (isinstance(value.x, Relational) and isinstance(value.y, Relational)):
      return

    self.relative_translations.append(value)

  def compute_relative_vector_translations(self):
    for translation in self.relative_translations:
      self.position.x += translation.x.percent * 0.01 * self.dimension.x
      self.position.y += translation.y.percent * 0.01 * self.dimension.y

  def set_dimension_constraint(self, constraint_vector: ConstraintVector):
    self.dimension_constraint = constraint_vector
    self.compute_dimension_from_constraint()

  def compute_dimension_from_constraint(self):
    def set_dimension(constraint, var):
      if isinstance(constraint, Pixel):
        self.dimension.__setattr__(var, constraint.pixels)

      if isinstance(constraint, Aspect):
        self.dimension.__setattr__(
            var,
            self.dimension.x / constraint.ratio
            if var == "y"
            else self.dimension.y * constraint.ratio,
        )

      if isinstance(constraint, Relational):
        self.dimension.__setattr__(
            var,
            constraint.percent * 0.01 * self.parent.dimension.__getattribute__(var),
        )

    x_is_aspect = isinstance(self.dimension_constraint.x, Aspect)
    y_is_aspect = isinstance(self.dimension_constraint.y, Aspect)

    if x_is_aspect and y_is_aspect:
      raise Exception("Both constraints can't be aspect ratio")

    if x_is_aspect:
      set_dimension(self.dimension_constraint.y, "y")
      set_dimension(self.dimension_constraint.x, "x")
      return

    set_dimension(self.dimension_constraint.x, "x")
    set_dimension(self.dimension_constraint.y, "y")
    self.update_children()

  def render_children(self):
    for child in self.children:
      child.render()

  def render(self):
    pass
