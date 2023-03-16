import json

class Creature:
  """A unique creature to exist within a world."""

  def __init__(self, species, size, speed, view_range, health, cohesion, aggression, location):
    self.species = species # species id dictates who creature can mate with and behavior
    self.size = size
    self.speed = speed
    self.view_range = view_range
    self.health = health
    self.cohesion = cohesion
    self.aggression = aggression
    (self.x, self.y) = location

  def act(self, context):
    """Decide on what action to take in a given context."""
    # What constitutes context? Should the creature calculate what it is able to see from
    # context, and thus context is just the whole world? How does the creature return
    # behavior? It should want to move to a location and perform some action (optionally).
    pass



class World:
  
  def __init__(self, settings):
    structure = json.loads(settings)
    pass
