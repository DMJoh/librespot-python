from __future__ import annotations
from librespot.core import Session
from librespot.player import Player, PlayerConfiguration
from librespot.player.state import DeviceStateHandler
from librespot.proto import Connect
from librespot.proto.Player import ContextPlayerOptions, PlayerState, Restrictions, Suppressions


class StateWrapper(DeviceStateHandler.Listener):
    _state: PlayerState = None
    _session: Session = None
    _player: Player = None
    _device: DeviceStateHandler = None

    def __init__(self, session: Session, player: Player,
                 conf: PlayerConfiguration):
        self._session = session
        self._player = player
        self._device = DeviceStateHandler(session, self, conf)
        self._state = self._init_state()

    def _init_state(self) -> PlayerState:
        return PlayerState(
            playback_speed=1.0,
            suppressions=Suppressions(),
            context_restrictions=Restrictions(),
            options=ContextPlayerOptions(
                repeating_context=False,
                shuffling_context=False,
                repeating_track=False
            ),
            position_as_of_timestamp=0,
            position=0,
            is_playing=False
        )

    def ready(self) -> None:
        self._device.update_state(Connect.PutStateReason.NEW_DEVICE, 0, self._state)