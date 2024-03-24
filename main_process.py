def factorize(numbers):
    factors_list = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        factors_list.append(factors)
    return factors_list

# Приклад використання:
input_numbers = [12, 24, 36]
result = factorize(input_numbers)
print(result)