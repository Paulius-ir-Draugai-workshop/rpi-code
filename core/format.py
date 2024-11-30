MSG1_ID = 0b10101010

# Bytes:
#      1   2   2   2   2     1          1
# MSG1_ID | P | R | Y | T | HAT | CHECKSUM |
# DLL adds S and E to msg

# 000001 : 1
# 000010 : 2
# 000011 : 3


def checksum(axes, hat):
    return (sum([v for v in axes.values()]) + hat) % 255


def format_msg1(values):
    axes = format_axes(values)
    hat = format_hat(values["hat"])
    chck = checksum(axes, hat).to_bytes(1, "big")
    pitch_b = axes["pitch"].to_bytes(2, "big")
    roll_b = axes["roll"].to_bytes(2, "big")
    yaw_b = axes["yaw"].to_bytes(2, "big")
    throttle_b = axes["throttle"].to_bytes(2, "big")
    hat_b = hat.to_bytes(1, "big")
    msg_b = [MSG1_ID]
    msg_b.extend(pitch_b)
    msg_b.extend(roll_b)
    msg_b.extend(yaw_b)
    msg_b.extend(throttle_b)
    msg_b.extend(hat_b)
    msg_b.extend(chck)
    return bytearray(msg_b)


def format_axes(axes):
    formatted_axes = {
        "throttle": 1400 - int((axes["throttle"] + 1) * 700),
        "yaw": int(axes["yaw"] * 700) + 700,
        "roll": int(axes["roll"] * 700) + 700,
        "pitch": int(axes["pitch"] * 700) + 700,
    }
    return formatted_axes


def format_hat(hat):
    x, y = hat
    return (y + 1) * 3 + x + 1


if __name__ == "__main__":
    ...
