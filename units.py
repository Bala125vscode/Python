# Comprehensive mapping of siunitx units to standard LaTeX
# Includes SI base units, derived units, abbreviations, and binary units.
# Based on siunitx v3.4.14 documentation.

UNIT_MAP = {
    # Base Units
    r'\meter': r'\mathrm{m}', r'\metre': r'\mathrm{m}', r'\m': r'\mathrm{m}',
    r'\kilogram': r'\mathrm{kg}', r'\kg': r'\mathrm{kg}', r'\gram': r'\mathrm{g}',
    r'\second': r'\mathrm{s}', r'\s': r'\mathrm{s}',
    r'\ampere': r'\mathrm{A}', r'\A': r'\mathrm{A}',
    r'\kelvin': r'\mathrm{K}', r'\K': r'\mathrm{K}',
    r'\mole': r'\mathrm{mol}', r'\mol': r'\mathrm{mol}',
    r'\candela': r'\mathrm{cd}', r'\cd': r'\mathrm{cd}',

    # Derived Units with Special Names
    r'\becquerel': r'\mathrm{Bq}',
    r'\degreeCelsius': r'^\circ\mathrm{C}', r'\celsius': r'^\circ\mathrm{C}',
    r'\coulomb': r'\mathrm{C}', r'\C': r'\mathrm{C}',
    r'\farad': r'\mathrm{F}', r'\F': r'\mathrm{F}',
    r'\gray': r'\mathrm{Gy}',
    r'\hertz': r'\mathrm{Hz}', r'\Hz': r'\mathrm{Hz}',
    r'\henry': r'\mathrm{H}', r'\H': r'\mathrm{H}',
    r'\joule': r'\mathrm{J}', r'\J': r'\mathrm{J}',
    r'\lumen': r'\mathrm{lm}', r'\lm': r'\mathrm{lm}',
    r'\katal': r'\mathrm{kat}',
    r'\lux': r'\mathrm{lx}', r'\lx': r'\mathrm{lx}',
    r'\newton': r'\mathrm{N}', r'\N': r'\mathrm{N}',
    r'\ohm': r'\Omega', r'\Ohm': r'\Omega',
    r'\pascal': r'\mathrm{Pa}', r'\Pa': r'\mathrm{Pa}',
    r'\radian': r'\mathrm{rad}',
    r'\siemens': r'\mathrm{S}', r'\S': r'\mathrm{S}',
    r'\sievert': r'\mathrm{Sv}',
    r'\steradian': r'\mathrm{sr}',
    r'\tesla': r'\mathrm{T}', r'\T': r'\mathrm{T}',
    r'\volt': r'\mathrm{V}', r'\V': r'\mathrm{V}',
    r'\watt': r'\mathrm{W}', r'\W': r'\mathrm{W}',
    r'\weber': r'\mathrm{Wb}', r'\Wb': r'\mathrm{Wb}',

    # Accepted Non-SI Units
    r'\astronomicalunit': r'\mathrm{au}',
    r'\bel': r'\mathrm{B}',
    r'\dalton': r'\mathrm{Da}',
    r'\day': r'\mathrm{d}',
    r'\decibel': r'\mathrm{dB}', r'\dB': r'\mathrm{dB}',
    r'\degree': r'^\circ',
    r'\electronvolt': r'\mathrm{eV}', r'\eV': r'\mathrm{eV}',
    r'\hectare': r'\mathrm{ha}',
    r'\hour': r'\mathrm{h}', r'\hr': r'\mathrm{h}',
    r'\litre': r'\mathrm{L}', r'\liter': r'\mathrm{L}', r'\l': r'\mathrm{L}', r'\L': r'\mathrm{L}',
    r'\arcminute': r'^{\prime}',
    r'\minute': r'\mathrm{min}', r'\min': r'\mathrm{min}',
    r'\arcsecond': r'^{\prime\prime}',
    r'\neper': r'\mathrm{Np}',
    r'\tonne': r'\mathrm{t}',

    # Abbreviations - Mass
    r'\fg': r'\mathrm{fg}',
    r'\pg': r'\mathrm{pg}',
    r'\ng': r'\mathrm{ng}',
    r'\ug': r'\mu\mathrm{g}',
    r'\mg': r'\mathrm{mg}',
    r'\g': r'\mathrm{g}', # Added \g

    # Abbreviations - Length
    r'\pm': r'\mathrm{pm}',
    r'\nm': r'\mathrm{nm}',
    r'\um': r'\mu\mathrm{m}',
    r'\mm': r'\mathrm{mm}',
    r'\cm': r'\mathrm{cm}',
    r'\dm': r'\mathrm{dm}',
    r'\km': r'\mathrm{km}',

    # Abbreviations - Time
    r'\as': r'\mathrm{as}',
    r'\fs': r'\mathrm{fs}',
    r'\ps': r'\mathrm{ps}',
    r'\ns': r'\mathrm{ns}',
    r'\us': r'\mu\mathrm{s}',
    r'\ms': r'\mathrm{ms}',

    # Abbreviations - Amount of Substance
    r'\fmol': r'\mathrm{fmol}',
    r'\pmol': r'\mathrm{pmol}',
    r'\nmol': r'\mathrm{nmol}',
    r'\umol': r'\mu\mathrm{mol}',
    r'\mmol': r'\mathrm{mmol}',
    r'\kmol': r'\mathrm{kmol}',

    # Abbreviations - Current
    r'\pA': r'\mathrm{pA}',
    r'\nA': r'\mathrm{nA}',
    r'\uA': r'\mu\mathrm{A}',
    r'\mA': r'\mathrm{mA}',
    r'\kA': r'\mathrm{kA}',

    # Abbreviations - Volume
    r'\ul': r'\mu\mathrm{L}', r'\uL': r'\mu\mathrm{L}',
    r'\ml': r'\mathrm{mL}', r'\mL': r'\mathrm{mL}',
    r'\hl': r'\mathrm{hL}', r'\hL': r'\mathrm{hL}',

    # Abbreviations - Frequency
    r'\mHz': r'\mathrm{mHz}',
    r'\kHz': r'\mathrm{kHz}',
    r'\MHz': r'\mathrm{MHz}',
    r'\GHz': r'\mathrm{GHz}',
    r'\THz': r'\mathrm{THz}',

    # Abbreviations - Force
    r'\mN': r'\mathrm{mN}',
    r'\kN': r'\mathrm{kN}',
    r'\MN': r'\mathrm{MN}',

    # Abbreviations - Pressure
    r'\kPa': r'\mathrm{kPa}',
    r'\MPa': r'\mathrm{MPa}',
    r'\GPa': r'\mathrm{GPa}',

    # Abbreviations - Resistance
    r'\mohm': r'\mathrm{m}\Omega',
    r'\kohm': r'\mathrm{k}\Omega',
    r'\Mohm': r'\mathrm{M}\Omega',

    # Abbreviations - Potential
    r'\pV': r'\mathrm{pV}',
    r'\nV': r'\mathrm{nV}',
    r'\uV': r'\mu\mathrm{V}',
    r'\mV': r'\mathrm{mV}',
    r'\kV': r'\mathrm{kV}',

    # Abbreviations - Power
    r'\nW': r'\mathrm{nW}',
    r'\uW': r'\mu\mathrm{W}',
    r'\mW': r'\mathrm{mW}',
    r'\kW': r'\mathrm{kW}',
    r'\MW': r'\mathrm{MW}',
    r'\GW': r'\mathrm{GW}',

    # Abbreviations - Energy
    r'\uJ': r'\mu\mathrm{J}',
    r'\mJ': r'\mathrm{mJ}',
    r'\kJ': r'\mathrm{kJ}',
    r'\MJ': r'\mathrm{MJ}',
    r'\kWh': r'\mathrm{kW\,h}',
    r'\meV': r'\mathrm{meV}',
    r'\keV': r'\mathrm{keV}',
    r'\MeV': r'\mathrm{MeV}',
    r'\GeV': r'\mathrm{GeV}',
    r'\TeV': r'\mathrm{TeV}',

    # Abbreviations - Capacitance
    r'\fF': r'\mathrm{fF}',
    r'\pF': r'\mathrm{pF}',
    r'\nF': r'\mathrm{nF}',
    r'\uF': r'\mu\mathrm{F}',
    r'\mF': r'\mathrm{mF}',

    # Abbreviations - Inductance
    r'\fH': r'\mathrm{fH}',
    r'\pH': r'\mathrm{pH}',
    r'\nH': r'\mathrm{nH}',
    r'\microhenry': r'\mu\mathrm{H}', r'\uH': r'\mu\mathrm{H}',
    r'\mH': r'\mathrm{mH}',

    # Abbreviations - Charge
    r'\nC': r'\mathrm{nC}',
    r'\mC': r'\mathrm{mC}',
    r'\uC': r'\mu\mathrm{C}',

    # Abbreviations - Magnetic Flux Density
    r'\mT': r'\mathrm{mT}',
    r'\uT': r'\mu\mathrm{T}',

    # Binary Units
    r'\bit': r'\text{bit}',
    r'\byte': r'\text{byte}',
    r'\kibi': r'\mathrm{Ki}',
    r'\mebi': r'\mathrm{Mi}',
    r'\gibi': r'\mathrm{Gi}',
    r'\tebi': r'\mathrm{Ti}',
    r'\pebi': r'\mathrm{Pi}',
    r'\exbi': r'\mathrm{Ei}',
    r'\zebi': r'\mathrm{Zi}',
    r'\yobi': r'\mathrm{Yi}',

    # Prefixes (Naive mapping for when they appear standalone in unit args)
    r'\quecto': r'\mathrm{q}',
    r'\ronto': r'\mathrm{r}',
    r'\yocto': r'\mathrm{y}',
    r'\zepto': r'\mathrm{z}',
    r'\atto': r'\mathrm{a}',
    r'\femto': r'\mathrm{f}',
    r'\pico': r'\mathrm{p}',
    r'\nano': r'\mathrm{n}',
    r'\micro': r'\mu',
    r'\milli': r'\mathrm{m}',
    r'\centi': r'\mathrm{c}',
    r'\deci': r'\mathrm{d}',
    r'\deca': r'\mathrm{da}',
    r'\deka': r'\mathrm{da}',
    r'\hecto': r'\mathrm{h}',
    r'\kilo': r'\mathrm{k}',
    r'\mega': r'\mathrm{M}',
    r'\giga': r'\mathrm{G}',
    r'\tera': r'\mathrm{T}',
    r'\peta': r'\mathrm{P}',
    r'\exa': r'\mathrm{E}',
    r'\zetta': r'\mathrm{Z}',
    r'\yotta': r'\mathrm{Y}',
    r'\ronna': r'\mathrm{R}',
    r'\quetta': r'\mathrm{Q}',

    # Misc modifiers
    r'\per': r'/', # Handled by logic usually, but here for safety
    r'\squared': r'^2',
    r'\cubed': r'^3',
    r'\to': r'\text{to}',
    r'\percent': r'\%',
}
