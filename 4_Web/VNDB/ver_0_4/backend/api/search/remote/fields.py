# Interface hints:
# 
# To define a new field group:
# class MyFieldGroup(FieldGroup):
#     _prefix = "my_prefix."
#     FIELD1 = "field1"
#     FIELD2 = "field2"
#
#     class NestedGroup(FieldGroup):
#         _prefix = "nested."
#         NESTED_FIELD = "nested_field"
#
# To access fields:
# MyFieldGroup.FIELD1  # Returns: "my_prefix.field1"
# MyFieldGroup.NestedGroup.NESTED_FIELD  # Returns: "my_prefix.nested.nested_field"
# MyFieldGroup.ALL  # Returns: ["my_prefix.field1", "my_prefix.field2", "my_prefix.nested.nested_field"]

class FieldMeta(type):
    """
    Metaclass for FieldGroup.
    Handles the creation of FieldGroup classes and manages attribute access.
    """

    def __new__(mcs, name, bases, attrs):
        """
        Create a new class with FieldMeta as its metaclass.

        Args:
            mcs (type): The metaclass (FieldMeta itself).
            name (str): Name of the class being created.
            bases (tuple): Base classes of the class being created.
            attrs (dict): Attributes of the class being created.

        Returns:
            type: The newly created class.
        """
        cls = super().__new__(mcs, name, bases, attrs)
        cls._set_outer_references()
        return cls

    def __getattribute__(cls, name):
        """
        Custom attribute access for FieldGroup classes.

        Args:
            cls (type): The class whose attribute is being accessed.
            name (str): Name of the attribute being accessed.

        Returns:
            Any: The value of the attribute, possibly modified.
        """
        if name == 'ALL':
            return cls._get_all_fields()

        value = super().__getattribute__(name)

        if not name.startswith('_'):
            return cls._handle_field(value)

        return value


class FieldGroup(metaclass=FieldMeta):
    """
    Base class for defining field groups.
    Uses FieldMeta as its metaclass to customize class creation and attribute access.
    """

    _outer = None  # Reference to the outer FieldGroup class, if any
    _prefix = ""   # Prefix to be added to field names
    ALL = 'ALL'    # Special attribute to get all fields

    @classmethod
    def _set_outer_references(cls):
        """
        Set the _outer attribute for all nested FieldGroup classes.
        This method is called during class creation by FieldMeta.__new__.

        Args:
            cls (type): The FieldGroup class being processed.
        """
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, type) and issubclass(attr_value, FieldGroup):
                setattr(attr_value, '_outer', cls)

    @classmethod
    def _get_outer_prefix(cls):
        """
        Recursively build the full prefix for a field by traversing outer classes.

        Args:
            cls (type): The FieldGroup class whose prefix is being determined.

        Returns:
            str: The full prefix for the field.
        """
        if cls._outer is None or cls._outer == VNDBFields:
            return ""
        return f"{cls._outer._get_outer_prefix()}{cls._outer._prefix}"

    @classmethod
    def _get_all_fields(cls):
        """
        Retrieve all fields defined in the FieldGroup, including nested FieldGroups.

        Args:
            cls (type): The FieldGroup class whose fields are being retrieved.

        Returns:
            list: A list of all field names, including those from nested FieldGroups.
        """
        all_fields = []
        for attr in dir(cls):
            if not attr.startswith('_') and attr != "ALL":
                value = getattr(cls, attr)
                if isinstance(value, type) and issubclass(value, FieldGroup):
                    all_fields.extend(value.ALL)
                if isinstance(value, str):
                    all_fields.append(value)
        return all_fields

    @classmethod
    def _handle_field(cls, value):
        """
        Process a field value, adding prefixes if necessary.

        Args:
            cls (type): The FieldGroup class containing the field.
            value (Any): The value of the field being processed.

        Returns:
            Any: The processed field value. If the value is a string, 
                 it will have the full prefix prepended.
        """
        if isinstance(value, str):
            return f"{cls._get_outer_prefix()}{cls._prefix}{value}"
        return value


class VNDBFields:

    class VN(FieldGroup):
        _prefix = ""
        ID = "id"
        TITLE = "title"
        ALIASES = "aliases"
        OLANG = "olang"
        DEVSTATUS = "devstatus"
        RELEASED = "released"
        LANGUAGES = "languages"
        PLATFORMS = "platforms"
        LENGTH = "length"
        LENGTH_MINUTES = "length_minutes"
        DESCRIPTION = "description"

        class TITLES(FieldGroup):
            _prefix = "titles."
            LANG = "lang"
            TITLE = "title"
            OFFICIAL = "official"
            MAIN = "main"

        class IMAGE(FieldGroup):
            _prefix = "image."
            ID = "id"
            URL = "url"
            DIMS = "dims"
            SEXUAL = "sexual"
            VIOLENCE = "violence"
            THUMBNAIL = "thumbnail"
            THUMBNAIL_DIMS = "thumbnail_dims"

        class SCREENSHOTS(FieldGroup):
            _prefix = "screenshots."
            URL = "url"
            DIMS = "dims"
            SEXUAL = "sexual"
            VIOLENCE = "violence"
            THUMBNAIL = "thumbnail"
            THUMBNAIL_DIMS = "thumbnail_dims"

        class RELATIONS(FieldGroup):
            _prefix = "relations."
            ID = "id"
            TITLE = "title"
            RELATION = "relation"
            RELATION_OFFICIAL = "relation_official"

        class TAGS(FieldGroup):
            _prefix = "tags."
            ID = "id"
            NAME = "name"
            CATEGORY = "category"
            RATING = "rating"
            SPOILER = "spoiler"
            LIE = "lie"

        class DEVELOPERS(FieldGroup):
            _prefix = "developers."
            ID = "id"
            NAME = "name"
            ORIGINAL = "original"

        class STAFF(FieldGroup):
            _prefix = "staff."
            ID = "id"
            NAME = "name"
            ORIGINAL = "original"
            EID = "eid"
            ROLE = "role"

        class VA(FieldGroup):
            _prefix = "va."

            class STAFF(FieldGroup):
                _prefix = "staff."
                ID = "id"
                NAME = "name"
                ORIGINAL = "original"

            class CHARACTER(FieldGroup):
                _prefix = "character."
                ID = "id"
                NAME = "name"
                ORIGINAL = "original"

        class EXTLINKS(FieldGroup):
            _prefix = "extlinks."
            URL = "url"
            LABEL = "label"
            NAME = "name"
            ID = "id"

    class Character(FieldGroup):
        _prefix = ""
        ID = "id"
        NAME = "name"
        ORIGINAL = "original"
        ALIASES = "aliases"
        DESCRIPTION = "description"
        BLOOD_TYPE = "blood_type"
        HEIGHT = "height"
        WEIGHT = "weight"
        BUST = "bust"
        WAIST = "waist"
        HIPS = "hips"
        CUP = "cup"
        AGE = "age"
        BIRTHDAY = "birthday"
        SEX = "sex"

        class IMAGE(FieldGroup):
            _prefix = "image."
            ID = "id"
            URL = "url"
            DIMS = "dims"
            SEXUAL = "sexual"
            VIOLENCE = "violence"

        class VNS(FieldGroup):
            _prefix = "vns."
            ID = "id"
            TITLE = "title"
            SPOILER = "spoiler"
            ROLE = "role"

        class TRAITS(FieldGroup):
            _prefix = "traits."
            ID = "id"
            NAME = "name"
            GROUP_ID = "group_id"
            GROUP_NAME = "group_name"
            SPOILER = "spoiler"
            LIE = "lie"

    class Tag(FieldGroup):
        _prefix = ""
        ID = "id"
        NAME = "name"
        ALIASES = "aliases"
        DESCRIPTION = "description"
        CATEGORY = "category"
        SEARCHABLE = "searchable"
        APPLICABLE = "applicable"
        VN_COUNT = "vn_count"

    class Producer(FieldGroup):
        _prefix = ""
        ID = "id"
        NAME = "name"
        ORIGINAL = "original"
        ALIASES = "aliases"
        LANG = "lang"
        TYPE = "type"
        DESCRIPTION = "description"

    class Staff(FieldGroup):
        _prefix = ""
        ID = "id"
        ISMAIN = "ismain"
        NAME = "name"
        ORIGINAL = "original"
        LANG = "lang"
        GENDER = "gender"
        DESCRIPTION = "description"

        class ALIASES(FieldGroup):
            _prefix = "aliases."
            AID = "aid"
            NAME = "name"
            ISMAIN = "ismain"

    class Trait(FieldGroup):
        _prefix = ""
        ID = "id"
        NAME = "name"
        ALIASES = "aliases"
        DESCRIPTION = "description"
        SEARCHABLE = "searchable"
        APPLICABLE = "applicable"
        GROUP_ID = "group_id"
        GROUP_NAME = "group_name"
        CHAR_COUNT = "char_count"


# Test the implementation
if __name__ == "__main__":
    print(VNDBFields.VN.ALL)
    print(VNDBFields.Character.ALL)
    print(VNDBFields.Producer.ALL)
    print(VNDBFields.Staff.ALL)
    print(VNDBFields.Tag.ALL)
    print(VNDBFields.Trait.ALL)
