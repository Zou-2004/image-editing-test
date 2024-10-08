from PIL import Image



def pic_editing(home_image_path, fur_image_path,width,height, ab_width, ab_height ):

    # Load the base image and the overlay image
    base_image = Image.open(home_image_path)
    overlay_image = Image.open(fur_image_path).convert("RGBA")

    # Define the grid cell dimensions
    grid_width = width
    grid_height = height

    # Resize the overlay image to fit the grid cell
    overlay_image = overlay_image.resize((grid_width, grid_height))

    # Define the position where the overlay should be placed on the grid
    position = (ab_width, ab_height)  # Example position (x, y) on the base image

    # Create a copy of the base image to not alter the original
    result_image = base_image.copy()

    # Paste the overlay image onto the base image using its alpha channel as a mask
    result_image.paste(overlay_image, position, overlay_image)

    # Save the result
    result_image.save(home_image_path)


#pic_editing('white_background.png','shaped_bed.png', 200,100,20,20)
