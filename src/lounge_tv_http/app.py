import asyncio

from litestar import Controller, Litestar, get
from litestar.datastructures import State


class LoungeTV:
    def __init__(self, command, serial_device):
        self.command = command
        self.serial_device = serial_device

    async def _run(self, *args):
        proc = await asyncio.create_subprocess_exec(
            self.command,
            self.serial_device,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(
                f'returncode {proc.returncode} '
                f'(args: {args}) '
                f'(stderr: {stderr})')
        return stdout

    async def on(self):
        await self._run('on')

    async def off(self):
        await self._run('off')

    async def power(self):
        await self._run('power')

    async def volume_up(self):
        await self._run('volume-up')

    async def volume_down(self):
        await self._run('volume-down')

    async def mute(self):
        await self._run('mute')

    async def brightness_up(self):
        await self._run('brightness-up')

    async def brightness_down(self):
        await self._run('brightness-down')

    async def status(self):
        return await self._run('status')


class BrightnessController(Controller):
    path = '/brightness'

    @get('/up')
    async def up(self, state: State) -> None:
        await state.lounge_tv.brightness_up()

    @get('/down')
    async def down(self, state: State) -> None:
        await state.lounge_tv.brightness_down()


class PowerController(Controller):
    path = '/power'

    @get('/on')
    async def on(self, state: State) -> None:
        await state.lounge_tv.on()

    @get('/off')
    async def off(self, state: State) -> None:
        await state.lounge_tv.off()

    @get('/toggle')
    async def toggle(self, state: State) -> None:
        await state.lounge_tv.power()


class VolumeController(Controller):
    path = '/volume'

    @get('/up')
    async def up(self, state: State) -> None:
        await state.lounge_tv.volume_up()

    @get('/down')
    async def down(self, state: State) -> None:
        await state.lounge_tv.volume_down()

    @get('/mute/toggle')
    async def mute_toggle(self, state: State) -> None:
        await state.lounge_tv.mute()


_DEFAULT_COMMAND = 'sony-bravia-cli'
_DEFAULT_DEVICE = '/dev/ttyUSB0'


def create_app(lounge_tv_cmd=_DEFAULT_COMMAND,
               serial_device=_DEFAULT_DEVICE):
    return Litestar(
        route_handlers=[
            BrightnessController,
            PowerController,
            VolumeController,
        ],
        state=State({'lounge_tv': LoungeTV(lounge_tv_cmd, serial_device)}),
    )
