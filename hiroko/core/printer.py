class ConsolePrinter:
    instance = None

    @staticmethod
    def getInstance():
        if not ConsolePrinter.instance:
            ConsolePrinter.instance = ConsolePrinter()
        return ConsolePrinter.instance
