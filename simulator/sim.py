import random
import json

class Entity:
  """An entity which exists within a world"""
  def __init__(self, location):
    (self.x, self.y) = location

class Creature:
  """An engity with agency to exist within a world"""

  def __init__(self, species, size, speed, viewRange, health, cohesion, aggression, location):
    self.species = species # species id dictates who creature can mate with and behavior
    self.size = size
    self.speed = speed
    self.viewRange = viewRange
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
    self.worldSizeX = structure["worldSizeX"]
    self.worldSizeY = structure["worldSizeY"]
    self.grid = [[Entity((i,j)) for i in range(self.worldSizeX)] for j in range(self.worldSizeY)]
    self.numTimesteps = structure["numTimesteps"]
    self.foodDensity = structure["foodDensity"]
    self.allCreatures = []
    for (j, species) in enumerate(structure["species"]):
      for i in range(species["startingNumber"]):
        location = (random.randint(0,self.worldSizeX-1), random.randint(0,self.worldSizeY-1))
        while query(location) != 0:
          location = (random.randint(0,self.worldSizeX-1), random.randint(0,self.worldSizeY-1))
        creature = Creature(j + 1,
          species["size"],
          species["speed"],
          species["sight"],
          species["health"],
          species["cohesion"],
          species["aggression"],
          location)
        set(location, creature)
        self.allCreatures.append(creature)

  def safeQuery(self, location):
    if location[0] < 0 or location[0] >= self.worldSizeX or location[1] < 0 or location[1] >= self.worldSizeY:
      return -1
    return query(location)

  def query(self, location):
    """Returns the contents of the grid at location (x,y)"""
    return self.grid[location[1]][location[0]]

  def set(self, location, value):
    self.grid[location[1]][location[0]] = value

  def nearby(self, location, distance):
    """Returns a slice of the grid within distance units of location"""
    ret = [[-1 for i in range(2*distance + 1)] for j in range(2*distance + 1)]
    for i,x in enumerate(range(location[1] - distance, location[1] + distance + 1)):
      for j,y in enumerate(range(location[0] - distance, location[0] + distance + 1)):
        ret[i][j] = self.safeQuery((x,y))
    return ret

  def calculateNextStep(self):
    nextStep = self.grid.copy()
    random.shuffle(self.allCreatures) # what order should actions be taken in?
    for creature in self.allCreatures:
      action = creature.act(self.nearby((creature.x, creature.y),creature.viewRange))
      nextStep[creature.y][creature.x] = 0
      nextStep[action[1]][action[0]] = creature
