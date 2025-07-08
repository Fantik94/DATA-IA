def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

# Test des fonctions
test_celsius = 0
print(f"{test_celsius}°C = {celsius_to_fahrenheit(test_celsius)}°F")
test_fahrenheit = 32
print(f"{test_fahrenheit}°F = {fahrenheit_to_celsius(test_fahrenheit)}°F")