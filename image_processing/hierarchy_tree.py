from typing import List


class Node:

    def __init__(self, index):
        self.index = index
        self._childes = {}
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def get_n_parents(self, n):
        """ returns the n parents of the parent of the parent...
        :param n: how many parents should be returned
        :return: the n next parents, if not enough parents it will just return
        as many as it has
        """
        cur = self
        parents = []
        for _ in range(n):
            if not cur.parent:
                break
            parents.append(cur.parent)
            cur = cur.parent

        return parents, cur.parent is not None

    @property
    def childes(self):
        return list(self._childes.values())

    def add_child(self, child):
        self._childes[child.index] = child

class Tree:

    def __init__(self, cv2_presentation):
        self.roots = []
        self.flat = {}
        self._leaves = None

        self._init_tree(cv2_presentation)

    def _init_tree(self, cv2_presentation):
        cv2_presentation = [[i] + cv2_presentation[0][i].tolist() for i in range(len(cv2_presentation[0]))]
        cv2_presentation = sorted(cv2_presentation, key=lambda x: x[4])

        i = 0
        while i < len(cv2_presentation):
            cv2_node = cv2_presentation[i]
            # create new node
            node = Node(cv2_node[0])

            # check if it is a root node
            if cv2_node[4] == -1:
                self.flat[node.index] = node
                self.roots.append(node)
            else: # no root node
                # check if parent is already in list
                if cv2_node[4] not in self.flat:
                    # move it to last position
                    tmp = cv2_presentation.pop(i)
                    cv2_presentation = cv2_presentation + [tmp]
                    continue

                parent = self.flat[cv2_node[4]]

                # insert node into tree
                self.flat[node.index] = node
                node.parent = parent
                parent.add_child(node)

            i += 1

    @property
    def leaves(self) -> List[Node]:
        if not self._leaves:
            self._leaves = [leave for key, leave in self.flat.items() if not leave.childes]
        return self._leaves