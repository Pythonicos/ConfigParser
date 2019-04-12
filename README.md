# ConfigParser
Realiza o parse de arquivos de configuração de maneira rápida e simples!

exemplo:

Configuração de servidor: server.config
```text
# Arquivo de configuração
[NOME SERVIDOR]
Produção 1

[PORTA]
5000

[LISTA DE CREDENCIAIS]
/etc/server/.configuracao1
/etc/server/.configuracao2
```

Parser:
```python
from functools import partial

from page_manager.configs.config_parser import parse_config, ConfigResolver


class Server:
    def __init__(self):
        self.nome = None
        self.porta = None
        self.paths = []


def resolve_simple_prop(prop: str, server: Server, value):
    setattr(server, prop, value)


def resolve_paths(server: Server, path):
    server.paths.append(path)


if __name__ == '__main__':
    servidor = Server()
    parse_config('teste.config', {
        '[NOME SERVIDOR]': ConfigResolver(prop=servidor, func=partial(resolve_simple_prop, 'nome')),
        '[PORTA]': ConfigResolver(prop=servidor, func=partial(resolve_simple_prop, 'porta')),
        '[LISTA DE CREDENCIAIS]': ConfigResolver(prop=servidor, func=resolve_paths),
    })

    print(servidor.nome, servidor.porta, servidor.paths)

```


Simples assim!
