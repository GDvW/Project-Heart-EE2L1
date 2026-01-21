from lib.localization.LocalizationPlot import LocalizationPlot
from lib.TUI.CommandProcessor import CommandProcessor

def generateLocalizationCommands(plot: LocalizationPlot) -> CommandProcessor:
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    cp = CommandProcessor()
    
    cp.register_command("print", plot.print, helpmsg="Print the set values")
    
    # Add refresh handlers for graph
    cp.register_action_after_symbolic(plot.plot_update)
    
    # Create the general settings
    general_group = cp.register_symbolic_group("Params", "Contains params for the localization algorithm")
    cp.register_symbolic_spec("P", general_group, lambda: plot.params, "Params settings")
    
    cp.register_symbolic_prop("bin",        general_group, lambda obj: obj.bin,        lambda obj, val: setattr(obj, "bin", val),        dtype=int,  helpmsg="Which frequency bin to use, influences center frequency")
    cp.register_symbolic_prop("z",          general_group, lambda obj: obj.z,          lambda obj, val: setattr(obj, "z", val),          dtype=float,helpmsg="The expected z-coordinate of the sound source")
    cp.register_symbolic_prop("Q",          general_group, lambda obj: obj.Q,          lambda obj, val: setattr(obj, "Q", val),          dtype=int,  helpmsg="The amount of sources")
    cp.register_symbolic_prop("M",          general_group, lambda obj: obj.M,          lambda obj, val: setattr(obj, "M", val),          dtype=int,  helpmsg="The amount of microphones")
    cp.register_symbolic_prop("v_sound",    general_group, lambda obj: obj.v_sound,    lambda obj, val: setattr(obj, "v_sound", val),    dtype=float,helpmsg="The speed of the sound")
    cp.register_symbolic_prop("resolution", general_group, lambda obj: obj.resolution, lambda obj, val: setattr(obj, "resolution", val), dtype=float,helpmsg="The difference between the scan points")
    cp.register_symbolic_prop("mode",       general_group, lambda obj: obj.mode,       lambda obj, val: setattr(obj, "mode", val),       dtype=str,  helpmsg="Either `music` or `mvdr`")
    return cp