import requests
import json

# A recursive utility function to solve Maze problem 
def solveMazeUtil(maze, x, y, sol, token):
    moveURL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    sol[x][y] = True
    
    #move right
    if x+1 < maze[0] and sol[x+1][y] == False:
        data = {"action":"RIGHT"}
        right = requests.post(moveURL, data=data, headers=headers)
        json = right.json()
        resultRight = json["result"]
        if resultRight == "END":
            return True
        elif resultRight == "SUCCESS":
            if solveMazeUtil(maze, x + 1, y, sol, token) == True:
                return True
            else:
                data = {"action":"LEFT"}
                requests.post(moveURL, data=data, headers=headers)
        elif resultRight == "WALL":
            sol[x+1][y] == True
    
    #move down
    if y+1 < maze[1] and sol[x][y+1] == False:
        data = {"action":"DOWN"}
        down = requests.post(moveURL, data=data, headers=headers)
        json = down.json()
        resultDown = json["result"]
        if resultDown == "END":
            return True
        elif resultDown == "SUCCESS":
            if solveMazeUtil(maze, x, y+1, sol, token) == True:
                return True
            else:
                data = {"action":"UP"}
                requests.post(moveURL, data=data, headers=headers)
        elif resultDown == "WALL":
            sol[x][y+1] == True

    #move left
    if x > 0 and sol[x-1][y] == False:
        data = {"action":"LEFT"}
        left = requests.post(moveURL, data=data, headers=headers)
        json = left.json()
        resultLeft = json["result"]
        if resultLeft == "END":
            return True
        elif resultLeft == "SUCCESS":
            if solveMazeUtil(maze, x - 1, y, sol, token) == True:
                return True
            else:
                data = {"action":"RIGHT"}
                requests.post(moveURL, data=data, headers=headers)
        elif resultLeft == "WALL":
            sol[x-1][y] == True

    #move up
    if y > 0 and sol[x][y-1] == False:     
        data = {"action":"UP"}
        up = requests.post(moveURL, data=data, headers=headers)
        json = up.json()
        resultUp = json["result"]
        if resultUp == "END":
            return True
        elif resultUp == "SUCCESS":
            if solveMazeUtil(maze, x, y - 1, sol, token) == True:
                return True
            else:
                data = {"action":"DOWN"}
                requests.post(moveURL, data=data, headers=headers)
        elif resultUp == "WALL":
            sol[x][y-1] == True

    return False


def main():
    URL = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"uid":"604726207"}
    p = requests.post(URL, data=data, headers=headers)
    json = p.json()
    token = json["token"]
    while (1):        
        URL2 = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token
        r = requests.get(URL2)
        info = r.json()
        status = info["status"]
        if status == "FINISHED":
            print("Finished")
            break
        elif status == "GAME_OVER":
            print("Game ended prematurely")
            break
        elif status == "NONE":
            print("Token expire")
            break
        maze_size = info["maze_size"]
        width = maze_size[0]
        height = maze_size[1]
        location = info["current_location"]
        x = location[0]
        y = location[1]
        levels_completed = info["levels_completed"]
        levels = info["total_levels"]
        sol = [ [ False for j in range(height) ] for i in range(width) ]
        print("maze width = " + str(width))
        print("maze height = " + str(height))
        solveMazeUtil(maze_size, x, y, sol, token)
        print("Total levels:" +str(levels))
        print("Solved maze "+str(levels_completed+1))
      


if __name__ == '__main__':
    main()
