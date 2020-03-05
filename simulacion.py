import simpy
import random
import numpy as np
import statistics as stats 
import plotly.graph_objects as go
import numpy as np

ram =100
cpu=1
instrucciones =3
intervalo= 10
random.seed(11)

inst = [25,50,100,150,200]
instrucciones = np.array(inst)
x = []
y = []

def Proceso(env, nombre, sistema, memoria, instrucciones):
    numeroR = random.randint(1, 3)
    with sistema.RAM.get(memoria) as me:
        yield me
        yield env.timeout(1)
        while instrucciones > 3:
            if numeroR == 1:
                with sistema.CPU.request() as req:
                    yield req
                    yield env.timeout(1)
                    instrucciones = instrucciones - sistema.INSTRUCCIONES
                    numeroR = random.randint(1, 3)
                    print(nombre + ": se opero en "+str(env.now)+"\n")
            else:
                with sistema.ESPERA.request() as req:
                    yield req
                    yield env.timeout(1)
                    numeroR = 1
    sistema.RAM.put(memoria)
    print(nombre + ": terminado en "+str(env.now)+"\n")
    
def procesos(env, n, sistema, intervalo):
    for i in range(n):
        memoria = random.randint(1, 11)
        instrucciones = random.randint(1, 11)
        env.process(Proceso(env, 'Proceso %d' % (i+1), sistema, memoria, instrucciones))
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)
        
fig = go.Figure()
#   print("Tiempo total: " + str(env.now)+"\n")
#x.append(0)
#y.append(0)
op = "1"
instr = [25,50,100,150,200]
instrucciones = np.array(instr)
        
op ="1"
while op != "2":
    op = input("1. Procesos\n2. Grafica\nSeleccione la opcion que desea: ")
    if op == "1":
        x = []
        y = []
        instrucciones = int(input("Ingrese el numero de instrucciones capaz de procesar: "))
        ram = int(input("Ingrese la ram: "))
        intervalo = int(input("Ingrese el intervalo entre procesos: "))
        ncpu = int(input("Ingrese el numero de nucleos: "))

        for i in range(len(inst)):
            env = simpy.Environment()
            class Sistema:
                def __init__(self, env):
                    self.RAM = simpy.Container(env, init=ram, capacity=ram)
                    self.CPU = simpy.Resource(env, capacity=ncpu)
                    self.INSTRUCCIONES = instrucciones
                    self.ESPERA = simpy.Resource(env)
            sistema = Sistema(env)
            env.process(procesos(env, inst[i], sistema, intervalo))
            env.run()
            x.append(inst[i])
            y.append((env.now)/inst[i])
            print("Promedio: "+str(env.now/inst[i]) + "\n")
            print("Total: " + str(env.now)+"\n")
            print("DEsv. est.: "+ str(stats.pstdev(y))+"\n")
        xp = np.array(x)
        yp = np.array(y)
        fig.add_trace(go.Scatter(x=xp, y=yp,
                    mode='lines+markers',
                    name='tiempo de espera de: '+str(intervalo)+'\n Numero de nucleos: '+str(ncpu)+'\n Numero de ram: '+str(ram)+'\n Numero de instrucciones: '+str(instrucciones)))       
        
fig.update_layout(title='Procesos vs Tiempo promedio', xaxis_title='Procesos', yaxis_title='Tiempo promedio')
fig.show()