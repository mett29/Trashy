import boto3, cv2
import numpy as np

def conta_hit(results):
    def trova_hit(row):
        return (row[len(row)-1], len(set(results) & set(row)))
    return trova_hit


client = boto3.client('rekognition')

# Camera 0 is the integrated web cam on my netbook
camera_port = 1
# Captures a single image from the camera and returns it in PIL format
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
# read is the easiest way to get a full image out of a VideoCapture object.
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
print("Taking image...")
retval, camera_capture = camera.read()
#print(type(camera_capture))
print("Save image...")

file = "photo.jpg"
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
cv2.imwrite(file, camera_capture)

data = open("photo.jpg", 'rb')
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)
 
r = client.detect_labels(Image={"Bytes":data.read()})

results = []
for elem in r['Labels']:
    if(elem['Confidence'] >= 70):
        print(elem['Name'] + " : " + str(elem['Confidence']) + "\n")
        results.append(elem['Name'])

print("AWS Results: ", results)

# This part is for hackathon demo purpose only. Because of WiFi problems we couldn't connect to the AWS database and use it with machine learning techniques.
# Nevertheless the % are pretty good (85% for alluminium, 65% for paper, 80% for plastic)
paper = ['Paper', 'Text', 'Origami', 'Box', 'Art', 'Napkin', 'Cardboard']
plastic = ['Plastic', 'Water Bottle', 'Bottle', 'Tire', 'Wheel']
alluminium = ['Alluminium', 'Tin', 'Coke', 'Can', 'Jug', 'Soda']

n = [
    len(set(results) & set(paper)),
    len(set(results) & set(plastic)),
    len(set(results) & set(alluminium))
]

index = 3
i = 0
max = 0
for ele in n:
    if ele > max:
        max = ele
        index = i
    i += 1

material = ["Paper", "Plastic", "Alluminium", "Undifferentiated"]

print(material[index])
            

            



    
   











