import numpy as np

[[399.99999999999994, 700.0], [659.8076211353317, 250.00000000000023], [140.19237886466863, 249.9999999999996]]

centre = (400, 400)

def cercle_bis(sommet):
    
    #for i in range(2):
    x0 = abs(sommet[1][0] - centre[0])
    y0 = abs(sommet[1][1] - centre[1])
    med0 = [x0/2, y0/2]
    pente_ortho0 = x0 / y0

    print(x0)
    print(y0)
    print(med0)
    print(pente_ortho0)


    x1 = abs(sommet[2][0] - centre[0])
    y1 = abs(sommet[2][1] - centre[1])  
    med1 = [x1/2, y1/2]
    pente_ortho1 = x1 / y1
    
    a = np.array((pente_ortho0, -1), (pente_ortho1, -1))
    b = np.array([-med0[1]+pente_ortho0*med0[0]], [-med1[1]+pente_ortho1*med1[0]])

    sol = np.linalg.solve(a, b)

    return [sol[0], sol[1]]


cercle_bis([[399.99999999999994, 700.0], [659.8076211353317, 250.00000000000023], [140.19237886466863, 249.9999999999996]])
#print(ghh)


