
class ConvertTemperature():

    def kelvinToFahrenheit(self, temperture):
        kelvinConvertedFH = 9 / 5 * (temperture - 273.15) + 32
        formattedFH = round(kelvinConvertedFH, 2)
        return formattedFH

    def kelvinToCelsius(self, temperture):
        kelvinConvertedCl = temperture - 273.15
        formattedCl = round(kelvinConvertedCl, 2)
        return formattedCl
