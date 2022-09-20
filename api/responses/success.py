from fastapi.responses import JSONResponse

PASSWORD_CHANGED = JSONResponse(content='Password successfull changed.')

EMAIL_PASS_RESTORE_SENT = JSONResponse(content='Password restore email sent.')


def email_invite_send(organization_id: int):
    return JSONResponse(content=f'Invite has been sent for organization with id={organization_id}')


USER_ROLE_UNASSIGNED = JSONResponse(content='User role succesfull unussigned.')

DELETED_SUCCESSFULLY = JSONResponse(content='Deleted successfully')

DELETED_NOT_SUCCESSFULLY = JSONResponse(content='Deleted not successfully')

ARCHIVED_SUCCESSFULLY = JSONResponse(content='Archived successfully')

UNARCHIVED_SUCCESSFULLY = JSONResponse(content='Unarchived successfully')

TASK_CREATED_FOR_WORKER = JSONResponse(content='Task created for worker')
