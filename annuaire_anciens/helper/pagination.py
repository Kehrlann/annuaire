# coding=utf-8

class Pagination():
    """
    Classe d'aide a la pagination
    Porte le nombre d'éléments, le nombre d'éléments par page, etc
    """
    _page_current = 1
    count = 0           # Nombre d'elements
    per_page = 100      # nombre d'elements a afficher par page    
    show_range = 2      # nombre de pages precedentes et suivantes a afficher

    def __init__(self, count = 0, per_page = 100, show_range = 2):
        self.count = count
        self.per_page = per_page
        self.show_range = show_range
        self._page_current = 1

    @property
    def current(self):
        """
        index de la page courante
        """
        return self._page_current

    @current.setter
    def current(self, page):
        print "lol"
        if page is not None and type(page) is int and page > 0:
            self._page_current = page
     
    
    @property
    def first(self):
        """
        index de la premiere page (page 1)
        """
        return 1
        
        
    @property
    def last(self):
        """
        index de la derniere page
        """
        return (self.count / self.per_page) + 1
        
    @property    
    def previous(self):
        """
        index de la page precedente
        """
        if self.current > 1:
            return self.current - 1
        else:
            return self.current
            
    @property
    def next(self):
        """
        index de la page suivante
        """
        if self.current < self.last:
            return self.current + 1
        else:
            return self.current

    def get_prev_list(self):
        """
        retourne la liste des *show_range* pages precedentes, dans l'ordre
        """
        result = []
        iter = 1
        while iter <= self.show_range and self.current - iter >= 1:
            result.append(self.current - iter)
            iter += 1
        result.sort()
        return result
    
    
    def get_next_list(self):
        """
        retourne la liste des *show_range* pages suivantes, dans l'ordre
        """
        result = []
        iter = 1
        while iter <= self.show_range and self.current + iter <= self.last:
            result.append(self.current + iter)
            iter += 1
        result.sort()
        return result
    

    def has_hidden_next(self):
        """
        retourne true si il y a plus de pages suivantes que range_show
        """
        if (self.current + self.show_range) < self.last:
            return True
        else:
            return False
            
            
    def has_hidden_prev(self):
        """
        retourne true si il y a plus de pages precedentes que range_show
        """
        if (self.current - self.show_range) > self.first:
            return True
        else:
            return False
    
     
    @property
    def offset(self):
        """
        offset en base (= premier element a aller chercher - 1) a partir de _page_current et per_page
        """
        if self.current == 1:
            return 0
        else:
            return (self.current - 1) * self.per_page
        
    
    @property
    def limit(self):
        """
        limit en base
        = nombre d'elements a aller chercher
        = per_page
        """
        return self.per_page