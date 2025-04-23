#!/usr/bin/env python3
"""
show_cams.py – display webcam feed and switch to the next camera with key "n".

Requirements
------------
pip install opencv-python
"""

import cv2


def find_available_cams(max_tested: int = 10) -> list[int]:
    """Probe indices 0..max_tested-1 and return the ones that open."""
    available = []
    for idx in range(max_tested):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)  # CAP_DSHOW avoids long delays on Windows
        if cap is not None and cap.isOpened():
            available.append(idx)
            cap.release()
    return available


def main() -> None:
    cam_indices = find_available_cams() or [0]          # at least try index 0
    current_idx = 0
    cap = cv2.VideoCapture(cam_indices[current_idx])

    print(
        "Controls:\n"
        "  n – next camera\n"
        "  q – quit\n"
    )

    while True:
        ok, frame = cap.read()
        if not ok:
            print(f"[WARN] Cannot read from camera {cam_indices[current_idx]}")
            break

        cv2.imshow(f"Camera {cam_indices[current_idx]}", frame)
        key = cv2.waitKey(1) & 0xFF

        # === handle keys =====================================================
        if key == ord("q"):
            break

        if key == ord("n"):
            # close current cam & window
            cap.release()
            cv2.destroyAllWindows()

            # advance index (wrap around)
            current_idx = (current_idx + 1) % len(cam_indices)
            print(f"[INFO] Switching to camera {cam_indices[current_idx]}")
            cap = cv2.VideoCapture(cam_indices[current_idx])

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()