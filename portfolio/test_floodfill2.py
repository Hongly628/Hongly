from PIL import Image

img = Image.open("assets/raw_profile.jpg").convert("RGBA")
width, height = img.size
pixels = img.load()

visited = set()
queue = []

# Add all edge pixels that are blue
for x in range(width):
    queue.extend([(x, 0), (x, height-1)])
for y in range(height):
    queue.extend([(0, y), (width-1, y)])

def is_blue(c):
    r, g, b, a = c
    return b > r + 40 and b > g + 20 and b > 100

valid_starts = []
for p in queue:
    if is_blue(pixels[p[0], p[1]]):
        valid_starts.append(p)
        visited.add(p)

# BFS
q = valid_starts
while q:
    x, y = q.pop(0)
    pixels[x, y] = (0, 0, 0, 0)
    
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < width and 0 <= ny < height:
            if (nx, ny) not in visited:
                if is_blue(pixels[nx, ny]):
                    visited.add((nx, ny))
                    q.append((nx, ny))

img.save("assets/profile.png", "PNG")
print("Smart flood fill complete.")
