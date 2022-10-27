from graphviz import Digraph
import requests
import os

choice = 'y'
accepted_symbols = 'qwertyuiopasdfghjklzxcvbnm123456789-'


def dependence_search(package) -> set:
    url = f'https://pypi.org/pypi/{package}/json'
    json = requests.get(url).json()
    try:
        var = json['info']['requires_dist']
        if var is None:
            return set()

        cur_set = set()
        for package in var:
            if len(package) == 0:
                continue
            str = ''
            i = 0
            while package[i] in accepted_symbols and i < len(package) - 1:
                str += package[i]
                i += 1
            if len(str) == 0:
                cur_set.add(str)
        return set(sorted(cur_set))

    except KeyError:
        return set()


def create_edges(graph, set, package) -> Digraph:
    if set is None:
        return

    if set:
        for require in set:
            graph.edge(package, require)
    else:
        graph.node(package)


def deep_search(package, graph, level):
    nodes = set()
    next_level = {package}
    while level > 0:
        list_of_packs = next_level.copy()
        next_level.clear()
        print(list_of_packs)
        if list_of_packs:
            for pack in list_of_packs:
                print(pack)
                new_dependencies = dependence_search(pack)
                new_dependencies -= nodes
                nodes.add(pack)
                create_edges(graph, new_dependencies, pack)
                next_level |= new_dependencies
        else:
            return
        level -= 1
    return graph


def main() -> None:
    pack = input("Введите название библиотеки: ")

    my_graph = Digraph(comment=f"Cписок зависимостей пакета {pack}")
    my_graph.node(pack)

    set_of_dependencies = dependence_search(pack)

    if len(set_of_dependencies) == 0:
        print("Нет зависимостей. Попробуйте еще раз.")
        main()
    else:
        depth = int(input("Зависимости найдены. Введите глубину поиска: "))
        my_graph = deep_search(pack, my_graph, depth)
        print(my_graph.source)
        my_graph.render(directory='homework2', view=True, engine='circo')


if __name__ == "__main__":
    main()