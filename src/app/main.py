from random import randint
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

funcMoviments = {
    "up": lambda head: {'x': head['x'],'y': head['y']+1}, # y+1
    "down": lambda head: {'x': head['x'],'y': head['y']-1}, # y-1
    "left": lambda head: {'x': head['x']-1,'y': head['y']}, # x-1
    "right": lambda head: {'x': head['x']+1,'y': head['y']} # x+1
}

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
  for snake in request['board']['snakes']:
     snakes = snakes + snake['body'].pop()
  if (position in snakes):
    return True
  return False

def move(request: dict):
  moviments = {
    0: "up", # y+1
    1: "down", # y-1
    2: "left", # x-1
    3: "right" # x+1
  }
  move = moviments.pop(randint(0, 3), None)
  newHead = funcMoviments[move](request['you']['head'])
  while len(moviments.keys()) > 0 and (body(newHead,request) or wall(newHead) or enemiesBody(newHead,request)):
    move = moviments.pop(randint(0, len(moviments.keys())-1), None)
    if(move is None):
      move = 'up'
    newHead = funcMoviments[move](request['you']['head'])
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
