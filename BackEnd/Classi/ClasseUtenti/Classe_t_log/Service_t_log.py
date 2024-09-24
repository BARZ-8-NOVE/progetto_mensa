from Classi.ClasseUtenti.Classe_t_log.Repository_t_log import Repository_t_log

class Service_t_Log:
    def __init__(self) -> None:
        self.repository = Repository_t_log()

    def log_to_db(self, level, message, user_id=None, route=None, data=None):
        return self.repository.log_to_db(level, message, user_id, route, data)