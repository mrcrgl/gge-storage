

def load_class(class_path):
    path, class_name = class_path.rsplit('.', 1)

    module = __import__(path, fromlist=[str(class_name)])
    return getattr(module, class_name)