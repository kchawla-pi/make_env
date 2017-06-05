import collections
import toolkit


class HandleError(object):
    
    def __init__(self, err_entity, fn=None, fn_args=None, frontend=False,
        raise_excep=True, retry=True):
        
        self.fn = fn
        self.err_entity = err_entity
        self.fn_args = fn_args
        self.frontend = frontend
        self.raise_excep = raise_excep
        self.excep_log = {}
        self.CorrectionArgs = collections.namedtuple('CorrectionArgs', 'excep print_msg user_fix_msg'
                                                                  ' retry correction_fns')
        
    def handle(self, excep, print_msg, user_fix_msg_, retry=False, correction_fn=[]):
        fn_return = []
        if self.frontend:
            print(*print_msg)
        if retry == 'user':
                user_fix_msgs = {'path': "Enter the complete path: ",
                                'arg': "Enter the correct arguments: "
                                }
                user_fix_msgs.setdefault(user_fix_msg_, user_fix_msgs)
                user_provided = input(user_fix_msgs[user_fix_msg_])
        elif retry == 'fn':
                correction_fn.append({'fn': self.fn, 'args': self.fn_args})
                for fn in correction_fn:
                    fn_return.append(fn['fn'](*fn['args']))
        else:
            raise excep
        return fn_return
    
    def file_not_found(self, excep, custom_msg=''):
        self.excep_log.setdefault('FileNotFoundError', [])
        self.excep_log['FileNotFoundError'].append(excep, self.err_entity)
        frontend_msg = "Could not find {}.".format(self.err_entity)
        print_msg = (excep, '\n', frontend_msg, '\n', custom_msg)
        file_not_found_corr_args = self.CorrectionArgs(excep=excep, print_msg=print_msg, user_fix_msg_='path',
                                                       retry='user', correction_fns=[])
        return file_not_found_corr_args
        
    def permission_error(self, excep, custom_msg='', change_permission_args='0o777'):
        self.excep_log.setdefault('PermissionError', [])
        self.excep_log['PermissionError'].append(excep, self.err_entity)
        frontend_msg = "ERROR: You do not have the necessary permissions to perform this action" \
                       "for {}.".format(self.err_entity)
        print_msg = (excep, '\n', frontend_msg, '\n', custom_msg)
        perm_args = (self.err_entity, change_permission_args)
        correction_fn =[{'fn': toolkit.change_permissions, 'args': *perm_args}]
        perm_err_corr_args = self.CorrectionArgs(excep=excep, print_msg=print_msg,
                                                 correction_fns=correction_fn )
        return perm_err_corr_args

        handled_returned = self.handle(self, excep=excep, print_msg=print_msg,
                                       user_fix_msg_=user_fix_msg)

