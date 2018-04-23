
def make_plan(region,start=(10.,10.),goal=(90.,90.),robot_size=1.,plot=True):
    x, y = region.get_points
    x = [int(val) for val in x]
    y = [int(val) for val in y]

    grid_size = 1.

    

    show_animation = plot #The imported libraries use global variables

    if (plot):
        plt.plot(x, y, ".k")
        plt.plot(start[0],start[1],"xr")
        plt.plot(goal[0],goal[1],"xb")
        plt.grid(True)
        plt.axis("equal")

    rx, ry = path_planner(sx, sy, gx, gy, x, y, grid_size, robot_size)

    if (plot):
        plt.plot(rx, ry, "-r")
        plt.show()

    return rx, ry 

    
