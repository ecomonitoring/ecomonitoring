# -*- encoding: utf-8 -*-
import os, sys
bw_child = 30
bw_adult = 70
at_kan = 70*365
at_nekan = 15*365
ir_wat = 0.13
ir_child_soil = 1.64*0.0001
ir_adult_soil = 8.6*0.00001
pc = 0.00084
abs = 0.05
af = 1.45*0.000001
rd_peros = 0.0003
rd_skin = 0.0007
cpf_peros = 1.5
cpf_skin = 3.7

class risk():
    def __init__(self):
        pass

    def dermwat(self,concentration,age,et,ef,ed,bw,at):
        if age > 18:
            sa = 19400
        else:
            sa = 15000
        return (concentration*sa*pc*et*ef*ed*0.001)/(bw*at)

    def dermsoil(self,concentration,age,et,ef,ed,bw,at):
        if age > 18:
            sa=5587.5
        else:
            sa=3650
        return (concentration*sa*abs*af*et*ef*ed*0.001)/(bw*at)

    def ingestwat(self,concentration,ir,ef,ed,bw,at):
        return (concentration*ir*ef*ed)/(bw*at)

    def ingestsoil(self,concentration,ir,ef,ed,bw,at):
        return (concentration*ir*ef*ed)/(bw*at)

    def DI(self,d,rd):
        return d/rd

    def ICR(self,d,cpf):
        return cpf*d 

    def DL(self,icr1,popl):
        return icr1*popl;

def Count(a,b,concentration,et_child,et_adult,ef_child,ef_adult,ed,popl_child,popl_adult,q):
    if (a == 1 or a == 2):
        if b == 1:
            c_child_kan = q.dermwat(concentration,16,et_child,ef_child,ed,bw_child,at_kan)
            c_adult_kan = q.dermwat(concentration,20,et_adult,ef_adult,ed,bw_adult,at_kan)
            c_child_nekan = q.dermwat(concentration,16,et_child,ef_child,ed,bw_child,at_nekan)
            c_adult_nekan = q.dermwat(concentration,20,et_adult,ef_adult,ed,bw_adult,at_nekan)        
        else:
            c_child_kan = q.ingestwat(concentration,ir_wat,ef_child,ed,bw_child,at_kan)
            c_adult_kan = q.ingestwat(concentration,ir_wat,ef_adult,ed,bw_adult,at_kan)
            c_child_nekan = q.ingestwat(concentration,ir_wat,ef_child,ed,bw_child,at_nekan)
            c_adult_nekan = q.ingestwat(concentration,ir_wat,ef_adult,ed,bw_adult,at_nekan)
    elif (a == 3):
        if b == 1:
            c_child_kan = q.dermsoil(concentration,16,et_child,ef_child,ed,bw_child,at_kan)
            c_adult_kan = q.dermsoil(concentration,20,et_adult,ef_adult,ed,bw_adult,at_kan)
            c_child_nekan = q.dermsoil(concentration,16,et_child,ef_child,ed,bw_child,at_nekan)
            c_adult_nekan = q.dermsoil(concentration,20,et_adult,ef_adult,ed,bw_adult,at_nekan)
    else:
        c_child_kan = q.ingestsoil(concentration,ir_child_soil,ef_child,ed,bw_child,at_kan)
        c_adult_kan = q.ingestsoil(concentration,ir_adult_soil,ef_adult,ed,bw_adult,at_kan)
        c_child_nekan = q.ingestsoil(concentration,ir_child_soil,ef_child,ed,bw_child,at_nekan)
        c_adult_nekan = q.ingestsoil(concentration,ir_adult_soil,ef_adult,ed,bw_adult,at_nekan)

    #p_child = (c_child_kan+c_child_nekan)
    #p_adult = (c_adult_kan+c_adult_nekan)
    #print('Поглощенная доза (для ребенка/взрослого)                        '+p_child+' / '+p_adult)
    #print(p_child +' / '+p_adult)

    output ={}

    output["p_child"]= str((c_child_kan+c_child_nekan, 3))
    output["p_adult"]= str((c_adult_kan+c_adult_nekan, 3))

    if b == 1:
        rd = rd_skin
    else:
        rd = rd_peros
    
    #s1 = 'Индекс опасности неканцерогенного риска (для ребенка/взрослого) '+str(q.DI(c_child_nekan, rd))+' / '+str(q.DI(c_adult_nekan, rd));
    #print(str(q.DI(c_child_nekan, rd))+' / '+str(q.DI(c_adult_nekan, rd))
    
    output["c_necan"]= str((q.DI(c_child_nekan, rd), 3))
    output["a_necan"]= str((q.DI(c_adult_nekan, rd), 3))

    if b == 1:
        cpf = cpf_skin
    else:
        cpf = cpf_peros

    #s2='Индивидуальный канцерогенный риск (для ребенка/взрослого)       '+str(q.ICR(c_child_kan,cpf))+' / '+str(q.ICR(c_adult_kan,cpf));
    #print(str(q.ICR(c_child_kan,cpf))+' / '+str(q.ICR(c_adult_kan,cpf))
    
    output["p_c_can"]= str((q.ICR(c_child_kan,cpf), 3))
    output["p_a_can"]= str((q.ICR(c_adult_kan,cpf), 3))
    
    #f = q.DL(popl_child,q.ICR(c_child_kan,cpf))+q.DL(popl_adult,q.ICR(c_adult_kan,cpf));
    #s3 = 'Канцерогенный риск для населения'+str(f);
    #print(str(f))

    output["pop_can"]= str((q.DL(popl_child,q.ICR(c_child_kan,cpf))+q.DL(popl_adult,q.ICR(c_adult_kan,cpf)), 3))
    return output


if __name__ == '__main__':
    t = open("risk.txt","r")
    q = risk()
    for line in t:
        tokens = line.split(' ')
        date = tokens[0]
        a = int(tokens[1])
        b = int(tokens[2])
        concentration = float(tokens[3])
        ir_child = et_child = int(tokens[4])
        ir_adult = et_adult = int(tokens[5])
        ef_child = int(tokens[6])
        ef_adult = int(tokens[7])
        ed = float(tokens[8])
        popl_child = int(tokens[9])
        popl_adult = int(tokens[10])
        r = Count(a,b,concentration,ir_child,ir_adult,ef_child,ef_adult,ed,popl_child,popl_adult,q)
