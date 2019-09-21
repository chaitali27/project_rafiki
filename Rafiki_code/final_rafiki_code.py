from playsound import playsound
import cv2
import time
import cv2.aruco as aruco
import datetime
import math
import numpy as np

WINDOW_TITLE = 'Rafiki'
WINDOW_LOAD_VIDEO_FILE_NAME = 'loading_screen.mp4'
BLANK_FILE_NAME = 'blank.jpg'
font= cv2.FONT_HERSHEY_SIMPLEX

loc_paintbrush = [] #global variable containing locations of paint marks
loc_paintbrush1 = []
loc_eraser = [] #global variable containing locations of eraser marks
loc_eraser1 = []
count_confirmbg = 300

colour_b = 0 #global variable storing colour blue
colour_r = 0 #global variable storing colour red
colour_g = 0 #global variable storing colour green

#global flag variables
flag_paintbrush = False
flag_paintbrush1 = False
flag_eraser = False
flag_zoom = False
x1 = -20
y1 = -20


def loadBlankFrame():

	return cv2.imread(BLANK_FILE_NAME, 1)

def playSound(sound): #plays sound from file
	playsound(sound)
	'''wave_obj = sa.WaveObject.from_wave_file(sound)
	play_obj = wave_obj.play()
	play_obj.wait_done()'''

def showWindow(frame): #shows the given window in fullscreen

	cv2.namedWindow(WINDOW_TITLE, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(WINDOW_TITLE,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
	cv2.imshow(WINDOW_TITLE, frame)

def initiateRafiki(frame):

	#displays loading screen
	video = cv2.VideoCapture(WINDOW_LOAD_VIDEO_FILE_NAME) #loads the opening video

	while(video.isOpened()):

		ret, frame = video.read()
		#frame = cv2.resize(frame, (1024, 768))

		if ret == True :
			showWindow(frame) #shows the video
		else:
			break

		if cv2.waitKey(25) & 0xFF == ord('a'):
			cv2.destroyAllWindows()
			break


	video.release()


def loadWindow(img): #loads a window

	frame = cv2.imread(img,1)
	showWindow(frame)

	if cv2.waitKey(25) & 0xFF == ord('a'):
		cv2.destroyAllWindows()


def showIcon(img,img1): #shows an icon on an image

    img = cv2.resize(img, (64,64), interpolation = cv2.INTER_AREA)
    img2 = cv2.resize(img1,(1024, 768), interpolation = cv2.INTER_AREA)



    x_offset=50
    y_offset = 100
    img2[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img



    return img2 #returns the image with the icon on it



def findCenter(id_list,corners,id): #finds the centre of a given marker

	flag = True
	tl_id = 0 #top left corner of the marker
	br_id = 0 #bottom right corner of the marker
	center = []
	for i in range(len(id_list)):
		element = id_list[i][0]
		if element == id and flag == True: #if the marker id is in id_list
			corner_id = corners[i] #finds the corners of the marker
			tl_id = corner_id[0][0] #stores the top left corner of the marker
			br_id = corner_id[0][2] #stores the bottom right corner of the marker
			center.append(int((tl_id[0] + br_id[0])/2)) #finds the x co-ordinate of the centre of the marker
			center.append(int((tl_id[1] + br_id[1])/2)) #finds the y co-ordinate of the centre of the marker
			flag = False

	return center

def detectMarkerLocation(id,img): #detects the location of the given marker

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converts the image to greyscale
	aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250) #dictionary being used
	parameters =  aruco.DetectorParameters_create()

	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters = parameters) #finds and returns the ids and corners of the
	#markers that can be detected currently

	try:
		id_list = ids.tolist() #converts the np array ids to a list and stores it in id_list
		marker_center = findCenter(id_list,corners,id) #finds and stores the centre of the marker using findCenter()
		return marker_center #returns marker_center


	except:
		return -20,-20 #if a marker can't be detected returns -20,-20

def resize(bg,img): #resizes the image

    scaleh = img.shape[0]
    scalew = img.shape[1]
    h,w = bg.shape[0:2]
    h2,w2 = int(scaleh),int(scalew)
    resized = cv2.resize(bg,(w2,h2),interpolation = cv2.INTER_AREA)

    return resized

    #x,y=detectMarkerLocation(id,img)

def Background(img,id,a): #replaces the green in the image with the given background

    scaleh = img.shape[0] #finds the height and width of the image
    scalew = img.shape[1]

    lower = np.array([40,50,50])
    upper = np.array([80,255,255])

    #background_selection = []
    #reads 4 background image files
    bg1 = cv2.imread('test1.jpeg',1)
    bg2 = cv2.imread('test2.jpeg',1)
    bg3 = cv2.imread('test3.jpeg',1)
    bg4 = cv2.imread('test4.jpeg',1)
    bg5 = cv2.imread('test5.png',1)
    bg6 = cv2.imread('test6.jpg',1)
    bg7 = cv2.imread('test7.jpg',1)
    bg8 = cv2.imread('test8.jpg',1)

    changebg = []
    #stores them in a list changebg[]
    changebg.append(bg1)
    changebg.append(bg2)
    changebg.append(bg3)
    changebg.append(bg4)
    changebg.append(bg5)
    changebg.append(bg6)
    changebg.append(bg7)
    changebg.append(bg8)



    current_bg = changebg[a] #selects the current background
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #converts the image to hsv
    img_resize = resize(current_bg,img) #resizes the background image to the resolution of the screen

    image_mask=cv2.inRange(hsv,lower,upper) #masks the image
    bg_mask=cv2.bitwise_and(img_resize,img_resize,mask=image_mask) #creates a background mask
    fg_mask=cv2.bitwise_and(img,img,mask=cv2.bitwise_not(image_mask)) #creates a foreground mask
    add = cv2.add(bg_mask,fg_mask) #adds the two masks

    return add #returns the image with the masks added

def drawRectBG(img): #draws rectangles on the image
    global count_confirmbg
    h = img.shape[0]
    w = img.shape[1]

    cv2.putText(img,'Change the background by hovering over the boxes',(40,60),font,0.7,(255,255,255),1,cv2.LINE_AA) #shows the text on the top
    #cv2.putText(img,'Timer: '+ str(count_confirmbg),(240,380),font,0.7,(255,255,255),1,cv2.LINE_AA)
    #shows 4 rectangles, each with text '1','2','3','4' respectively
    cv2.rectangle(img,(75,int(h/2)-150),(175,int(h/2)-50),(120,2,1),3)
    #cv2.putText(img,'1',(90,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(200,int(h/2)-150),(300,int(h/2)-50),(120,2,1),3)
    #cv2.putText(img,'2',(220,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(325,int(h/2)-150),(425,int(h/2)-50),(120,2,1),3)
    #cv2.putText(img,'3',(350,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(450,int(h/2)-150),(550,int(h/2)-50),(120,2,1),3)
    #cv2.putText(img,'4',(480,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(75,int(h/2)-25),(175,int(h/2)+75),(120,2,1),3)
    #cv2.putText(img,'1',(90,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(200,int(h/2)-25),(300,int(h/2)+75),(120,2,1),3)
    #cv2.putText(img,'2',(220,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(325,int(h/2)-25),(425,int(h/2)+75),(120,2,1),3)
    #cv2.putText(img,'3',(350,265),font,3,(255,255,255),2,cv2.LINE_AA)

    cv2.rectangle(img,(450,int(h/2)-25),(550,int(h/2)+75),(120,2,1),3)
    #cv2.putText(img,'4',(480,265),font,3,(255,255,255),2,cv2.LINE_AA)

    return img #returns the image with the rectangles and text added


def constructPaintScreen(img): #constructs the paint window on the image
    h,w  = img.shape[0:2]
    #img = cv2.flip(img,1)
    a = int(w) - 10 # offset the width
    b = int(h) - 10 # offset the height
    c = int(w)

    cv2.rectangle(img,(10,10),(a,45),(120,2,1),-1,cv2.LINE_AA) #filled blue box
    cv2.rectangle(img,(10,10),(a,b),(199,199,199),2,cv2.LINE_AA) #gray rectangle border
    cv2.rectangle(img,((c-40),20),((c-20),40),(199,199,199),-1,cv2.LINE_AA) #small box on the right
    cv2.rectangle(img,((c-65),20),((c-45),40),(199,199,199),-1,cv2.LINE_AA) #small box in the middle
    cv2.rectangle(img,((c-90),20),((c-70),40),(199,199,199),-1,cv2.LINE_AA) #small box on the left

    cv2.putText(img,'untitled - Paint',(58,38),font,0.7,(255,255,255),2,cv2.LINE_AA) # text at the top left in the blue box
    cv2.putText(img,'x',(c-35,35),font,0.7,(0,0,0),1,cv2.LINE_AA)  #the x icon in the box on the right most small box
    cv2.rectangle(img,((c-60),25),((c-50),35),(0,0,0),1,cv2.LINE_AA) #icon to show window resize in small box in the middle
    cv2.putText(img,'_',(c-86,35),font,0.7,(0,0,0),1,cv2.LINE_AA)  #the x mark in the box on the right most small box

    return img #returns the image with the paint window



def showToolTip(image): #shows the tooltip on the image

	h,w = image.shape[0:2]
	a = int(w)-15 #top right x
	b = int(h)-15 #top right y

	cv2.rectangle(image,(a,b),(a-360,b-80),(199,199,199),-1)#draws a grey rectangle
	cv2.putText(image,'''Use bucket to change background.''',(a-350,b-20),font,0.6,(0,0,0),1,cv2.LINE_AA)#adds text
	cv2.putText(image,'''TOOL TIP:''',(a-350,b-52),font,0.6,(0,0,0),1,cv2.LINE_AA)

	return image #returns the image with the tooltip window on it

def getMarkerCorner(id,img): #gets the corners of the marker
	pts = []
	p = []

	tl_id = 0
	tr_id = 0
	bl_id = 0
	br_id = 0
	center = []

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
	parameters =  aruco.DetectorParameters_create()

	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)

	try:
		print("Entered fx try")
		id_list = ids.tolist()
		for i in range(len(id_list)):
			element = id_list[i][0]
			print("Entered for loop")
			if element == id: #if the marker id is in id_list
				print("Entered id if")
				corner_id = corners[i] #gets the corners of the marker

				#stores all 4 corners of the marker
				tl_id = corner_id[0][0]
				tr_id = corner_id[0][1]
				br_id = corner_id[0][2]
				bl_id = corner_id[0][3]

				#converts the 4 corners to an np array
				p = np.array([tl_id,tr_id,br_id,bl_id],np.int32)
				p = p.reshape(-1,1,2) #reshapes the array

				return p #returns the array

	except:
		return p #returns an empty array

	return p

def getMidPoint(pts): #gets the midpoint of the marker

	p1x = pts[0][0][0]
	p1y = pts[0][0][1]

	p2x = pts[1][0][0]
	p2y = pts[1][0][1]

	mpx = (p1x + p2x)/2
	mpy = (p2x + p2y)/2

	return (int(mpx),int(mpy)) #returns the midpoint of the marker

def colourAvg(p,img): #finds the average of the colour around point p

	x,y = p

	a = x - 50
	b = y - 50

	c = x + 50
	d = y + 50

	#uses an image of 100px x 100px around point p
	img = img[b:d,a:c]

	red = 0
	blue = 0
	green = 0

	#finds the sum of the blue, green and red pixel values in the square
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):

			blue = blue + img[i,j][0]
			green = green + img[i,j][1]
			red = red + img[i,j][2]

	try: #finds the average of these pixels
		blue_avg = blue/(100*100)
		green_avg = green/(100*100)
		red_avg = red/(100*100)

		#returns the average colour values
		return int(blue_avg),int(green_avg),int(red_avg)

	except: #if the marker isn't detected
		print('inside colorAvg() catch')


def paintbrush(id,id1,img,b,g,r): #adds the paintbrush marker locations to a list
	global loc_paintbrush
	global flag_paintbrush
	global loc_paintbrush1
	global flag_paintbrush1


	try:
		x,y = detectMarkerLocation(id, img) #returns the centre, if the paintbrush marker is detected
		flag_paintbrush = True #makes the global flag variable true if the marker is detected
	except:
		x,y = -20,-20

	loc_paintbrush.append((x,y,b,g,r)) #appends the position as well as the current colour of the paintbrush

	try:
		x1,y1 = detectMarkerLocation(id1, img) #returns the centre, if the paintbrush marker is detected
		flag_paintbrush1 = True #makes the global flag variable true if the marker is detected
	except:
		x1,y1 = -20,-20

	loc_paintbrush1.append((x1,y1,b,g,r)) #appends the position as well as the current colour of the paintbrush

def eraser(id,img): #adds eraser marker locations to a global list
	global loc_eraser
	global flag_eraser

	try:
		x,y = detectMarkerLocation(id,img)
		flag_eraser = True #makes the global flag variable true if the marker is detected

	except:
		x,y = -20,-20

	loc_eraser.append((x,y)) #appends the position to a global list

def drawAllEraserMarks(img): #removes the paintmarks from the given locations
	global loc_eraser
	global loc_paintbrush
	global loc_paintbrush1

	for e in loc_eraser:
		for p in loc_paintbrush:
			if (e[0] - 20 <= p[0] <= e[0] + 20 ) and (e[1] - 20 <= p[1] <= e[1] + 20): #if the eraser marker is within 20px of the drawn paintmarks
				cv2.ellipse(img,(e[0],e[1]),(10,10),0,0,360,(255,255,255),-1,3)
				loc_paintbrush.remove(p) #removes that particular paintmark from the image

	for e in loc_eraser:
		for p in loc_paintbrush1:
			if (e[0] - 20 <= p[0] <= e[0] + 20 ) and (e[1] - 20 <= p[1] <= e[1] + 20): #if the eraser marker is within 20px of the drawn paintmarks
				cv2.ellipse(img,(e[0],e[1]),(10,10),0,0,360,(255,255,255),-1,3)
				loc_paintbrush1.remove(p) #removes that particular paintmark from the image

def drawAllPaintMarks(img): #draws an ellipse at all the paintmarks in the image
	global loc_paintbrush
	global loc_paintbrush1

	for p in loc_paintbrush:
		x,y = p[0],p[1]
		'''colour_b = random.randint(0,255)
		colour_g = random.randint(0,255)
		colour_r = random.randint(0,255)
		r = random.randint(0,20)'''
		cv2.ellipse(img,(x,y),(5,5),0,0,360,(p[2],p[3],p[4]),-1,8) #draws an ellipse with the given colours at the given position

	for p in loc_paintbrush1:
		x,y = p[0],p[1]
		'''colour_b = random.randint(0,255)
		colour_g = random.randint(0,255)
		colour_r = random.randint(0,255)
		r = random.randint(0,20)'''
		cv2.ellipse(img,(x,y),(5,5),0,0,360,(p[2],p[3],p[4]),-1,8) #draws an ellipse with the given co
	return img #returns the image with the paintmarks

def screenshot(img,hourandminute,id):
	try:
		x,y = detectMarkerLocation(id,img) #checks if id of the screenshot marker is detected and finds centre
		cv2.imwrite("screenshot_"+hourandminute+".jpg", img) #saves a screenshot with the timestamp to the folder

	except:
		x,y = -20,-20


def zoom(img,id_1,id_2):

	h,w = img.shape[0:2]
	#print(h,w)
	a = 0
	b = 0
	c = w
	d = h

	try :
		x,y = detectMarkerLocation(id_1,img)
		x1,y1 = detectMarkerLocation(id_2,img)

		#print(x,y,x1,y1)

		flag_zoom = True

		#cv2.ellipse(img,(x,y),(10,10),0,0,360,(0,255,0),-1,8)
		#cv2.ellipse(img,(x1,y1),(10,10),0,0,360,(0,255,0),-1,8)

		side = int(math.sqrt((x1-x)**2 + (y1-y)**2))

		base_side = 55

		#print(side)

		if side>base_side :

			diff_side = side - base_side
			#print(diff_side)

			diff_side = diff_side/1000

			a = int(a + a*diff_side)
			b = int(b + b*diff_side)
			c = int(c - c*diff_side)
			d = int(d - d*diff_side)

		#print(a,b,c,d)
		return b,d,a,c

	except :
		print(".")
		return b,d,a,c





def main(): #this is where the main code starts

	camera = cv2.VideoCapture(1)

	id_cursor = 0
	id_paintbrush = 2
	id_paintbrush1 = 5
	id_eraser = 3
	id_screenshot = 6
	id1_zoom = 15
	id2_zoom = 8
	id_eyedropper = 4
	id_bg = 1
	id_end = 9


	blank_frame = loadBlankFrame()
	icon = cv2.imread('paint_icon1.png',1) #read the image of the paint icon
	background = cv2.imread('bliss.jpg',1) #read the image of the desktop background
	initiateRafiki(blank_frame) #initiates the code
	playSound('loadsound.wav') #plays the startup sound

	time.sleep(2)
	count_startpaint = 0 #counter to start paint
	flag_startpaint = False #to check if paint has to be opened
	flag_changebg = True #to check if background has to be changed or not
	count_bg = 0 #counter to check selection of background
	count_confirmbg = 300 #counter to check if background has been confirmed
	bg_no = 0 #background number from list of backgrounds


	b = 0 #colour blue
	g = 255 #colour green
	r = 255 #colour red


	while True:

		now = str(datetime.datetime.now().time()) #finds the current time
		hourandminute = now[0:5] #finds the current hour and minute
		hourminute = hourandminute.replace(':', '')
		return_value,orig_img = camera.read() #reads the original image from the camera
		orig_img = cv2.flip(orig_img,1) #flips the original image along the horizontal plane
		showWindow(orig_img) #shows the original image
		image_desktop = showIcon(icon,background) #creates an image with the paint icon on the desktop background

		h = orig_img.shape[1] #finds the height and width of the original image (since all are fullscreen these values remain the same)
		w = orig_img.shape[0]


		try:
			x,y=detectMarkerLocation(id_cursor,orig_img) #finds and returns the centre of the cursor marker, with ID 0
			cv2.ellipse(image_desktop,(x,y),(5,5),0,0,360,(0,0,0),-1,8) #draws an ellipse at the centre of the marker on the desktop image

			if (50 <= x <= 120) and (100 <= y <= 170) and flag_startpaint == False: #checks if the cursor is on the paint icon
				count_startpaint = count_startpaint + 1 #increments count to calculate time
				if count_startpaint >= 20: #if the cursor is placed there for 50 iterations
					flag_startpaint = True #paint should start



			else: #if the cursor is not on the paint icon
				if count_startpaint >= 1 and flag_startpaint == False: #doesn't let the value of counter go below one
					count_startpaint = count_startpaint - 1 #decrements counter by 1



		except:
			x,y = -20,-20 #if the cursor marker isn't detected, gives x and y a default value
			cv2.ellipse(image_desktop,(x,y),(5,5),0,0,360,(0,127,127),-1,4) #draws an ellipse at given x and y

		if flag_startpaint == False: #if paint is not to be opened
			showWindow(image_desktop) #it keeps showing the desktop background image

		if flag_startpaint == True: #if paint is to be opened
			img_paintscreen = constructPaintScreen(orig_img) #constructs the paint window on the current image

			if flag_changebg == True: #if background is still to be selected
				cv2.putText(orig_img,'Timer: '+ str(count_confirmbg),(240,360),font,0.7,(255,255,255),2,cv2.LINE_AA)
				tooltip_paint_window = showToolTip(img_paintscreen) #draws the background selection options on the screen
				tooltip_paint_window_withrect = drawRectBG(tooltip_paint_window) #shows the tooltip on the screen
				showWindow(tooltip_paint_window_withrect)
				tooltip_paint_window_withbg = Background(tooltip_paint_window_withrect,id_bg,bg_no) #calls the background function with the default bg_no 0 for the first
				#iteration. For the next, passes the new chosen bg_no.
				try:
					x,y = detectMarkerLocation(id_bg,orig_img) #finds the bg marker location and returns the centre
					print(x,y)
					cv2.ellipse(tooltip_paint_window_withbg,(x,y),(5,5),0,0,360,(0,0,255),-1,8) #draws an ellipse at the centre of the marker
					showWindow(tooltip_paint_window_withbg) #shows the image with the background

					if (75 <= x <= 175) and (90 <= y <= 190) and (flag_changebg == True): #checks if the marker is in the first box
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 0 #bg_no becomes 0
							count_bg = 0 #resets counter

					if (200 <= x <= 300) and (90 <= y <= 190) and (flag_changebg == True): #checks if the marker is in the second box
						print("here")
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 1 #bg_no becomes 1
							count_bg = 0 #resets counter

					if (325 <= x <= 425) and (90 <= y <= 190) and (flag_changebg ==True): #checks if the marker is in the third box
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 2 #bg_no becomes 2
							count_bg = 0 #resets counter

					if (450 <= x <= 550) and (90 <= y <= 190) and (flag_changebg ==True): #checks if the marker is in the fourth box
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 3 #bg_no becomes 3
							count_bg = 0 #resets counter



					if (75 <= x <= 175) and (215 <= y <= 315) and (flag_changebg == True): #checks if the marker is in the first box
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 4 #bg_no becomes 0
							count_bg = 0 #resets counter

					if (200 <= x <= 300) and (215 <= y <=315) and (flag_changebg == True): #checks if the marker is in the second box
						print("here")
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 5 #bg_no becomes 1
							count_bg = 0 #resets counter

					if (325 <= x <= 425) and (215 <= y <= 315) and (flag_changebg ==True): #checks if the marker is in the third box
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 6 #bg_no becomes 2
							count_bg = 0 #resets counter

					if (450 <= x <= 550) and (215 <= y <= 315) and (flag_changebg ==True): #checks if the marker is in the fourth box
						count_bg = count_bg + 1 #increments count by 1
						if count_bg == 20: #if it stays within the box for 50 seconds
							bg_no = 7 #bg_no becomes 3
							count_bg = 0#resets counter

					elif flag_changebg == True: #if the marker is not in any of the boxes
						count_confirmbg = count_confirmbg - 1 #increments count_confirmbg by 1
						if count_confirmbg == 0: #if it reaches 100
							cv2.putText(tooltip_paint_window_withbg,'Background set!',(40,380),font,2,(255,255,255),1,cv2.LINE_AA) #shows the user that
							#the background is set
							time.sleep(1) #sleep for 1 second
							flag_changebg = False #changes the value of flag to False
				except:
					x,y = -20,-20 #if the bg marker is not detected
					print("ChangeBG()")
					showWindow(tooltip_paint_window_withbg) #shows the window without a background


			elif flag_changebg == False: #if the background is confirmed
				tooltip_paint_window = img_paintscreen #removes the rectangles and the tooltip from the image
				paint_window_withbg = Background(tooltip_paint_window,id,bg_no) #applies the background to this image

				showWindow(paint_window_withbg) #shows only the paint window with the background

				#the current image is paint_window_withbg
				screenshot(paint_window_withbg,hourminute,id_screenshot) #calls function screenshot

				paintbrush(id_paintbrush,id_paintbrush1,orig_img,b,g,r) #calls function paintbrush
				if flag_paintbrush == True: #flag_paintbrush is a global variable that is true if the paintbrush marker is detected
					tooltip_paint_window = drawAllPaintMarks(paint_window_withbg) #calls drawAllPaintMarks() to show paint marks on the image
				if flag_paintbrush1 == True: #flag_paintbrush is a global variable that is true if the paintbrush marker is detected
					tooltip_paint_window = drawAllPaintMarks(paint_window_withbg)

				eraser(id_eraser,orig_img) #calls function eraser
				if flag_eraser == True: #flag_eraser is a global variable that is true if the eraser marker is detected
					drawAllEraserMarks(paint_window_withbg) #calls drawAllEraserMarks() to show eraser marks on the image

				b,d,a,c = zoom(orig_img,id1_zoom,id2_zoom) #calls function zoom which returns the dimensions of the zoomed image
				if flag_zoom == True: #flag_paintbrush is a global variable that is true if the zoom markers are detected
					paint_window_withbg = paint_window_withbg[b:d,a:c] #crops the image to the given dimensions

				pts = getMarkerCorner(id_eyedropper,orig_img) #calls getMarkerCorner which returns an np array of the corners of the
				#eyedropper marker

				try:
					x,y = getMidPoint(pts) #gets the centre of the eyedropper marker
					pt = (x + 100, y) #creates a new point at 200px from x of the centre

					b,g,r = colourAvg(pt,paint_window_withbg) #calls colour average which returns average b,g,r values for 50px around point pt
					cv2.circle(paint_window_withbg,pt,20,(b,g,r),-1) #draws a 20px circle filled with colour (b,g,r)
					cv2.circle(paint_window_withbg,pt,21,(255,255,255)) #draws a white outline of 1px for the above circle



				except:
					print("Eyedrop error!") #if eyedropper marker is not detected

				showWindow(paint_window_withbg) #shows the paint_window_withbg


		if cv2.waitKey(25) & 0xFF == ord('a'): #ends the code if a is pressed
			cv2.destroyAllWindows() #destroys all windows
			break #breaks out of the loop


if __name__ == '__main__':
	main()
