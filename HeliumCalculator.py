M_Air = 28.97
M_He = 4.003

def findAtmDens (altitude):
    alt_array = [1.225,0.4135,0.08891,0.01841,0.003996,0.001027,0.0003097,0.00008283,0.00001846]
    ind = int(altitude / 10)
    remainder = altitude % 10
    return (remainder/10.0) * alt_array[ind+1] +\
           ((5 - remainder)/10.0) * alt_array[ind]

def findAtmPress (altitude):
    alt_array = [101.3,26.5,5.529,1.197,0.287,0.07988,0.02196,0.0052,0.0011]
    ind = int(altitude / 10)
    remainder = altitude % 10
    return (remainder/10.0) * alt_array[ind+1] +\
           ((10.0 - remainder)/10.0) * alt_array[ind]

def findDensAltitude(atmDens):
    alt_array = [1.225,0.4135,0.08891,0.01841,0.003996,0.001027,0.0003097,0.00008283,0.00001846]
    ind = 0
    for i in range(0,len(alt_array)):
        ind = i
        if atmDens >= alt_array[i]:
            break
    delta = alt_array[ind - 1]-alt_array[ind]
    return (alt_array[ind-1] - atmDens)/delta * ind * 10 + \
           (atmDens - alt_array[ind])/delta * (ind - 1) * 10

def findGaugePress (helium, volume, atmPress, atmDens):
    R_universal = 8314.472
    #pv=nRT
    #n = mass/M
    #T = pv/nr
    temp = atmPress / ((atmDens/ M_Air) * R_universal)
    print("temp = ", temp)
    #P = nRT/V
    HePress = (helium/M_He * R_universal * temp)/volume
    return HePress - atmPress

#atmDens = (helium + mass) / volume

def findVolume (helium, mass, altitude):
    atmDens = findAtmDens(altitude)
    atmPress = findAtmDens(altitude)
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
    print("atmDens", atmDens)
    altitude = findDensAltitude(atmDens)
    print("altitude", altitude)
    atmPress = findAtmPress(altitude)
    print("atmPress", atmPress)
    gage = findGaugePress(helium, volume, atmPress, atmDens)
    print("Pressure difference = ", gage)
    if gage < 0:
        print("Balloon will implode")
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
    helium = mass / ((M_Air/M_He) - 1)
    volume = findVolume(helium, mass, altitude)
    return [helium, volume]

def findFloatAlt(mass, volume):
    helium = mass / ((M_Air/M_He) - 1)
    print("helium", helium)
    altitude = findAltitude(helium, mass, volume)
    print("altitude", altitude)
    return [helium, altitude]

def findPopAlt(mass,volume,ascent_rate):
    radius = (volume / (4/3.0 * 3.14))**(1/3)
    proj_area = radius**2 * 3.14
    Cd = 0.3 #we'll see
    #Fnet = 0 = V*rho_he*g + .5*rho_air*v^2*Cd*A - V*rho_air*g
    #.5*rho_air*v^2*Cd*A = V*rho_air*g - V*rho_he*g
    #.5*rho_air*v^2*Cd*A = V*g*(rho_air - rho_he)
    #.5*rho_air*v^2*Cd*A/(V*g) = rho_air - rho_he
    #rho_air(1-.5*v^2*Cd*A/(V*g)) = rho_he
    #m_he = (rho_air - rho_air*0.5*v^2*Cd*A/(V*g)) * V
    #m_he = rho_air * V - rho_air*.5*v^2*Cd*A/g
    altitude = 50.0
    alt_diff = 50.0
    while alt_diff > .01:
        helium = findAtmDens(altitude) * (volume - 0.5 * ascent_rate**2 * Cd * proj_area / 9.81 )
        print("helium", helium)
        print("helium in cubic meters", helium / (1.225*(4.003/28.97)))
        old_alt = altitude
        print("old_alt", old_alt)
        altitude = float(findAltitude(helium, mass, volume))
        alt_diff = abs(old_alt - altitude)
        print("altitude",altitude)
    return[helium, altitude]
