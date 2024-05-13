import fastapi
import logging
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import OpenAPI
from fastapi.responses import HTMLResponse
from app.models.book import (
    Address,
    GetAddress,
    AddressCreate,
    AddressUpdate,
    DeleteAddress,
    DistanceRequest
)
from app.database import get_db
from fastapi import Query, Depends, HTTPException
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from app.utils.utils import calculate_distance
from typing import List


router = fastapi.APIRouter() # create a new router instance


# Configure logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@router.get("/openapi.json")
async def get_open_api_endpoint():
    """
    Returns the OPENAPI schema in JSON Format
    """
    logging.info("GET /openapi.json")
    return HTMLResponse(OpenAPI().dict())


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Serves a customized Swagger UI HTML page
    """
    logging.info("GET /docs")
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


@router.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the root URL ("/") with a custom HTML response
    """
    logging.info("GET /")
    return """
    <html>
        <head>
            <title>Custom Swagger UI</title>
        </head>
        <body>
            <h1>Custom Swagger UI</h1>
            <p>Find the API documentation <a href="/docs">here</a>.</p>
        </body>
    </html>
    """


@router.post("/create_address", response_model=GetAddress, tags=["Address"])
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """
    Create new Address Book
    :param address: class
    :param db: class
    :return: class
    """
    try:
        logging.info("POST /create_address")
        # Create a new address object with the data from AddressCreate input
        address = Address(**address.dict())
        # Add the new created address to the database session
        db.add(address)
        # Commit the transaction
        db.commit()
        # Refresh the address object to ensure the changes
        db.refresh(address)
        return address
    except Exception as e:
        logging.error(f"Error occurred: {e}")


@router.put("/update_address/{address_id}", response_model=GetAddress, tags=["Address"])
def update_address(
    address_id: int, address: AddressUpdate, db: Session = Depends(get_db)
):
    """
    Update details Address Book
    :param address_id: int
    :param address: class
    :param db: class
    :return: query
    """
    logging.info(f"PUT /update_address/{address_id}")
    # Get the address by ID
    query = db.query(Address).filter(Address.id == address_id).first()
    if query is None:
        # Return Exception 404 when no address found
        logging.error(f"PUT /update_address/{address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")

    # update the selected query
    for key, value in address.dict().items():
        setattr(query, key, value)
    # Commit the transaction
    db.commit()
    # Refresh the address object to ensure the changes
    db.refresh(query)
    return query


@router.get("/get_address/{address_id}", response_model=GetAddress, tags=["Address"])
def get_address(address_id: int, db: Session = Depends(get_db)):
    """
    Get the address book by id
    :param address_id: int
    :param db: class
    :return: query
    """
    logging.info(f"GET /get_address/{address_id}")
    # Get the address by ID
    query = db.query(Address).filter(Address.id == address_id).first()
    if query is None:
        # Return Exception 404 when no address found
        logging.error(f"GET /get_address/{address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return query


@router.get("/get_addresses", response_model=List[GetAddress], tags=["Address"])
def get_addresses(db: Session = Depends(get_db)):
    """
    Get all the addresses
    :param db: class
    :return: query
    """
    logging.info(f"GET /get_addresses")
    # Get all the addresses
    query = db.query(Address).all() 
    return query


@router.get("/addresses/distance/", response_model=List[GetAddress], tags=["Address"])
def get_addresses_within_distance(
    request: DistanceRequest,
    db: Session = Depends(get_db)
):
    """
    Get the addresses within the given distance
    :param latitude: float
    :param longitude: float
    :param distance: float
    :param db: class
    :return: list
    """
    logging.info(f"GET /addresses/distance")
    center_point = (request.latitude, request.longitude)
    addresses_within_distance = []
    all_addresses = db.query(Address).all()
    for address in all_addresses:
        address_coordinates = (address.latitude,address.longitude)
        if calculate_distance(*center_point, *address_coordinates) <= request.distance:
            addresses_within_distance.append(address)
    return addresses_within_distance


@router.delete("/delete_address/{address_id}", response_model=DeleteAddress , tags=["Address"])
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete the address book by id
    :param address_id: int
    :param db: class
    :return: query
    """
    logging.info(f"DELETE /delete_address/{address_id}")
    # Get the address by ID
    query = db.query(Address).filter(Address.id == address_id).first()
    if query is None:
        logging.error(f"DELETE /delete_address/{address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    # Delete the selected query address
    db.delete(query) 
    # Commit the transaction
    db.commit()
    return query
