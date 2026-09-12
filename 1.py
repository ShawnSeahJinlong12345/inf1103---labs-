traffic_light = 0
while traffic_light < 10:
    color = input("Color of traffic light: ").lower()
    if color == "green":
        print("Go")
        traffic_light += 1 
    elif color == "yellow":
        print("Slow down")
        traffic_light += 1
    else:
        print("Stop")
        traffic_light += 1

print("Done")