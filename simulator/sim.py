import math
import random
import json

class Entity:
  """An entity which exists within a world"""
  def __init__(self, location):
    (self.x, self.y) = location

class Food(Entity):
  pass

class Creature(Entity):
  """An engity with agency to exist within a world"""

  def __init__(self, species, size, speed, viewRange, health, cohesion, aggression, location, cid):
    self.species = species # species id dictates who creature can mate with and behavior
    self.size = size
    self.speed = speed
    self.viewRange = viewRange
    self.maxHealth = health
    self.health = health
    self.cohesion = cohesion
    self.aggression = aggression
    self.cid = cid
    super().__init__(location)

  def heal(self, amt):
    self.health = min(self.health + amt, self.maxHealth)

  def nearby_entities(self, context):
    entities = []
    for row in context:
      for column in row:
        if isinstance(column, Entity):
          entities.append(column)
    entities.sort(key = lambda c : (c.x - self.x)**2 + (c.y - self.y)**2)
    return entities

  def nearby_creatures(self, context):
    entities = self.nearby_entities(context)
    return filter(lambda c : isinstance(c, Creature), entities)

  def nearby_my_species(self, context):
    creatures = self.nearby_creatures(context)
    return list(filter(lambda c : c.species == self.species, creatures))

  def nearby_other_species(self, context):
    creatures = self.nearby_creatures(context)
    return list(filter(lambda c : c.species != self.species, creatures))

  def nearby_food(self, context):
    entities = self.nearby_entities(context)
    return list(filter(lambda c : isinstance(c, Food), entities))

  def wander(self):
    angle = random.random() * 2 * math.pi
    dist = (1-random.random()**2) * self.speed
    print(str(self.cid),"wants to wander from",str((self.x,self.y)),"to",str((self.x + int(math.cos(angle)*dist), self.y + int(math.sin(angle)*dist))))
    return ((self.x + int(math.cos(angle)*dist), self.y + int(math.sin(angle)*dist)), (0,0))
    
  def go_towards(self, target, context):
    """Returns the furthest the creature can move in one timestep towards the closest adjacent empty cell to a target."""
    loc_context = (target.x - self.x + self.viewRange, target.y - self.y + self.viewRange)
    potential_targets = []
    directions = []
    for i, near in enumerate([(0,-1),(-1,0),(0,1),(1,0)]):
      if near[0] + loc_context[0] >= 0 and near[0] + loc_context[0] < len(context[0]) and near[1] + loc_context[1] >= 0 and near[1] + loc_context[1] < len(context):
        if context[loc_context[1] + near[1]][loc_context[0] + near[0]] == 0:
          potential_targets.append((target.x + near[0], target.y + near[1]))
    potential_targets.sort(key=lambda t : (t[0] - self.y)**2 + (t[1] - self.x)**2)
    target_loc = (0,0)
    if len(potential_targets) == 0:
      target_loc = (target.x,target.y)
    else:
      target_loc = potential_targets[0]
    angle = math.atan2(target_loc[1]-self.y,target_loc[0]-self.x)
    print(self.cid, "wants to go from",str((self.x,self.y)),"to",target_loc,"which is occupied by",context[target_loc[1] - self.y + self.viewRange][target_loc[0] - self.x + self.viewRange])
    distance = min(self.speed, math.sqrt((target_loc[1] - self.y)**2 + (target_loc[0] - self.x)**2))
    target_loc = (int(self.x + distance * math.cos(angle)), int(self.y + distance * math.sin(angle)))
    try_speed = self.speed
    while context[target_loc[1] - self.y + self.viewRange][target_loc[0] - self.x + self.viewRange] != 0 and target_loc != (self.x, self.y) and try_speed >= 0:
      # ultra sketchy raytracing type math???
      print(target_loc)
      try_speed -= 1
      angle = math.atan2(target_loc[1]-self.y,target_loc[0]-self.x)
      distance = min(try_speed, math.sqrt((target_loc[1] - self.y)**2 + (target_loc[0] - self.x)**2))
      target_loc = (int(self.x + distance * math.cos(angle)), int(self.y + distance * math.sin(angle)))
    return target_loc

  def act(self, context):
    """Decide on what action to take in a given context."""
    # What constitutes context? Should the creature calculate what it is able to see from
    # context, and thus context is just the whole world? How does the creature return
    # behavior? It should want to move to a location and perform some action (optionally).
    # returns (location, action) where location is a destination within bounds, and action
    # is an integer tuple:
    #   action[0] defines which action:
    #     0: Do nothing
    #     1: Eat
    #     2: Reproduce
    #     3: Attack
    #   action[1] defines which cell to interact with:
    #     0: (0,1)
    #     1: (1,0)
    #     2: (0,-1)
    #     3: (-1,0)
    #print("Extracting context...")
    nearby_allies = self.nearby_my_species(context)
    nearby_enemies = self.nearby_other_species(context)
    nearby_food = self.nearby_food(context)
    #print("Context extracted!")
    cohesion_floor = 0
    aggression_floor = self.cohesion
    food_floor = self.cohesion + self.aggression
    ceiling = 2
    if len(nearby_enemies) == 0:
      cohesion_floor += self.aggression
      aggression_floor += self.aggression
    if len(nearby_allies) == 0:
      cohesion_floor += self.cohesion
    if len(nearby_food) == 0:
      ceiling = food_floor
    if cohesion_floor == ceiling:
      # nothing nearby, just wander
      #print("Wandering...")
      return self.wander() 
    #print("Making a choice...")
    behavior = random.random() * (ceiling - cohesion_floor) + cohesion_floor
    target = 0
    action = 0
    if behavior < aggression_floor:
      # cooperate
      target = nearby_allies[0]
      action = 2
    elif behavior < food_floor:
      # attack
      target = nearby_enemies[0]
      action = 3
    else:
      # eat
      target = nearby_food[0]
      action = 1
    dest = self.go_towards(target, context)
    direction = 0
    #print("Choice made! Going towards",dest)
    match (target.x-dest[0], target.y-dest[1]):
      case (0,1):
        direction = 0
      case (1,0):
        direction = 1
      case (0,-1):
        direction = 2
      case (-1,0):
        direction = 3
      case _:
        action = 0
    return (dest, (action, direction))
    
class World:
  
  def __init__(self, settings):
    structure = json.loads(settings)
    self.worldSizeX = structure["worldSizeX"]
    self.worldSizeY = structure["worldSizeY"]
    self.grid = [[0 for i in range(self.worldSizeX)] for j in range(self.worldSizeY)]
    self.numTimesteps = structure["numTimesteps"]
    self.foodDensity = structure["foodDensity"]
    self.allCreatures = []
    for (j, species) in enumerate(structure["species"]):
      print("Initializing species " + str(j+1))
      for i in range(species["startingNumber"]):
        location = (random.randint(0,self.worldSizeX-1), random.randint(0,self.worldSizeY-1))
        while self.query(location) != 0:
          location = (random.randint(0,self.worldSizeX-1), random.randint(0,self.worldSizeY-1))
        creature = Creature(j + 1,
          species["size"],
          species["speed"],
          species["sight"],
          species["health"],
          species["cohesion"],
          species["aggression"],
          location,
          i)
        self.set_value(location, creature)
        self.allCreatures.append(creature)

  def safeQuery(self, location):
    if location[0] < 0 or location[0] >= self.worldSizeX or location[1] < 0 or location[1] >= self.worldSizeY:
      return -1
    return self.query(location)

  def query(self, location):
    """Returns the contents of the grid at location (x,y)"""
    return self.grid[location[1]][location[0]]

  def set_value(self, location, value):
    self.grid[location[1]][location[0]] = value

  def nearby(self, location, distance):
    """Returns a slice of the grid within distance units of location"""
    ret = [[-1 for i in range(2*distance + 1)] for j in range(2*distance + 1)]
    for i,y in enumerate(range(location[1] - distance, location[1] + distance + 1)):
      for j,x in enumerate(range(location[0] - distance, location[0] + distance + 1)):
        ret[i][j] = self.safeQuery((x,y))
    return ret

  def calculateNextStep(self):
    random.shuffle(self.allCreatures) # what order should actions be taken in?
    dead = []
    for i, creature in enumerate(self.allCreatures):
      #print("Creature",i)
      assert(self.query((creature.x,creature.y)) == creature)
      creature.health -= 1 # passively lose health, eat to stay alive
      if creature.health <= 0:
        self.set_value((creature.x, creature.y), Food((creature.x,creature.y))) # replace dead body with food
        dead.append(i)
        continue
      #print("About to act...")
      (dest, action) = creature.act(self.nearby((creature.x, creature.y),creature.viewRange))
      #print("Decision made!")
      # sanity check
      if self.safeQuery(dest) != 0:
        continue
      self.set_value((creature.x,creature.y),0)
      self.set_value(dest, creature)
      creature.x = dest[0]
      creature.y = dest[1]
      (act, direction) = action
      dirs = [(0,1),(1,0),(0,-1),(-1,0)]
      if act == 0: continue
      act_dest = (dest[0] + dirs[direction][0], dest[1] + dirs[direction][1])
      if self.safeQuery(act_dest) == -1: continue
      if act == 1:
        if not isinstance(self.query(act_dest), Food): continue
        creature.heal(5)
        self.set_value(act_dest, 0)
      if act == 2:
        if not isinstance(self.query(act_dest), Creature) or self.query(act_dest).species != creature.species: continue
        # procreate
      if act == 3:
        if not isinstance(self.query(act_dest), Creature): continue
        # attack
    self.allCreatures = [c for i, c in enumerate(self.allCreatures) if i not in dead] # remove dead creatures

  def log(self):
    print("--------------------------")
    for i in range(self.worldSizeY):
      out = []
      for j in range(self.worldSizeX):
        if isinstance(self.safeQuery((j,i)), Creature):
          out.append(str(self.safeQuery((j,i)).cid))
        elif isinstance(self.safeQuery((j,i)), Food):
          out.append(".")
        else:
          out.append(" ")
      print(" ".join(out))

world = World('{"numTimesteps":10,"viewGranularity":1,"cacheViews":true,"worldSizeX":15,"worldSizeY":15,"foodDensity":0.1,"species":[{"startingNumber":5,"size":1,"speed":3,"sight":5,"health":5,"cohesion":0.5,"aggression":0.5}]}')
for i in range(world.numTimesteps):
  world.log()
  world.calculateNextStep()
world.log()
