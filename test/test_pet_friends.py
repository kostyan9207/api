from api import PetFriends
from settings import valid_email, valid_password, incorrect_email, incorrect_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_information_about_new_pet_with_valid_data(name='Frank', animal_type='corgi', age='3',
                                                       pet_photo='images/dog.jpeg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet_from_database_with_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_information_about_new_pet(auth_key, 'Тестовый', 'котейка', '10', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Steve', animal_type='Doge', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name,
                                                         animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='Jerax', animal_type='corgi', age='8'):
    """Проверяем, что можно добавить питомца с корректными данными, но без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_successful_adding_pet_photo_to_pet_card_without_photo(pet_photo='images/dog.jpeg'):
    """Проверяем возможность добавить фотографию к существующему питомцу без фотографии"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0 or 'pet_photo' in my_pets['pets'][0]:
        pf.add_information_about_new_pet_without_photo(auth_key, 'Тестовый', 'Собакен', '3')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert 'pet_photo' in my_pets['pets'][0]


def test_add_new_pet_simple_with_incorrect_auth_key(name='Jerax', animal_type='corgi', age='8'):
    """Рассматриваем возможность добавления питомца с некорректным API ключом. Ожидаем, что сервер не пропустит
    данную операцию"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = auth_key['key'] + '8(800)555-35-35'
    status, _ = pf.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 403


def test_get_api_key_with_incorrect_email(email=valid_email, password=valid_password):
    """Пытаемся получить API ключ, используя некорректный Email """
    email = incorrect_email
    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_get_list_of_pets_with_nonexistent_filter(filter='all_pets'):
    """Проверяем возможность запросить список животных с несуществующим фильтром 'all_pets' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


def test_add_new_pet_without_name(name='', animal_type='corgi', age='3',
                                                       pet_photo='images/dog.jpeg'):
    """Проверяем возможность добавления нового питомца без указания имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo_in_gif_format(pet_photo='images/anim_dog.gif'):
    """Проверяем возможность добавления питоца с анимацией в формате gif, вместо фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0 or 'pet_photo' in my_pets['pets'][0]:
        pf.add_information_about_new_pet_without_photo(auth_key, 'Тестовый', 'Собакен', '3')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 500


def test_delete_pet_from_database_with_incorrect_pet_id():
    """Проверка возможности удаления карты питомца с несуществующим ID питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_information_about_new_pet(auth_key, 'Тестовый', 'котейка', '10', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    quantity_before = len(my_pets['pets'])
    my_pets['pets'][0]['id'] = my_pets['pets'][0]['id'] + '8-800-555-35-35'
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    quantity_after = len(my_pets['pets'])

    assert status == 200
    assert quantity_before == quantity_after


def test_delete_pet_from_database_with_incorrect_auth_key():
    """Проверка возможности удаления карты питомца с некорректным API ключом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_information_about_new_pet(auth_key, 'Тестовый', 'котейка', '10', 'images/cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    auth_key['key'] = auth_key['key'] + '8(800)555-35-35'
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    assert status == 403


def test_get_api_key_with_incorrect_password(email=valid_email, password=valid_password):
    """Пытаемся получить API ключ, используя некорректный пароль"""
    password = incorrect_password
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_update_self_pet_info_with_incorrect_auth_key(name='Steve', animal_type='Doge', age='5'):
    """Проверяем возможность изменить информацию о питомце используя некорректный API ключ"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        auth_key['key'] = auth_key['key'] + '8(800)555-35-35'
        status, _ = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 403
    else:
        raise Exception("There is no my pets")