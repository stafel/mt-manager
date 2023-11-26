#!/usr/bin/python

__doc__ = """Enables or disables a minetest mod"""


def load_world_config(world_mt_path: str):
    """Parses dict from world.mt file"""

    data = {}
    with open(world_mt_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            k, v = line.split("=", 2)
            k = k.strip()
            v = v.strip()
            data[k] = v
    return data


def save_world_config(world_mt_path: str, config):
    """Saves dict into world.mt file"""

    with open(world_mt_path, "w", encoding="utf-8") as f:
        for k, v in config.items():
            f.write(f"{k} = {v}\n")


def disable_mod(config, mod_name: str):
    """Disables mod loading by setting world.mt line to false"""

    config["load_mod_" + mod_name] = "false"


if __name__ == "__main__":
    test_path = "test/world.mt"

    config = load_world_config(world_mt_path=test_path)

    disable_mod(
        config,
        "armor_wood",
    )

    assert config["load_mod_armor_wood"] == "false"

    # save_world_config(world_mt_path=world_mt_path, config=config)
