from typing import List
from tdw.object_data.composite_object.sub_object.light_dynamic import LightDynamic
from tdw.object_data.composite_object.sub_object.hinge_dynamic import HingeDynamic


class CompositeObjectDynamic:
    """
    Dynamic data for a composite object and its sub-objects.
    
    Note that not all sub-objects will be in this output data because some of them don't have specialized dynamic properties.
    For example, non-machines have dynamic positions, velocities, etc. but these can be found in `Transforms` and `Rigidbodies` data, respectively.
    """

    def __init__(self, object_id: int, hinges: List[HingeDynamic], lights: List[LightDynamic]):
        """
        :param object_id: The ID of the root object.
        :param hinges: A list of [`HingeDynamic`](sub_object/hinge_dynamic.md) sub-objects, which includes all hinges, springs, and motors.
        :param lights: A list of [`LightDynamic`](sub_object/light_dynamic.md) sub-objects such as lamp lightbulbs.
        """

        """:field
        The ID of the root object.
        """
        self.object_id = object_id
        """:field
        A list of [`HingeDynamic`](sub_object/hinge_dynamic.md) sub-objects, which includes all hinges, springs, and motors.
        """
        self.hinges: List[HingeDynamic] = hinges
        """:field
        A list of [`LightDynamic`](sub_object/light_dynamic.md) sub-objects such as lamp lightbulbs.
        """
        self.lights: List[LightDynamic] = lights
