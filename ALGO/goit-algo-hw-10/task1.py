from pulp import *

prob = LpProblem("Maximize_Production", LpMaximize)

lemonade = LpVariable("Lemonade", lowBound=0, cat='Integer')
fruit_juice = LpVariable("Fruit_Juice", lowBound=0, cat='Integer')

prob += lemonade + fruit_juice, "Total_Production"

prob += 2 * lemonade + 1 * fruit_juice <= 100, "Water_Constraint"
prob += 1 * lemonade <= 50, "Sugar_Constraint"
prob += 1 * lemonade <= 30, "Lemon_Juice_Constraint"
prob += 2 * fruit_juice <= 40, "Fruit_Puree_Constraint"

prob.solve()

print("Status:", LpStatus[prob.status])
print("Максимальна загальна кількість продуктів:", value(prob.objective))
print("Оптимальна кількість Лимонаду:", value(lemonade))
print("Оптимальна кількість Фруктового соку:", value(fruit_juice))

print("\nВикористання ресурсів:")
print(f"Вода: {2*value(lemonade) + 1*value(fruit_juice)} з 100 доступних")
print(f"Цукор: {1*value(lemonade)} з 50 доступних")
print(f"Лимонний сік: {1*value(lemonade)} з 30 доступних")
print(f"Фруктове пюре: {2*value(fruit_juice)} з 40 доступних")