

class IdIsAlreadyAdded(Exception):
    def __str__(self):
        return 'The primary key field "id" is already used as the primary one, do not specify the id as the primary ' \
               'key field'
