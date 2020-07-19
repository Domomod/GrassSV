from abc import ABC, abstractmethod


class RegionComponent(ABC):
    """
    Common interface for all Region classes.
    """
    def __init__(self, region_name="<none>", region_type="<not-specified>", qualifiers=None):
        self.type = region_type
        self.name = region_name
        if qualifiers is None:
            self.qualifiers = {}
        elif isinstance(qualifiers, dict):
            self.qualifiers = qualifiers
        else:
            raise TypeError('In RegionComponent __init__ variable qualifiers was set to ' + repr(
                qualifiers) + 'which is not a dictionary')

    @abstractmethod
    def intersects(self, other, minimal_intersection = 0.0):
        """
        Detects intersection between two RegionComponent objects.
        :param other: A RegionComponent object.
        :return: A boolean value
        """
        pass

    @abstractmethod
    def flatten(self):
        """
        Returns a flat list of all regions composing for this object
        """
        pass

    def __repr__(self):
        return self.to_str()

    @abstractmethod
    def to_str(self, n=0):
        """
        Converts the object to a string representation, with proper indednation.
        :param n: Number of tabs of indentation
        :return: A string
        """
        pass


class RegionComposite(RegionComponent):
    """
    Composition of Region objects. Can be used to represent a complex mutation, parts of a read alligned to reference genome etc...
    """
    def __init__(self, regions, region_name="<none>", region_type="<not-specified>", qualifiers=None):
        RegionComponent.__init__(self, region_name=region_name, region_type=region_type, qualifiers=qualifiers)
        for loc in regions:
            if not isinstance(loc, RegionComponent):
                raise ValueError("%s should be given a list of "
                                 "%s objects, not %s" % (
                                     self.__class__.__name__, RegionComponent.__name__, loc.__class__))

        self.region_components = regions

    def paired_iter(self):
        for i in range(len(self.region_components) - 1):
            yield [self.region_components[i], self.region_components[i+1]]

    def __iter__(self):
        yield from self.region_components

    def intersects(self, other, minimal_intersection = 0.0):
        """
        Detects intersection between a RegionComposite object and a RegionComponent object.
        If the RegionComponent object happens to be:
        <ui>
            <li> a Region object, the caller will check if any of it's regions intersects with the Region object.
            <li> a RegionComposite object, the caller will check if any of it's regions intersects with
            the other RegionComposite's regions.
        </ui>
        :param other: a RegionComponent object
        :return: A boolean value.
        """
        if isinstance(other, RegionComponent):
            if isinstance(other, Region):
                return any([other.intersects(my_region, minimal_intersection)
                            for my_region in self.region_components])
            elif isinstance(other, RegionComposite):
                return any([his_region.intersects(my_region, minimal_intersection)
                            for my_region in self.region_components
                            for his_region in other.region_components])
        else:
            raise ValueError("intersects should be given a %s objects, not %s" % (RegionComponent, other.__class__))

    def flatten(self):
        """
        Returns a flat list of all regions composing for this object
        """
        return [region_component for region_component in self.region_components.flatten()]

    def _str_list(self, n=0):
        return ',\n'.join([region.to_str(n) for region in self.region_components])

    def to_str(self, n=0):
        """
        Converts the object to a string representation, with proper indednation.
        :param n: Number of tabs of indentation
        :return: A string
        """
        tab = ''
        for i in range(n):
            tab += '\t'
        return (f"{tab}<{self.__class__.__name__}: name={self.name}, type= {self.type},\n"
                f"{tab}\tregion_components= [\n"
                f"{self._str_list(2)}\n"
                f"{tab}\t],\n"
                f"{tab}\tqualifiers= {self.qualifiers}>")

class Contig(RegionComposite):
    """A type safe subclass of RegionComposite. Is equivalent to a non-nested list of ContigRegion
    (subclasses allowed) objects."""
    def __init__(self, regions, region_name="<none>", region_type="<not-specified>", qualifiers=None):
        for loc in regions:
            if not isinstance(loc, ContigRegion):
                raise ValueError("%s should be given a list of "
                                 "%s objects, not %s" % (
                                     self.__class__.__name__, RegionComponent.__name__, loc.__class__))
        RegionComposite.__init__(self, regions=regions, region_name=region_name, region_type=region_type, qualifiers=qualifiers)

class ShallowRegionComposite(RegionComposite):
    """A type safe subclass of RegionComposite. Is equivalent to a non-nested list of Region (no subclasses) objects."""
    def __init__(self, regions, region_name="<none>", region_type="<not-specified>", qualifiers=None):
        for loc in regions:
            if not type(loc) is Region:
                raise ValueError("%s should be given a list of "
                                 "%s objects, not %s" % (
                                     self.__class__.__name__, RegionComponent.__name__, loc.__class__))
        RegionComposite.__init__(self, regions=regions, region_name=region_name, region_type=region_type, qualifiers=qualifiers)

class Region(RegionComponent):
    """
    Region represents a single, continuous sequence of a genome from one chromosome.
    """
    def __init__(self, start, end, region_name="<none>", ref='<not-specified>', region_type="<not-specified>",
                 qualifiers=None):
        RegionComponent.__init__(self, region_name=region_name, region_type=region_type, qualifiers=qualifiers)
        self.start = int(start)
        self.end = int(end)
        self.length = abs(self.start - self.end)
        self.ref = ref

    def intersects(self, other, minimal_intersection = 0.0):
        """
        Detects intersection between a Region object and a RegionComponent object.
        :param other: a RegionComponent object
        :return: A boolean value.
        """
        if isinstance(other, RegionComponent):
            if isinstance(other, RegionComposite):
                return other.intersects(self)
            elif isinstance(other, Region):
                return self.ref == other.ref and (self._region_intersects(other, minimal_intersection) or other._region_intersects(self, minimal_intersection))
        else:
            raise ValueError("Region.intersects should be given object of one of the type %s" % RegionComponent)

    def _region_intersects(self, other, minimal_intersection = 0.0):
        """
        Helper method for intsersection detection of two Region objects. Needs to be called twice with calling
        order inverted for proper detection.
        :param other: a Region object
        :return: A boolean value.
        """
        is_interecting = False
        is_significant = False
        intersection_length = 0

        if other.start <= self.start <= other.end:
            intersection_length = other.end - self.start
            is_interecting = True

        elif other.end <= self.start <= other.start:
            intersection_length = other.start - self.start
            is_interecting = True

        elif other.start <= self.end <= other.end:
            intersection_length = other.end - self.end
            is_interecting = True

        elif other.end <= self.end <= other.start:
            intersection_length = other.start - self.end
            is_interecting = True

        is_significant = minimal_intersection < (2 * intersection_length / (self.length + other.length))

        return is_interecting and is_significant

    def flatten(self):
        """
        Returns a list continig only this Region.
        """
        return [self]

    def to_str(self, n=0):
        tab = ''
        for i in range(n):
            tab += '\t'
        return (f"{tab}<{self.__class__.__name__}: name={self.name}, type= {self.type},\n"
                f"{tab}\tstart= {self.start}, end= {self.end}, ref= {self.ref},\n"
                f"{tab}\tqualifiers={self.qualifiers}>")


class ContigRegion(Region):
    """
    Subclass of region, representing an aligned part of a contig.
    """
    def __init__(self, start, end, contig_space_start, contig_space_end, contig_name="<unspecified>",
                 region_name="<none>", ref='<not-specified>', region_type="<not-specified>", qualifiers=None):
        Region.__init__(self, start=start, end=end, ref=ref, region_name=region_name, region_type=region_type,
                        qualifiers=qualifiers)
        self.contig_space_start = int(contig_space_start)
        self.contig_space_end = int(contig_space_end)
        self.contig_name = contig_name
        self.orientation = "->" if self.contig_space_start < self.contig_space_end else "<-"

    def to_str(self, n=0):
        """
        Converts the object to a string representation, with proper indednation.
        :param n: Number of tabs of indentation
        :return: A string
        """
        tab = ''
        for i in range(n):
            tab += '\t'
        return (f"{tab}<{self.__class__.__name__}: name={self.name}, type= {self.type},\n"
                f"{tab}\tstart= {self.start}, end= {self.end}, ref= {self.ref},\n"
                f"{tab}\tcontig_name={self.contig_name}, contig_start= {self.contig_space_start}, contig_end={self.contig_space_end},\n"
                f"{tab}\tqualifiers={self.qualifiers}>")
