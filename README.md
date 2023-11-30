# mt-manager

Ansible module to manage a minetest server remotely


To use directly:

```bash
ANSIBLE_LIBRARY=./library ansible -m setmod -a 'savepath=/wherever/.minetest/worlds/world modname=petz modpath=false' localhost
```