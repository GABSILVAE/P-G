print("Nombre: Gabriel Felipe Silva Espejo")
print("Codigo: 201310989")
print("")

matriz = [[1,1,0,0,1,0,0,1,1,1],
          [1,0,0,0,1,0,0,1,1,1],
          [0,0,0,0,0,0,0,1,1,1],
          [0,0,0,0,0,0,1,0,0,0],
          [0,0,0,0,0,1,1,1,0,0],
          [0,0,0,0,1,1,1,1,1,0],
          [0,1,0,1,1,1,1,1,1,0],
          [0,0,0,0,1,1,1,1,1,0],
          [0,0,0,0,0,1,1,1,1,0],
          [0,0,0,0,0,0,1,1,1,1]]
numeroIslas=2
print(matriz)
for i in range(10):
    for j in range(10):
        valorPos=matriz[i][j]
        dirN=i+1
        dirS=i-1
        dirD=j+1
        dirI=j-1
        if(dirN<0 or dirN>9):
            posN=0
        else:
            posN=matriz[dirN][j]
        
        if(dirS<0 or dirS>10):
            posS=0
        else:
            posS=matriz[dirS][j]
        
        if(dirD<0 or dirD>9):
            posD=0
        else:
            posD=matriz[i][dirD]
        
        if(dirI<0 or dirI>10):
            posI=0
        else:
            posI=matriz[i][dirI]
        
        if (valorPos==1):
            if(posD==1 or posD==0):
                matriz[i][j]=numeroIslas
                if(posN==1):
                    matriz[i+1][j]=numeroIslas
                if(posS==1):
                    matriz[i-1][j]=numeroIslas
                if(posD==1):
                    matriz[i][j+1]=numeroIslas
                if(posI==1):
                    matriz[i][j-1]=numeroIslas
                numeroIslas=numeroIslas+1
            if(posD>1):
                matriz[i][j]=posD
                if(posN==1):
                    matriz[i+1][j]=posD
                if(posS==1):
                    matriz[i-1][j]=posD
                if(posD==1):
                    matriz[i][j+1]=posD
                if(posI==1):
                    matriz[i][j-1]=posD

        if(valorPos!=0 and valorPos!=1):
            if(posN==1):
                matriz[i+1][j]=valorPos
            if(posS==1):
                matriz[i-1][j]=valorPos
            if(posD==1):
                matriz[i][j+1]=valorPos
            if(posI==1):
                matriz[i][j-1]=valorPos
print("")
print(matriz)
print("")
numeroIslas=numeroIslas-2
print("numero de islas = %s" %numeroIslas)

input()
