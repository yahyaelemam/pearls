from pearls.utilities import get_data, date_format, insert_data


def sp_country_name(city_id):
    sql_str = """
        Select country from crm_countries 
        where country_id in(Select country_id From crm_states 
                where state_id in(Select state_id from crm_cities where city_id = """ + str(city_id) + """) )
    """
    county_name = get_data(sql_str)
    return county_name[0][0]
