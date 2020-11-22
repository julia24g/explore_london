import csv
import requests
import json
import googlemaps
from geopy.geocoders import Nominatim
class Session:
    def __init__(self, userinput, distance):
        self.url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        self.api_key = 'AIzaSyDnsX9Fpb8jvEp7RssX49SF1oGQzqz4ojY'
        self.user_wants_parks = False
        self.user_wants_art = False
        self.desiredLength = int(distance) / 2  # user walks back the way they came
        self.path = []
        self.pathlength = 0  # the walking distance of the generated path
        self.parks = {}
        self.userinput = userinput
        self.start = '1151 Richmond St, London, ON N6A 3K7'

    def main(self):
        # TESTING

        self.checkInput()

        return
        #return self.greedyPlan()

    # def addCoords(self):
    #     rows = [[]]
    #     with open('Parks.csv') as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=',')
    #         line_count = 0
    #         for row in csv_reader:
    #             address = row[0]
    #             rows.append([address, 0, 0])
    #             line_count += 1
    #     #print(rows)

    #     with open('newParks.csv', 'wt', newline='') as outf:
    #         csv_writer = csv.writer(outf, delimiter=',')
    #         geolocator = Nominatim(user_agent="test")
    #         for i in range(2, line_count):
    #             addressSTR = rows[i][0]
    #             # print(addressSTR)
    #             location = geolocator.geocode(addressSTR)
    #             try:
    #                 X = location.longitude
    #                 Y = location.latitude
    #             except:
    #                 X = 0
    #                 Y = 0
    #             print([addressSTR, X, Y])
    #             rows[i] = [addressSTR, X, Y]
    #         print(rows)
    #         csv_writer.writerows(rows)

    #     return

    def checkInput(self):
        if "Parks" in self.userinput:
            self.user_wants_parks = True
            self.readParks()
        if "Art" in self.userinput:
            self.user_wants_art = True

    def readParks(self):
        # read in parks data, stores it as a list of address strings
        with open('newParks.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    # add address to parks[]
                    address = row[0]
                    X = float(row[1])
                    Y = float(row[2])
                    if (address != '') and (X != 0.0):
                        self.parks[address] = [address, X, Y]
                        line_count += 1
            # print("file had %d lines" % line_count)
            # print(parks)

    def calcDist(self, goal):
        # calculate walking distance between two places
        r = requests.get(self.url + 'origins=' + self.start + '&mode=walking' + '&destinations=' + goal + '&key=' + self.api_key)
        x = r.json()
        # print(x)
        try:
            x["rows"][0]["elements"][0]["distance"]["value"] / 1000
        except:
            # error in reading spreadsheet data, set weighting so point isnt used.
            return 10000000000
        # return the distance only (in metres)
        return x["rows"][0]["elements"][0]["distance"]["value"] / 1000  # /1000 to get km

    def addNearestPark(self):
        threshold = 5  # Parks within X km are automatically added
        for park in self.parks:
            dist = self.calcDist(park)
            # print(dist)
            if (dist <= threshold) and (park not in self.path):  # if park is close enough and not visited
                nearestPark = park
                if (self.pathlength + dist) <= (self.desiredLength):  # check if park overshoots
                    self.pathlength += dist
                    self.path.append(nearestPark)
                    self.start = nearestPark
                return


    def greedyPlan(self):
        # simple pathfinder, not efficient, but returns "best" path
        self.path.append(self.start)
        if (self.user_wants_parks and not self.user_wants_art):
            while self.pathlength < self.desiredLength:
                self.addNearestPark()

                # print(self.path)

        self.pathlength += self.pathlength
        print(self.pathlength)
        return self.path

# user_wants_art = False
# user_wants_trees = False
# return_to_start = True
# total_distanceM = 10000
# first_park_dist_threshold = 5000  # this is the max acceptable distance for the first park
# path = []
# art = {}
# parks = []
# TESTING
# goal = '378 Horton St E, London, ON N6B 1L7'
# start = '111 Wharncliffe Rd S, London, ON N6J 2K2'
# ONE TIME USE
# numClosestParks = 3  # number of closest parks to find for each park (walking distance)

# def main():


# def checkInput(inputList):
#     user_wants_parks = False
#     # check user input
#     if "Parks" in inputList:
#         user_wants_parks = True
#     return user_wants_parks

# def calcDist(start, goal):
#     # calculate walking distance between two places
#     r = requests.get(url + 'origins=' + start + '&mode=walking' + '&destinations=' + goal + '&key=' + api_key)
#     x = r.json()
#     # print(x)
#     # return the distance only (in metres)
#     return x["rows"][0]["elements"][0]["distance"]["value"]  # /1000 to get km

# def readParks(parks):
#     # read in parks data, stores it as a list of address strings
#     with open('Parks.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_count = 0
#         for row in csv_reader:
#             if line_count == 0:
#                 line_count += 1
#             else:
#                 # add address to parks[]
#                 parks.append(row[2])
#                 line_count += 1
#         # print("file had %d lines" % line_count)
#         # print(parks)

# def readArt(art):
#     # read in art data
#     with open('Public_Art.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_count = 0
#         for row in csv_reader:
#             if line_count == 0:
#                 line_count += 1
#             else:
#                 # add name and address to art{}
#                 art[row[3]] = row[5]
#                 line_count += 1
#         # print("file had %d lines" % line_count)
#         # print(art)

# def findFirstPark(parks, threshold, start_location):
#     # finds the first park in list that is in acceptable threshold
#     # returns the address of the park
#     # this may be very time consuming/costly (lots of api calls), use sparingly
#     for park in parks:
#         if calcDist(start_location, park) <= threshold:
#             return park
#     return("no parks within threshold")

# def findNearestArt(art, start, path, pathLength):
#     distanceToBeat = 100000000
#     for name, address in art:
#         dist = calcDist(start, name + ' ' + address)
#         if dist <= distanceToBeat:
#             nearestArt = name + address
#             distanceToBeat = dist

#     return nearestArt

# def findNearestPark(parks, start, path, pathlength):
#     distanceToBeat = 100000000
#     for park in parks:
#         dist = calcDist(start, park)
#         if (dist <= distanceToBeat) and (park not in path):
#             nearestPark = park
#             distanceToBeat = dist
#     pathlength += distanceToBeat
#     return nearestPark

#def greedyPlan(path, wantsArt, wantsParks, desiredLength, start, parks, art):
    # simple pathfinder, not efficient, but returns "best" path
 #   pathlength = 0
  #  if (wantsParks and not wantsArt):
   #     while pathlength < desiredLength:
    #        nextStop = findNearestPark(parks, start, path, pathlength)
     #       start = nextStop
      #      path.append(nextStop))

    #return path

# def closestParks(X, parks):
#     # RUN ONCE TO GENERATE SPREADSHEET (lots of api calls)
#     # Finds the X closest parks to each park
#     # Finds the distance between the found parks and the OG park


#     for OGpark in parks:
#         for otherPark in parks:
#             if (OGpark != otherPark):
#                 # check distance
#                 dist = calcDist(OGpark, otherPark)
#         smallest = 0
#         secondSmallest = 0
#         thirdSmallest = 0

#     row_list = [[]]

#     with open('ClosestParks.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows()

#     return

# def plan(path, wantsArt, wantsTrees, desiredLength, start, parks, art, threshold):
#     # returns an ordered list of locations
#     # plans until pathLength == desiredLength

#     # find first park or art depending on choices and start location
#     # if both are selected, choose closeset one
#     if (wantsArt and wantsTrees):
#         # find a park within threshold
#         firstPark = findFirstPark(parks, threshold, start)
#         # find the nearest art
#         firstArt = findNearestArt(art, start)
#         if calcDist(start, firstPark) > calcDist(start, firstArt):
#             path.append(firstArt)
#         else:
#             path.append(firstPark)
#     elif (wantsArt and not wantsTrees):
#         # find the nearest art
#         firstArt = findNearestArt(art, start)
#         path.append(firstArt)
#     elif (not wantsArt and wantsTrees):
#         # find a park within threshold
#         firstPark = findFirstPark(parks, threshold, start)
#         path.append(firstPark)

#     # First destination found based on preferences
#     # Now loop to create rest of path
#     # include randomness for variation??

#     return path

# def feedback():
#     # most visited destinations


# TESTING
# print(calcDist(start, goal))
# readParks(parks)
# readArt(art)

# TESTING
# if __name__ == "__main__":
#     calcDist()
#     readParks(parks)
#     readArt(art)

Session(["Parks"], "20").main()
