"""
Lazy Assistant - Deferred loading of assistant modules
"""

class LazyAssistant:
    """
    Lazy loading wrapper for assistants to improve startup time
    and reduce memory usage for unused assistants
    """
    def __init__(self, module_name, assistant_name):
        self.module_name = module_name
        self.assistant_name = assistant_name
        self._instance = None
        self.__name__ = f"lazy_{assistant_name}"
    
    def __call__(self, *args, **kwargs):
        if self._instance is None:
            try:
                module = __import__(self.module_name, fromlist=[self.assistant_name])
                self._instance = getattr(module, self.assistant_name)
                print(f"Lazy loaded: {self.assistant_name} from {self.module_name}")
            except Exception as e:
                print(f"Error lazy loading {self.assistant_name}: {str(e)}")
                # Return a simple function that explains the error
                def error_assistant(prompt):
                    return f"Sorry, I couldn't load the {self.assistant_name}. Please try again later."
                return error_assistant(*args, **kwargs)
        
        return self._instance(*args, **kwargs)