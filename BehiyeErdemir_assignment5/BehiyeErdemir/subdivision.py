# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013

from vec3d import Vec3d
from object_parser import *

class subdivision:
    @staticmethod
    def ChangeVertex(vec:Vec3d,s,inc):
        for i in s:
            if i==0:
                vec=Vec3d((vec.x)+inc,vec.y,vec.z,1)
            if i==1:
                vec=Vec3d((vec.x),vec.y+inc,vec.z,1)
            if i==2:
                vec=Vec3d((vec.x),vec.y,vec.z+inc,1)
        return vec
    @staticmethod
    def new_vertice(theobj,ver1,ver2,a):
        dif=[]
        zip_obj=zip(ver1,ver2)
        for i,j in zip_obj:
            dif.append(j-i)
        d = [idx for idx, val in enumerate(dif) if val != 0]
        inc=dif[d[0]]/2
        new=subdivision.ChangeVertex(theobj.vertice().__getitem__(a),d,inc)
        return new

    @staticmethod
    def subdivision(theobj,faceList,div):
        if div<1:
            print("division number can not be less than 1,")
            div=1  
        new_vertex_List=[]
        new_face_list=[]
    
        for face in faceList:
            new_vertices=[]#a,b,c,d,e
            vertice0=[(theobj.vertice().__getitem__(0).x),(theobj.vertice().__getitem__(0).y),(theobj.vertice().__getitem__(0).z)]
            vertice1=[(theobj.vertice().__getitem__(1).x),(theobj.vertice().__getitem__(1).y),(theobj.vertice().__getitem__(1).z)]
            vertice2=[(theobj.vertice().__getitem__(2).x),(theobj.vertice().__getitem__(2).y),(theobj.vertice().__getitem__(2).z)]
            vertice3=[(theobj.vertice().__getitem__(3).x),(theobj.vertice().__getitem__(3).y),(theobj.vertice().__getitem__(3).z)]

            newa=subdivision.new_vertice(theobj,vertice0,vertice1,0) #for a
            new_vertices.append(newa)

            newb=subdivision.new_vertice(theobj,vertice1,vertice3,1) #for b
            new_vertices.append(newb)
            
            newc=subdivision.new_vertice(theobj,vertice0,vertice3,0) #for c
            new_vertices.append(newc)

            newd=subdivision.new_vertice(theobj,vertice1,vertice2,1) #for d
            new_vertices.append(newd)

            newe=subdivision.new_vertice(theobj,vertice2,vertice3,2) #for e
            new_vertices.append(newe)

            new_vertex_List.extend([theobj.vertice().__getitem__(0),theobj.vertice().__getitem__(1),theobj.vertice().__getitem__(2),theobj.vertice().__getitem__(3),
                        new_vertices[0],new_vertices[1],new_vertices[2],new_vertices[3],new_vertices[4]])
 
            new_face_list.append([0,4,5,6])
            new_face_list.append([4,1,7,5])
            new_face_list.append([5,7,8,2])
            new_face_list.append([6,5,8,3])

        return new_vertex_List,new_face_list
    


