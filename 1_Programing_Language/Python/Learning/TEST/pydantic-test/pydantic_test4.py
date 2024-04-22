import re
from pydantic import BaseModel, field_validator, ValidationError, Field
from typing import Optional


class Address(BaseModel):
    street: str
    number: int
    zipode: str


class Person(BaseModel):
    first_name: str
    last_name: str
    cell_phone_number: str
    address: Optional[Address]

    # This is a class method that is used to validate the cell_phone_number field.
    # It will be called after the field is set and before the model is created.
    @field_validator('cell_phone_number')
    def vaildate_cell_phone_number(cls, v):
        match = re.match(r'^\+?1?\d{9,15}$', v)
        if not match:
            raise ValueError('Invalid phone number')
        elif len(v) != 11:
            raise ValueError('Phone number must be 11 digits')
        return v


if __name__ == '__main__':
    try:
        Person(
            first_name = 'John',
            last_name = 'Doe',
            cell_phone_number = '123456789',
            address = Address(street = 'Main St', number = 123, zipode = '12345')
        )
    except ValidationError as e:
        print(f'Throw Error: {e}')
    else:
        print('No error')

    print('='*50)

    try:
        Person(
            first_name = 'John',
            last_name = 'Doe',
            cell_phone_number = '1234567890',
            address = Address(street = 'Main St', number = 123, zipode = '12345')
        ) 
    except ValidationError as e:
        print(f'Throw Error: {e}')
    else:
        print('No error')
