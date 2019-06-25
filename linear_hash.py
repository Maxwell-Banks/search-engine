"""Maxwell Banks
mbanks01
LAB7
CPE202
"""

def hash_string(string, size): 
    hash = 0
    for c in string:
        hash = (hash * 31 + ord(c)) % size
    return hash


class HashTableLinear:
    """Class object that creates a hash table and allocates 
    integers to it. Collisions are handled with linear probing.
    
    Attribues:
        table_siz(int): The number of slots in the table
        table(list): The hash table to values will be stored in
        num_coll(int): Number of collisions in the hash table
        num_items(int): Number of items in the hash table
    """

    def __init__(self, table_size = 11):
        
        self.table_size = table_size
        self.table = [None] * table_size
        self.num_coll = 0
        self.num_items = 0

    def __repr__(self):
        st = ""
        for x in self.table:
            st += str(x)
            st += '\n'
        return st

    def __eq__(self, other):
        return self.table_size == other.table_size\
            and self.table == other.table\
            and self.num_coll == other.num_coll\
            and self.num_items == other.num_items

    def __getitem__(self,key): 
        return self.get(key)
    
    def __setitem__(self,key,data):
        self.put(key,data)
    
    def __contains__(self, key): 
        return self.contains(key)

    def put(self, key, data):
        #creates the hash
        hash = hash_string(key, self.table_size)
        

        #checks if the space is open
        if self.table[hash] == None:
            #add the value into the empty slots
            self.table[hash] = (key, data)
            #increases the number of items counter
            self.num_items += 1

        #checks if the string is already stored there
        elif self.table[hash][0] == key:
            #increases its count if it is
            self.table[hash] = (key, self.table[hash][1] + data)

        #if the space is full
        else:
            #create a location pointer
            pointer = hash
            #searchs through the list to find an empty slot
            #print(self.table)
            #print()
            while self.table[pointer] != None:
                if self.table[pointer] == key:
                    self.table[pointer] = (key, self.table[pointer][1] + data)
                    break
                    
                pointer += 1
                pointer %= self.table_size
                #print(pointer)
            self.num_items += 1
            self.num_coll += 1
            self.table[pointer] = (key, data)

        if self.load_factor() > .75:
            #print("REHASHING...")
            self.rehash()

    def get(self, key):
        
        hash = hash_string(key, self.table_size)
        
        if self.table[hash] is None:
            raise LookupError

        if self.table[hash][0] == key:
            self.num_items += 1
            return self.table[hash]
        
        else:
            pointer = hash

            while self.table[pointer] is not None:
                if self.table[pointer][0] == key:
                    return self.table[pointer]

                pointer += 1
                pointer %= self.table_size

            raise LookupError

    def contains(self, key):

        hash = hash_string(key, self.table_size)

        if self.table[hash] is None:
            #print('slot empty at ' + str(hash))
            return False

        if self.table[hash][0] == key:
            #print('found in first place ' + str(hash))
            return True

        else:
            pointer = hash

            while self.table[pointer] is not None:
                #print(pointer)
                if self.table[pointer][0] == key:
                    #print('found in ' + str(pointer))
                    return True
                pointer += 1
                #print(self.num_items)
                pointer %= self.table_size

            #print('unable to find at ' + str(pointer))
            return False

    def remove(self, key):

        if self.contains(key):
            raise LookupError

        hash = hash_string(key, self.table_size)

        if self.table[hash][0] == key:
            self.num_items -= 1
            self.table[hash] = None

        else:
            pointer = hash

            while self.table[pointer] == None:
                if self.table[pointer][0] == key:
                    return self.table[pointer]
                pointer += 1 
                pointer %= self.size
            self.num_items -= 1
            self.num_coll -= 1
            self.table[pointer] = None

    def size(self):

        return self.num_items

    def load_factor(self):

        return self.num_items / self.table_size

    def collisions(self):

        return self.num_coll

    def rehash(self):
        #print("REHASHING...")
        new_slots = (self.table_size * 2) + 1
        self.table_size = new_slots
        for n in range (self.table_size - len(self.table)):
            self.table.append(None)
        #print('table size: ' + str(self.table_size))
        #print('table length: ' + str(len(self.table)))
        assert self.table_size == len(self.table)

        old_hash = []
        for n in range(len(self.table)):
            if self.table[n]!= None:
                old_hash.append(self.table[n])
                self.table[n] = None
        self.num_items = 0
        self.num_coll = 0
        for val in old_hash:
            self.put(val[0], val[1])


def main():

    pass

if __name__ == "__main__":
    main()