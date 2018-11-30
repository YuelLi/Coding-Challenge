import requests

direction=[
	"UP",
	"LEFT",
	"RIGHT",
	"DOWN"
]
oppsite_direction= {
	"UP": "DOWN",
	"LEFT" : "RIGHT",
	"RIGHT" : "LEFT",
	"DOWN" : "UP"
}
def get_token(uid):
	uid={
	"uid": uid
	}	
	r = requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session", data=uid)
	if(r.status_code == requests.codes.ok):
		return r.json()["token"]

def get_data():
	r= requests.get("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token)
	if(r.status_code == requests.codes.ok):
		return r.json()

def move(dir):
	action={
		"action":dir
	}
	r=requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token, data=action)
	return r.json()["result"]

def solve_maze_recur(dir):
	result = move(dir)
	if result=='END':
		print("END")
		return True
	if result=='WALL' or result=='OUT_OF_BOUNDS':
		return False
	game_data= get_data()
	x =game_data["current_location"][0]
	y =game_data["current_location"][1]
	print(game_data)
	if(isVisited[x][y]==1):
		move(oppsite_direction[dir])
		return False
	isVisited[x][y]=1
	if solve_maze_recur("RIGHT") ==True:
		return True
	if solve_maze_recur("UP") == True:
		return True
	if solve_maze_recur("LEFT") ==True:
		return True
	if solve_maze_recur("DOWN") ==True:
		return True
	move(oppsite_direction[dir])
	return False

def solve_maze():
	game_data=get_data()
	x =game_data["current_location"][0]
	y =game_data["current_location"][1]
	isVisited[x][y]=1
	if solve_maze_recur("RIGHT") ==True:
		return True
	if solve_maze_recur("UP") == True:
		return True
	if solve_maze_recur("LEFT") ==True:
		return True
	if solve_maze_recur("DOWN") ==True:
		return True
	return False


#entry
if __name__=="__main__":
	token=get_token(705063404)
	game_data=get_data()
	if game_data["status"]=="GAME_OVER" or game_data["status"]=="NONE":
		print("GAME_OVER")
		exit(0)
	while game_data["status"]!="FINISHED":
		game_data=get_data()
		if game_data["maze_size"]:
			row =game_data["maze_size"][0]
			col =game_data["maze_size"][1]
			isVisited= [[0]*col for i in range(row)]
			solve_maze()

	print("GAME FINISHED")
	exit(0)