#!/usr/bin/python

DOCUMENTATION = r"""
---
module: mt_manager

short_description: Manage minetest mod settings

version_added: "0.0.1"

description: Manage minetest mod settings.

options:
    savepath:
        description: Path to the save folder of the world.
        required: true
        type: str
    modname:
        description: Name of the mod to be modified.
        required: true
        type: str
    modpath:
        description: 
            - Relative path to the mods folder.
            - 'false' to disable.
        required: true
        type: str

author:
    - stafel
"""

EXAMPLES = r"""
TODO
"""

RETURN = r"""
TODO
"""

import os.path
from ansible.module_utils.basic import AnsibleModule


def _load_world_config(world_mt_path: str):
    """Parses dict from world.mt file"""

    data = {}
    with open(world_mt_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            k, v = line.split("=", 2)
            k = k.strip()
            v = v.strip()
            data[k] = v
    return data


def _save_world_config(world_mt_path: str, config):
    """Saves dict into world.mt file"""

    with open(world_mt_path, "w", encoding="utf-8") as f:
        for k, v in config.items():
            f.write(f"{k} = {v}\n")


def _construct_full_mod_id(mod_name: str):
    """Returns full mod id out of name"""

    return f"load_mod_{mod_name}"


def _get_mod_path(config, mod_name: str):
    """Returns current set mod path"""

    return config.get(_construct_full_mod_id(mod_name=mod_name))


def _set_mod_path(config, mod_name: str, mod_path: str):
    """Sets mod path"""

    config[_construct_full_mod_id(mod_name=mod_name)] = mod_path


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        savepath=dict(type="str", required=True),
        modname=dict(type="str", required=True),
        modpath=dict(type="str", required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, original_modpath="false")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    config = None
    worldmt_path = os.path.join(module.params["savepath"], "world.mt")
    modname = module.params["modname"]
    modpath = module.params["modpath"]
    try:
        config = _load_world_config(worldmt_path)
    except Exception as ex:
        module.fail_json(msg="Can't open savepath", err=str(ex), **result)

    old_state = _get_mod_path(config=config, mod_name=modname)
    result["original_modpath"] = old_state

    if (
        (old_state == None or old_state == "false") and modpath == "false"
    ) or old_state == modpath:
        result["changed"] = False
    else:
        _set_mod_path(
            config=config,
            mod_name=modname,
            mod_path=modpath,
        )
        try:
            _save_world_config(worldmt_path, config=config)
        except Exception as ex:
            module.fail_json(msg="Can't save world.mt file", err=str(ex), **result)
        result["changed"] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
