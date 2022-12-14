import xml.etree.ElementTree as ET
import re

def rewrite_xml(path, filename):
    print('processing', filename)
    count_inconsistent_offset = 0
    count_correct_to = 0
    raw = ET.parse(path+filename)
    root = raw.getroot()
    for id, node in enumerate(root):
        text = node.findtext('text')
        ops_xml = node.find('Opinions')
        # there are ill-formatted attributes like <Opinions/> in train and dev dataset
        # After ops_xml is not None, you must double check len(ops_xml)>0
        # to avoid index out of range in element Opinions (if you are using one)
        if ops_xml is not None:
            # if it's a deprecated Opinions element, remove it completely first,
            # then insert a NULL opinion if it's relevant
            if len(ops_xml) == 0:
                node.remove(ops_xml)
                r = node.findtext('relevance')
                relevance = True if r=='true' else False
                if relevance:
                    sentiment = node.findtext('sentiment')
                    o = ET.SubElement(node, 'Opinions')
                    null_op = ET.SubElement(o, 'Opinion')
                    null_op.set('category', 'Allgemein#Haupt')
                    null_op.set('from', '0')
                    null_op.set('to', '0')
                    null_op.set('target', 'NULL')
                    null_op.set('polarity', sentiment)
            elif ops_xml[0].attrib['target']!='NULL':
                for op in ops_xml:
                    # get attributes for an opinion
                    offset_from = int(op.attrib['from'])
                    offset_to = int(op.attrib['to'])
                    target = op.attrib['target']
                    abs = op.attrib['polarity']

                    # fix polarity format
                    if abs=='positve':
                        op.set('polarity', 'positive')
                    elif abs==' negative':
                        op.set('polarity', 'negative')

                    # fix inconsistent offset
                    if text[offset_from:offset_to]!=target:
                        count_inconsistent_offset += 1
                        endword = target.split()[-1]
                        repetition = target.count(endword)
                        new_to = offset_from
                        for step in range(repetition):
                            new_to = new_to + text[new_to:].find(endword) + len(endword)
                        target = text[offset_from:new_to]
                        if filename == 'test_dia-2017-09-15.xml':
                            offset_to2 = int(op.attrib['to2'])
                            if new_to == offset_to2:
                                count_correct_to += 1
                        else:
                            if new_to == offset_to:
                                count_correct_to += 1
                        offset_to = new_to
                        op.set('target', target)
                        op.set('to', str(offset_to))

    print('inconsistent offset:'+str(count_inconsistent_offset))
    print('correct offset to:'+str(count_correct_to))
    raw.write(path+'fixed_'+filename)


def main():
    """
    read the xml format of GermEval 2017 dataset and fix the following question:
    1.There are some incomplete tags. Remove it completely and fill with null tag if needed.
    2.Change mispelled polarity to correct spelling
    3.Some target terms are inconsistent with their offset, correct and find the first match.
      Repetition of the same word is recorded in lef-to-right order. Dia-testset has 'to2' attribute
      which will be handled differently.
    A modified version will be saved with prefix 'fixed_' + original filename
    """

    target_dir = "./data/"
    filenames = ['train-2017-09-15.xml', 'dev-2017-09-15.xml', 'test_syn-2017-09-15.xml', 'test_dia-2017-09-15.xml']
    for filename in filenames:
        rewrite_xml(target_dir, filename)
    print('modified xml saved in directory '+target_dir)


if __name__ == "__main__":
    main()
