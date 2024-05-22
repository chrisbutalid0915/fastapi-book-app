import logging
import os
from typing import List

import fastapi
from fastapi import Depends, HTTPException, Query
from geopy.distance import geodesic
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.address import Address
from app.schemas.book import (AddressCreate, AddressUpdate, DeleteAddress,
                              DistanceRequest, GetAddress)
from app.schemas.user import UserBase
from app.services import get_current_active_user

router = fastapi.APIRouter()  # create a new router instance


# Create a folder for logs if it doesn't exist
log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)


# Configure logging settings
log_file_path = os.path.join(log_folder, "app.log")
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define log message format
    filename=log_file_path,  # Specify the log file
    filemode="a",  # Append mode for the log file
)


@router.post("/address", response_model=GetAddress)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    UserBase=Depends(get_current_active_user),
):
    from app.models.address import Address

    """
    Create new Address Book
    :param address: class
    :param db: class
    :return: class
    """
    try:
        logging.info("POST /address")
        # Create a new address object with the data from AddressCreate input
        address = Address(**dict(address))
        # Add the new created address to the database session
        db.add(address)
        # Commit the transaction
        db.commit()
        # Refresh the address object to ensure the changes
        db.refresh(address)
        return address
    except Exception as e:
        logging.error(f"Error occurred: {e}")


@router.put("/address/{address_id}", response_model=GetAddress)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    UserBase=Depends(get_current_active_user),
):
    """
    Update details Address Book
    :param address_id: int
    :param address: class
    :param db: class
    :return: query
    """
    logging.info(f"PUT /address/{address_id}")
    # Get the address by ID
    query = db.query(Address).filter(Address.id == address_id).first()
    if query is None:
        # Return Exception 404 when no address found
        logging.error(f"PUT /address/{address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")

    # update the selected query
    for key, value in address.dict().items():
        setattr(query, key, value)
    # Commit the transaction
    db.commit()
    # Refresh the address object to ensure the changes
    db.refresh(query)
    return query


@router.get("/address/{address_id}", response_model=GetAddress)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    UserBase=Depends(get_current_active_user),
):
    """
    Get the address book by id
    :param address_id: int
    :param db: class
    :return: query
    """
    logging.info(f"GET /address/{address_id}")
    # Get the address by ID
    query = db.query(Address).filter(Address.id == address_id).first()
    if query is None:
        # Return Exception 404 when no address found
        logging.error(f"GET /address/{address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return query


@router.get("/address", response_model=List[GetAddress])
def get_addresses(
    db: Session = Depends(get_db), UserBase=Depends(get_current_active_user)
):
    """
    Get all the addresses
    :param db: class
    :return: query
    """
    logging.info(f"GET /address")
    # Get all the addresses
    query = db.query(Address).all()
    return query


@router.get("/address/distance/", response_model=List[GetAddress])
def get_addresses_within_distance(
    request: DistanceRequest,
    db: Session = Depends(get_db),
    UserBase=Depends(get_current_active_user),
):
    """
    Get the addresses within the given distance
    :param latitude: float
    :param longitude: float
    :param distance: float
    :param db: class
    :return: list
    """
    logging.info(f"GET /address/distance")
    current_location = (request.latitude, request.longitude)
    addresses_within_distance = []
    all_addresses = db.query(Address).all()
    for address in all_addresses:
        address_coordinates = (address.latitude, address.longitude)
        if geodesic(current_location, address_coordinates).km <= request.distance:
            addresses_within_distance.append(address)
    return addresses_within_distance


@router.delete("/address/{address_id}", response_model=DeleteAddress)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_active_user),
):
    """
    Delete the address book by id
    :param address_id: int
    :param db: class
    :return: query
    """
    if current_user:
        logging.info(f"DELETE /address/{address_id}")
        # Get the address by ID
        query = db.query(Address).filter(Address.id == address_id).first()
        if query is None:
            logging.error(f"DELETE /address/{address_id} not found")
            raise HTTPException(status_code=404, detail="Address not found")
        # Delete the selected query address
        db.delete(query)
        # Commit the transaction
        db.commit()
        return query
