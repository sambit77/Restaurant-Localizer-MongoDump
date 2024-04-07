import random
import sys
from pymongo import MongoClient


def insert_localized_restauants(lat, lng, num_restaurants_to_change):
    # print(
    #     "Enter co-ordinates in the format {latitude},{longitude}. For ex: 12.01,27.66"
    # )
    # try:
    #     lat, lng = map(float, input().split(","))
    # except:
    #     print(sys.exc_info())
    #     sys.exit("Input format incorrect.")

    client = MongoClient()
    db = client["restaurant-database"]
    restaurant_collection = db["restaurants"]
    num_restaurants = restaurant_collection.count_documents({})

    random.seed(1)
    start_index = round(random.random() * (num_restaurants / 2))

    cursor = db["restaurants"].find(skip=start_index, limit=num_restaurants_to_change)

    for restaurant in cursor:
        restaurant["latitude"] = lat
        restaurant["longitude"] = lng
        print(restaurant['name'])
        restaurant_collection.find_one_and_replace(
            {"_id": restaurant["_id"]}, restaurant
        )

    print("{} Restaurants around {},{} co-ordinates created.".format(num_restaurants_to_change, lat, lng))


if __name__ == "__main__":
    print(
        "Accepting co-ordinates in the format {latitude} {longitude} {num_restaurants_to_change}. For ex: 12.01 27.66 200"
    )
    
    print ("Number of arguments passed to localize_restaurants {}".format(len(sys.argv)))
    
    assert (len(sys.argv) == 4)
    insert_localized_restauants(sys.argv[1], sys.argv[2], int(sys.argv[3]))
