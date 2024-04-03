if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def check_condition(*args, **kwargs) -> bool:
    if 'keyword' not in kwargs.keys() or kwargs['keyword'] is None:
        print('you should provide the keyword')
        return False
    
    if 'location' not in kwargs.keys() or kwargs['location'] is None:
        print('you should provide the location')
        return False

    return True