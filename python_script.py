#!/usr/bin/python

import os

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.module_utils.basic import *


class ActionModule(ActionBase):
    def run(self, task_vars=None):
        '''
        Run a local Python script from within Ansible.

        :param task_vars:
        :return:
        '''

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(task_vars)
        source = self._task.args.get('src')

        if not source:
            raise AnsibleError("You must define a source script.")

        if self._task._role is not None:
            source = self._loader.path_dwim_relative(self._task._role._role_path, 'python_scripts', source)
        else:
            source = self._loader.path_dwim_relative(self._loader.get_basedir(), 'python_scripts', source)

        source = os.path.abspath(source)
        inline = open(source).read()

        temp_vars = task_vars.copy()
        temp_vars['meta_action'] = self
        temp_vars['facts'] = dict()

        exec(inline, temp_vars)  # Don't worry. It's going to be awesome.

        if not isinstance(temp_vars.get('facts'), dict):
            raise AnsibleError("The facts variable must be a dict.")

        result['ansible_facts'] = temp_vars['facts']

        return result







#def main():

#    fields = {
#        "version_no": {"default": True, "type": "str"},
#        "version_name": {"default": True, "type": "str"},
#        "unchanged_value": {"default": True, "type": "str"}
#    }

#    module = AnsibleModule(argument_spec=fields)
    # change the name
#    module.params.update({"version_name": "After"})
#    # bump minor and patch version
#    mylist = module.params["version_no"].split('.')
#    mylist[2] = str(int(mylist[2]) + 2)
#   mylist[1] = str(int(mylist[1]) + 1)
#    mystr= '.'.join(mylist)
#    module.params.update({"version_no": mystr})

    
#    module.exit_json(changed=True, meta=module.params)


#if __name__ == '__main__':
#    main()