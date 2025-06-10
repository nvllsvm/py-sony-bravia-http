import asyncio
from typing import Annotated

from litestar import Controller, Litestar, get
from litestar.datastructures import State
from litestar.params import Parameter
from litestar.logging import LoggingConfig


logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["queue_listener"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    log_exceptions="always",
)

logger = logging_config.configure()()


class LoungeTV:
    INPUT_TYPE_HDMI = "hdmi"

    def __init__(self, command, serial_device):
        self.command = command
        self.serial_device = serial_device

    async def _run(self, *args):
        proc = await asyncio.create_subprocess_exec(
            self.command,
            "--dev",
            self.serial_device,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(
                f"returncode {proc.returncode} (args: {args}) (stderr: {stderr})"
            )
        return stdout

    async def on(self):
        await self._run("power", "on")

    async def off(self):
        await self._run("power", "off")

    async def power(self):
        await self._run("power", "toggle")

    async def display(self):
        await self._run("display", "toggle")

    async def picture_on(self):
        await self._run("picture", "on")

    async def picture_off(self):
        await self._run("picture", "off")

    async def picture(self):
        await self._run("picture", "toggle")

    async def volume_up(self):
        await self._run("volume", "up")

    async def volume_down(self):
        await self._run("volume", "down")

    async def mute(self):
        await self._run("mute", "toggle")

    async def brightness_up(self):
        await self._run("brightness", "up")

    async def brightness_down(self):
        await self._run("brightness", "down")

    async def brightness_min(self):
        await self._run("brightness", "min")

    async def brightness_max(self):
        await self._run("brightness", "max")

    async def input_select(self, input_type, input_num):
        await self._run(f"input-{input_type}", f"{input_num}")

    async def status(self):
        return await self._run("status")


class BrightnessController(Controller):
    path = "/brightness"
    tags = ["brightness"]

    @get("/up")
    async def up(self, state: State) -> None:
        await state.lounge_tv.brightness_up()

    @get("/down")
    async def down(self, state: State) -> None:
        await state.lounge_tv.brightness_down()

    @get("/min")
    async def min(self, state: State) -> None:
        await state.lounge_tv.brightness_min()

    @get("/max")
    async def max(self, state: State) -> None:
        await state.lounge_tv.brightness_max()


class DisplayController(Controller):
    path = "/display"
    tags = ["display"]

    @get("/toggle")
    async def toggle(self, state: State) -> None:
        await state.lounge_tv.display()


class PictureController(Controller):
    path = "/picture"
    tags = ["picture"]

    @get("/on")
    async def on(self, state: State) -> None:
        await state.lounge_tv.picture_on()

    @get("/off")
    async def off(self, state: State) -> None:
        await state.lounge_tv.picture_off()

    @get("/toggle")
    async def toggle(self, state: State) -> None:
        await state.lounge_tv.picture()


class PowerController(Controller):
    path = "/power"
    tags = ["power"]

    @get("/on")
    async def on(self, state: State) -> None:
        await state.lounge_tv.on()

    @get("/off")
    async def off(self, state: State) -> None:
        await state.lounge_tv.off()

    @get("/toggle")
    async def toggle(self, state: State) -> None:
        await state.lounge_tv.power()


class VolumeController(Controller):
    path = "/volume"
    tags = ["volume"]

    @get("/up")
    async def up(self, state: State) -> None:
        await state.lounge_tv.volume_up()

    @get("/down")
    async def down(self, state: State) -> None:
        await state.lounge_tv.volume_down()

    @get("/mute/toggle")
    async def mute_toggle(self, state: State) -> None:
        await state.lounge_tv.mute()


class InputSelectController(Controller):
    path = "/input"
    tags = ["input"]

    @get("/hdmi/{port:int}")
    async def hdmi_1(
        self,
        state: State,
        port: Annotated[int, Parameter(ge=1, le=5)],
    ) -> None:
        await state.lounge_tv.input_select(state.lounge_tv.INPUT_TYPE_HDMI, port)


_DEFAULT_COMMAND = "sony-bravia-cli"
_DEFAULT_DEVICE = "/dev/ttyUSB0"


def create_app(lounge_tv_cmd=_DEFAULT_COMMAND, serial_device=_DEFAULT_DEVICE):
    return Litestar(
        logging_config=logging_config,
        route_handlers=[
            BrightnessController,
            DisplayController,
            InputSelectController,
            PictureController,
            PowerController,
            VolumeController,
        ],
        state=State({"lounge_tv": LoungeTV(lounge_tv_cmd, serial_device)}),
    )
