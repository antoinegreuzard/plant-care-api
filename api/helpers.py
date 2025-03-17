def get_personalized_advice(plant):
    """ Génère des conseils en fonction des conditions saisies. """
    advice = []

    # Conseil basé sur l'ensoleillement
    if plant.sunlight_level == 'low':
        advice.append(
            "Placez votre plante à l'ombre ou dans un endroit peu lumineux.")
    elif plant.sunlight_level == 'medium':
        advice.append(
            "Votre plante a besoin de lumière indirecte, évitez le soleil.")
    elif plant.sunlight_level == 'high':
        advice.append(
            "Assurez-vous que votre plante reçoit beaucoup de lumière.")

    # Conseil basé sur la température
    if plant.temperature:
        if plant.temperature < 15:
            advice.append(
                "Protégez votre plante du froid.")
        elif plant.temperature > 30:
            advice.append(
                "Évitez l'exposition à des températures élevées et arrosez.")

    # Conseil basé sur l'humidité
    if plant.humidity_level == 'low':
        advice.append(
            "Pulvérisez régulièrement de l'eau sur les feuilles.")
    elif plant.humidity_level == 'medium':
        advice.append(
            "L'humidité est correcte, surveillez les signes de sécheresse.")
    elif plant.humidity_level == 'high':
        advice.append(
            "Assurez une bonne ventilation pour éviter les moisissures.")

    return advice
