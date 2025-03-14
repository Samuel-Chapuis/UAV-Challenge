import cv2
import numpy as np

def camera_selection():
    """
    Opens the first available camera and displays its feed in a window.
    Allows user to:
      - Press 'n' to switch to the next camera.
      - Press 's' to select the current camera.
      - Press 'q' or ESC to exit without selection.

    Returns:
      The selected camera index, or None if no selection was made.
    """
    camera_index = 0
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"❌ Camera {camera_index} is not available.")
        return None

    print("Press 'n' for the next camera, 's' to select, or 'q'/'ESC' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"❌ Could not read from camera {camera_index}.")
            break

        # Display the video feed
        cv2.imshow("Camera Preview", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('n'):  # Next camera
            # Release the current camera before moving to the next
            cap.release()
            camera_index += 1
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                print(f"❌ Camera {camera_index} is not available. Returning to previous camera.")
                camera_index -= 1
                cap = cv2.VideoCapture(camera_index)
        elif key == ord('s'):  # Select current camera
            print(f"✅ Camera {camera_index} selected.")
            cap.release()
            cv2.destroyAllWindows()
            return camera_index
        elif key in [ord('q'), 27]:  # 'q' or ESC
            print("Exiting without selecting a camera.")
            cap.release()
            cv2.destroyAllWindows()
            return None


def key_test():
    """
    Displays an empty window and prints the integer value of each key pressed.
    Press 'q' or ESC to close the window and exit.
    """
    cv2.namedWindow('Key Test')
    while True:
        blank_image = np.zeros((100,100,3), dtype=np.uint8)  # A small blank image
        cv2.imshow('Key Test', blank_image)

        key = cv2.waitKey(1) & 0xFF
        if key != 255:  # 255 (or -1 before masking) indicates no key was pressed
            print(f"Key pressed: {key} (ASCII: '{chr(key)}')")

            if key == ord('q') or key == 27:
                print(f"Closing window (key {key} pressed).")
                break

    cv2.destroyAllWindows()