from pydantic import BaseModel
from pydantic import BaseModel, Field, root_validator
from api.responses.exceptions import raise_logic_exception
from api.schemas.message import MessageDB
import phonenumbers
from phonenumbers import NumberParseException

