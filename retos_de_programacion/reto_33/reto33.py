maze = [
    ["⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️"],
    ["⬜️", "⬛️", "⬛️", "⬛️", "⬛️", "⬜️"],
    ["⬜️", "⬜️", "⬛️", "⬛️", "⬛️", "⬜️"],
    ["⬜️", "⬛️", "⬜️", "⬜️", "⬜️", "⬜️"],
    ["⬜️", "⬛️", "⬛️", "⬛️", "⬜️", "⬛️"],
    ["🐭", "⬛️", "⬛️", "⬛️", "⬜️", "🚪"],
]


def print_maze(maze):
    # imprimiendo el laberinto
    for row in maze:
        for item in row:
            print(item, end="")
        print()


def mover_mickey(maze, x, y, new_x, new_y):
    # moviendo a mickey
    if new_x < 0 or new_x >= len(maze) or new_y < 0 or new_y >= len(maze[0]):
        print("No se puede mover a Mickey Mouse a esa posicion")
        return False
    elif maze[new_x][new_y] == "⬜️":
        maze[x][y] = "⬜️"
        maze[new_x][new_y] = "🐭"
        print_maze(maze)
        return False
    elif maze[new_x][new_y] == "🚪":
        print("Mickey Mouse ha encontrado la salida!")
        print_maze(maze)
        return True
    else:
        print("No se puede mover a Mickey Mouse a esa posicion")
        return False


def posicion_mickey(maze):
    # buscando la posicion de mickey
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "🐭":
                return i, j


print("Rescatando a Mickey Mouse...")
print_maze(maze)

while True:
    # posicion de mickey
    x, y = posicion_mickey(maze)
    print("Posicion de Mickey Mouse: ", x, y)
    print("Hacia donde se desea mover a Mickey Mouse?")
    print("1: ⬆️ Arriba")
    print("2: ⬇️ Abajo")
    print("3: ⬅️ Izquierda")
    print("4: ➡️ Derecha")
    opcion = int(input("Elige una opcionpcion: "))

    match opcion:
        case 1:
            mover_mickey(maze, x, y, x - 1, y)
        case 2:
            mover_mickey(maze, x, y, x + 1, y)
        case 3:
            mover_mickey(maze, x, y, x, y - 1)
        case 4:
            mover_mickey(maze, x, y, x, y + 1)
        case _:
            print("Opcion no valida, por favor elige una opcion valida")
