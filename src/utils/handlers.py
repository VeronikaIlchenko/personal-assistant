def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"❌ Data error: {e}"
        except KeyError:
            return "❌ Error: Not found."
        except IndexError:
            return "❌ Error: Argument missing."
    return inner