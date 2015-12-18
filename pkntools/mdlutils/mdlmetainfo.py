__author__ = 'imalkov'

import xml.etree.ElementTree as etree



class PknXmlReader:
    def __init__(self, pekan_xml):
        self.root = etree.parse(pekan_xml).getroot()

    def rec_find_by_el_attr(self, arr, res):
        if arr == []:
            return res
        el, attr = arr.pop(0)
        for i in res.findall(el):
            if i.attrib['name'] == attr:
                return self.rec_find_by_el_attr(arr, i)

class MetaStateMachine(PknXmlReader):
    def __init__(self, pekan_xml):
        PknXmlReader.__init__(self, pekan_xml)

    def convert(self, states_list):
        res = []
        root_state = self.rec_find_by_el_attr([('statemachine', 'pekan')], self.root)
        for state in root_state.findall('state'):
            if state.attrib['name'] not in states_list:
                continue
            res.append((state.find('class').text, int(state.find('rank').text)))
        return [s for s, r in sorted(res, key=lambda s: s[1])]

class MetaEnvInput(PknXmlReader):
    def __init__(self, pekan_xml):
        PknXmlReader.__init__(self, pekan_xml)

    def filename(self, name):
        return self.rec_find_by_el_attr([('input', 'input'), ('file', name)], self.root).get('value')

    @property
    def topofile(self):
        return self.filename('topography')

    @property
    def faultfile(self):
        return self.filename('fault')

class MetaInputGrid(PknXmlReader):
    def __init__(self, pekan_xml):
        PknXmlReader.__init__(self, pekan_xml)

    def gridtype(self, type):
        root_state = self.rec_find_by_el_attr([('statemachine', 'env')], self.root)
        for state in root_state.findall('state'):
            if int(state.find('rank').text) == int(type):
                return state.find('class').text
        raise KeyError('drid type not found')


class MetaCsv(PknXmlReader):
    def __init__(self, pekan_xml):
        PknXmlReader.__init__(self, pekan_xml)
    #csv file metadata
    def col_name(self, name):
        return self.rec_find_by_el_attr([('input', 'csv'), ('column', name)], self.root).get('value')

    @property
    def exec_dir(self):
        return self.col_name('A')
    @property
    def topo_2d_grid_dimentions(self):
        return self.col_name('B')
    @property
    def topo_2d_grid_type(self):
        return self.col_name('C')
    @property
    def create_env(self):
        return self.col_name('D')
    @property
    def topo_2d_max_hights(self):
        return self.col_name('E')
    @property
    def ref_dir(self):
        return self.col_name('F')
    @property
    def test_step(self):
        return self.col_name('G')
    @property
    def pecube_step(self):
        return self.col_name('H')
    @property
    def vtk_step(self):
        return self.col_name('I')

