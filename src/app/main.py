from random import randint
from fastapi import FastAPI
from mangum import Mangum
import math
app = FastAPI()

funcMoviments = {
    "up": lambda head: {'x': head['x'],'y': head['y']+1}, # y+1
    "down": lambda head: {'x': head['x'],'y': head['y']-1}, # y-1
    "left": lambda head: {'x': head['x']-1,'y': head['y']}, # x-1
    "right": lambda head: {'x': head['x']+1,'y': head['y']} # x+1
}
directionQuad = {
   'Q1': ['up','right'],
    'Q2': ['up','left'],
    'Q3': ['down','left'],
    'Q4': ['down','right']
}



def searchFood(position, food_list,blockPosition):
  menor_distancia = 0
  foodTarget = food_list[0]
  x, y = position['x'], position['y']
  blockX,blockY = blockPosition['x'],blockPosition['y']
  for ponto in food_list:
      x2, y2 = ponto['x'], ponto['y']
      distancia = math.sqrt((x2 - x)**2 + (y2 - y)**2)
      if distancia < menor_distancia:
          menor_distancia = distancia
          foodTarget = ponto
  x1,y1 = foodTarget['x'],foodTarget['y']

  if((abs(x1 - x) == 1 and y1 == y) or (abs(y1 - y) == 1 and x1 == x)):
    if(x1 - x == 1):
      return ['right']
    elif(x1 - x == -1):
      return ['left']
    elif(y1 - y == 1):
      return ['up']
    elif(y1 - y == -1):
      return ['down']
  if (x1 == x and y1 > y):
    return ['up']
  elif(x1 == x and y1 < y):
    return ['down']
  elif(x1 > x and y1 == y):
    return ['right']
  elif(x1 < x and y1 == y):
    return ['left']
  
  if(x1 > x and y1 > y):
    return directionQuad['Q1']
  elif(x1 < x and y1 > y):
    return directionQuad['Q2']
  elif(x1 < x and y1 < y):
    return directionQuad['Q3']
  elif(x1 > x and y1 < y):
    return directionQuad['Q4']
  else:
    return ['up','right','down','left']

def body(position,request):
  if (position in request['you']['body']):
    return True
  return False

def wall(position):
  if (position['x'] < 0 or position['x'] > 10 or position['y'] < 0 or position['y'] > 10):
    return True
  return False

def enemiesBody(position,request):
  snakes = []
  listSnakes = request['board']['snakes'].copy()
  for snake in listSnakes:
     snake['body'].pop()
     snakes = snakes + snake['body']
  if (position in snakes):
    return True
  return False

def move(request: dict):
  moviments = [
    "up", # y+1
    "down", # y-1
    "left", # x-1
    "right" # x+1
  ]
  quadrante = searchFood(request['you']['head'], request['board']['food'],request['you']['body'][1])
  moviments = quadrante.copy()
  print(moviments)
  move = moviments.pop(randint(0, len(moviments)-1))
  newHead = funcMoviments[move](request['you']['head'])
  while len(moviments) > 0 and (body(newHead,request) or wall(newHead) or enemiesBody(newHead,request)):
    move = moviments.pop(randint(0, len(moviments)-1))
    if(move is None):
      move = 'up'
    newHead = funcMoviments[move](request['you']['head'])
  print(move)
  return move


@app.get("/")
def read_root():
    return {
      "apiversion": "1",
      "author": "snake_ronron",
      "color": "#000000",
      "head": "default",
      "tail": "default",
      "version": "1"
    }


@app.post("/start")
def read_item(request: dict, status_code=200):
    return 

@app.post("/move")
def create_item(request: dict, status_code=200):
    return {
      "move": move(request),
      "shout": "THIS IS SPARTA!"
    }
   
@app.post("/end")
def create_item(request: dict, status_code=200):
    return

handler = Mangum(app, lifespan="off")
