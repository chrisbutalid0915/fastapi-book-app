from pydantic import confloat, field_validator, BaseModel # It a way to define data model with validating the incoming request


class AddressBase(BaseModel): # defining a data that you want to access 
    location: str
    latitude: float
    longitude: float


    @field_validator('latitude')
    def validate_latitude(cls, lat):
         if -90 < lat <= 90:
            return lat
         else:
            raise ValueError('Latitude must be between -90 and 90 degrees')
         
    @field_validator('longitude')
    def validate_longitude(cls, long):
         if -180 < long <= 180:
            return long
         else:
             raise ValueError('Longitude must be between -180 and 180 degrees')


class AddressID(BaseModel):
    id: int


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class GetAddress(AddressBase,AddressID):
    pass


class DeleteAddress(AddressBase, AddressID):
    pass


class DistanceRequest(BaseModel):
    distance: float
    latitude: float
    longitude: float
