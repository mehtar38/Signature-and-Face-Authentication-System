import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from numpy import result_type
from face import matchface
from signature import matchsig

# Mach Threshold
THRESHOLD_Face = 50
THRESHOLD_Sig = 70

#global f
#global p

#f=0
#p=0

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)  # add this


def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("test")

    # img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # make sure the directory exists
            # img_name = "./temp/opencv_frame_{}.png".format(img_counter)
            if(sign == 1):
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
            # img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    return True


def captureImage(ent, sign=1):
    if(sign == 1):
        filename = os.getcwd()+'\\temp\\test_img1.png'
    else:
        filename = os.getcwd()+'\\temp\\test_img2.png'
    # messagebox.showinfo(
    #     'SUCCESS!!!', 'Press Space Bar to click picture and ESC to exit')
    res = None
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True


def checkSimilarityfaces(window, path1, path2):
    result = matchface(path1=path1, path2=path2)
    global f
    if(result <= THRESHOLD_Face):
        messagebox.showerror("Failure: Faces Do Not Match",
                             "Faces are "+str(result)+f" matches!!")
        #global f
        f =1
        pass
    else:
        messagebox.showinfo("Success: Faces Match",
                            "Faces are "+str(result)+f" matches!!")
        f = 0
    return True

def checkSimilaritysignatures(window, path1, path2):
    result = matchsig(path1=path1, path2=path2)
    global p
    if(result <= THRESHOLD_Sig):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % matches!!")
        p = 1
        pass
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % matches!!")
        p = 0
    return True

def Authentication(p, f): 
    if(p == 1 and f == 1):
         messagebox.showerror("Authentication","Signature and Face authentication Failed. Cannot verify user.")
    elif(f == 1 and p == 0): 
        messagebox.showerror("Authentication","Signature authentication successful but Face authentication Failed. Cannot verify user.")
    elif(f == 0 and p == 1): 
        messagebox.showerror("Authentication","Face authentication successful but Signature authentication Failed. Cannot verify user.")
    else: 
        messagebox.showinfo("Authentication","Face and Signature authentication successful! User verified.")


root = tk.Tk()
root.title("Signature/Face Matching")
root.geometry("500x700")  # 300x200
uname_label = tk.Label(root, text="Compare Two Signatures/Faces:", font=10)
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Image 1", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=140)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=150, y=240)

img2_message = tk.Label(root, text="Image 2", font=10)
img2_message.place(x=10, y=250)

img2_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=400, y=260)

compare_button_face = tk.Button(
    root, text="Compare face", font=10, command=lambda: checkSimilarityfaces(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(),))

compare_button_signature = tk.Button(
    root, text="Compare signature", font=10, command=lambda: checkSimilaritysignatures(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(),))

authenticate_button = tk.Button(
    root, text="Authenticate", font=10, command=lambda: Authentication(p, f))

compare_button_face.place(x=200, y=320)
compare_button_signature.place(x=200, y=420)
authenticate_button.place(x=200, y=520)
root.mainloop()