# ground-station-api
The ground station API is a Flask app that habours the network of multiple data streams from LoT devices of various purposes.

## The Devices
Devices collect and transmit sensor data to a nearby server using their assigned ID. IDs are in the form: TT##, where TT is the ID type specifying the type of device, and ## is the ID index.

## Device Types
LoT devices include but are not limited to:
- Weather Stations (WS)
- Habs (B)
- Drones (D)
- Planes (P)

Use the ID type in the brakets when querying for type.

## Active Devices
The following is an updated list of devices actively transmitting data with their IDs.

### Weather Stations
- Origin (WS01)

## The Server
The app is ran on a server that accepts sensor data from LoT devices and saves them to a SQL database. Currently, any client can send a request to the app to get parsed sensor data in JSON format.

The server listens to the frequency of the devices using SDR, decodes the sent data and uses the ID in The decoded data to save it to the corresponding table in the SQL database.

## Public Endpoints
```
"/"

Home page of API
Parameters: NA
Format: HTML
```

```
"/data"

Endpoint for getting all data from certain device.
Required Parameters: ID
Optional Parameters: Date (dd-mm-yy), Time (hhmm)
Format: JSON

Output: {
    ID: TT##,
    Lat: ##.####,
    Long: ##.####,
    Sensor1: ...,
    Sensor2: ...,
}
```

```
"/status"

Endpoint for getting status of certain device(s).
Required Parameters: ID or Type (See Device Types)
Format: JSON

Output: {
    ID: TT##,
    BatLvl: ##%,
    Errors: []
}
```

```
"/statusall"

Endpoint for getting status of all devices.
Parameters: NA
Format: JSON

Output: {
    ID: TT##,
    BatLvl: ##%,
    Errors: []
}
```

# To-do
- reserach how to update one-to-many tables
- research how to query for range of date and times