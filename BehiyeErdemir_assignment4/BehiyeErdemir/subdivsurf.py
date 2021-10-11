#!/usr/bin/env python3
# CENG 487 Assignment3 by
# Behiye Erdemir
# StudentId: 240206013
"""
I made use of information on https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface 
 while preparing this assignment.
The algorithm is 'Catmull–Clark subdivision surface'
"""
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from mat3d import *
from vec3d import Vec3d
from object import object 
import sys
import numpy as np
from mat3d import *
from typing import List
from vec3d import Vec3d
from os.path import exists, splitext, isfile

class subdivision_surfaces:
    
    #calculate mid point of the each faces by averaging the vertices of the face
    def mid_face_p(vertices,faces):
        mid_points=[]
        
        
        for face_index,face in enumerate(faces):
            mid_point=[0.0,0.0,0.0]
            #calculate mid point of the each faces by averaging the vertices of the face
            for vertex_index in face:
                point = vertices[vertex_index]
    
                mid_point=[x+y for x,y in zip(mid_point, point)]
            mid_point = [x / len(face) for x in mid_point]
            mid_points.append(mid_point)
    
        return mid_points
    
    #calculate center of the each edge
    def center_of_edges(vertices,faces):
        edges = []
        merged_edges=[]
        centers_edges=[]
        
        for face_index,face in enumerate(faces):
            #calculate edges of each faces in format: [vertex1, vertex2, faceNumber]
            for vertex_index in range(len(face)):
                #check the last point of the face
                if vertex_index < (len(face) - 1):
                    vertex_1=face[vertex_index]
                    vertex_2=face[vertex_index+1]
                    
                #assign last point and first point of the face
                else:
                    vertex_1=face[vertex_index]
                    vertex_2=face[0]
                
                #first low valued index
                if vertex_1 > vertex_2: 
                    temp=vertex_1
                    vertex_1=vertex_2
                    vertex_2=temp
                edges.append([vertex_1,vertex_2,face_index])
                
        edges=sorted(edges)
    
        
        #merge edges with 2 adjacent faces
        counter=0
        while counter < len(edges):
            edge_1 = edges[counter]
            #check the last edge of the edges
            if counter < (len(edges) - 1):
                edge_2 = edges[counter + 1]
                #check the similarity of the vertices inside edges contain
                if ((edge_1[0] == edge_2[0]) and (edge_1[1] == edge_2[1])):
                    #add in format: [vertex1, vertex2, faceNumber1, faceNumber2]
                    merged_edges.append([edge_1[0], edge_1[1], edge_1[2], edge_2[2]])
                    counter += 2
                #if not adjacent faces    
                else:
                    #add in format: [vertex1, vertex2, faceNumber1, None]
                    merged_edges.append([edge_1[0], edge_1[1], edge_1[2], None])
            #if the edge is the last edge
            else:
                #add in format: [vertex1, vertex2, faceNumber1, None]
                merged_edges.append([edge_1[0], edge_1[1], edge_1[2], None])
                counter += 1
                
        for edge in merged_edges:
            #format in: [vertex1, vertex2, face1, face2, [center]]
            centers_edges.append(edge + [[ (x+y)/2 for x,y in zip(vertices[edge[0]],
                                                                 vertices[edge[1]])]])   
        return centers_edges
    
    #get midpoint between center of edge and center of facepoints
    def mid_centerEdge_centerFace(vertices,centers,midpoints):
        edgeCenter_midp = []
     
        for center in centers:
            #center of edge format: [vertex1, vertex2, face1, face2, [center]]
            center_of_edge = center[4]
            #center of two mid points of the two adjacent face
            mid_point_1 = midpoints[center[2]]
            #if there is no an adjacent of the face
            if center[3] == None:
                mid_point_2 = mid_point_1
            #if there is an adjacent of the face like solid cube
            else:
                mid_point_2 = midpoints[center[3]]
            
            # center of midpoint of the faces
            center_of_midp = [ (x+y)/2 for x,y in zip(mid_point_1,mid_point_2)]
            
            #get midpoint between center of edge and center of facepoints
            edgeCenter_midp.append([ (x+y)/2 for x,y in zip(center_of_edge,center_of_midp)])  
        return edgeCenter_midp
    
    # the average of the face points of the faces
    def avg_face_points(vertices, faces, midpoints):
         temp = []
         avg_face_midpoints=[]
         
         for i in range(len(vertices)):
            temp.append([[0.0, 0.0, 0.0], 0])
            
         for face_index in range(len(faces)):
             mid_point_1=midpoints[face_index]
             for face in faces[face_index]:
                 cum=temp[face][0]
                 #sum all midpoints
                 temp[face][0] = [x+y for x,y in zip(mid_point_1, cum)]
                 temp[face][1] += 1
    
         for t in temp:
             #to get average sum(points)/repeat.
             div=[x/t[1] for x in t[0]]
             avg_face_midpoints.append(div)
    
         return avg_face_midpoints
        
    #the average of the centers of edges
    def avg_centers(vertices, centers):
        temp = []
        avg_centers = []
     
        for i in range(len(vertices)):
            temp.append([[0.0, 0.0, 0.0], 0])
        #center of edge format: [vertex1, vertex2, face1, face2, [center]]
        for center in centers:
            center_point_1 = center[4]
            for vertex in [center[0], center[1]]:
                cum = temp[vertex][0]
                #sum all edge centers
                temp[vertex][0] = [x+y for x,y in zip(center_point_1, cum)]
                temp[vertex][1] += 1
     
        #to get average sum(centers)/repeat.
        for t in temp:
           div=[x/t[1] for x in t[0]]
           avg_centers.append(div)
     
        return avg_centers               
    
    #number of faces a vertex belongs to                
    def number_of_faces(vertices, faces):
        numberFaces = [0]*len(vertices)
        for face_index in range(len(faces)):
            for vertex_index in faces[face_index]:
                numberFaces[vertex_index] += 1
        return numberFaces
    
    def get_new_vertices(vertices, numb_of_f, avg_midpoints, avg_edge_centers):
        """
        Formula of new vertice:
        m1 = (n - 3.0) / n
        m2 = 1.0 / n
        m3 = 2.0 / n
        new_coords = (m1 * vertices)
                   + (m2 * avg_midpoints)
                   + (m3 * avg_edge_centers)
     
        """             
        new_vertices =[]
     
        for vertex_index in range(len(vertices)):
            n = numb_of_f[vertex_index]
            m1 = (n - 3.0) / n
            m2 = 1.0 / n
            m3 = 2.0 / n
            old_vertex = vertices[vertex_index]
            m1_mul_v = [x*m1 for x in old_vertex] # m1 * vertices
            avg_mp = avg_midpoints[vertex_index]
            m2_mul_avg_m = [x*m2 for x in avg_mp] # (m2 * avg_midpoints)
            avg_edge_c = avg_edge_centers[vertex_index]
            m3_mul_avg_edgec = [x*m3 for x in avg_edge_c]
    
            new_vertex=[x+y+z for x,y,z in zip(m1_mul_v, m2_mul_avg_m,m3_mul_avg_edgec)]
            new_vertices.append(new_vertex)
     
        return new_vertices   
    
    def switch_nums(point_nums):
        """
        Returns tuple of point numbers
        sorted least to most
        """
        if point_nums[0] < point_nums[1]:
            return point_nums
        else:
            return (point_nums[1], point_nums[0])              
    
    """
    Each face is replaced by new faces made with the new vertices
    for a quad face (a,b,c,d):
           (a, edge_point ab, face_point abcd, edge_point da)
           (b, edge_point bc, face_point abcd, edge_point ab)
           (c, edge_point cd, face_point abcd, edge_point bc)
           (d, edge_point da, face_point abcd, edge_point cd)              
                      
    """                 
                      
    def calc_new_obj(vertices,faces):
        midpoints=subdivision_surfaces.mid_face_p(vertices, faces)       
        centers=subdivision_surfaces.center_of_edges(vertices,faces)
        midface_edge=subdivision_surfaces.mid_centerEdge_centerFace(vertices,centers,midpoints)
        avg_midpoints=subdivision_surfaces.avg_face_points(vertices, faces, midpoints)
        avg_edge_centers = subdivision_surfaces.avg_centers(vertices, centers) 
        numb_of_f = subdivision_surfaces.number_of_faces(vertices, faces)
        new_vertices = subdivision_surfaces.get_new_vertices(vertices, numb_of_f, avg_midpoints, avg_edge_centers)
        
        face_point_nums = []
         
        # point num after next append to new_points
        next_pointnum = len(new_vertices)
        for midpoint in midpoints:
            new_vertices.append(midpoint)
            face_point_nums.append(next_pointnum)
            next_pointnum += 1
        # add edge points to new_points
        edge_point_nums = dict()
         
        for edgenum in range(len(centers)):
            pointnum_1 = centers[edgenum][0]
            pointnum_2 = centers[edgenum][1]
            edge_point = midface_edge[edgenum]
            new_vertices.append(edge_point)
            edge_point_nums[(pointnum_1, pointnum_2)] = next_pointnum
            next_pointnum += 1
        
        new_faces =[]
         
        for old_face_index in range(len(faces)):
            old_face = faces[old_face_index]
            # 4 point face
            if len(old_face) == 4:
                a = old_face[0]
                b = old_face[1]
                c = old_face[2]
                d = old_face[3]
                face_point_abcd = face_point_nums[old_face_index]
                edge_point_ab = edge_point_nums[subdivision_surfaces.switch_nums((a, b))]
                edge_point_da = edge_point_nums[subdivision_surfaces.switch_nums((d, a))]
                edge_point_bc = edge_point_nums[subdivision_surfaces.switch_nums((b, c))]
                edge_point_cd = edge_point_nums[subdivision_surfaces.switch_nums((c, d))]
                new_faces.append((a, edge_point_ab, face_point_abcd, edge_point_da))
                new_faces.append((b, edge_point_bc, face_point_abcd, edge_point_ab))
                new_faces.append((c, edge_point_cd, face_point_abcd, edge_point_bc))
                new_faces.append((d, edge_point_da, face_point_abcd, edge_point_cd))
        
        return new_vertices, new_faces
    

    
    
    
    
    
    
    
