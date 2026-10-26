from PIL import Image, ImageDraw

img = Image.open("assets/raw_profile.jpg").convert("RGBA")
# We can use ImageDraw.floodfill or a custom BFS
# Let's write a BFS to find contiguous background pixels
width, height = img.size
pixels = img.load()

# Let's sample the background color from the top left corner
bg_color = pixels[0, 0]

visited = set()
queue = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]

tolerance = 60

def color_distance(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])

for start_node in queue:
    if start_node not in visited:
        q = [start_node]
        visited.add(start_node)
        while q:
            x, y = q.pop(0)
            # Make it transparent
            pixels[x, y] = (0, 0, 0, 0)
            
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        if color_distance(pixels[nx, ny], bg_color) < tolerance:
                            visited.add((nx, ny))
                            q.append((nx, ny))

img.save("assets/profile.png", "PNG")
print("Flood fill complete.")
