
lat=12.9
lng=77.8

source coordinates.txt

if test $latitude
then
    lat=$latitude
else
  echo "latitude value not set in coordinates.txt, using default"
fi

if test $longitude
then
    lng=$longitude
else
    echo "$longitude value not set in coordinates.txt, using default"
fi

echo -e "Please note down location coordinates which we are populating data for - \n( latitude = $lat, longitude = $lng )"
echo "If you think this is incorrect, check your coordinates.txt file."


if ps -ef | grep mongo | grep -v grep | wc -l | tr -d ' '; then
#if systemctl status mongod | grep active > /dev/null; then
    echo "MongoDB is running..."
else
    echo "MongoDB not running; Exiting"
    exit -1
fi

# Ensure a clean slate & populate all collections
mongosh restaurant-database --eval "db.dropDatabase()" 
mongorestore --host localhost --db restaurant-database --gzip --archive=./restaurants-norm-gzipped-mongo-dump

pip3 install pymongo

# Localize restaurants
echo "Localizing restaurants for your region, so that you can see them when you load the app..."
python3 ./localize_restaurants.py $lat $lng 50
