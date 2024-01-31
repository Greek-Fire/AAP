# custom_filters.py
class FilterModule(object):
    def filters(self):
        return {
            'copy_dict': self.copy_dict,
            'copy_list': self.copy_list,
            'generate_survey': self.generate_survey
        }
    def generate_survey(self, item, key):
        return (item, key)
    
    def copy_list(self, item, key):
        """
        Extracts a list of items corresponding to a given key from each dictionary in a list.
        If the input is a string, it returns the string as is.
        Args:
            list_of_dicts: A list of dictionaries or a string.
            key: The key to extract items for.
        Returns:
            A list of extracted items, or the original string if the input is a string.
        """
        # Proceed with the original logic if the input is a list
        if not isinstance(item, dict):
            raise ValueError("Input must be a dictionary !!!")
        
        if not isinstance(key, str):
            raise ValueError("Key must be a string !!!")

        if item.get(key) is None:
            raise ValueError(f'Your value: "{key}" not found in dictionary !!!')       
        
        extracted_items = []
        list_of_dicts = item.get(key)

        for dic in list_of_dicts:

            if dic['name'] and len(dic) == 1:
                continue

            org = dic.get('organization')
            if 'organization' not in dic:
                dic['organization'] = org
                extracted_items.append(dic)
        
        return extracted_items

    def copy_dict(self, dic, key):
        """
        Extracts a list of items corresponding to a given key from each dictionary in a list.
        If the input is a string, it returns the string as is.
        Args:
            list_of_dicts: A list of dictionaries or a string.
            key: The key to extract items for.
        Returns:
            A list of extracted items, or the original string if the input is a string.
        """

        # Proceed with the original logic if the input is a list
    
        extracted_items = []
        org = dic.get('organization')

        if not isinstance(dic, dict):
            raise ValueError("Input must be a dictionary")
        
        if not isinstance(key, str):
            raise ValueError("Key must be a string")        

        if key not in dic:
            raise ValueError(f'Your value: "{key}" not found in dictionary')
        
        keys_list = list(dic[key].keys())

        if 'name' in keys_list and len(keys_list) == 1:
            return extracted_items

        if isinstance(dic[key], dict):
            if 'organization' not in dic[key]:
                dic[key]['organization'] = org
            extracted_items.append(dic[key])
        else:
            raise ValueError(f'Your value: "{key}" is not dictionary')
        
        return extracted_items