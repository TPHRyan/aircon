import ir.decoder
from device import acquire_device
from lg.packet import LGCommandPacket, ModeCommandPacket, OffCommandPacket
from lg.packet.mode import ModeValue, SpeedValue

INTERACTIVE_MODES = {
    "off": lambda: OffCommandPacket(),
    "on": lambda: run_interactive_mode("on"),
    "auto": lambda: run_interactive_mode("auto"),
    "cool": lambda: run_interactive_mode("cool"),
    "dehumidify": lambda: run_interactive_mode("dehumidify"),
    "heat": lambda: run_interactive_mode("heat"),
}

MODE_VALUES = {
    "on": ModeValue.ON,
    "auto": ModeValue.AUTO,
    "cool": ModeValue.COOL,
    "dehumidify": ModeValue.DEHUMIDIFY,
    "heat": ModeValue.HEAT,
}

SPEED_VALUES = {
    "chaos": SpeedValue.CHAOS,
    "low": SpeedValue.LOW,
    "med": SpeedValue.MED,
    "high": SpeedValue.HIGH,
}


def run_interactive():
    acquire_device().send_data(
        ir.decoder.ir_to_broadlink_full_packet(signals_in=prompt_mode().encode_ir)
    )


def prompt_mode() -> LGCommandPacket:
    return INTERACTIVE_MODES[prompt_for_mode_choice()]()


def prompt_for_mode_choice() -> str:
    mode_in = input("What mode to select? ")
    if mode_in not in INTERACTIVE_MODES:
        raise ValueError(f'Allowed options: ({", ".join(MODE_VALUES.keys())})')
    return mode_in


def run_interactive_mode(selected_mode: str) -> LGCommandPacket:
    command: ModeCommandPacket = ModeCommandPacket()
    command.mode = get_mode_value_for_selection(selected_mode)
    command.speed = get_speed_for_mode(command.mode)
    command.temperature = prompt_for_temperature()
    return command


def get_mode_value_for_selection(mode: str) -> ModeValue:
    return MODE_VALUES[mode]


def get_speed_for_mode(mode: ModeValue) -> SpeedValue:
    if mode == ModeValue.DEHUMIDIFY:
        return SpeedValue.DEHUM
    return prompt_for_speed()


def prompt_for_speed() -> SpeedValue:
    try:
        return SPEED_VALUES[input("What speed to select? ")]
    except KeyError:
        raise ValueError(f'Allowed options: ({", ".join(SPEED_VALUES.keys())})')


def prompt_for_temperature() -> int:
    try:
        return clamp_temperature(int(input("What temperature to select? ")))
    except ValueError:
        raise ValueError("Please enter a number (between 16 and 30)!")


def clamp_temperature(temperature: int) -> int:
    return clamp_temperature_lower_bound(clamp_temperature_upper_bound(temperature))


def clamp_temperature_lower_bound(temperature: int) -> int:
    if temperature < 16:
        return 16
    return temperature


def clamp_temperature_upper_bound(temperature: int) -> int:
    if temperature > 30:
        return 30
    return temperature
