from abc import ABC
from typing import Dict
from overrides import final
from tdw.add_ons.container_manager_data.container_collider_tag import ContainerColliderTag
from tdw.add_ons.container_manager_data.container_trigger_collider import ContainerTriggerCollider


class ContainerNonUniformScaleTriggerCollider(ContainerTriggerCollider, ABC):
    """
    Data for a container trigger collider that can have a non-uniform scale.
    """

    @final
    def __init__(self, tag: ContainerColliderTag, position: Dict[str, float], scale: Dict[str, float]):
        """
        :param tag: The collider's semantic [`ContainerColliderTag`](container_collider_tag.md).
        :param position: The local position of the collider.
        :param scale: The scale of the collider.
        """

        super().__init__(tag=tag, position=position)
        """:field
        The scale of the collider.
        """
        self.scale: Dict[str, float] = {"x": round(scale["x"], 8),
                                        "y": round(scale["y"], 8),
                                        "z": round(scale["z"], 8)}
