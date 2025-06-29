import turtle
import math
import sys

def setup_turtle():
    window = turtle.Screen()
    window.bgcolor("white")
    
    painter = turtle.Turtle()
    painter.speed(0)  # Найшвидша швидкість
    painter.color("green")
    painter.pensize(2)
    painter.left(90)  # Початковий напрямок - вгору
    painter.up()
    painter.goto(0, -200)
    painter.down()
    
    return painter, window

def draw_pythagoras_tree(t, length, level, angle=45, shrink_factor=0.7):
    if level == 0:
        return
    
    # Малюємо основну гілку
    t.forward(length)
    
    current_pos = t.position()
    current_heading = t.heading()
    
    # Права гілка
    t.right(angle)
    draw_pythagoras_tree(t, length * shrink_factor, level-1, angle)
    
    # Повертаємось до основної гілки
    t.setposition(current_pos)
    t.setheading(current_heading)
    
    # Ліва гілка
    t.left(angle)
    draw_pythagoras_tree(t, length * shrink_factor, level-1, angle)
    
    # Повертаємось до основної гілки
    t.setposition(current_pos)
    t.setheading(current_heading)

def get_recursion_level():
    while True:
        try:
            level = int(input("Введіть рівень рекурсії (ціле число від 1 до 10): "))
            if 1 <= level <= 10:
                return level
            else:
                print("Будь ласка, введіть число від 1 до 10.")
        except ValueError:
            print("Будь ласка, введіть ціле число.")

def main():
    painter, window = setup_turtle()
    
    recursion_level = get_recursion_level()
    
    # Малюємо дерево Піфагора
    draw_pythagoras_tree(painter, 100, recursion_level)
    
    # Завершуємо роботу після натискання клавіші
    window.exitonclick()

if __name__ == "__main__":
    main()