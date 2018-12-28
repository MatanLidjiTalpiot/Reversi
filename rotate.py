import cv2
import numpy as np

def first_editing(image):
   image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)
   image = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((4, 4)))
   image = cv2.medianBlur(image, 3)
   return image

def show_image(image):
   cv2.imshow("image", image)
   cv2.waitKey(0)

def resize(image):
   shape = image.shape
   if len(shape) == 2:
      height, width = shape
   else:
      height, width, chanels = shape
   image = image[10:height, 10:width] #cut the edge of the image
   image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
   return image

def bolding(image):
   kernel = np.ones((5, 5), np.uint8)
   image = 255 - image
   dilation = cv2.dilate(image, kernel, iterations=1)
   dilation = 255 - dilation
   return dilation

img = cv2.imread('WIN_20181129_13_32_56_Pro.jpg')
img = resize(img)
gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
gray = first_editing(gray)
gray = 255-gray
# edges = cv2.Canny(gray,50,150,apertureSize = 3)
# show_image(edges)
lines = cv2.HoughLines(gray,1,np.pi/720,380)
lines_filtered = [lines[0]]
for i in range(len(lines)):
    selected = True
    rho1, theta1 = lines[i][0]
    if abs(rho1)> 1000:
        selected = False
    for j in range(len(lines_filtered)):
        rho2, theta2 = lines_filtered[j][0]
        if abs(theta1 - theta2) < 10 * np.pi / 180 and abs(rho1 - rho2) < 70:
            selected = False
    if selected:
        lines_filtered.append(lines[i])



for line in lines_filtered:
   for rho,theta in line:
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      x1 = int(x0 + 1000*(-b))
      y1 = int(y0 + 1000*(a))
      x2 = int(x0 - 1000*(-b))
      y2 = int(y0 - 1000*(a))
      if theta> np.pi/2-0.2 and theta < np.pi/2+0.2:
         cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
      else:
         cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)
         print("rho:" +str(rho) + "theta" + str(theta))

show_image(img)