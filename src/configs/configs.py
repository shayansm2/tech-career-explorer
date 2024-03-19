import yaml

def get_config(file_name: str, key = None):
    with open(f'src/configs/{file_name}.yml', 'r') as file:
        configs = yaml.safe_load(file)
    
    if key is None:
        return configs
    
    keys = key.split('.')
    for k in keys:
        configs = configs.get(k)
        if configs is None:
            return None
    return configs