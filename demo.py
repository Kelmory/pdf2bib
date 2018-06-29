from PREI import pdf2ref


if __name__ == '__main__':
    extractor = pdf2ref.RefExtractor('F:/review.pdf', scholar='dblp')
    extractor.extract()
    total = len(extractor.records)
    count = 0
    for rec in extractor.records:
        if rec is not None:
            count += 1
    print('Successfully get bibtex: %d / %d' % (count, total))
