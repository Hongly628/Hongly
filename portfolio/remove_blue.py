from PIL import Image

def process_image(in_path, out_path):
    img = Image.open(in_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()

    visited = set()
    queue = []

    # Add all edge pixels that are blue to the start queue
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

    # Perform Flood Fill (BFS) to remove contiguous background only
    q = valid_starts
    while q:
        x, y = q.pop(0)
        # Make the pixel transparent
        pixels[x, y] = (0, 0, 0, 0)
        
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    if is_blue(pixels[nx, ny]):
                        visited.add((nx, ny))
                        q.append((nx, ny))

    img.save(out_path, "PNG")

process_image("assets/raw_profile.jpg", "assets/profile.png")
print("Smart flood fill background removal complete.")
