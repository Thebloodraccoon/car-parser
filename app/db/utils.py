from typing import Union, Dict, Any, List

from passlib.context import CryptContext


def convert_object_id_to_str(obj_data: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """Convert ObjectId to string in document(s) and rename _id to id"""
    if isinstance(obj_data, list):
        for obj in obj_data:
            if obj and "_id" in obj:
                obj["id"] = str(obj["_id"])
                del obj["_id"]
        return obj_data
    elif obj_data and "_id" in obj_data:
        obj_data["id"] = str(obj_data["_id"])
        del obj_data["_id"]
    return obj_data


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
