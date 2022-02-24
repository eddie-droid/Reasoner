from copy import deepcopy


class Reasoner:

    def __init__(self, kb):
        self.kb = kb

    def forward_chain(self, query):
        truths = set()

        for atom in self.kb.atoms:
            truths.add(atom)
            print(".")
        listLength = len(truths)
        newListLength = 0

        while newListLength != listLength:
            listLength = len(truths)
            for head in self.kb.get_heads(truths):
                print(".")
                truths.add(head)
            newListLength = len(truths)
        if query in truths:
            return True
        else:
            return False

    def backward_chain(self, query):
        unproven = []
        proven = []

        unproven.append(query)
        while len(unproven) > 0:
            curr = unproven.pop()
            head = self.kb.get_heads(curr)
            if curr in self.kb.atoms:   #checks if query is one of the atom variables
                proven.append(head)
                continue
            elif head in proven:
                continue
            else:
                counter = 1
                inCompound = False
                #Searches top down from compound props
                for head in self.kb.compound_props:
                    print(".")
                    if curr == head:
                        inCompound = True
                        for body in self.kb.get_bodies(curr):
                            print(".")
                            for i in body:
                                print(".")
                                unproven.append(i)
                    else:
                        if len(self.kb.compound_props) == counter and inCompound == False:
                            return False
                    counter += 1
        return True


class KB:

    def __init__(self):
        self.atoms = set() # set
        self.compound_props = {}  # dictionary; head: list of bodies (sets)

    def get_bodies(self, head):
        return self.compound_props[head]

    def get_heads(self, antecedents):
        heads = set()
        for h, a_list in self.compound_props.items():
            for a in a_list:
                if a.issubset(antecedents):
                    heads.add(h)
                    break  # no need to add the same head multiple times
        return heads

    def add_atom(self, atom):
        self.atoms.add(atom)

    def add_compound(self, head, body):
        if head in self.compound_props:
            self.compound_props[head].append(body)
        else:
            self.compound_props[head] = [body]


if __name__ == '__main__':
    kb = KB()
    kb.add_atom("has_cat")
    kb.add_atom("plays_guitar")
    kb.add_atom("is_artist")
    kb.add_atom("no_sneeze")
    kb.add_compound("no_allergy", {"has_pet", "no_sneeze"})
    kb.add_compound("has_pet", {"has_dog"})
    kb.add_compound("has_pet", {"has_cat"})
    kb.add_compound("has_pet", {"has_gerbil"})
    kb.add_compound("allergy", {"has_pet", "sneezes"})
    kb.add_compound("allergy", {"no_pet"})
    kb.add_compound("is_musician", {"plays_guitar"})

    reasoner = Reasoner(kb)


    print(reasoner.forward_chain("no_allergy"))
    print("***********************************")
    print(reasoner.backward_chain("no_allergy"))

    print(reasoner.forward_chain("allergy"))
    #print("***********************************")
    #print(reasoner.backward_chain("allergy"))

    print(reasoner.forward_chain("has_dog"))
    #print("***********************************")
    #print(reasoner.backward_chain("has_dog"))

    print(reasoner.forward_chain("has_cat"))
    #print("***********************************")
    #print(reasoner.backward_chain("has_cat"))

    # TODO: test forward and backward chaining here

