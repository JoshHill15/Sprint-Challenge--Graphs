from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


def check_move(move, x, y):
    if move == "n":
        return world.room_grid[x][y+1]
    elif move == "s":
        return world.room_grid[x][y-1]
    elif move == "e":
        return world.room_grid[x+1][y]
    else:
        return world.room_grid[x-1][y]


def inverse_move(move):
    if move == "n":
        return "s"
    elif move == "s":
        return "n"
    elif move == "e":
        return "w"
    else:
        return "e"


def convert_to_directions(arr, visited):
    for i in range(1, len(arr)):
        x1, y1 = visited[arr[i-1]][0]
        x2, y2 = visited[arr[i]][0]
        if x1 == x2+1 and y1 == y2:
            traversal_path.append("w")
        elif x1 == x2-1 and y1 == y2:
            traversal_path.append("e")
        elif y1 == y2-1 and x1 == x2:
            traversal_path.append("n")
        else:
            traversal_path.append("s")
    last = arr[-1]
    x, y = visited[last][0]
    last_room = world.room_grid[x][y]
    return last_room


def dfs(room, visited):
    stack = [room]
    path = []
    while len(stack) > 0:
        curr = stack.pop()
        path.append(curr.id)
        exits = curr.get_exits()
        x, y = curr.get_coords()
        neighbors = {}
        for move in exits:
            next_room = check_move(move, x, y)
            if next_room.id in visited:
                neighbors[move] = next_room.id
                opposite = inverse_move(move)
                visited[next_room.id][1][opposite] = curr.id
            else:
                neighbors[move] = "?"
        visited[curr.id] = [(x, y), neighbors]
        connected_rooms = visited[curr.id][1]
        flag = False
        for move in connected_rooms:
            if connected_rooms[move] == "?":
                flag = True
        if flag == False:
            convert_to_directions(path, visited)
            return curr
        for move in connected_rooms:
            if connected_rooms[move] == "?":
                next_room = check_move(move, x, y)
                stack.append(next_room)


def bfs(room, visited):
    q = [[room.id]]
    fin = set()
    while len(q) > 0 and len(visited) != len(world.rooms):
        path = q.pop(0)
        curr = path[-1]
        connected_rooms = visited[curr][1]
        for move in connected_rooms:
            if connected_rooms[move] not in fin:
                fin.add(curr)
                np = path.copy()
                if connected_rooms[move] == "?":
                    return np
                np.append(connected_rooms[move])
                q.append(np)


def traverse_all_rooms(starting_room):
    visited = {}
    q = [starting_room]
    while len(q) > 0 and len(world.rooms) != len(visited):
        current = q.pop(0)
        if current not in visited:
            last_discovered_room = dfs(current, visited)
            bfs_path = bfs(last_discovered_room, visited)
            if bfs_path is None:
                return
            last_visited_room = convert_to_directions(bfs_path, visited)
            q.append(last_visited_room)


traverse_all_rooms(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
