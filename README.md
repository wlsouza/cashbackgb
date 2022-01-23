# cashbackgb


============= Planejamento v1.0 ============

[x] criar estrutura básica (pacotes, módulos, requirements e makefile)  
[x] criar configuração inicial (dynaconf ou pydantic)? Pydantic pois já é utilizado nos esquemas (1 dependência a menos)  
[x] criar conexão com o banco (async)  
[x] criar models do banco  
[x] configurar migrations para usar async  
[x] criar schemas para validação e parsing dos dados  
[x] criar segurança inicial (hash de senhas)  
[x] fazer o crud de todos os models (obviamente os testes também)  
[x] fazer o domain com as regras de negócio(etapa pode ser adiantada se necessária para os cruds)  
[x] criar autenticação JWT  
[ ] criar rotas de usuário (no caso o revendedor)  
[ ] criar rotas de compra  
[ ] dockerizar a aplicação  
[ ] criar actions no github (CI/CD)  
[ ] se sobrar tempo fazer deploy na amazon usando lambda(ou ec2), rds e apigateway  


============= Decisões ==================

O representante será chamado e armazenado no banco como "user" a fim de ser possível destinar o sistema para outros tipos de pessoas como colaboradores e afins caso necessário.

O status foi separado da tabela de purchase seguindo os conceitos de formalização de bancos relacionais. (evita o surgimento de status aleatórios e também economiza recurso de armazenamento visto que o dado repetido é um inteiro e não uma string com 11 dígitos)

O cpf não foi mantido na tabela de compras também seguindo os conceitos de formalização de bancos. 

Seguindo a premissa de que cada teste deve testar apenas uma coisa, esse projeto irá conter testes com apenas um assert cada.
Tal escolha aumenta o número de testes mas os tornas mais específicos, aumentando a legibilidade e a manutenção futura.

Os testes terão um padrão de nome explicativo que pode fazer com que tenham nomes fora do padrão de tamanho da pep8 ( <=79 caracteres ), o motivo para tal é que mesmo com nomes compridos os testes terão uma maior manutenabilidade visto que seus nomes explicam sua intenção.
