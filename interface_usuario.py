#código para geração de pontos intermediarios em uma reta dado os pontos inicial e final

x1, y1, z1 = [int(x) for x in input("Enter the initial coordinate ").split()]
x2, y2, z2 = [int(x) for x in input("Enter the final coordinate ").split()]

qtd_pts = 10 #tentar otimizar esse valor para melhor controle
vetor = []
for p in range(qtd_pts+1):
    x = x1 + (x2-x1)*(1/qtd_pts*p)
    y = y1 + (y2-y1)*(1/qtd_pts*p)
    z = z1 + (z2-z1)*(1/qtd_pts*p)
    
    vetor.append([x,y,z])
    
print(vetor) #tem que colocar como point em vez de vetor