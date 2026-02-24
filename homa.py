import cv2
import time

def draw_text(frame, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2):
    # Draw filled rectangle as text background
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_width, text_height = text_size
    x, y = position
    cv2.rectangle(frame, (x, y), (x + text_width + 10, y - text_height - 10), (0, 0, 0), -1)
    # Put text onto the frame
    cv2.putText(frame, text, (x + 5, y - 5), font, font_scale, color, thickness)

cap = cv2.VideoCapture('video.mp4')

if not cap.isOpened():
    print("Error opening video file")

fps = cap.get(cv2.CAP_PROP_FPS)

frame_counter = 0
start_time = time.time()
fps_display = 0

pause = False
wait_time = 25
playback_speed = 1.0
message = ""
message_duration = 0
current_frame = 0

while cap.isOpened():
    if not pause:
        ret, frame = cap.read()
        if ret:
            current_frame += 1

    if ret:
        frame_counter += 1

        end_time = time.time()
        fps_display = frame_counter / (end_time - start_time)

        if (end_time - start_time) > 1:
            frame_counter = 0
            start_time = time.time()

        draw_text(frame, f"FPS: {fps_display:.0f}", (10, frame.shape[0] - 10))
        draw_text(frame, f"Speed: {playback_speed:.1f}x", (10, frame.shape[0] - 40))

        if message_duration > 0:
            draw_text(frame, message, (frame.shape[1] - 300 , frame.shape[0] - 10))
            message_duration -= 1

        cv2.imshow('frame', frame)

        key = cv2.waitKey(wait_time)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord(' '):
            pause = not pause
            message = "Pause" if pause else "Play"
            message_duration = fps
        elif key & 0xFF == ord('s'):
            cv2.imwrite('screenshot.png', frame)
            message = "Screenshot saved"
            message_duration = fps
        elif key & 0xFF == ord('+'):
            wait_time = max(1, wait_time - 5)
            playback_speed = 25.0 / wait_time
        elif key & 0xFF == ord('-'):
            wait_time += 5
            playback_speed = 25.0 / wait_time
        elif key & 0xFF == ord('a'):
            current_frame = max(0, current_frame - 2)
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if ret:
                message = "Previous frame"
                message_duration = fps
                current_frame += 1
        elif key & 0xFF == ord('d'):
            ret, frame = cap.read()
            current_frame += 1
            message = "Next frame"
            message_duration = fps
        elif key & 0xff == ord("z"):
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC)
            new_time = max(0, current_time - 5000)
            cap.set(cv2.CAP_PROP_POS_MSEC, new_time)
            current_frame = int(new_time / 1000 * fps)
            message = "5 Sec. Backward"
            message_duration = fps
        elif key & 0xff == ord("x"):
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC)
            new_time = current_time + 5000
            cap.set(cv2.CAP_PROP_POS_MSEC, new_time)
            current_frame = int(new_time / 1000 * fps)
            message = "5 Sec. Forward"
            message_duration = fps
    else:
        print("Video playback has completed.")
        break

cap.release()
cv2.destroyAllWindows()
