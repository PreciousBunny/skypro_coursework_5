class JobParserMeta(type):
    """
    Метакласс для приложения по поиску работы (для класса JobParser).
    """

    def __call__(cls, *args, **kwargs):
        """
        Создает экземпляр класса, и инициирует "общение" с пользователем.
        """
        sample = super().__call__(*args, **kwargs)
        sample._user_interaction()
        return sample
