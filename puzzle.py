


def create_puzzle(image_path, grid_size=3):
    from PIL import Image
    import os

    img = Image.open(image_path)
    width, height = img.size

    piece_w = width // grid_size
    piece_h = height // grid_size

    pieces = []

    if not os.path.exists("pieces"):
        os.makedirs("pieces")

    index = 0
    for i in range(grid_size):
        for j in range(grid_size):
            box = (j*piece_w, i*piece_h, (j+1)*piece_w, (i+1)*piece_h)
            piece = img.crop(box)

            filename = f"pieces/piece_{i}_{j}.jpg"
            piece.save(filename)

            pieces.append({
                "image": filename,
                "correct_pos": index
            })

            index += 1

    return pieces