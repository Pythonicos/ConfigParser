from functools import partial

from page_manager.configs.config_parser import parse_config, ConfigResolver


class Pessoa:
    def __init__(self):
        self.nome = None
        self.idade = None
        self.sobrenome = None
        self.enderecos = []


def resolve_simple_prop(prop: str, pessoa: Pessoa, value):
    setattr(pessoa, prop, value)


def resolve_enderecos(pessoa: Pessoa, end):
    pessoa.enderecos.append(end)


if __name__ == '__main__':
    eu = Pessoa()
    parse_config('teste.config', {
        'NOME': ConfigResolver(prop=eu, func=partial(resolve_simple_prop, 'nome')),
        'IDADE': ConfigResolver(prop=eu, func=partial(resolve_simple_prop, 'idade')),
        'SOBRENOME': ConfigResolver(prop=eu, func=partial(resolve_simple_prop, 'sobrenome')),
        'ENDERECOS': ConfigResolver(prop=eu, func=resolve_enderecos),
    })

    print(eu)
