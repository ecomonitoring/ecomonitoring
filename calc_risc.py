import os, sys

class risk():
    def __init__(self,concentration):
        self.concentration = concentration

    def dermwat(self,age,et,ef,ed,bw,at):
        if age > 18:
            sa = 19400
        else:
            sa = 15000
        return (self.concentration*sa*pc*et*ef*ed*0.001)/(bw*at)

    def dermsoil(self,age,et,ef,ed,bw,at):
        if age > 18:
            sa=5587.5
        else:
            sa=3650
        return (self.concentration*sa*abs*af*et*ef*ed*0.001)/(bw*at)

    def ingestwat(self,ir,ef,ed,bw,at):
        return (self.concentration*ir*ef*ed)/(bw*at)

    def ingestsoil(self,ir,ef,ed,bw,at):
        return (self.concentration*ir*ef*ed)/(bw*at)

    def DI(self,d,rd):
        return d/rd

    def ICR(self,d,cpf):
        return cpf*d

    def DL(self,icr1,popl):
        return icr1*popl
