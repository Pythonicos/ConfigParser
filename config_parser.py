"""
Cuidados ao implementar o arquivo de configuração:
- Os valores das configurações não podem ter o mesmo nome que a propriedade que será definida. exemplo:
```debug.config
NOME_PROPRIEDADE                  <- Nome da propriedade, a próxima linha espera-se que seja o valor(es) da propriedade
NOME_PROPRIEDADE                  <- Tentar atribuir a propriedade `NOME_PROPRIEDADE` com o valor `NOME_PROPRIEDADE`
                                     não é possível. Caso isso seja necessário, recomendo definir
                                     o valor entre aspas: "NOME_PROPRIEDADE" e o resolver conseguir tratar esse valor

```

- É permitido complementar as propriedades em mais de uma linha
```debug.config
NOME_PROPRIEDADE_1
valor1

NOME_PROPRIEDADE_2
valorX

NOME_PROPRIEDADE_1
valor2
```
"""


from collections import namedtuple
import re

__all__ = ['parse_config', 'ConfigResolver', 'ConfigurationFileError']

REGEX_PROPERTY = re.compile(r'(?:#PROP#)(?P<property>.+)')
REGEX_COMMENT = re.compile(r'(?:\w*?#)(?P<comment>.+)')

ConfigResolver = namedtuple("Resolver", ['prop', 'func'])


def _tag(line: str, properties: dict):
    clean_line = line.strip()

    if not clean_line:
        return None

    if clean_line in properties:
        clean_line = '#PROP#{}'.format(clean_line)

    return clean_line


class ConfigurationFileError(Exception):
    pass


def parse_config(config_filename: str, region_properties: dict):
    """
    Arquivo de configuração com padrão de implementação específicio:
```sample.config
PROPRIEDADE1
valor1
# linhas que comecem com caracter '#' não serão evaluadas e podem ser utilizadas como comentário
valorN
              -> linhas com somente whitespaces não serão evaluadas <-
PROPRIEDADE2
valor1
```
    Realiza o parse de um arquivo de configuração. Os resolvers são métodos que recebem o objeto a ser trabalhado e
    linha (stripped).
    :param config_filename: Nome do arquivo
    :param region_properties: Dicionário cuja chave é o nome da propriedade e o valor é ConfigResolver
    `{'PROPERTY_NAME': ConfigResolver(property, function_resolver)}`
    :return:
    """

    with open(config_filename, 'r') as config:
        config_lines = (
            _tag(line, region_properties) for line in config.readlines()
        )
        prop = None
        for line in config_lines:
            if line:
                match = REGEX_PROPERTY.fullmatch(line)

                if match:
                    prop = match.group('property')
                    continue

                if prop is not None and not REGEX_COMMENT.fullmatch(line):
                    region_properties[prop].func(region_properties[prop].prop, line)
