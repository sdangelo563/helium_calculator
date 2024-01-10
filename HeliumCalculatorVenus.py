M_CO2 = 43.7
M_He = 4.003

def findAtmDens (altitude):
#http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?bibcode=1988EM%26P...42...29P&db_key=AST&page_ind=5&plate_select=NO&data_type=GIF&type=SCREEN_GIF&classic=YES
    alt40 = 3.96 #kg/m^3
    alt45 = 2.46
    alt50 = 1.46
    alt55 = .868
    alt60 = .381
    
    if altitude >= 40 and altitude <= 45:
        return (altitude - 40)/5*alt45 + (45 - altitude)/5*alt40
    elif altitude >= 45 and altitude <= 50:
        return (altitude - 45)/5*alt50 + (50 - altitude)/5*alt45
    elif altitude >= 50 and altitude <= 55:
        return (altitude - 50)/5*alt55 + (55 - altitude)/5*alt50
    elif altitude >= 55 and altitude <= 60:
        return (altitude - 55)/5*alt60 + (60 - altitude)/5*alt55
    elif altitude > 60:
        return 0

def findAtmPress (altitude):
    alt40 = 318 #kPa
    alt45 = 179
    alt50 = 94.7
    alt55 = 44.6
    alt60 = 18.7
    
    if altitude >= 40 and altitude <= 45:
        return (altitude - 40)/5*alt45 + (45 - altitude)/5*alt40
    elif altitude >= 45 and altitude <= 50:
        return (altitude - 45)/5*alt50 + (50 - altitude)/5*alt45
    elif altitude >= 50 and altitude <= 55:
        return (altitude - 50)/5*alt55 + (55 - altitude)/5*alt50
    elif altitude >= 55 and altitude <= 60:
        return (altitude - 55)/5*alt60 + (60 - altitude)/5*alt55
    elif altitude > 60:
        return 0

def findDensAltitude (atmDens):
#http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?bibcode=1988EM%26P...42...29P&db_key=AST&page_ind=5&plate_select=NO&data_type=GIF&type=SCREEN_GIF&classic=YES
    alt40 = 3.96 #kg/m^3
    alt45 = 2.46
    alt50 = 1.46
    alt55 = .868
    alt60 = .381
    
    if atmDens >= alt60 and atmDens <= alt55:
        delta = alt55-alt60
        return (alt55 - atmDens)/delta * 60 + (atmDens - alt60)/delta * 55
    elif atmDens >= alt55 and atmDens <= alt50:
        delta = alt50-alt55
        return (alt50 - atmDens)/delta * 55 + (atmDens - alt55)/delta * 50
    elif atmDens >= alt50 and atmDens <= alt45:
        delta = alt45-alt50
        return (alt45 - atmDens)/delta * 50 + (atmDens - alt50)/delta * 45
    elif atmDens >= alt45 and atmDens <= alt40:
        delta = alt40-alt45
        return (alt40 - atmDens)/delta * 45 + (atmDens - alt45)/delta * 40
    else:
        return 0

def findGaugePress (helium, volume, atmPress, atmDens):
    R_universal = 8314.472
    #pv=nRT
    #n = mass/M
    #T = pv/nr
    temp = atmPress / ((atmDens/ M_CO2) * R_universal)
    print("temp = ", temp)
    #P = nRT/V
    HePress = (helium/M_He * R_universal * temp)/volume
    return HePress - atmPress

#atmDens = (helium + mass) / volume

def findVolume (helium, mass, altitude):
    atmDens = findAtmDens(altitude)
    atmPress = findAtmPress(altitude)
    volume = (helium + mass) / atmDens
    gage = findGaugePress(helium, volume, atmPress, atmDens)
    print("Pressure difference = ", gage)
    if gage < 0:
        return "Balloon will implode"
    else:
        return volume

def findHelium (mass, volume, altitude):
    atmDens = findAtmDens(altitude)
    atmPress = findAtmPress(altitude)
    helium = (atmDens * volume) - mass
    gage = findGaugePress(helium, volume, atmPress, atmDens)
    print("Pressure difference = ", gage)
    if gage < 0:
        return "Balloon will implode"
    else:
        return helium   

def findAltitude (helium, mass, volume):
    atmDens = (helium+mass) / volume
    altitude = findDensAltitude(atmDens)
    atmPress = findAtmPress(altitude)
    gage = findGaugePress(helium, volume, atmPress, atmDens)
    print("Pressure difference = ", gage)
    if gage < 0:
        return "Balloon will implode"
    else:
        return altitude 
    
def findMass (helium, volume, altitude):
    atmDens = findAtmDens(altitude)
    atmPress = findAtmPress(altitude)
    mass = (atmDens * volume) - helium
    gage = findGaugePress(helium, volume, atmPress, atmDens)
    print("Pressure difference = ", gage)
    if gage < 0:
        return "Balloon will implode"
    else:
        return mass

def findOptimal(mass,altitude):
    helium = mass / ((M_CO2/M_He) - 1)
    volume = findVolume(helium,mass,altitude)
    return [helium, volume]
