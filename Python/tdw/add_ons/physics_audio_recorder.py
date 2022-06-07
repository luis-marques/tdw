from typing import List, Union
from pathlib import Path
import numpy as np
from tdw.output_data import OutputData, AudioSources, Rigidbodies, Transforms
from tdw.audio_utils import AudioUtils
from tdw.add_ons.add_on import AddOn


class PhysicsAudioRecorder(AddOn):
    """
    Record audio generated by physics events.
    """

    def __init__(self, max_frames: int = -1, record_audio: bool = True):
        """
        :param max_frames: If greater than 0, stop recording after this many frames even if objects are still moving or making sound.
        :param record_audio: If True, record audio to a file. If False, only listen to audio events.
        """

        super().__init__()

        """:field
        # If greater than 0, stop recording after this many frames even if objects are still moving or making sound.
        """
        self.max_frames: int = max_frames
        # The current frame.
        self._frame: int = 0
        """:field
        The path to the next audio file.
        """
        self.path: Path = Path.home()
        """:field
        If False, there is an ongoing audio.
        """
        self.done: bool = True
        self._record_audio: bool = record_audio

    def get_initialization_commands(self) -> List[dict]:
        return []

    def on_send(self, resp: List[bytes]) -> None:
        if self.done:
            return
        # Stop recording at the maximum number of frames.
        self._frame += 1
        if 0 < self.max_frames <= self._frame:
            if self._record_audio:
                AudioUtils.stop()
            return
        # Get any objects that fell below the floor.
        below_floor: List[int] = list()
        for i in range(len(resp) - 1):
            r_id = OutputData.get_data_type_id(resp[i])
            if r_id == "tran":
                transforms = Transforms(resp[i])
                for j in range(transforms.get_num()):
                    if transforms.get_position(j)[1] < -0.1:
                        below_floor.append(transforms.get_id(j))
        # Check if objects have stopped moving and no audio is playing.
        sleeping = True
        playing_audio = False
        for i in range(len(resp) - 1):
            r_id = OutputData.get_data_type_id(resp[i])
            if r_id == "rigi":
                rigidbodies = Rigidbodies(resp[i])
                for j in range(rigidbodies.get_num()):
                    if rigidbodies.get_id(j) not in below_floor and not rigidbodies.get_sleeping(j):
                        sleeping = False
                        break
            elif r_id == "audi":
                audio_sources = AudioSources(resp[i])
                for j in range(audio_sources.get_num()):
                    if audio_sources.get_is_playing(j):
                        playing_audio = True
                        break
                # Check if the simulation is totally silent (there might be Resonance Audio reverb).
                if not playing_audio and np.max(audio_sources.get_samples()) > 0:
                    playing_audio = True
        if sleeping and not playing_audio:
            self.stop()

    def start(self, path: Union[str, Path]) -> None:
        """
        Start recording.

        :param path: The path to the output .wav file.
        """

        # Don't start a new recording if one is ongoing.
        if not self.done:
            return
        self.done = False
        if isinstance(path, str):
            self.path = Path(path)
        else:
            self.path = path
        if not self.path.parent.exists:
            self.path.parent.mkdir(parents=True)
        if self.path.exists():
            self.path.unlink()

        self._frame = 0
        # Start listening.
        if self._record_audio:
            AudioUtils.start(output_path=self.path)
        self.commands.extend([{"$type": "send_audio_sources",
                               "frequency": "always"},
                              {"$type": "send_rigidbodies",
                               "frequency": "always"},
                              {"$type": "send_transforms",
                               "frequency": "always"}])

    def stop(self) -> None:
        """
        Stop an ongoing recording. Use ffmpeg to remove initial silence.
        """

        if self._record_audio:
            AudioUtils.stop()
        self.done = True
