from dataclasses import dataclass

class IntConversionDescriptor:
  def __init__(self, *, default):
    self._default = default

  def __set_name__(self, owner, name):
    self._name = "_" + name

  def __get__(self, obj, type):
    if obj is None:
      return self._default

    return getattr(obj, self._name, self._default)

  def __set__(self, obj, value):
    setattr(obj, self._name, int(value))

@dataclass
class InventoryItem:
  quantity_on_hand: IntConversionDescriptor = IntConversionDescriptor(default=100)

i = InventoryItem()
print(i.quantity_on_hand)   # 100
i.quantity_on_hand = 2.5    # calls __set__ with 2.5
print(i.quantity_on_hand)   # 2