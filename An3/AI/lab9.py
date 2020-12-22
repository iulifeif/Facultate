import lightrdf


if __name__ == '__main__':
    parser = lightrdf.Parser()
    word = input("Cuavntul pe care il cauti: ")
    with open("CSO.3.2.owl", "rb") as f:
        for triple in parser.parse(f, format="owl", base_iri=None):
            # print(triple)
            name, sameas, topics = triple
            # print(name)
            link_word = name.split("/")[-1]
            # print(link_word)
            if word == link_word:
                print(name)
