import turtle

def koch_curve(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        koch_curve(t, length, depth-1)
        t.left(60)
        koch_curve(t, length, depth-1)
        t.right(120)
        koch_curve(t, length, depth-1)
        t.left(60)
        koch_curve(t, length, depth-1)

def draw_koch_snowflake(t, length, depth):
    for _ in range(3):
        koch_curve(t, length, depth)
        t.right(120)

def main():
    window = turtle.Screen()
    window.bgcolor("white")
    window.title("Сніжинка Коха")

    snowflake = turtle.Turtle()
    snowflake.speed(0)  
    snowflake.color("blue")
    snowflake.penup()
    
    snowflake.goto(-150, 90)
    snowflake.pendown()

    depth = int(turtle.numinput("Рівень рекурсії", 
                               "Введіть рівень рекурсії (рекомендовано 0-5):", 
                               default=3, minval=0, maxval=6))

    draw_koch_snowflake(snowflake, 300, depth)

    snowflake.hideturtle()
    window.mainloop()

if __name__ == "__main__":
    main()