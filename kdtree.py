from typing import List, Tuple

class Node:
    def __init__(self, point: Tuple[int, int], left: 'Node' = None, right: 'Node' = None, depth: int = 0):
        self.point = point
        self.left = left
        self.right = right
        self.depth = depth

class KDTree:
    def __init__(self):
        self.root = None
    
    def distanceSquared(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    
    def insert(self, point: Tuple[int, int]):
        def insertHelper(node: Node, point: Tuple[int, int], depth: int):
            if node is None:
                return Node(point, depth=depth)
            
            dim = depth % 2
            if point[dim] < node.point[dim]:
                node.left = insertHelper(node.left, point, depth + 1)
            else:
                node.right = insertHelper(node.right, point, depth + 1)
            
            return node
        
        self.root = insertHelper(self.root, point, 0)
    
    def range(self, lower: Tuple[int, int], upper: Tuple[int, int]) -> List[Tuple[int, int]]:
        def rangeHelper(node: Node, lower: Tuple[int, int], upper: Tuple[int, int], points: List[Tuple[int, int]]):
            if node is None:
                return
            
            if lower[0] <= node.point[0] <= upper[0] and lower[1] <= node.point[1] <= upper[1]:
                points.append(node.point)
            
            dim = node.depth % 2
            if lower[dim] < node.point[dim]:
                rangeHelper(node.left, lower, upper, points)
            if upper[dim] > node.point[dim]:
                rangeHelper(node.right, lower, upper, points)
        
        points = []
        rangeHelper(self.root, lower, upper, points)
        return points
    
    def nearestNeighbor(self, point: Tuple[int, int]) -> Tuple[int, int]:
        def nearestNeighborHelper(node: Node, point: Tuple[int, int], nearest: Tuple[int, int], nearestDistance: int):
            if node is None:
                return nearest, nearestDistance
            
            currentDistance = self.distanceSquared(node.point, point)
            if currentDistance < nearestDistance:
                nearest = node.point
                nearestDistance = currentDistance
            
            dim = node.depth % 2
            nextNode = None
            if point[dim] < node.point[dim]:
                nextNode = node.left
            else:
                nextNode = node.right
                
            nearest, nearestDistance = nearestNeighborHelper(nextNode, point, nearest, nearestDistance)
            # Check if there may be a closer point in the other child
            otherChild = None
            if nextNode is None:
                otherChild = node.left if node.right is nextNode else node.right
            elif point[dim] < node.point[dim]:
                otherChild = node.right
            else:
                otherChild = node.left
            
            # If the distance to the splitting plane is less than the current nearest distance,
            # there could be a closer point on the other side of the plane
            splitPlaneDistance = (node.point[dim] - point[dim]) ** 2
            if splitPlaneDistance < nearestDistance:
                otherNearest, otherNearestDistance = nearestNeighborHelper(otherChild, point, nearest, nearestDistance)
                if otherNearestDistance < nearestDistance:
                    nearest = otherNearest
                    nearestDistance = otherNearestDistance
                    
            return nearest, nearestDistance
        
        return nearestNeighborHelper(self.root, point, self.root.point, self.distanceSquared(self.root.point, point))
