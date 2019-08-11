from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="OmniApp")


def convertToCoordinates(jobLocation):
    location = geolocator.geocode(jobLocation)
    return (location.latitude, location.longitude)

