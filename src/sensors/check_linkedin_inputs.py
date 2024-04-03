if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def check_condition(*args, **kwargs) -> bool:
    if 'keyword' not in kwargs.keys() or kwargs['keyword'] is None:
        print('you should provide the keyword')
        return False
    
    if 'geo_id' not in kwargs.keys() or kwargs['geo_id'] is None:
        print('you should provide the geo_id')
        return False

    return True