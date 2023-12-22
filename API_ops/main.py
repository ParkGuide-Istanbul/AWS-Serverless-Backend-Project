import GoogleMaps_PlaceID as gmpid
import GoogleMaps_PlaceInfo as gmpi
import IBB_parks as ibbp
import IBB_parkID as ibbpid
import string



destID = gmpid.google_maps_place_id("ITU Maslak Türkiye")
print(destID)


info = gmpi.google_maps_place_info(destID.get_place_id()).get_place_info()
print(info)

district = gmpi.google_maps_place_info(destID.get_place_id()).get_district_name()
print(district)
district = district.upper()

parks_ID = ibbp.ParkFinder.search_by_district(district)

IBB_parks = ibbpid.ibb_parks_ID(parks_ID)
print(IBB_parks.get_place_info())



