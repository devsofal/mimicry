import tkinter as tk
import time

from tkinter import *

from deap import base, algorithms
from deap import creator
from deap import tools

import random


def canvas_reset(red_value=170):
    global current_red
    current_red = red_value

    color = '#%02x%02x%02x' % (int(current_red), 183, 244)

    canvas = tk.Canvas(win, width=500, height=500, bg=color)
    canvas.grid(row=0, column=0)

    for i in range(0, 5):
        for j in range(0, 5, 1):
            canvas.create_oval([i * 100 + 20, j * 100 + 20], [i * 100 + 70, j * 100 + 70], fill="pink")


def evolution_launch(red=170):
    # константы генетического алгоритма
    genome_length = 3
    population_size = 25
    crossover_probability = 0.7
    mutation_probability = 0.05
    max_generations = 20

    ideal = [int(current_red), 183, 244]  # условие к которому стремимся

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    def color_fitness(individual: list) -> int:
        result = 0
        for i in range(3):
            result += 0 - abs(individual[i] - ideal[i])
        return result,

    toolbox = base.Toolbox()

    toolbox.register("getColor", random.randint, 0, 255)
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.getColor, genome_length)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    population = toolbox.populationCreator(n=population_size)

    toolbox.register("evaluate", color_fitness)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=255, indpb=1.0 / genome_length)

    bots = []

    canvas = tk.Canvas(win, width=500, height=500, bg='#%02x%02x%02x' % (int(current_red), 183, 244))
    canvas.grid(row=0, column=0)

    for j in range(0, 5):
        for i in range(0, 5):
            bots.append(canvas.create_oval([i * 100 + 20, j * 100 + 20], [i * 100 + 70, j * 100 + 70],
                                           fill='yellow'))

    for i in range(0, max_generations):
        population, logbook = algorithms.eaSimple(population, toolbox,
                                                  cxpb=crossover_probability,
                                                  mutpb=mutation_probability,
                                                  ngen=i + 1,
                                                  # stats=stats,
                                                  verbose=False)  # if uncomment stats change to true)
        for n in range(25):
            canvas.itemconfig(bots[n],
                              fill='#%02x%02x%02x' % (population[n][0], population[n][1], population[n][2]))
        print(population)
        canvas.update()
        time.sleep(0.5)


if __name__ == '__main__':
    win = tk.Tk()

    win.title("mimicry")
    photo = tk.PhotoImage(file="icon.png")
    win.iconphoto(False, photo)
    win.geometry("600x550+10+10")

    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=3)

    button_widget = tk.Button(win, text='Поехали!', command=evolution_launch)

    scale_widget = tk.Scale(win, orient="vertical", length=400, sliderlength=15, resolution=1,
                            command=canvas_reset,
                            from_=170, to=255)
    scale_widget.grid(row=0, column=1)

    button_widget.grid(row=1, column=1)

    canvas_reset(170)

    win.mainloop()
