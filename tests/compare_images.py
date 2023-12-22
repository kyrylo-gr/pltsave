from PIL import Image


def images_are_similar(image1_path, image2_path, tolerance=0.02):
    """
    Compares two images and checks if their difference is within the tolerance.
    Tolerance is the maximum number of pixels that can differ.
    """
    with Image.open(image1_path) as img1, Image.open(image2_path) as img2:
        if img1.size != img2.size or img1.mode != img2.mode:
            return False

        # Calculate the difference
        pairs = zip(img1.getdata(), img2.getdata())
        if len(img1.getbands()) == 1:
            # for grayscale images
            dif = sum(abs(p1 - p2) for p1, p2 in pairs)
        else:
            dif = sum(abs(c1 - c2)
                      for p1, p2 in pairs for c1, c2 in zip(p1, p2))

        # Calculate the percentage of different pixels
        ncomponents = img1.size[0] * img1.size[1] * len(img1.getbands())
        percentage = (dif / 255.0 * 100) / ncomponents

        # Check if the difference is within tolerance
        return percentage <= tolerance
