#This code was taken from https://www.geeksforgeeks.org/priority-queue-in-python/

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
 
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
 
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def insert(self, edge, distance_cost, heuristic_cost):
        self.queue.append((edge,distance_cost, heuristic_cost))
 
    # for popping an element based on Priority
    def pop(self):
        try:
            min_val = 0
            for i in range(len(self.queue)):
                if self.queue[i][1] + self.queue[i][2] < self.queue[min_val][1] + self.queue[min_val][2]:
                    min_val = i
            item = self.queue[min_val]
            del self.queue[min_val]
            return item
        except IndexError:
            print()
            exit()
 
if __name__ == '__main__':
    #Testing
    myQueue = PriorityQueue()
    myQueue.insert("Vienna",12,34)
    myQueue.insert("Anastacia",15,15)
    myQueue.insert("Shaggy",27,8)
    myQueue.insert("Roma",14,56)
    myQueue.insert("Goicochea",7,22)
    print(myQueue)           
    while not myQueue.isEmpty():
        print(myQueue.pop())