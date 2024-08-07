import copy
import re
from pysubs2 import SSAFile, SSAStyle, SSAEvent


def info_select_current_info(ssafile: SSAFile, **kwargs) -> list:
    return [ssafile.info]


def info_action_save(ssafile: SSAFile, info: dict, **kwargs) -> dict:
    return copy.copy(info)


def info_action_update(ssafile: SSAFile, info: dict, **kwargs):
    info.update(kwargs)

    return info


def styles_select_all(ssafile: SSAFile, **kwargs):
    return [ssafile.styles[k] for k in ssafile.styles]


def styles_select_top(ssafile: SSAFile, **kwargs):

    counts = {}
    for event in ssafile.events:

        if event.style in counts:
            counts[event.style] += 1
        else:
            counts[event.style] = 1

    value = max(counts.values())
    key = next(k for k, v in counts.items() if v == value)

    return [ssafile.styles.get(key)]


def styles_action_scale_margins(ssafile: SSAFile, style: SSAStyle, **kwargs):

    y_ratio = float(kwargs["y_new"]) / float(kwargs["y_old"])
    x_ratio = float(kwargs["x_new"]) / float(kwargs["x_old"])

    style.fontsize = round(style.fontsize * y_ratio)
    style.marginv = round(style.marginv * y_ratio)
    style.marginl = round(style.marginl * x_ratio)
    style.marginr = round(style.marginr * x_ratio)

    return style


def styles_action_scale(ssafile: SSAFile, style: SSAStyle, **kwargs):
    return styles_action_scale_margins(ssafile, style, **kwargs)


def events_action_scale_position(ssafile: SSAFile, event: SSAEvent, **kwargs):

    y_ratio = float(kwargs["y_new"]) / float(kwargs["y_old"])
    x_ratio = float(kwargs["x_new"]) / float(kwargs["x_old"])

    m: re.Match
    for m in re.finditer(r"\\pos\(([0-9\.]+),([0-9\.]+)\)", str(event.text)):
        x_pos = float(m.group(1)) * x_ratio
        y_pos = float(m.group(2)) * y_ratio

        new_pos = f"\\pos({x_pos:.1f},{y_pos:.1f})"
        event.text = event.text.replace(str(m.group(0)), new_pos)

    return event


def events_action_scale_margins(ssafile: SSAFile, event: SSAEvent, **kwargs):

    y_ratio = float(kwargs["y_new"]) / float(kwargs["y_old"])
    x_ratio = float(kwargs["x_new"]) / float(kwargs["x_old"])

    event.marginv = round(event.marginv * y_ratio)
    event.marginl = round(event.marginl * x_ratio)
    event.marginr = round(event.marginr * x_ratio)

    return event


def events_action_scale(ssafile: SSAFile, event: SSAEvent, **kwargs):
    events_action_scale_margins(ssafile, event, **kwargs)
    events_action_scale_position(ssafile, event, **kwargs)
    return event


def styles_action_update_properties(ssafile: SSAFile, style: SSAStyle, **kwargs):
    style.__dict__.update(kwargs)

    return style


def styles_remove(ssafile: SSAFile, style: SSAStyle, **kwargs):
    for key in ssafile.styles.keys():
        if ssafile.styles[key] is style:
            del ssafile.styles[key]

    return style


def events_select_all(ssafile: SSAFile, **kwargs):
    return ssafile.events


def events_filter_regex(ssafile: SSAFile, event: SSAEvent, regex="", **kwargs):
    return bool(re.match(regex, event.text))


def events_filter_properties(ssafile: SSAFile, event: SSAEvent, **kwargs):

    fil = True

    if "is_comment" in kwargs:
        fil = fil and event.is_comment == kwargs["is_comment"]

    if "is_drawing" in kwargs:
        fil = fil and event.is_drawing == kwargs["is_drawing"]

    return fil


def events_action_regex_substitution(
    ssafile: SSAFile, event: SSAEvent, regex="", replace=""
):
    event.text = re.sub(regex, replace, event.text)

    return event


def events_action_delete(ssafile: SSAFile, event: SSAEvent, **kwargs):
    ssafile.events.remove(event)
    return event


def events_action_update_properties(ssafile: SSAFile, event: SSAEvent, **kwargs):
    event.__dict__.update(kwargs)
    return event


def events_misc_remove_miscellaneous_events(ssafile: SSAFile, **kwargs):
    ssafile.remove_miscellaneous_events()
