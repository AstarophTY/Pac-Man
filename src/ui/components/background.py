from __future__ import annotations

from dataclasses import dataclass

from ursina import Entity, Sprite, camera, color, time


@dataclass
class _AnimatedSprite:
    entity: Sprite
    texture: str
    row: int
    frame: int
    columns: int
    rows: int


@dataclass
class _SpriteLane:
    sprites: list[_AnimatedSprite]
    speed: float
    spacing: float


class PacmanBackground(Entity):
    def __init__(self) -> None:
        super().__init__(parent=camera.ui)

        self._track_rows: list[_SpriteLane] = []
        self._frame_timer = 0.0
        self._frame_interval = 0.12
        self._pacman_sheet = "assets/sprites/PacManAssets-PacMan.png"

        Entity(
            parent=self,
            model="quad",
            color=color.rgb(0.04, 0.06, 0.12),
            scale=(2.4, 1.4),
            z=2,
        )

        self._create_sprite_lanes()

    def _create_sprite_lanes(self) -> None:
        lane_y = [0.24, 0.02, -0.20]
        lane_speed = [0.24, 0.28, 0.22]
        spacing = 0.28
        sprites_per_lane = 10

        lane_config = [(self._pacman_sheet, 0, 4, 3)]

        for lane_index, y in enumerate(lane_y):
            lane_entities: list[_AnimatedSprite] = []
            texture_path, sprite_row, columns, rows = lane_config[0]

            for i in range(sprites_per_lane):
                sprite = Sprite(
                    parent=self,
                    texture=texture_path,
                    x=-1.3 + i * spacing,
                    y=y,
                    z=1.6,
                    scale_x=0.09,
                    scale_y=0.09,
                    color=color.rgb(1.0, 1.0, 1.0),
                )
                animated_sprite = _AnimatedSprite(
                    entity=sprite,
                    texture=texture_path,
                    row=sprite_row,
                    frame=i % columns,
                    columns=columns,
                    rows=rows,
                )
                self._apply_frame(animated_sprite)
                lane_entities.append(animated_sprite)

            self._track_rows.append(
                _SpriteLane(
                    sprites=lane_entities,
                    speed=lane_speed[lane_index],
                    spacing=spacing,
                )
            )

    def update(self) -> None:
        self._frame_timer += time.dt

        for row in self._track_rows:
            for animated in row.sprites:
                animated.entity.x -= row.speed * time.dt

            if not row.sprites:
                continue

            rightmost_x = max(animated.entity.x for animated in row.sprites)
            for animated in row.sprites:
                if animated.entity.x < -1.35:
                    animated.entity.x = rightmost_x + row.spacing
                    rightmost_x = animated.entity.x

        if self._frame_timer >= self._frame_interval:
            self._frame_timer = 0.0
            self._animate_rows()

    def _animate_rows(self) -> None:
        for row in self._track_rows:
            for animated in row.sprites:
                animated.frame = (animated.frame + 1) % animated.columns
                self._apply_frame(animated)

    def _apply_frame(self, animated: _AnimatedSprite) -> None:
        frame_w = 1.0 / animated.columns
        frame_h = 1.0 / animated.rows
        offset_x = animated.frame * frame_w
        offset_y = 1.0 - (animated.row + 1) * frame_h

        animated.entity.texture = animated.texture
        animated.entity.texture_scale = (frame_w, frame_h)
        animated.entity.texture_offset = (offset_x, offset_y)
