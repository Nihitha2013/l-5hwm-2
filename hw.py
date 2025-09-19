import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    """Utility function to display an image using matplotlib."""
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def interactive_edge_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original Image", gray_image)

    print("\nEdge Detection Options:")
    print("1: Sobel Edge Detection")
    print("2: Canny Edge Detection")
    print("3: Laplacian Edge Detection")
    print("4: Gaussian Smoothing")
    print("5: Median Filtering")
    print("6: Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
            combined_sobel = cv2.bitwise_or(np.uint8(np.absolute(sobelx)), np.uint8(np.absolute(sobely)))
            display_image("Sobel Edge Detection", combined_sobel)

        elif choice == "2":
            try:
                low = int(input("Enter low threshold: "))
                high = int(input("Enter high threshold: "))
                edges = cv2.Canny(gray_image, low, high)
                display_image("Canny Edge Detection", edges)
            except ValueError:
                print("Invalid input. Please enter integers.")

        elif choice == "3":
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_image("Laplacian Edge Detection", np.uint8(np.absolute(laplacian)))

        elif choice == "4":
            try:
                ksize = int(input("Enter kernel size (odd number): "))
                if ksize % 2 == 1:
                    blurred = cv2.GaussianBlur(gray_image, (ksize, ksize), 0)
                    display_image("Gaussian Smoothing", blurred)
                else:
                    print("Kernel size must be an odd number.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == "5":
            try:
                ksize = int(input("Enter kernel size (odd number): "))
                if ksize % 2 == 1:
                    median = cv2.medianBlur(gray_image, ksize)
                    display_image("Median Filtering", median)
                else:
                    print("Kernel size must be an odd number.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == "6":
            print("Exiting edge detection...")
            break

        else:
            print("Invalid choice. Try again.")

def apply_color_filter(image, filter_type):
    filtered = image.copy()
    if filter_type == "red_tint":
        filtered[:, :, 0] = 0
        filtered[:, :, 1] = 0
    elif filter_type == "blue_tint":
        filtered[:, :, 1] = 0
        filtered[:, :, 2] = 0
    elif filter_type == "green_tint":
        filtered[:, :, 0] = 0
        filtered[:, :, 2] = 0
    elif filter_type == "increase_red":
        filtered[:, :, 2] = cv2.add(filtered[:, :, 2], 50)
    elif filter_type == "decrease_blue":
        filtered[:, :, 0] = cv2.subtract(filtered[:, :, 0], 50)
    elif filter_type == "increase_green":
        try:
            intensity = int(input("Enter green intensity to increase: "))
            filtered[:, :, 1] = cv2.add(filtered[:, :, 1], intensity)
        except ValueError:
            print("Invalid input. Using default intensity of 50.")
            filtered[:, :, 1] = cv2.add(filtered[:, :, 1], 50)
    elif filter_type == "decrease_red":
        filtered[:, :, 2] = cv2.subtract(filtered[:, :, 2], 50)
    return filtered

def interactive_color_filter(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    print("\nColor Filter Options:")
    print("r - Red Tint")
    print("b - Blue Tint")
    print("g - Green Tint")
    print("i - Increase Red")
    print("d - Decrease Blue")
    print("x - Increase Green")
    print("y - Decrease Red")
    print("q - Quit")

    filter_type = "original"
    while True:
        filtered_image = apply_color_filter(image, filter_type)
        cv2.imshow("Filtered Image", filtered_image)
        key = cv2.waitKey(0)

        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('i'):
            filter_type = "increase_red"
        elif key == ord('d'):
            filter_type = "decrease_blue"
        elif key == ord('x'):
            filter_type = "increase_green"
        elif key == ord('y'):
            filter_type = "decrease_red"
        elif key == ord('q'):
            print("Exiting color filter...")
            break
        else:
            print("Invalid key pressed.")

    cv2.destroyAllWindows()


print("Choose one of the following:")
print("e - Edge Detection")
print("c - Change Tint Color")
user_choice = input("Enter your choice (e/c): ").lower()

image_path = input("Enter the path to your image file: ")

if user_choice == "e":
    interactive_edge_detection(image_path)
elif user_choice == "c":
    interactive_color_filter(image_path)
else:
    print("Invalid choice. Please restart and choose 'e' or 'c'.")