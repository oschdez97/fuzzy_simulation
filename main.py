from fuzzy_system   import FuzzySystem
from fuzzy_variable import FuzzyVariable

edad = FuzzyVariable(18, 70, 100, 'Edad')
edad.add_trapezoid('Joven', 18, 18, 25, 30)
edad.add_triangular('Adulto', 20, 35, 50)
edad.add_trapezoid('Mayor', 40, 60, 70, 70)

manejo = FuzzyVariable(0, 100, 100, 'Manejo')
manejo.add_trapezoid('Bajo', 0, 0, 10, 20)
manejo.add_triangular('Medio', 10, 40, 60)
manejo.add_trapezoid('Alto', 50, 70, 100, 100)

riesgo_financiero = FuzzyVariable(0, 100, 100, 'Riesgo')
riesgo_financiero.add_trapezoid('Bajo', 0, 0, 10, 20)
riesgo_financiero.add_triangular('Medio', 10, 30, 45)
riesgo_financiero.add_trapezoid('Alto', 40, 55, 100, 100)

system = FuzzySystem()
system.add_input_variable(edad)
system.add_input_variable(manejo)
system.add_output_variable(riesgo_financiero)

system.add_rules([
    'Edad Joven AND Manejo Bajo THEN Riesgo Medio',
    'Edad Joven AND Manejo Medio THEN Riesgo Alto',
    'Edad Joven AND Manejo Alto THEN Riesgo Alto',
    'Edad Adulto AND Manejo Bajo THEN Riesgo Bajo',
    'Edad Adulto AND Manejo Medio THEN Riesgo Medio',
    'Edad Adulto AND Manejo Alto THEN Riesgo Alto',
    'Edad Mayor AND Manejo Bajo THEN Riesgo Medio',
    'Edad Mayor AND Manejo Medio THEN Riesgo Alto',
    'Edad Mayor AND Manejo Alto THEN Riesgo Alto'
])


sample1 = { 'Edad' : 25, 'Manejo': 50 }
sample2 = { 'Edad' : 52, 'Manejo': 63 }
samples = [sample1, sample2]

for i, smp in enumerate(samples):
    print('sample_' + str(i))
    print()
    print(smp)
    mam = system.eval(smp, 'mamdani')
    lar = system.eval(smp, 'larsen')

    print('Método: Mamdani')
    print('Centroide: ' + str(system.centroide(mam)))
    print('Bisectriz: ' + str(system.bisectriz(mam)))
    print('Media de los Máximos: ' + str(system.media_max(mam)))
    print()
    print('Método: Larsen')
    print('Centroide: ' + str(system.centroide(lar)))
    print('Bisectriz: ' + str(system.bisectriz(lar)))
    print('Media de los Máximos: ' + str(system.media_max(lar)))
    print()

# plot el sistema del ejemplo 1 para mamdani
system.plot_system(system.eval(sample1))

